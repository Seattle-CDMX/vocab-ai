import json
import logging

from dotenv import load_dotenv
from livekit.agents import (
    NOT_GIVEN,
    Agent,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    RunContext,
    WorkerOptions,
    cli,
    get_job_context,
    metrics,
)
from livekit.agents.llm import function_tool
from livekit.plugins import (
    deepgram,
    google,
    noise_cancellation,
    openai,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from config.credentials import parse_google_credentials
from handlers.participant import process_participant_voice_card_data
from langfuse_setup import setup_langfuse
from models.session import MySessionInfo
from prompts.loader import load_prompt

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class NativeExplainAgent(Agent):
    def __init__(self) -> None:
        instructions = load_prompt("native_explain_agent")
        super().__init__(instructions=instructions)
        logger.info("🔧 [Agent] NativeExplainAgent initialized with enhanced tool calling instructions")

    @function_tool
    async def correct_sense_explained(self, context: RunContext, sense_number: int):
        """REQUIRED: Call this immediately when the user correctly explains any sense of the target lexical item.
        
        Use this when the user's explanation demonstrates understanding of the meaning, even if not perfectly worded.
        This should be called for ANY correct explanation, regardless of how it's phrased.

        Args:
            sense_number: The sense number that was correctly explained (1, 2, 3, etc.)
        """
        logger.info(f"User correctly explained sense {sense_number}")

        session_info = context.session.userdata
        if isinstance(session_info, MySessionInfo) and session_info.target_lexical_item:
            session_info.target_lexical_item.mark_sense_explained(sense_number)
            remaining = session_info.target_lexical_item.remaining_senses

            # Send RPC to frontend for toast notification
            try:
                # Find the first remote participant (should be the student)
                for participant in get_job_context().room.remote_participants.values():
                    await get_job_context().room.local_participant.perform_rpc(
                        destination_identity=participant.identity,
                        method="show_toast",
                        payload=json.dumps({
                            "type": "success",
                            "message": f"Great job! You explained sense {sense_number} correctly! ✓"
                        }),
                        response_timeout=1.0,
                    )
                    logger.info(f"Sent success toast RPC to {participant.identity}")
                    break
            except Exception as e:
                logger.error(f"Failed to send RPC: {e}")

            if remaining > 0:
                return f"Great job! You got sense {sense_number} correct. You have {remaining} more sense{'s' if remaining != 1 else ''} to explain."
            else:
                # Send special completion toast
                try:
                    for participant in get_job_context().room.remote_participants.values():
                        await get_job_context().room.local_participant.perform_rpc(
                            destination_identity=participant.identity,
                            method="show_toast",
                            payload=json.dumps({
                                "type": "success",
                                "message": "Excellent! You've mastered all meanings of this phrasal verb! 🎉"
                            }),
                            response_timeout=1.0,
                        )
                        logger.info(f"Sent completion toast RPC to {participant.identity}")
                        break
                except Exception as e:
                    logger.error(f"Failed to send completion RPC: {e}")
                    
                return "Excellent! You've successfully explained all senses of this phrasal verb."

        return "Good work on explaining that sense!"

    @function_tool
    async def wrong_answer(
        self, context: RunContext, correct_definition: str, helpful_hint: str = ""
    ):
        """REQUIRED: Call this immediately when the user provides an incorrect or incomplete explanation.
        
        Use this whenever the user's explanation doesn't capture the core meaning of the sense.
        Always provide the correct definition to help them learn.

        Args:
            correct_definition: The correct definition to share with the user (be specific and clear)
            helpful_hint: Optional additional hint, example, or explanation to help the user understand better
        """
        logger.info("User provided incorrect explanation")

        # Send RPC to frontend for error toast notification
        try:
            for participant in get_job_context().room.remote_participants.values():
                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant.identity,
                    method="show_toast",
                    payload=json.dumps({
                        "type": "error",
                        "message": f"Not quite right. Here's the correct meaning: {correct_definition[:50]}..."
                    }),
                    response_timeout=1.0,
                )
                logger.info(f"Sent error toast RPC to {participant.identity}")
                break
        except Exception as e:
            logger.error(f"Failed to send error RPC: {e}")

        response = f"Not quite right. The correct definition is: {correct_definition}"
        if helpful_hint:
            response += f" {helpful_hint}"
        response += " Let's try the next sense."

        return response

    @function_tool
    async def all_senses_completed(self, context: RunContext):
        """REQUIRED: Call this immediately when the user has successfully explained ALL senses of the target lexical item.
        
        This should only be called once all senses have been correctly explained and marked as complete."""
        logger.info("All senses completed successfully")

        session_info = context.session.userdata
        if isinstance(session_info, MySessionInfo) and session_info.target_lexical_item:
            phrase = session_info.target_lexical_item.phrase
            total_senses = session_info.target_lexical_item.total_senses
            return f"Congratulations {session_info.user_name}! You've successfully explained all {total_senses} senses of '{phrase}'. Great work on expanding your vocabulary!"

        return "Congratulations! You've completed explaining all the senses of this phrasal verb."

    @function_tool
    async def request_clarification(self, context: RunContext, sense_number: int, clarifying_question: str):
        """Call this when the user's explanation is unclear and you need them to elaborate or clarify.
        
        Use this when you're not sure if their explanation is correct or incorrect and need more information.

        Args:
            sense_number: The sense number they're trying to explain
            clarifying_question: A specific question to help them clarify their explanation
        """
        logger.info(f"Requesting clarification for sense {sense_number}")
        return f"I want to make sure I understand your explanation correctly. {clarifying_question}"

    async def on_enter(self) -> None:
        """Agent initialization hook called when this agent becomes active."""
        logger.info("🎯 [Agent] NativeExplainAgent on_enter called")
        logger.info(
            "🎯 [Agent] Waiting for participant to connect before starting conversation..."
        )
        # Don't send any message yet - wait for participant to connect first


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    setup_langfuse()
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Initialize session info with placeholder - will be updated when participant connects
    session_info = MySessionInfo(
        user_name="Max",
        age=25,
        target_lexical_item=None,  # Will be set dynamically from participant attributes
    )

    # Set up a voice AI pipeline using OpenAI, Cartesia, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all providers at https://docs.livekit.io/agents/integrations/llm/
        llm=openai.LLM(model="gpt-4o-mini"),
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all providers at https://docs.livekit.io/agents/integrations/stt/
        stt=deepgram.STT(model="nova-3", language="multi"),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all providers at https://docs.livekit.io/agents/integrations/tts/
        tts=google.TTS(
            language="es-US",
            voice_name="es-US-Chirp3-HD-Schedar",
            credentials_info=parse_google_credentials(),
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
        # Add the session userdata with vocabulary learning information
        userdata=session_info,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead:
    # session = AgentSession(
    #     # See all providers at https://docs.livekit.io/agents/integrations/realtime/
    #     llm=openai.realtime.RealtimeModel()
    # )

    # sometimes background noise could interrupt the agent session, these are considered false positive interruptions
    # when it's detected, you may resume the agent's speech
    @session.on("agent_false_interruption")
    def _on_agent_false_interruption(ev: AgentFalseInterruptionEvent):
        logger.info("false positive interruption, resuming")
        session.generate_reply(instructions=ev.extra_instructions or NOT_GIVEN)

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Handle participant connection to get voice card data
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant):
        logger.info("🎯 [Agent] NEW participant connected event fired!")
        process_participant_voice_card_data(participant, session)

    # Check for existing participants when agent starts
    async def check_existing_participants():
        logger.info("🎯 [Agent] Checking for existing participants...")
        for participant in ctx.room.remote_participants.values():
            logger.info(
                f"🎯 [Agent] Found existing participant: {participant.identity}"
            )
            process_participant_voice_card_data(participant, session)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=NativeExplainAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()

    # Check for existing participants after connecting
    logger.info("🎯 [Agent] Agent connected, checking for existing participants...")
    await check_existing_participants()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

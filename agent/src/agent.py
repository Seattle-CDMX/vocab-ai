import logging

from dotenv import load_dotenv
from livekit.agents import (
    NOT_GIVEN,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.plugins import (
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Agents are imported when needed to avoid circular imports
from handlers.participant import process_participant_data
from langfuse_setup import setup_langfuse
from models.session import MySessionInfo

logger = logging.getLogger("agent")

load_dotenv(".env.local")


# Agent classes are now imported from separate modules


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

    # Set up a session - agents will now provide their own STT/TTS configuration
    session = AgentSession(
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

    # Variable to store the selected agent
    selected_agent = None

    # Handle participant connection to determine agent and get data
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant):
        nonlocal selected_agent
        logger.info("🎯 [Agent] NEW participant connected event fired!")
        logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Participant identity: {participant.identity}")
        logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Participant attributes: {participant.attributes}")
        logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Participant metadata: {getattr(participant, 'metadata', 'None')}")

        new_agent = process_participant_data(participant, session)
        if new_agent is not None:
            selected_agent = new_agent
            logger.info(f"🎯 [Agent] ✅ Selected agent: {type(selected_agent).__name__}")
            # If session is already started, we need to update the agent dynamically
            if hasattr(session, '_agent') and session._agent is not None:
                logger.info("🎯 [Agent] 🔄 CLOUD DEBUG: Session already started - agent will be updated dynamically")
        else:
            logger.warning("🎯 [Agent] ⚠️ CLOUD DEBUG: process_participant_data returned None - will retry on next connection")

    # Add retry mechanism for metadata processing
    retry_count = 0
    max_retries = 5

    async def retry_participant_processing():
        nonlocal selected_agent, retry_count
        if retry_count >= max_retries:
            logger.error(f"🎯 [Agent] ❌ Max retries ({max_retries}) reached for participant processing")
            return

        retry_count += 1
        logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Retry attempt {retry_count}/{max_retries} for participant processing")

        for participant in ctx.room.remote_participants.values():
            logger.info(f"🎯 [Agent] 🔄 RETRY: Processing participant {participant.identity}")
            new_agent = process_participant_data(participant, session)
            if new_agent is not None:
                selected_agent = new_agent
                logger.info(f"🎯 [Agent] ✅ RETRY SUCCESS: Selected agent: {type(selected_agent).__name__}")
                return

        # Schedule another retry after a delay
        import asyncio
        await asyncio.sleep(2.0)  # Wait 2 seconds before next retry
        await retry_participant_processing()

    # Check for existing participants when agent starts
    async def check_existing_participants():
        nonlocal selected_agent
        logger.info("🎯 [Agent] Checking for existing participants...")
        for participant in ctx.room.remote_participants.values():
            logger.info(f"🎯 [Agent] Found existing participant: {participant.identity}")
            logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Existing participant attributes: {participant.attributes}")
            logger.info(f"🎯 [Agent] 🔄 CLOUD DEBUG: Existing participant metadata: {getattr(participant, 'metadata', 'None')}")

            new_agent = process_participant_data(participant, session)
            if new_agent is not None:
                selected_agent = new_agent
                logger.info(f"🎯 [Agent] ✅ Selected agent from existing participant: {type(selected_agent).__name__}")
            else:
                logger.warning("🎯 [Agent] ⚠️ CLOUD DEBUG: process_participant_data returned None for existing participant - will wait for proper connection")

    # Connect to room first to check for participants
    await ctx.connect()

    # Check for existing participants after connecting
    logger.info("🎯 [Agent] Agent connected, checking for existing participants...")
    await check_existing_participants()

    # Wait for proper agent selection - don't fallback to NativeExplainAgent
    if not selected_agent:
        logger.info("🎯 [Agent] 🔄 CLOUD DEBUG: No valid agent selected yet - starting retry mechanism")
        # Try retry mechanism before creating waiting agent
        await retry_participant_processing()

        if not selected_agent:
            logger.info("🎯 [Agent] 🔄 CLOUD DEBUG: Still no valid agent after retries - creating waiting ContextAgent")
            # Create a minimal waiting agent that just waits for proper connection
            from agents.context_agent import ContextAgent

            # Create ContextAgent with no scenario data - it will use defaults but won't start inappropriate conversation
            selected_agent = ContextAgent(scenario_data=None)
            logger.info("🎯 [Agent] Created waiting ContextAgent - waiting for user connection with proper scenario data")
        else:
            logger.info("🎯 [Agent] ✅ RETRY SUCCESS: Got valid agent from retry mechanism")

    # Start the session with the selected agent
    await session.start(
        agent=selected_agent,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Agent is already started and connected


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

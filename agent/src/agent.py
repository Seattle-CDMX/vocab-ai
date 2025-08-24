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
    deepgram,
    google,
    noise_cancellation,
    openai,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from agents.native_explain_agent import NativeExplainAgent
from config.credentials import parse_google_credentials
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

    # Variable to store the selected agent
    selected_agent = None

    # Handle participant connection to determine agent and get data
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant):
        nonlocal selected_agent
        logger.info("🎯 [Agent] NEW participant connected event fired!")
        selected_agent = process_participant_data(participant, session)
        logger.info(f"🎯 [Agent] Selected agent: {type(selected_agent).__name__}")

    # Check for existing participants when agent starts
    async def check_existing_participants():
        nonlocal selected_agent
        logger.info("🎯 [Agent] Checking for existing participants...")
        for participant in ctx.room.remote_participants.values():
            logger.info(
                f"🎯 [Agent] Found existing participant: {participant.identity}"
            )
            selected_agent = process_participant_data(participant, session)
            logger.info(f"🎯 [Agent] Selected agent: {type(selected_agent).__name__ if selected_agent else 'None'}")

    # Connect to room first to check for participants
    await ctx.connect()

    # Check for existing participants after connecting
    logger.info("🎯 [Agent] Agent connected, checking for existing participants...")
    await check_existing_participants()

    # Use the selected agent or default to NativeExplainAgent
    if not selected_agent:
        logger.info("🎯 [Agent] No participants found yet, using default NativeExplainAgent")
        selected_agent = NativeExplainAgent()

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

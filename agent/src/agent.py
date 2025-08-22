import base64
import json
import logging
import os
from dataclasses import dataclass
from typing import List, Optional
from langfuse_setup import setup_langfuse
from prompts.loader import load_prompt

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
    metrics,
)
from livekit.agents.llm import function_tool
from livekit.plugins import cartesia, deepgram, google, noise_cancellation, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


@dataclass
class LexicalSense:
    sense_number: int
    definition: str
    examples: List[str]
    explained: bool = False


@dataclass
class TargetLexicalItem:
    phrase: str
    senses: List[LexicalSense]
    
    @property
    def total_senses(self) -> int:
        return len(self.senses)
    
    @property
    def explained_senses(self) -> int:
        return sum(1 for sense in self.senses if sense.explained)
    
    @property
    def remaining_senses(self) -> int:
        return self.total_senses - self.explained_senses
    
    def get_next_unexplained_sense(self) -> LexicalSense | None:
        for sense in self.senses:
            if not sense.explained:
                return sense
        return None
    
    def mark_sense_explained(self, sense_number: int) -> bool:
        for sense in self.senses:
            if sense.sense_number == sense_number:
                sense.explained = True
                return True
        return False


@dataclass
class MySessionInfo:
    user_name: str
    age: int
    target_lexical_item: Optional[TargetLexicalItem]


def create_target_lexical_item(phrase: str, sense_data: List[dict]) -> TargetLexicalItem:
    senses = []
    for data in sense_data:
        sense = LexicalSense(
            sense_number=data["senseNumber"],
            definition=data["definition"],
            examples=data["examples"]
        )
        senses.append(sense)
    
    return TargetLexicalItem(phrase=phrase, senses=senses)


def _parse_google_credentials():
    """Parse Google Cloud credentials from environment variable with proper error handling.
    
    Supports both regular JSON and base64-encoded JSON for better compatibility
    with different deployment environments.
    """
    credentials_b64 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_B64")
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    # Try base64-encoded credentials first (more robust for env vars)
    if credentials_b64:
        try:
            decoded_json = base64.b64decode(credentials_b64).decode('utf-8')
            credentials_data = json.loads(decoded_json)
            logger.info("Successfully loaded Google Cloud credentials from base64 environment variable")
            return credentials_data
        except Exception as e:
            logger.error(f"Failed to parse base64 credentials: {e}")
    
    # Fall back to regular JSON credentials
    if credentials_json:
        try:
            credentials_data = json.loads(credentials_json)
            logger.info("Successfully loaded Google Cloud credentials from JSON environment variable")
            return credentials_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GOOGLE_APPLICATION_CREDENTIALS_JSON: {e}")
            logger.error("Hint: Try using GOOGLE_APPLICATION_CREDENTIALS_B64 with base64-encoded JSON instead")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing Google credentials: {e}")
            return None
    
    logger.warning("Neither GOOGLE_APPLICATION_CREDENTIALS_JSON nor GOOGLE_APPLICATION_CREDENTIALS_B64 environment variables are set")
    return None


class NativeExplainAgent(Agent):
    def __init__(self) -> None:
        instructions = load_prompt("native_explain_agent")
        super().__init__(instructions=instructions)

    @function_tool
    async def correct_sense_explained(self, context: RunContext, sense_number: int):
        """Call this when the user has correctly explained a sense of the target lexical item.
        
        Args:
            sense_number: The sense number that was correctly explained
        """
        logger.info(f"User correctly explained sense {sense_number}")
        
        session_info = context.session.userdata
        if isinstance(session_info, MySessionInfo) and session_info.target_lexical_item:
            session_info.target_lexical_item.mark_sense_explained(sense_number)
            remaining = session_info.target_lexical_item.remaining_senses
            
            if remaining > 0:
                return f"Great job! You got sense {sense_number} correct. You have {remaining} more sense{'s' if remaining != 1 else ''} to explain."
            else:
                return "Excellent! You've successfully explained all senses of this phrasal verb."
        
        return "Good work on explaining that sense!"

    @function_tool
    async def wrong_answer(self, _: RunContext, correct_definition: str, helpful_hint: str = ""):
        """Call this when the user provides an incorrect explanation for a sense.
        
        Args:
            correct_definition: The correct definition to share with the user
            helpful_hint: Optional additional hint or explanation to help the user understand
        """
        logger.info("User provided incorrect explanation")
        
        response = f"Not quite right. The correct definition is: {correct_definition}"
        if helpful_hint:
            response += f" {helpful_hint}"
        response += " Let's try the next sense."
        
        return response

    @function_tool
    async def all_senses_completed(self, context: RunContext):
        """Call this when the user has successfully explained all senses of the target lexical item."""
        logger.info("All senses completed successfully")
        
        session_info = context.session.userdata
        if isinstance(session_info, MySessionInfo) and session_info.target_lexical_item:
            phrase = session_info.target_lexical_item.phrase
            total_senses = session_info.target_lexical_item.total_senses
            return f"Congratulations {session_info.user_name}! You've successfully explained all {total_senses} senses of '{phrase}'. Great work on expanding your vocabulary!"
        
        return "Congratulations! You've completed explaining all the senses of this phrasal verb."

    async def on_enter(self) -> None:
        """Agent initialization hook called when this agent becomes active."""
        logger.info("🎯 [Agent] NativeExplainAgent on_enter called")
        logger.info("🎯 [Agent] Waiting for participant to connect before starting conversation...")
        # Don't send any message yet - wait for participant to connect first


def _parse_google_credentials():
    """Parse Google Cloud credentials from environment variable with proper error handling.
    
    Supports both regular JSON and base64-encoded JSON for better compatibility
    with different deployment environments.
    """
    credentials_b64 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_B64")
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    # Try base64-encoded credentials first (more robust for env vars)
    if credentials_b64:
        try:
            decoded_json = base64.b64decode(credentials_b64).decode('utf-8')
            credentials_data = json.loads(decoded_json)
            logger.info("Successfully loaded Google Cloud credentials from base64 environment variable")
            return credentials_data
        except Exception as e:
            logger.error(f"Failed to parse base64 credentials: {e}")
    
    # Fall back to regular JSON credentials
    if credentials_json:
        try:
            credentials_data = json.loads(credentials_json)
            logger.info("Successfully loaded Google Cloud credentials from JSON environment variable")
            return credentials_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GOOGLE_APPLICATION_CREDENTIALS_JSON: {e}")
            logger.error("Hint: Try using GOOGLE_APPLICATION_CREDENTIALS_B64 with base64-encoded JSON instead")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing Google credentials: {e}")
            return None
    
    logger.warning("Neither GOOGLE_APPLICATION_CREDENTIALS_JSON nor GOOGLE_APPLICATION_CREDENTIALS_B64 environment variables are set")
    return None


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
        target_lexical_item=None  # Will be set dynamically from participant attributes
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
            voice_name="es-US-Chirp3-HD-Puck",
            credentials_info=_parse_google_credentials(),
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

    # Function to process participant and get voice card data
    def process_participant_voice_card_data(participant):
        logger.info(f"🎯 [Agent] Processing participant: {participant.identity}")
        logger.info(f"🎯 [Agent] All participant attributes: {participant.attributes}")
        
        # Get voice card data from participant attributes
        voice_card_json = participant.attributes.get("voice_card_data")
        logger.info(f"🎯 [Agent] Voice card JSON received: {voice_card_json}")
        
        if voice_card_json:
            try:
                voice_card = json.loads(voice_card_json)
                logger.info(f"🎯 [Agent] Parsed voice card data successfully: {voice_card['title']}")
                logger.info(f"🎯 [Agent] Voice card type: {voice_card['type']}")
                logger.info(f"🎯 [Agent] Full voice card object: {voice_card}")
                
                # Extract phrasal verb data from voice card
                phrasal_verb = voice_card["targetPhrasalVerb"]
                verb = phrasal_verb["verb"]
                senses = phrasal_verb["senses"]
                
                logger.info(f"🎯 [Agent] Extracted verb: {verb}")
                logger.info(f"🎯 [Agent] Extracted senses: {senses}")
                
                # Create target lexical item from voice card data
                target_item = create_target_lexical_item(verb, senses)
                logger.info(f"🎯 [Agent] Created target lexical item with {target_item.total_senses} senses")
                
                # Update session info with dynamic data
                session_info.target_lexical_item = target_item
                session.userdata = session_info
                
                logger.info(f"🎯 [Agent] ✅ COMPLETE: Updated session with voice card data for: {verb}")
                
                # Now start the conversation with the voice card data
                instructions = f"""The TARGET LEXICAL ITEM IS '{target_item.phrase}'. This phrasal verb has {target_item.total_senses} different meanings. 

Ask the user to explain what this phrasal verb means. When they explain a meaning, determine which of the {target_item.total_senses} senses they are explaining and whether it's correct.

The {target_item.total_senses} senses are:
"""
                for sense in target_item.senses:
                    instructions += f"{sense.sense_number}. {sense.definition} (Example: {sense.examples[0]})\n"
                
                instructions += f"\nStart by asking them to explain what '{target_item.phrase}' means."
                
                logger.info(f"🎯 [Agent] 🗣️ Starting conversation about: {target_item.phrase}")
                session.generate_reply(instructions=instructions)
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"🎯 [Agent] ❌ Failed to parse voice card data: {e}")
                logger.error(f"🎯 [Agent] Raw JSON that failed: {voice_card_json}")
                # Fallback: create a simple target item
                fallback_data = [{"senseNumber": 1, "definition": "Practice phrasal verb", "examples": ["Example sentence"]}]
                session_info.target_lexical_item = create_target_lexical_item("PRACTICE VERB", fallback_data)
                session.userdata = session_info
                logger.info(f"🎯 [Agent] Using fallback data: PRACTICE VERB")
                session.generate_reply(instructions="I couldn't get the voice card data. Let me ask you about a practice phrasal verb instead.")
        else:
            logger.warning("🎯 [Agent] ❌ No voice card data found in participant attributes")
            logger.warning(f"🎯 [Agent] Available attribute keys: {list(participant.attributes.keys())}")
            # Fallback: create a simple target item  
            fallback_data = [{"senseNumber": 1, "definition": "Practice phrasal verb", "examples": ["Example sentence"]}]
            session_info.target_lexical_item = create_target_lexical_item("PRACTICE VERB", fallback_data)
            session.userdata = session_info
            logger.info(f"🎯 [Agent] Using fallback data: PRACTICE VERB")
            session.generate_reply(instructions="I'm waiting for voice card data. Please ensure your connection includes the phrasal verb information.")

    # Handle participant connection to get voice card data
    @ctx.room.on("participant_connected") 
    def on_participant_connected(participant):
        logger.info(f"🎯 [Agent] NEW participant connected event fired!")
        process_participant_voice_card_data(participant)

    # Check for existing participants when agent starts
    async def check_existing_participants():
        logger.info(f"🎯 [Agent] Checking for existing participants...")
        for participant in ctx.room.remote_participants.values():
            logger.info(f"🎯 [Agent] Found existing participant: {participant.identity}")
            process_participant_voice_card_data(participant)


    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/integrations/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/integrations/avatar/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

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
    logger.info(f"🎯 [Agent] Agent connected, checking for existing participants...")
    await check_existing_participants()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

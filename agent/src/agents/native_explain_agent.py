import json
import logging

from livekit.agents import (
    Agent,
    RunContext,
    get_job_context,
)
from livekit.agents.llm import function_tool
from livekit.plugins import deepgram, google, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from config.credentials import parse_google_credentials
from models.session import MySessionInfo
from services.terminal_state_manager import TerminalStateManager

logger = logging.getLogger("agent.native_explain")


class NativeExplainAgent(Agent):
    def __init__(self) -> None:
        from prompts.loader import load_prompt

        instructions = load_prompt("native_explain_agent")
        super().__init__(
            instructions=instructions,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=google.TTS(
                language="es-US",
                voice_name="es-US-Chirp3-HD-Schedar",
                credentials_info=parse_google_credentials(),
            ),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )
        logger.info(
            "🔧 [Agent] NativeExplainAgent initialized with enhanced tool calling instructions"
        )

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

            # Send RPC to frontend for toast notification (not terminal state, continue learning)
            try:
                # Find the first remote participant (should be the student)
                for participant in get_job_context().room.remote_participants.values():
                    await get_job_context().room.local_participant.perform_rpc(
                        destination_identity=participant.identity,
                        method="show_toast",
                        payload=json.dumps(
                            {
                                "type": "success",
                                "message": f"Great job! You explained sense {sense_number} correctly! ✓",
                            }
                        ),
                        response_timeout=1.0,
                    )
                    logger.info(f"Sent success toast RPC to {participant.identity}")
                    break
            except Exception as e:
                logger.error(f"Failed to send RPC: {e}")

            if remaining > 0:
                return f"Great job! You got sense {sense_number} correct. You have {remaining} more sense{'s' if remaining != 1 else ''} to explain."
            else:
                # All senses completed - handle terminal success state
                await TerminalStateManager.handle_success(
                    "Excellent! You've mastered all meanings of this phrasal verb! 🎉"
                )

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

        # For wrong answers, we continue teaching, so this is not a terminal state
        # Just send a regular error toast (not using terminal state manager)
        try:
            for participant in get_job_context().room.remote_participants.values():
                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant.identity,
                    method="show_toast",
                    payload=json.dumps(
                        {
                            "type": "error",
                            "message": f"Not quite right. Here's the correct meaning: {correct_definition[:50]}...",
                        }
                    ),
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
            
            # Handle terminal success state
            await TerminalStateManager.handle_success(
                f"Congratulations! You've successfully explained all {total_senses} senses of '{phrase}'. Great work! 🎉"
            )
            
            return f"Congratulations {session_info.user_name}! You've successfully explained all {total_senses} senses of '{phrase}'. Great work on expanding your vocabulary!"

        # Handle terminal success state for fallback case
        await TerminalStateManager.handle_success(
            "Congratulations! You've completed explaining all the senses of this phrasal verb! 🎉"
        )
        
        return "Congratulations! You've completed explaining all the senses of this phrasal verb."

    @function_tool
    async def request_clarification(
        self, context: RunContext, sense_number: int, clarifying_question: str
    ):
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

        # Get session info to check if we have target lexical item data
        session_info = self.session.userdata

        if isinstance(session_info, MySessionInfo) and session_info.target_lexical_item:
            target_item = session_info.target_lexical_item

            # Build the initial instructions with the target phrasal verb data
            instructions = f"""The TARGET LEXICAL ITEM IS '{target_item.phrase}'. This phrasal verb has {target_item.total_senses} different meanings.

Ask the user to explain what this phrasal verb means. When they explain a meaning, determine which of the {target_item.total_senses} senses they are explaining and whether it's correct.

The {target_item.total_senses} senses are:
"""
            for sense in target_item.senses:
                instructions += f"{sense.sense_number}. {sense.definition} (Example: {sense.examples[0]})\n"

            instructions += (
                f"\nStart by asking them to explain what '{target_item.phrase}' means."
            )

            logger.info(f"🎯 [Agent] Starting conversation about: {target_item.phrase}")

            # Generate the initial message to the user
            self.session.generate_reply(instructions=instructions)
        else:
            # Fallback if no target lexical item is set
            logger.warning("🎯 [Agent] No target lexical item found in session")
            self.session.generate_reply(
                instructions="I'm waiting for phrasal verb data. Please ensure your connection includes the necessary information."
            )

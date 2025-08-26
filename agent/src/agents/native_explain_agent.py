import asyncio
import json
import logging

from livekit.agents import (
    Agent,
    RunContext,
    get_job_context,
)
from livekit.agents.llm import ChatContext, ChatMessage, function_tool
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
        self.spanish_validation_result = None  # Store RAG validation results

        logger.info(
            "🔧 [Agent] NativeExplainAgent initialized with Spanish translation support"
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

            # END SESSION AFTER ONE CORRECT SENSE
            # Schedule terminal success state immediately for single correct answer
            asyncio.create_task(  # noqa: RUF006
                TerminalStateManager.handle_success(
                    f"Excellent! You correctly explained sense {sense_number} of this phrasal verb! 🎉",
                    delay_seconds=5.0,  # Delay to allow agent to finish speaking
                )
            )

            return f"Excellent! You correctly explained sense {sense_number}. Great job understanding this phrasal verb!"

        return "Good work on explaining that sense!"

    @function_tool
    async def wrong_answer(
        self, context: RunContext, correct_definition: str, helpful_hint: str = ""
    ):
        """ONLY call this for completely wrong explanations that show NO understanding of any sense.

        Use this ONLY when the user's explanation is totally unrelated or demonstrates no grasp of the phrasal verb.
        Do NOT use this for explanations that are "not quite right" but show some understanding.
        For partial understanding, use request_clarification instead.

        Args:
            correct_definition: The correct definition to share with the user (be specific and clear)
            helpful_hint: Optional additional hint, example, or explanation to help the user understand better
        """
        logger.info("User provided incorrect explanation")

        # END SESSION FOR WRONG ANSWERS
        response = f"Not quite right. The correct definition is: {correct_definition}"
        if helpful_hint:
            response += f" {helpful_hint}"
        response += " Keep practicing and you'll get it next time!"

        # Schedule terminal failure state with delay
        asyncio.create_task(  # noqa: RUF006
            TerminalStateManager.handle_failure(
                f"Not quite right. The correct meaning is: {correct_definition[:100]}...",
                hint="Keep practicing! You'll master this phrasal verb.",
                delay_seconds=5.0,  # Delay to allow agent to finish speaking
            )
        )

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

            # Schedule terminal success state with delay
            asyncio.create_task(  # noqa: RUF006
                TerminalStateManager.handle_success(
                    f"Congratulations! You've successfully explained all {total_senses} senses of '{phrase}'. Great work! 🎉",
                    delay_seconds=5.0,  # Longer delay for final completion message
                )
            )

            return f"Congratulations {session_info.user_name}! You've successfully explained all {total_senses} senses of '{phrase}'. Great work on expanding your vocabulary!"

        # Schedule terminal success state for fallback case with delay
        asyncio.create_task(  # noqa: RUF006
            TerminalStateManager.handle_success(
                "Congratulations! You've completed explaining all the senses of this phrasal verb! 🎉",
                delay_seconds=5.0,  # Longer delay for final completion message
            )
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
                f"\nStart by asking '¿Qué significa esta palabra, o verbo frasal?' without mentioning '{target_item.phrase}'. "
                f"Only reveal the target word when they ask what word you're referring to."
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

    async def on_user_turn_completed(
        self, turn_ctx: ChatContext, new_message: ChatMessage
    ) -> None:
        """RAG method to validate Spanish translations before LLM processing."""
        session_info = self.session.userdata

        if (
            not isinstance(session_info, MySessionInfo)
            or not session_info.target_lexical_item
        ):
            return

        target_item = session_info.target_lexical_item
        user_response = new_message.content

        # Build sense definitions for RAG validation
        senses_info = ""
        for sense in target_item.senses:
            senses_info += f"Sense {sense.sense_number}: {sense.definition}\n"

        # Use LLM to check if response is a Spanish translation - BE VERY GENEROUS
        validation_prompt = f"""Analyze this user response for the phrasal verb '{target_item.phrase}':

User said: "{user_response}"

Phrasal verb senses:
{senses_info}

BE EXTREMELY GENEROUS in evaluation. Accept Spanish translations that show ANY understanding.

Common Spanish translations to accept:
- "go on" = "continuar" or "pasar" 
- "pick up" = "recoger"
- "come back" = "regresar"
- "close down" = "cerrar" or "cerrar un negocio" (close a business)

For "close down" specifically: Accept ANY Spanish phrase about closing businesses, stopping operations, or shutting down.

Determine:
1. Is this response in Spanish? (yes/no)
2. If Spanish, which sense number does it correctly translate to? (1, 2, etc. or 'none' if incorrect)
3. Brief explanation of why

BE LENIENT - if there's any reasonable connection, mark it as correct!

Respond in JSON format:
{{"is_spanish": boolean, "correct_sense": number or null, "explanation": "brief explanation"}}
"""

        try:
            # Create a simple LLM instance for RAG validation
            llm = openai.LLM(model="gpt-4o-mini")
            validation_response = await llm.chat(
                messages=[
                    ChatMessage.system(
                        "You are a language validation assistant. Respond only in JSON format."
                    ),
                    ChatMessage.user(validation_prompt),
                ]
            )

            # Parse the validation result
            import json

            result = json.loads(validation_response.content)

            # Store result for function tools to use
            self.spanish_validation_result = result

            # If Spanish translation is correct, add context to help the agent
            if result.get("is_spanish") and result.get("correct_sense"):
                # Inject context into the chat to guide the agent
                turn_ctx.messages.append(
                    ChatMessage.system(
                        f"[SPANISH TRANSLATION DETECTED] The user provided a correct Spanish translation for sense {result['correct_sense']}. "
                        f"Call correct_sense_explained with sense_number={result['correct_sense']} immediately."
                    )
                )
                logger.info(
                    f"✅ Spanish translation validated for sense {result['correct_sense']}: {user_response}"
                )
            elif result.get("is_spanish") and not result.get("correct_sense"):
                # Spanish but incorrect
                turn_ctx.messages.append(
                    ChatMessage.system(
                        f"[SPANISH TRANSLATION DETECTED] The user provided a Spanish response but it doesn't correctly match any sense. "
                        f"Call wrong_answer and provide the correct definition."
                    )
                )
                logger.info(
                    f"❌ Incorrect Spanish translation detected: {user_response}"
                )

        except Exception as e:
            logger.error(f"Failed to validate Spanish translation: {e}")
            # Continue without validation on error
            self.spanish_validation_result = None

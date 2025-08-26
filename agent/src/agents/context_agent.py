import asyncio
import logging
from typing import Optional

from livekit.agents import (
    Agent,
    ChatContext,
    ChatMessage,
)
from livekit.plugins import deepgram, google, openai, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from config.credentials import parse_google_credentials
from services.phrasal_evaluator import PhrasalEvaluator
from services.terminal_state_manager import TerminalStateManager

logger = logging.getLogger("agent.context")


class ContextAgent(Agent):
    """Agent for context-based phrasal verb practice with role-playing scenarios."""

    def __init__(
        self, scenario_data: Optional[dict] = None, voice_persona: Optional[dict] = None
    ):
        self.max_turns = 5
        self.turn_count = 0
        self.success = False
        self.evaluator = PhrasalEvaluator()
        self.voice_persona = voice_persona or {}

        # Extract scenario data
        if scenario_data:
            self.character = scenario_data.get("character", "Mr. Yang")
            self.situation = scenario_data.get("situation", "a meeting")
            self.phrasal_verb = scenario_data.get("phrasalVerb", "go on")
            self.phrasal_verb_definition = scenario_data.get("phrasalVerbDefinition")
            self.phrasal_verb_examples = scenario_data.get("phrasalVerbExamples", [])
            self.context_text = scenario_data.get("contextText", "")
            self.conversation_starter = scenario_data.get("conversationStarter", "")
            self.max_turns = scenario_data.get("maxTurns", 5)

            # Fail loudly if critical data is missing
            if not self.character:
                raise ValueError(
                    "Character data is missing from metadata. Check frontend metadata passing."
                )
            if not self.phrasal_verb_definition:
                raise ValueError(
                    "Phrasal verb definition is missing from metadata. This is required for proper evaluation."
                )
        else:
            # Defaults for testing/fallback - should not be used in production
            logger.warning(
                "⚠️ [ContextAgent] No scenario_data provided - using fallbacks. This should not happen in production."
            )
            self.character = "Mr. Yang"
            self.situation = "a meeting"
            self.phrasal_verb = "go on"
            self.phrasal_verb_definition = "Happen, take place"  # Default for testing
            self.context_text = "You need to speak with Mr. Yang"

        # Build agent instructions with persona information
        persona_info = self.voice_persona.get("persona", {})
        teaching_style = persona_info.get("teaching_style", "professional and clear")

        instructions = f"""You are {self.character} in this scenario: {self.situation}

Teaching style: {teaching_style}

Your role:
1. Act naturally as {self.character}
2. Respond authentically to the student
3. Keep conversations brief and natural
4. Do NOT mention the phrasal verb
5. Stay in character

Context: {self.context_text}"""

        # Configure TTS with voice persona data
        voice_info = self.voice_persona.get("voice", {})
        language_code = voice_info.get("language_code", "en-US")
        voice_name = voice_info.get(
            "name", "en-US-Chirp3-HD-Achernar"
        )  # Default CHIRP 3 HD voice

        super().__init__(
            instructions=instructions,
            stt=deepgram.STT(model="nova-3", language="multi"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=google.TTS(
                language=language_code,
                voice_name=voice_name,
                credentials_info=parse_google_credentials(),
            ),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )
        logger.info(
            f"🎭 [ContextAgent] Initialized as {self.character} for phrasal verb: {self.phrasal_verb}"
        )
        logger.info(
            f"🔊 [ContextAgent] Voice configured: {voice_name} ({language_code})"
        )
        logger.info(
            f"👤 [ContextAgent] Persona: {persona_info.get('name', 'Unknown')} with {teaching_style} style"
        )

    async def on_user_turn_completed(
        self, turn_ctx: ChatContext, new_message: ChatMessage
    ) -> None:
        """Called after each user turn to evaluate phrasal verb usage."""

        self.turn_count += 1
        # Extract text content from the message (content is a list of strings)
        user_text = (
            " ".join(new_message.content)
            if isinstance(new_message.content, list)
            else str(new_message.content)
        )

        logger.info(
            f"🎯 [ContextAgent] Turn {self.turn_count}/{self.max_turns}: User said: {user_text}"
        )

        # Start background evaluation - don't block conversation
        self._evaluation_task = asyncio.create_task(
            self._evaluate_and_notify(user_text)
        )

        # Allow conversation to continue immediately while evaluation runs in background
        logger.info(
            "⚡ [ContextAgent] Evaluation started in background, conversation continues"
        )

    async def _evaluate_and_notify(self, user_text: str) -> None:
        """Evaluate phrasal verb usage in background and notify UI accordingly."""
        try:
            # Evaluate phrasal verb usage
            evaluation = await self.evaluator.evaluate_usage(
                user_text=user_text,
                phrasal_verb=self.phrasal_verb,
                phrasal_verb_definition=self.phrasal_verb_definition,
                scenario=self.situation,
                phrasal_verb_examples=self.phrasal_verb_examples,
                character=self.character,
            )

            logger.info(
                f"📊 [ContextAgent] Background evaluation completed: {evaluation}"
            )

            if evaluation["used_correctly"]:
                # Success! User used the phrasal verb correctly
                self.success = True
                # Schedule terminal success state with delay to allow agent to finish speaking
                asyncio.create_task(  # noqa: RUF006
                    TerminalStateManager.handle_success(
                        f"Excellent! You used '{self.phrasal_verb}' correctly in context! 🎯",
                        delay_seconds=3.5,  # Shorter delay for context conversations
                    )
                )
                logger.info(
                    f"✅ [ContextAgent] Success! User correctly used '{self.phrasal_verb}'"
                )

            elif self.turn_count >= self.max_turns and not self.success:
                # Failed - out of turns
                hint = evaluation.get(
                    "hint",
                    f"You could have said something like: 'Could you {self.phrasal_verb} with your explanation?'",
                )
                # Schedule terminal failure state with delay to allow agent to finish speaking
                asyncio.create_task(  # noqa: RUF006
                    TerminalStateManager.handle_failure(
                        "Out of turns. Time to move on!",
                        hint,
                        delay_seconds=2.5,  # Shorter delay for failure messages
                    )
                )
                logger.info(
                    "❌ [ContextAgent] Failed - out of turns without correct usage"
                )

            else:
                # Still have turns remaining - just log for now
                remaining = self.max_turns - self.turn_count
                if evaluation.get("used_verb") and not evaluation.get("used_correctly"):
                    logger.info(
                        f"⚠️ [ContextAgent] Incorrect usage attempt detected. {remaining} turns remaining"
                    )
                else:
                    logger.info(
                        f"⏳ [ContextAgent] No usage detected yet. {remaining} turns remaining"
                    )

        except Exception as e:
            logger.error(f"❌ [ContextAgent] Background evaluation failed: {e}")

    async def on_enter(self) -> None:
        """Called when the agent becomes active."""
        logger.info(f"🎭 [ContextAgent] Agent entering as {self.character}")
        logger.info(f"🎯 [ContextAgent] Target phrasal verb: {self.phrasal_verb}")
        logger.info(f"📝 [ContextAgent] Scenario: {self.situation}")
        logger.info(f"🔢 [ContextAgent] Max turns: {self.max_turns}")

        # Use conversationStarter from scenario data, or fallback to simple greeting
        if self.conversation_starter:
            # Remove [username] placeholder if present
            greeting = self.conversation_starter.replace("[username]", "").strip()
            # Make it shorter - just take the first sentence if it's too long
            if len(greeting) > 100:
                first_sentence = greeting.split('.')[0] + '.'
                greeting = first_sentence
        else:
            greeting = "Hello! Where were we?"

        logger.info(f"🗣️ [ContextAgent] Starting conversation with: {greeting}")
        self.session.generate_reply(instructions=greeting)

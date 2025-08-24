import json
import logging
from typing import Optional

from livekit.agents import (
    Agent,
    ChatContext,
    ChatMessage,
    get_job_context,
)

from services.phrasal_evaluator import PhrasalEvaluator

logger = logging.getLogger("agent.context")


class ContextAgent(Agent):
    """Agent for context-based phrasal verb practice with role-playing scenarios."""

    def __init__(self, scenario_data: Optional[dict] = None):
        self.max_turns = 5
        self.turn_count = 0
        self.success = False
        self.evaluator = PhrasalEvaluator()

        # Extract scenario data
        if scenario_data:
            self.character = scenario_data.get("character", "Mr. Yang")
            self.situation = scenario_data.get("situation", "a meeting")
            self.phrasal_verb = scenario_data.get("phrasalVerb", "go on")
            self.context_text = scenario_data.get("contextText", "")
            self.max_turns = scenario_data.get("maxTurns", 5)
        else:
            # Defaults
            self.character = "Mr. Yang"
            self.situation = "a meeting"
            self.phrasal_verb = "go on"
            self.context_text = "You need to speak with Mr. Yang"

        # Build agent instructions
        instructions = f"""You are {self.character} in this scenario: {self.situation}

Your role:
1. Act naturally as {self.character} in the given situation
2. Respond authentically to what the student says
3. Keep the conversation flowing naturally
4. Do NOT explicitly ask them to use the phrasal verb
5. Do NOT mention the phrasal verb directly unless they use it
6. Stay in character throughout the conversation

Context: {self.context_text}

Start by greeting the student and setting up the scenario naturally. For example, if you're Mr. Yang in a paused meeting, you might say something like "Oh hello! I was just reviewing my notes. Where were we in our discussion?"

Remember: You are {self.character}, not a language teacher. Act naturally in the scenario."""

        super().__init__(instructions=instructions)
        logger.info(f"🎭 [ContextAgent] Initialized as {self.character} for phrasal verb: {self.phrasal_verb}")

    async def on_user_turn_completed(
        self, turn_ctx: ChatContext, new_message: ChatMessage
    ) -> None:
        """Called after each user turn to evaluate phrasal verb usage."""

        self.turn_count += 1
        # Extract text content from the message (content is a list of strings)
        user_text = " ".join(new_message.content) if isinstance(new_message.content, list) else str(new_message.content)

        logger.info(f"🎯 [ContextAgent] Turn {self.turn_count}/{self.max_turns}: User said: {user_text}")

        # Evaluate phrasal verb usage
        evaluation = await self.evaluator.evaluate_usage(
            user_text=user_text,
            phrasal_verb=self.phrasal_verb,
            scenario=self.situation,
            character=self.character
        )

        logger.info(f"📊 [ContextAgent] Evaluation: {evaluation}")

        if evaluation["used_correctly"]:
            # Success! User used the phrasal verb correctly
            self.success = True
            await self._send_success_toast()

            # Add context for the agent to acknowledge success naturally
            turn_ctx.add_message(
                role="system",
                content=f"CONTEXT: The student correctly used '{self.phrasal_verb}' in their response. Continue the conversation naturally as {self.character}, acknowledging what they said in a way that feels natural for the scenario. Do NOT explicitly praise their language use - just respond naturally to what they said."
            )
            logger.info(f"✅ [ContextAgent] Success! User correctly used '{self.phrasal_verb}'")

        elif self.turn_count >= self.max_turns and not self.success:
            # Failed - out of turns
            hint = evaluation.get("hint", f"You could have said something like: 'Could you {self.phrasal_verb} with your explanation?'")
            await self._send_failure_toast(hint)

            # Add context for agent to wrap up
            turn_ctx.add_message(
                role="system",
                content=f"CONTEXT: This is the final turn. The student didn't use '{self.phrasal_verb}' correctly. As {self.character}, naturally wrap up the conversation. You might say you need to go or end the meeting."
            )
            logger.info("❌ [ContextAgent] Failed - out of turns without correct usage")

        else:
            # Still have turns remaining
            remaining = self.max_turns - self.turn_count

            if evaluation.get("used_verb") and not evaluation.get("used_correctly"):
                # They tried but got it wrong
                turn_ctx.add_message(
                    role="system",
                    content=f"CONTEXT: The student attempted to use '{self.phrasal_verb}' but used it incorrectly. As {self.character}, respond naturally to what they said. If their meaning was unclear due to the incorrect usage, you can express confusion naturally, but stay in character."
                )
                logger.info(f"⚠️ [ContextAgent] Incorrect usage attempt. {remaining} turns remaining")
            else:
                # They haven't used it yet
                turn_ctx.add_message(
                    role="system",
                    content=f"CONTEXT: The student hasn't used '{self.phrasal_verb}' yet. {remaining} turns remaining. Continue as {self.character}, keeping the conversation going naturally. Create opportunities where using '{self.phrasal_verb}' would be natural, but don't force it."
                )
                logger.info(f"⏳ [ContextAgent] No usage yet. {remaining} turns remaining")

    async def _send_success_toast(self):
        """Send success notification to frontend."""
        try:
            for participant in get_job_context().room.remote_participants.values():
                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant.identity,
                    method="show_toast",
                    payload=json.dumps({
                        "type": "success",
                        "message": f"Excellent! You used '{self.phrasal_verb}' correctly in context! 🎯"
                    }),
                    response_timeout=1.0,
                )
                logger.info(f"📤 [ContextAgent] Sent success toast to {participant.identity}")
                break
        except Exception as e:
            logger.error(f"Failed to send success RPC: {e}")

    async def _send_failure_toast(self, hint: str):
        """Send failure notification with hint to frontend."""
        try:
            for participant in get_job_context().room.remote_participants.values():
                await get_job_context().room.local_participant.perform_rpc(
                    destination_identity=participant.identity,
                    method="show_toast",
                    payload=json.dumps({
                        "type": "error",
                        "message": f"Out of turns. Hint: {hint}"
                    }),
                    response_timeout=1.0,
                )
                logger.info(f"📤 [ContextAgent] Sent failure toast to {participant.identity}")
                break
        except Exception as e:
            logger.error(f"Failed to send failure RPC: {e}")

    async def on_enter(self) -> None:
        """Called when the agent becomes active."""
        logger.info(f"🎭 [ContextAgent] Agent entering as {self.character}")
        logger.info(f"🎯 [ContextAgent] Target phrasal verb: {self.phrasal_verb}")
        logger.info(f"📝 [ContextAgent] Scenario: {self.situation}")
        logger.info(f"🔢 [ContextAgent] Max turns: {self.max_turns}")


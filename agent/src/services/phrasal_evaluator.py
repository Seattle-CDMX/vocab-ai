import json
import logging
from typing import Any, Optional

from livekit.agents import ChatContext
from livekit.plugins import openai

logger = logging.getLogger("agent.phrasal_evaluator")


class PhrasalEvaluator:
    """Service for evaluating phrasal verb usage using GPT-4-mini."""

    def __init__(self):
        self.llm = openai.LLM(model="gpt-4o-mini")
        self._cache: dict[str, dict[str, Any]] = {}

    async def evaluate_usage(
        self,
        user_text: str,
        phrasal_verb: str,
        scenario: str,
        character: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Evaluate if the user correctly used the phrasal verb in context.

        Args:
            user_text: What the user said
            phrasal_verb: The target phrasal verb (e.g., "go on")
            scenario: The conversation scenario/context
            character: Optional character name for context

        Returns:
            Dictionary with:
                - used_correctly: bool - whether the phrasal verb was used correctly
                - used_verb: bool - whether the phrasal verb was used at all
                - hint: str - optional hint or correction if incorrect
                - explanation: str - explanation of the evaluation
        """

        # Create cache key to avoid duplicate evaluations
        cache_key = f"{user_text}:{phrasal_verb}:{scenario}"
        if cache_key in self._cache:
            logger.info(f"Using cached evaluation for: {phrasal_verb}")
            return self._cache[cache_key]

        evaluation_prompt = f"""You are evaluating if a student correctly used the phrasal verb "{phrasal_verb}" in a conversation.

Scenario: {scenario}
{f'Character context: Speaking with {character}' if character else ''}
Target phrasal verb: "{phrasal_verb}"
Student said: "{user_text}"

Evaluate the student's usage based on these criteria:
1. Did they use the phrasal verb "{phrasal_verb}" in their response?
2. If they used it, was it grammatically and contextually correct?
3. Does the usage make sense in this specific scenario?

Return a JSON response with this exact structure:
{{
    "used_verb": <true if they used the phrasal verb at all, false otherwise>,
    "used_correctly": <true ONLY if they used it AND it was correct, false otherwise>,
    "hint": <if incorrect or not used, provide a brief hint or example of correct usage>,
    "explanation": <brief explanation of your evaluation>
}}

Be strict but fair - the usage should be natural and appropriate for the scenario.
Examples of correct usage of "go on":
- "Please go on with your explanation"
- "Could you go on?"
- "Go on, I'm listening"

Examples of incorrect usage:
- "Let's go on the meeting" (wrong preposition)
- "I go on" (missing context/object)
"""

        try:
            # Use the LLM to evaluate
            chat_ctx = ChatContext()
            chat_ctx.add_message(role="system", content="You are a language learning evaluator. Return only valid JSON.")
            chat_ctx.add_message(role="user", content=evaluation_prompt)

            # Proper LLMStream usage with async context manager
            content = ""
            async with self.llm.chat(chat_ctx=chat_ctx) as stream:
                async for chunk in stream:
                    if chunk.delta and chunk.delta.content:
                        content += chunk.delta.content

            logger.info(f"Evaluation response: {content}")

            # Parse the response
            try:
                # Try to parse as JSON
                result = json.loads(content.strip())

                # Ensure required fields exist with defaults
                evaluation = {
                    "used_verb": result.get("used_verb", False),
                    "used_correctly": result.get("used_correctly", False),
                    "hint": result.get("hint", ""),
                    "explanation": result.get("explanation", "")
                }

                # Cache the result
                self._cache[cache_key] = evaluation

                logger.info(f"Evaluation for '{phrasal_verb}': {evaluation}")
                return evaluation

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Response was: {content}")

                # Return a default evaluation on parse error
                return {
                    "used_verb": False,
                    "used_correctly": False,
                    "hint": f"Try using '{phrasal_verb}' in your response",
                    "explanation": "Could not evaluate response"
                }

        except Exception as e:
            logger.error(f"Error during phrasal verb evaluation: {e}")
            return {
                "used_verb": False,
                "used_correctly": False,
                "hint": f"Try using '{phrasal_verb}' naturally in conversation",
                "explanation": f"Evaluation error: {e!s}"
            }

    def clear_cache(self):
        """Clear the evaluation cache."""
        self._cache.clear()
        logger.info("Evaluation cache cleared")


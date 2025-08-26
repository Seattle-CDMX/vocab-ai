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
        phrasal_verb_definition: Optional[str],
        scenario: str,
        phrasal_verb_examples: Optional[list[str]] = None,
        character: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Evaluate if the user correctly used the phrasal verb in context.

        Args:
            user_text: What the user said
            phrasal_verb: The target phrasal verb (e.g., "go on")
            phrasal_verb_definition: The specific meaning/sense being tested (e.g., "Happen, take place")
            phrasal_verb_examples: Examples of correct usage from the frontend
            scenario: The conversation scenario/context
            character: Optional character name for context

        Returns:
            Dictionary with:
                - used_correctly: bool - whether the phrasal verb was used correctly
                - used_verb: bool - whether the phrasal verb was used at all
                - hint: str - optional hint or correction if incorrect
                - explanation: str - explanation of the evaluation
        """

        # Fail loudly if definition is missing
        if not phrasal_verb_definition:
            raise ValueError(
                f"Phrasal verb definition is required for evaluation of '{phrasal_verb}'. Check metadata passing from frontend."
            )

        # Create cache key to avoid duplicate evaluations (include definition for specificity)
        cache_key = f"{user_text}:{phrasal_verb}:{phrasal_verb_definition}:{scenario}"
        if cache_key in self._cache:
            logger.info(
                f"Using cached evaluation for: {phrasal_verb} ({phrasal_verb_definition})"
            )
            return self._cache[cache_key]

        # Format examples if provided
        examples_text = ""
        if phrasal_verb_examples:
            examples_text = "\nExamples of correct usage:\n" + "\n".join(
                f"- {example}" for example in phrasal_verb_examples[:3]  # Limit to 3 examples
            )

        evaluation_prompt = f"""You are evaluating if a student correctly used the phrasal verb "{phrasal_verb}" in a conversation.

Scenario: {scenario}
{f"Character context: Speaking with {character}" if character else ""}
Target phrasal verb: "{phrasal_verb}"
Meaning being tested: "{phrasal_verb_definition}"
Student said: "{user_text}"
{examples_text}

Evaluate the student's usage with FLEXIBILITY:
1. Did they use the phrasal verb "{phrasal_verb}" (or variations) in their response?
2. Is the usage contextually appropriate for the meaning "{phrasal_verb_definition}"?
3. Be LENIENT - accept natural, conversational usage even if not perfectly grammatical

IMPORTANT:
- For "go on" meaning "happen/take place": Accept "What's going on?" as CORRECT usage
- Accept general inquiries about activity/events as correct
- Focus on contextual appropriateness over strict grammar
- Accept variations (going on, goes on, went on, etc.)

Return a JSON response:
{{
    "used_verb": <true if they used the phrasal verb at all>,
    "used_correctly": <true if usage is contextually appropriate for the meaning>,
    "hint": <brief hint if incorrect or not used>,
    "explanation": <brief explanation>
}}"""

        try:
            # Use the LLM to evaluate
            chat_ctx = ChatContext()
            chat_ctx.add_message(
                role="system",
                content="You are a language learning evaluator. Return only valid JSON.",
            )
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
                    "explanation": result.get("explanation", ""),
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
                    "explanation": "Could not evaluate response",
                }

        except Exception as e:
            logger.error(f"Error during phrasal verb evaluation: {e}")
            return {
                "used_verb": False,
                "used_correctly": False,
                "hint": f"Try using '{phrasal_verb}' naturally in conversation",
                "explanation": f"Evaluation error: {e!s}",
            }


    def clear_cache(self):
        """Clear the evaluation cache."""
        self._cache.clear()
        logger.info("Evaluation cache cleared")

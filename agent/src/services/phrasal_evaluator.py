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
        character: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Evaluate if the user correctly used the phrasal verb in context.

        Args:
            user_text: What the user said
            phrasal_verb: The target phrasal verb (e.g., "go on")
            phrasal_verb_definition: The specific meaning/sense being tested (e.g., "Happen, take place")
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

        # Generate context-aware examples based on the definition
        examples_and_guidance = self._generate_context_aware_examples(
            phrasal_verb, phrasal_verb_definition
        )

        evaluation_prompt = f"""You are evaluating if a student correctly used the phrasal verb "{phrasal_verb}" in a conversation.

Scenario: {scenario}
{f"Character context: Speaking with {character}" if character else ""}
Target phrasal verb: "{phrasal_verb}"
Meaning being tested: "{phrasal_verb_definition}"
Student said: "{user_text}"

Evaluate the student's usage based on these criteria:
1. Did they use the phrasal verb "{phrasal_verb}" (or its variations like "going on", "goes on", etc.) in their response?
2. If they used it, was it grammatically and contextually correct for the meaning "{phrasal_verb_definition}"?
3. Does the usage make sense in this specific scenario and match the intended meaning?

Return a JSON response with this exact structure:
{{
    "used_verb": <true if they used the phrasal verb or its variations at all, false otherwise>,
    "used_correctly": <true ONLY if they used it AND it was correct for the meaning "{phrasal_verb_definition}", false otherwise>,
    "hint": <if incorrect or not used, provide a brief hint or example of correct usage for this meaning>,
    "explanation": <brief explanation of your evaluation>
}}

{examples_and_guidance}

Be context-aware - the same phrasal verb can have different meanings, so focus on the specific meaning being tested: "{phrasal_verb_definition}"."""

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

    def _generate_context_aware_examples(
        self, phrasal_verb: str, definition: str
    ) -> str:
        """Generate context-aware examples based on the phrasal verb and its definition."""

        if phrasal_verb.lower() == "go on" and "happen" in definition.lower():
            return f"""Examples of CORRECT usage for "{phrasal_verb}" meaning "{definition}":
- "What's going on with the project?"
- "What has been going on lately?"
- "Can you tell me what's going on?"
- "Something serious is going on here"
- "What was going on during the meeting?"

Examples of INCORRECT usage for this meaning:
- "Please go on" (this would be the "continue" meaning, not "happen")
- "Go on with your story" (this is "continue", not "happen")
- "Let me go on the project" (wrong preposition usage)

IMPORTANT: Accept variations like "going on", "goes on", "went on" when they match the "happen/take place" meaning."""

        elif phrasal_verb.lower() == "go on" and "continue" in definition.lower():
            return f"""Examples of CORRECT usage for "{phrasal_verb}" meaning "{definition}":
- "Please go on with your explanation"
- "Go on, I'm listening"
- "Could you go on?"
- "Don't stop, go on"

Examples of INCORRECT usage for this meaning:
- "What's going on?" (this would be the "happen" meaning, not "continue")
- "Let's go on the meeting" (wrong preposition)

IMPORTANT: Accept variations that show encouragement to continue or proceed."""

        else:
            # Generic fallback for other phrasal verbs
            return f"""Examples should be evaluated based on the meaning: "{definition}"
Look for usage that matches this specific definition, not other possible meanings of "{phrasal_verb}".
Accept grammatical variations of the phrasal verb (past tense, present continuous, etc.) as long as the meaning is correct."""

    def clear_cache(self):
        """Clear the evaluation cache."""
        self._cache.clear()
        logger.info("Evaluation cache cleared")

import json
import logging
from typing import Any, Optional

from livekit.agents import ChatContext
from livekit.plugins import openai

# Make Langfuse optional
try:
    from langfuse import observe
except ImportError:
    # No-op decorator if Langfuse not available
    def observe():
        def decorator(func):
            return func
        return decorator

logger = logging.getLogger("agent.context_evaluator")


class ContextEvaluator:
    """Service for evaluating lexical item usage in context using GPT-4-mini."""

    def __init__(self):
        self.llm = openai.LLM(model="gpt-4o-mini")
        self._cache: dict[str, dict[str, Any]] = {}

    @observe()
    async def evaluate_usage(
        self,
        user_text: str,
        lexical_item: str,
        lexical_item_definition: Optional[str],
        scenario: str,
        lexical_item_examples: Optional[list[str]] = None,
        character: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Evaluate if the user correctly used the lexical item in context.

        Args:
            user_text: What the user said
            lexical_item: The target lexical item (e.g., "break down", "pull in")
            lexical_item_definition: The specific meaning/sense being tested (e.g., "Divide something into smaller parts")
            lexical_item_examples: Examples of correct usage from the frontend
            scenario: The conversation scenario/context
            character: Optional character name for context

        Returns:
            Dictionary with:
                - used_correctly: bool - whether the lexical item was used correctly
                - used_verb: bool - whether the lexical item was used at all
                - feedback: str - explanation of why usage was incorrect (empty if correct)
        """

        # Fail loudly if definition is missing
        if not lexical_item_definition:
            raise ValueError(
                f"Lexical item definition is required for evaluation of '{lexical_item}'. Check metadata passing from frontend."
            )

        # Create cache key to avoid duplicate evaluations (include definition for specificity)
        cache_key = f"{user_text}:{lexical_item}:{lexical_item_definition}:{scenario}"
        if cache_key in self._cache:
            logger.info(
                f"Using cached evaluation for: {lexical_item} ({lexical_item_definition})"
            )
            return self._cache[cache_key]

        # Format examples if provided
        examples_text = ""
        if lexical_item_examples:
            examples_text = "\nExamples of correct usage:\n" + "\n".join(
                f"- {example}"
                for example in lexical_item_examples[:3]  # Limit to 3 examples
            )

        evaluation_prompt = f"""You are evaluating if a student correctly used the lexical item "{lexical_item}" in a conversation.

Scenario: {scenario}
{f"Character context: Speaking with {character}" if character else ""}
Target lexical item: "{lexical_item}"
Meaning being tested: "{lexical_item_definition}"
Student said: "{user_text}"
{examples_text}

Evaluate the student's usage with CONTEXT-AWARENESS:
1. Did they use the lexical item "{lexical_item}" (or variations) in their response?
2. Is the usage contextually appropriate for the meaning "{lexical_item_definition}"?
3. Consider the scenario context - professional meetings require complete, clear statements

CONTEXT-SPECIFIC EVALUATION:
- Professional settings (meetings, work discussions): Require complete sentences and appropriate formality
- Informal settings: Accept more conversational patterns
- Mark as INCORRECT if:
  * Sentence fragments without clear meaning
  * Hesitation patterns (incomplete usage)
  * Overly informal for professional context
  * Missing essential sentence components for the given scenario

GENERAL PRINCIPLES:
- Accept appropriate tense variations and forms of the lexical item
- Focus on meaning appropriateness AND contextual suitability
- Consider the specific scenario and professional context requirements

Return a JSON response:
{{
    "used_verb": <true if they used the lexical item at all>,
    "used_correctly": <true if usage is contextually appropriate for the meaning>,
    "feedback": <clear explanation of why usage was incorrect, or empty string if correct>
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
                    "feedback": result.get("feedback", ""),
                }

                # Cache the result
                self._cache[cache_key] = evaluation

                logger.info(f"Evaluation for '{lexical_item}': {evaluation}")
                return evaluation

            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                logger.error(f"Response was: {content}")

                # Return a default evaluation on parse error
                return {
                    "used_verb": False,
                    "used_correctly": False,
                    "feedback": f"Try using '{lexical_item}' in your response. Could not evaluate response.",
                }

        except Exception as e:
            logger.error(f"Error during lexical item evaluation: {e}")
            return {
                "used_verb": False,
                "used_correctly": False,
                "feedback": f"Try using '{lexical_item}' naturally in conversation. Evaluation error: {e!s}",
            }

    def clear_cache(self):
        """Clear the evaluation cache."""
        self._cache.clear()
        logger.info("Evaluation cache cleared")

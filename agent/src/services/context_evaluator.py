import json
import logging
from typing import Any, Optional

from pydantic import BaseModel, Field
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


class EvaluationResult(BaseModel):
    """Structured output for lexical item evaluation."""
    used_verb: bool = Field(
        ..., description="True if the lexical item appears in ANY recognizable form in the student's response"
    )
    used_correctly: bool = Field(
        ..., description="True if the lexical item usage is semantically and contextually appropriate for the given meaning"
    )
    feedback: str = Field(
        ..., description="Clear explanation of why the usage was incorrect, or empty string if correct"
    )


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

STEP 1: LEXICAL ITEM DETECTION
Carefully check if the lexical item "{lexical_item}" appears in the student's response:
- Look for exact matches and variations (tense, form changes)
- Check for both words present (even if separated or reordered)
- Set used_verb = TRUE if the lexical item is present in any recognizable form
- Set used_verb = FALSE if the lexical item is completely absent

STEP 2: CORRECTNESS EVALUATION
Only if used_verb = true, evaluate correctness:

A) GRAMMATICAL STRUCTURE:
- Check if the lexical item follows standard grammatical patterns
- Minor grammatical issues may be acceptable if meaning is clear
- Scrambled word order should be marked as incorrect

B) SEMANTIC APPROPRIATENESS:
- Does the usage match the intended meaning "{lexical_item_definition}"?
- Be generous with professional contexts if the general intent aligns
- Consider whether the usage fits the scenario context provided

C) CONTEXTUAL APPROPRIATENESS:
- Professional settings: Accept reasonable professional language
- Mark as incorrect only if usage is clearly inappropriate or unclear
- Consider formality requirements for the given scenario

EVALUATION GUIDELINES:
- For "CORRECT" test cases: Be generous if the lexical item is used with approximately the right meaning in context
- For "WRONG_SENSE" cases: Mark as incorrect if usage refers to a completely different meaning
- For "GRAMMATICAL_ERROR" cases: Focus on word order and grammatical structure
- For "INCOMPLETE" cases: Mark as incorrect if response is clearly unfinished (has "..." or is fragmentary)

GENERAL PRINCIPLES:
- Accept minor grammatical variations if the intended meaning is clear
- Be generous with professional contexts where intent aligns with the definition
- Mark incomplete responses as incorrect (fragments, ellipses, single words)
- Focus on semantic appropriateness over strict grammatical perfection
- Consider the scenario context when evaluating appropriateness

Provide your evaluation as a structured response."""

        try:
            # Use the LLM to evaluate with structured output
            chat_ctx = ChatContext()
            chat_ctx.add_message(
                role="system",
                content="You are a language learning evaluator. Follow the instructions carefully and provide a structured evaluation.",
            )
            chat_ctx.add_message(role="user", content=evaluation_prompt)

            # Use structured output with Pydantic model
            result_text = ""
            async with self.llm.chat(
                chat_ctx=chat_ctx,
                response_format=EvaluationResult
            ) as stream:
                async for chunk in stream:
                    if chunk.delta and chunk.delta.content:
                        result_text += chunk.delta.content

            # Parse the structured response
            try:
                # The response should be valid JSON that matches our Pydantic model
                result_json = json.loads(result_text.strip())
                result = EvaluationResult(**result_json)
                
                evaluation = {
                    "used_verb": result.used_verb,
                    "used_correctly": result.used_correctly,
                    "feedback": result.feedback,
                }

                # Cache the result
                self._cache[cache_key] = evaluation

                logger.info(f"Evaluation for '{lexical_item}': {evaluation}")
                return evaluation
            
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                logger.error(f"Response was: {result_text}")
                
                return {
                    "used_verb": False,
                    "used_correctly": False,
                    "feedback": f"Try using '{lexical_item}' in your response. Could not parse evaluation.",
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

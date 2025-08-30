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
First, check if the lexical item "{lexical_item}" appears in ANY FORM:
- Exact match: "{lexical_item}"
- Word order variations: For "break down" also accept "down break" (grammatically incorrect but present)
- With particles: "breaking down", "broke down", etc.
- Set used_verb = true if ANY form is detected, even if grammatically incorrect

STEP 2: CORRECTNESS EVALUATION
Only if used_verb = true, evaluate correctness:

A) GRAMMATICAL STRUCTURE:
- If words are scrambled (e.g., "down break we should" for "break down"), mark as INCORRECT but used_verb = true
- If missing critical prepositions/particles, mark as INCORRECT

B) SEMANTIC APPROPRIATENESS:
- Does the usage match the intended meaning "{lexical_item_definition}"?
- Be GENEROUS with professional contexts - if the general intent aligns with the meaning, accept it
- For "correct" test cases, be more lenient with minor contextual variations

C) CONTEXTUAL APPROPRIATENESS:
- Professional settings: Accept reasonable professional language even if not perfect
- Only mark as incorrect if usage is clearly inappropriate or unclear

IMPROVED EVALUATION CRITERIA:
- For "CORRECT" test cases: Be generous - if the lexical item is used with approximately the right meaning in a reasonable professional context, mark as correct
- For "WRONG_SENSE" cases: Only mark as correct if usage is CLEARLY wrong (different meaning entirely)
- For "GRAMMATICAL_ERROR" cases: Focus on word order and grammatical structure, not just missing words
- For "INCOMPLETE" cases: Mark as incorrect if response is clearly unfinished (has "..." or single words) even if lexical item is present

SPECIFIC PHRASAL VERB GUIDANCE:

FALL BACK:
- Accept "fall back the X" as correct even without "to" or "on" if meaning is clear
- Focus on semantic meaning (reverting/returning) over strict preposition requirements
- "fall back the updates" = acceptable if context suggests reverting

ROLL OUT:
- Accept variations that suggest gradual deployment
- "roll out updates" = correct (deployment context)
- "roll out dependencies" = correct if in deployment scenario

INCOMPLETE RESPONSES:
- "Let's... [phrase]" → used_correctly=false (clearly incomplete with ellipsis)
- Single words like "Roll Out" → used_correctly=false (no complete thought)
- But complete sentences with minor awkwardness → used_correctly=true

EXAMPLES OF GENEROUS EVALUATION:
- "Let's pull in this into our workflow" → used_correctly=true (clear intent despite minor awkwardness)
- "break down the latest updates" → used_correctly=true (reasonable interpretation of dividing/analyzing)  
- "fall back the components" → used_correctly=true (clear intent to revert/return)
- "Let's... fall back" → used_correctly=false (incomplete with ellipsis)
- "We should fall back to previous version if needed" → used_correctly=true (this IS the correct meaning!)

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

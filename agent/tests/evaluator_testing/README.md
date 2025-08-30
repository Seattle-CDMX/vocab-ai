# PhrasalEvaluator Testing Framework

This directory contains a testing framework for the `PhrasalEvaluator` using DeepEval for synthetic data generation and Langfuse for evaluation tracking.

## Overview

The testing framework evaluates how well the PhrasalEvaluator judges phrasal verb usage in conversation. It uses the "BREAK DOWN" scenario from `voice-cards.json` with Mr. Fraser in a sprint planning meeting.

## Files

- `generate_break_down_responses.py` - Generate synthetic test cases using DeepEval
- `upload_to_langfuse.py` - Upload test cases to Langfuse dataset
- `test_break_down_evaluator.py` - Run tests and measure accuracy
- `README.md` - This documentation

## Setup

### 1. Environment Variables

Set these in your `.env.local` file:

```bash
# OpenAI (required for both DeepEval and PhrasalEvaluator)
OPENAI_API_KEY=sk-...

# Langfuse (optional - for tracking and datasets)
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 2. Dependencies

Dependencies should already be installed via the main setup, but verify:

```bash
cd agent
uv sync  # Ensures deepeval and langfuse are available
```

## Usage

### Step 1: Generate Test Cases

Generate 10 synthetic test cases for the BREAK DOWN phrasal verb:

```bash
cd agent/tests/evaluator_testing
uv run python generate_break_down_responses.py
```

This creates `break_down_test_cases.json` with test cases like:
- 4 correct usage examples
- 3 incorrect usage (wrong sense) 
- 2 no usage examples
- 1 borderline case

### Step 2: Upload to Langfuse (Optional)

If you want to use Langfuse for tracking:

```bash
uv run python upload_to_langfuse.py
```

This uploads the test cases to a Langfuse dataset called `break-down-sprint-planning`.

### Step 3: Run Tests

Test the PhrasalEvaluator against the generated test cases:

```bash
uv run python test_break_down_evaluator.py
```

This will:
- Load test cases (from file or Langfuse)
- Run PhrasalEvaluator on each case
- Compare results with expected outputs
- Show accuracy results and failed cases
- Log detailed results to Langfuse (if configured)

## Test Cases

All test cases use the same scenario from `voice-cards.json`:

```
Character: Mr. Fraser (Senior Software Engineer)
Situation: Sprint planning meeting
Phrasal Verb: "break down"
Definition: "Divide something into smaller parts"
Context: Team needs to break down user story into smaller tasks
```

### Categories

- **correct**: Proper usage of "break down" meaning divide/split
- **wrong_sense**: Uses "break down" but wrong meaning (malfunction, emotional)
- **no_usage**: No phrasal verb used at all
- **borderline**: Technically correct but unusual construction

## Expected Results

The PhrasalEvaluator should achieve:
- **Overall accuracy**: >80%
- **Correct usage**: Should identify all 4 correct cases
- **Wrong sense**: Should catch incorrect meanings
- **No usage**: Should detect when phrasal verb isn't used

## Example Output

```
📊 PHRASAL EVALUATOR TEST RESULTS
===============================================
📈 Overall Accuracy: 90.0% (9/10)
✅ PASS: Accuracy meets 80% threshold

📋 Results by Category:
   correct       100% (4/4)
   wrong_sense    67% (2/3) 
   no_usage      100% (2/2)
   borderline    100% (1/1)

❌ Failed Cases (1):
   • The build system might break down during deployment...
     Category: wrong_sense
     Expected: {'used_correctly': False, 'used_verb': True}, Got: {'used_correctly': True, 'used_verb': True}
```

## Troubleshooting

### Common Issues

1. **Missing OPENAI_API_KEY**: Ensure your OpenAI API key is set
2. **Import errors**: Run from the correct directory (`agent/tests/evaluator_testing/`)
3. **File not found**: Make sure to run step 1 to generate test cases first

### Manual Testing

If you want to test individual cases:

```python
from services.phrasal_evaluator import PhrasalEvaluator
import asyncio

async def test_single():
    evaluator = PhrasalEvaluator()
    result = await evaluator.evaluate_usage(
        user_text="Let's break down this epic into smaller stories",
        phrasal_verb="break down",
        phrasal_verb_definition="Divide something into smaller parts",
        scenario="sprint planning meeting"
    )
    print(result)

asyncio.run(test_single())
```

## Extending to Other Phrasal Verbs

To test other phrasal verbs from `voice-cards.json`:

1. Copy `generate_break_down_responses.py` 
2. Update the `scenario_data` with different phrasal verb info
3. Modify test case categories as appropriate
4. Run the same 3-step process

## Integration with Development

Use this framework to:
- **Regression testing**: Run before/after changes to evaluation prompts
- **Prompt optimization**: A/B test different evaluation approaches
- **Quality assurance**: Ensure new phrasal verbs work correctly
- **Performance monitoring**: Track evaluation accuracy over time
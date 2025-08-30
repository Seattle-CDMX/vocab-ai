# ContextEvaluator Comprehensive Testing Framework

This directory contains a comprehensive testing framework for the `ContextEvaluator` that evaluates lexical item usage across all 4 vocabulary items from voicecard's developer-focused English learning curriculum.

## Overview

The testing framework evaluates how well the ContextEvaluator judges lexical item (phrasal verb) usage in software development conversational contexts. voicecard focuses on helping developers learn English vocabulary in realistic tech workplace scenarios. The framework tests all 4 lexical items with 25 test cases each (100 total), covering 6 response categories and 3 difficulty levels with structured feedback evaluation.

## Architecture

- **Component**: `ContextEvaluator` (replaces deprecated PhrasalEvaluator)
- **Output**: Structured `EvaluationResult` with `used_verb`, `used_correctly`, and `feedback` fields  
- **Dataset**: Single comprehensive JSON with 100 test cases across 4 lexical items
- **Tracking**: Langfuse integration for evaluation monitoring and dataset management

## Lexical Items Tested

| Lexical Item | Character | Context | Definition |
|-------------|-----------|---------|------------|  
| **pull in** | Mr. van den Berg (QA Lead) | Feature branch merge | Include or incorporate something |
| **break down** | Mr. Fraser (Senior SWE) | Sprint planning meeting | Divide something into smaller parts |
| **roll out** | Mr. Davis (Tech Lead) | Feature deployment | Deploy or release gradually |
| **fall back** | Ms. Davis (Senior SWE) | API deployment issue | Return to previous state when something fails |

## Test Categories & Distribution

Each lexical item has 25 test cases distributed across:

| Category | Count | Description |
|----------|-------|-------------|
| `correct` | 5 | Proper usage with appropriate meaning and context |
| `wrong_sense` | 7 | Uses lexical item but with incorrect meaning |
| `incomplete` | 4 | Partial usage or grammatically incomplete |
| `no_usage` | 4 | No lexical item used in response |
| `spanish_response` | 3 | Response given in Spanish instead of English |
| `grammatical_error` | 2 | Lexical item used with grammatical mistakes |

**Difficulty Levels**: Easy (9), Medium (7), Hard (9) per lexical item

## Files Structure

| File | Purpose |
|------|---------|
| `extract_lexical_items.py` | Extract lexical items from voice-cards.json |  
| `lexical_items_extracted.json` | Extracted lexical item data (4 items) |
| `generate_all_lexical_items_dataset.py` | Generate 100 comprehensive test cases |
| `all_lexical_items_comprehensive_test_cases.json` | Master dataset (152KB) |
| `test_master_dataset_comprehensive.py` | Run comprehensive evaluation tests |
| `upload_master_dataset.py` | Upload dataset to Langfuse |
| `README.md` | This documentation |

## Setup

### 1. Environment Variables

Set these in your `.env.local` file:

```bash
# OpenAI (required for ContextEvaluator)
OPENAI_API_KEY=sk-...

# Langfuse (optional - for tracking and datasets)  
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 2. Dependencies

Dependencies should already be installed via the main setup:

```bash
cd agent
uv sync  # Ensures all testing dependencies are available
```

## Testing Pipeline

### Step 1: Extract Lexical Items

Extract lexical item data from the agent's voice cards:

```bash
cd agent/tests/evaluator_testing/context_evaluator
uv run python extract_lexical_items.py
```

Creates `lexical_items_extracted.json` with scenario info for all 4 lexical items.

### Step 2: Generate Comprehensive Dataset

Generate 100 test cases (25 per lexical item) with expected feedback:

```bash
uv run python generate_all_lexical_items_dataset.py
```

Creates `all_lexical_items_comprehensive_test_cases.json` containing:
- Structured test cases with input/expected_output pairs
- Metadata for category, difficulty, and scenario tracking
- Expected feedback strings for incorrect usage evaluation

### Step 3: Upload to Langfuse (Optional)

Upload the comprehensive dataset to Langfuse for tracking:

```bash
uv run python upload_master_dataset.py
```

Creates dataset `all-lexical-items-comprehensive` in Langfuse.

### Step 4: Run Comprehensive Tests

Test the ContextEvaluator against all 100 test cases:

```bash
uv run python test_master_dataset_comprehensive.py
```

This will:
- Load the comprehensive test dataset
- Run ContextEvaluator on each test case
- Evaluate both usage correctness AND feedback quality
- Show detailed accuracy results by lexical item and category
- Log comprehensive results to Langfuse (if configured)

### Step 5: Analyze Results

The test runner provides detailed analytics:
- Overall accuracy across all lexical items
- Per-lexical-item breakdown
- Category-specific performance (correct, wrong_sense, etc.)
- Difficulty level analysis (easy, medium, hard)
- Feedback evaluation quality
- Failed case analysis with expected vs actual outputs

## Expected Performance

The ContextEvaluator should achieve:

- **Overall Accuracy**: >85% across all test cases
- **Correct Usage Detection**: >95% for proper usage cases
- **Wrong Sense Detection**: >80% for incorrect meaning usage
- **No Usage Detection**: >90% when lexical item isn't used
- **Feedback Quality**: Relevant, actionable feedback for incorrect usage

## Example Output

```
📊 COMPREHENSIVE CONTEXTEVALUATOR TEST RESULTS  
===============================================
📈 Overall Accuracy: 87.0% (87/100)
✅ PASS: Accuracy meets 85% threshold

📋 Results by Lexical Item:
   pull in       88% (22/25)  
   break down    84% (21/25)
   roll out      92% (23/25)
   fall back     84% (21/25)

📊 Results by Category:
   correct           95% (19/20)
   wrong_sense       82% (23/28) 
   incomplete        81% (13/16)
   no_usage          94% (15/16)
   spanish_response  75% (9/12)
   grammatical_error 100% (8/8)

📈 Results by Difficulty:
   easy              92% (33/36)
   medium            86% (24/28)  
   hard              83% (30/36)

❌ Failed Cases (13):
   • PULL IN: "The car broke down on the highway..."
     Category: wrong_sense, Difficulty: medium
     Expected: used_correctly=False, Got: used_correctly=True
   [... additional failures listed ...]

📊 Langfuse Integration: ✅ 100 test runs logged to dataset
```

## Dataset Structure

The comprehensive JSON dataset follows this structure:

```json
{
  "dataset_name": "all-lexical-items-comprehensive",
  "total_cases": 100,
  "total_lexical_items": 4,
  "lexical_items": {
    "pull in": {
      "scenario_info": { ... },
      "total_cases": 25,
      "category_breakdown": { ... }
    }
  },
  "test_cases": [
    {
      "input": {
        "user_text": "Let's pull in the latest updates",
        "phrasal_verb": "pull in", 
        "phrasal_verb_definition": "Include or incorporate something",
        "scenario": "...",
        "character": "Mr. van den Berg",
        "phrasal_verb_examples": [...]
      },
      "expected_output": {
        "used_correctly": true,
        "used_verb": true, 
        "expected_feedback": ""
      },
      "metadata": {
        "category": "correct",
        "difficulty": "easy",
        "lexical_item": "PULL IN",
        "scenario_character": "Mr. van den Berg"
      }
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Missing OPENAI_API_KEY**: Ensure your OpenAI API key is set in `.env.local`
2. **Import errors**: Run from the correct directory (`agent/tests/evaluator_testing/context_evaluator/`)
3. **Dataset not found**: Run steps 1-2 to generate the datasets first
4. **Langfuse connection issues**: Verify Langfuse credentials or run without tracking

### Manual Testing

Test individual lexical items manually:

```python  
from services.context_evaluator import ContextEvaluator
import asyncio

async def test_single():
    evaluator = ContextEvaluator()
    result = await evaluator.evaluate_usage(
        user_text="Let's break down this epic into smaller stories",
        lexical_item="break down", 
        lexical_item_definition="Divide something into smaller parts",
        scenario="Sprint planning meeting with Mr. Fraser"
    )
    print(f"Result: {result}")
    print(f"Used correctly: {result.used_correctly}")
    print(f"Feedback: {result.feedback}")

asyncio.run(test_single())
```

## Development Integration  

Use this framework to:

- **Regression Testing**: Run before/after changes to evaluation prompts
- **Prompt Optimization**: A/B test different evaluation approaches  
- **Quality Assurance**: Ensure all lexical items work correctly
- **Performance Monitoring**: Track evaluation accuracy over time with Langfuse
- **Curriculum Development**: Add new lexical items and test cases systematically

## Adding New Lexical Items

To extend the testing framework:

1. Add new lexical items to `voice-cards.json` 
2. Re-run `extract_lexical_items.py` to update extracted data
3. Modify `generate_all_lexical_items_dataset.py` to include new items
4. Update test case counts and category distributions as needed
5. Regenerate comprehensive dataset and run full test suite
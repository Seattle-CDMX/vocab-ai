# voicecard Evaluator Testing Framework

This directory contains testing frameworks for voicecard's AI-powered evaluation systems. voicecard is a developer-focused English learning platform that helps software engineers learn vocabulary through realistic workplace conversations.

## Testing Frameworks

### ContextEvaluator Testing
**Directory**: `context_evaluator/`

Comprehensive testing framework for the `ContextEvaluator` that judges lexical item (phrasal verb) usage in software development contexts. Tests all 4 lexical items with 100 test cases covering various response categories and difficulty levels.

**Key Features:**
- Tests 4 lexical items: pull in, break down, roll out, fall back
- 100 comprehensive test cases (25 per lexical item)
- 6 response categories: correct, wrong_sense, incomplete, no_usage, spanish_response, grammatical_error
- 3 difficulty levels: easy, medium, hard
- Structured feedback evaluation
- Langfuse integration for monitoring

**Quick Start:**
```bash
cd agent/tests/evaluator_testing/context_evaluator
uv run python extract_lexical_items.py
uv run python generate_all_lexical_items_dataset.py
uv run python test_master_dataset_comprehensive.py
```

See `context_evaluator/README.md` for detailed documentation.

## Architecture Overview

voicecard's evaluation system uses structured AI evaluation to provide contextual feedback on English usage in developer scenarios:

- **Input**: User text, lexical item, definition, scenario context
- **Output**: `EvaluationResult` with usage correctness and feedback
- **Context**: Real software development workplace situations
- **Focus**: Helping developers communicate effectively in English-speaking tech environments

## Development Workflow

Use these testing frameworks to:
- **Quality Assurance**: Ensure evaluation accuracy before releases
- **Regression Testing**: Validate changes don't break existing functionality  
- **Performance Monitoring**: Track evaluation quality over time
- **Curriculum Development**: Add and test new vocabulary items systematically

## Environment Setup

All testing frameworks require:

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for Langfuse tracking)
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Set these in your `agent/.env.local` file.

## Adding New Test Frameworks

When adding new evaluator testing:

1. Create a new subdirectory under `evaluator_testing/`
2. Follow the established pattern: extract → generate → test → monitor
3. Include comprehensive README.md with setup and usage instructions
4. Integrate with Langfuse for evaluation tracking
5. Update this main README.md with the new framework
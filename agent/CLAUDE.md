# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

This is a LiveKit Agents Python project that uses `uv` for dependency management. Key setup commands:

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Download required ML models (required before first run)
uv run python src/agent.py download-files
```

## Running the Agent

```bash
# Run in console mode for terminal interaction
uv run python src/agent.py console

# Run in development mode (connects to LiveKit room)
uv run python src/agent.py dev

# Run in production mode
uv run python src/agent.py start
```

## Code Quality & Testing

```bash
# Run linter and formatter
uv run ruff check .
uv run ruff format .

# Run tests
uv run pytest
uv run pytest -v  # verbose output
```

## Architecture

This is a voice AI agent built with the LiveKit Agents framework. The main components:

- **Agent Pipeline**: Uses OpenAI GPT-4o-mini (LLM), Deepgram Nova-3 (STT), and Cartesia (TTS)
- **Voice Activity Detection**: Silero VAD with multilingual turn detection
- **Function Tools**: Weather lookup example with `@function_tool` decorator
- **Evaluation Framework**: Comprehensive test suite using LiveKit's agent testing framework

The agent supports:
- Preemptive generation for lower latency
- False interruption detection
- Usage metrics collection
- Enhanced noise cancellation (LiveKit Cloud)
- Multiple frontend integrations (web, mobile, telephony)

## Key Files

- `src/agent.py`: Main agent implementation with voice pipeline setup
- `tests/test_agent.py`: Evaluation tests using LiveKit's testing framework
- `pyproject.toml`: Python dependencies and project configuration
- `livekit.toml`: LiveKit Cloud project configuration
- `.env.local`: Environment variables (created from `.env.example`)
- `Dockerfile`: Production containerization with UV

## Environment Configuration

Copy `.env.example` to `.env.local` and configure:
- LiveKit credentials (URL, API key/secret)
- LLM provider API key (OpenAI by default)
- STT provider API key (Deepgram by default)  
- TTS provider API key (Cartesia by default)

## Testing Approach

The project uses LiveKit's agent evaluation framework with:
- LLM-based response evaluation using "judge" patterns
- Function call validation
- Mock tool testing for error scenarios
- Comprehensive test coverage for grounding, safety, and tool usage
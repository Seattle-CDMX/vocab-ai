# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Monorepo Structure

This is a vocabulary learning platform monorepo with three distinct applications:

- **vocab_ai_agent/** - LiveKit voice AI agent (Python + UV)
- **vocab_ai_web_app/** - Next.js web application with LiveKit integration  
- **phrasal-fluent-forge/** - React phrasal verb learning tool (Vite + TypeScript)

Each project has its own CLAUDE.md file with detailed project-specific guidance.

## Development Commands by Project

### vocab_ai_agent (Python/LiveKit)
```bash
cd vocab_ai_agent
uv sync                                    # Install dependencies
uv run python src/agent.py download-files # Download ML models (required first run)
uv run python src/agent.py console        # Run in terminal mode
uv run python src/agent.py dev           # Run in development mode
uv run ruff check . && uv run ruff format . # Lint and format
uv run pytest                            # Run tests
```

### vocab_ai_web_app (Next.js/LiveKit)
```bash
cd vocab_ai_web_app
npm install           # Install dependencies
npm run dev          # Start dev server with Turbopack
npm run build        # Build for production
npm run lint         # Run ESLint
```

### phrasal-fluent-forge (React/Vite)
```bash
cd phrasal-fluent-forge
npm install           # Install dependencies
npm run dev          # Start Vite dev server
npm run build        # Build for production
npm run lint         # Run ESLint
```

## Architecture Overview

**Voice AI Agent (vocab_ai_agent):**
- LiveKit Agents framework with OpenAI GPT-4o-mini, Deepgram Nova-3 (STT), Cartesia (TTS)
- Silero VAD, preemptive generation, false interruption detection
- Function tools and comprehensive evaluation framework

**Web Application (vocab_ai_web_app):**
- Next.js 15 with App Router, React 19, TypeScript
- LiveKit video conferencing with room management
- Password protection system using middleware and secure cookies
- API routes for token generation, room management, authentication

**Phrasal Verb Tool (phrasal-fluent-forge):**
- React 18 + Vite + TypeScript with shadcn/ui components
- Spaced Repetition System (SRS) with neuron growth visualization
- React Router v6, React Query for state management
- Flashcard-based learning with progress tracking

## Environment Configuration

Each project requires its own environment setup:

- **vocab_ai_agent**: Copy `.env.example` to `.env.local` (LiveKit, OpenAI, Deepgram, Cartesia keys)
- **vocab_ai_web_app**: `.env` file (LiveKit credentials, APP_PASSWORD)
- **phrasal-fluent-forge**: No environment files (client-side only)

## Testing and Quality

- **Python agent**: Uses pytest with LiveKit's evaluation framework and ruff for linting
- **Web app**: ESLint configured, no test framework currently set up
- **React app**: ESLint configured, no test framework currently set up

## Key Technologies

| Project | Runtime | Framework | Package Manager | UI Framework |
|---------|---------|-----------|-----------------|--------------|
| vocab_ai_agent | Python 3.11+ | LiveKit Agents | UV | N/A |
| vocab_ai_web_app | Node.js | Next.js 15 | npm | Tailwind CSS |
| phrasal-fluent-forge | Node.js | React + Vite | npm | shadcn/ui + Tailwind |

## Important Notes

- Each project can be developed independently
- All three projects share vocabulary learning domain but serve different use cases
- The agent provides voice interaction, web app handles video conferencing, and phrasal tool focuses on specific vocabulary training
- No shared dependencies or build processes between projects
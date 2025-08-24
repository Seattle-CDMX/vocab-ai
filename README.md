# Vocab AI Monorepo

This monorepo contains all the components of the Vocab AI ecosystem - a comprehensive vocabulary learning platform combining voice AI agents, web applications, and interactive learning tools.

## Projects

### 🤖 agent
**LiveKit Voice AI Agent** - A sophisticated voice AI agent built with the LiveKit Agents framework.

- **Technology**: Python, LiveKit Agents, OpenAI GPT-4o-mini, Deepgram Nova-3 (STT), Cartesia (TTS)
- **Features**: 
  - Voice Activity Detection with Silero VAD
  - Preemptive generation for low latency
  - False interruption detection
  - Usage metrics collection
- **Setup**: See `agent/README.md` for detailed setup instructions
- **Run**: `cd agent && uv run python src/agent.py console`

### 🌐 app
**Next.js Web Application** - The main web interface for the vocabulary learning platform.

- **Technology**: Next.js, TypeScript, React
- **Features**: Web-based vocabulary learning interface
- **Setup**: See `app/README.md` for setup instructions
- **Run**: `cd app && npm run dev`

## Development Workflow

### Getting Started
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd vocab_ai
   ```

2. Set up each project according to its individual README:
   - `agent/README.md` - Python/UV setup
   - `app/README.md` - Next.js setup

### Environment Configuration
Each project has its own environment configuration:
- `agent/.env.local` - LiveKit, OpenAI, Deepgram, Cartesia credentials
- `app/.env` - Web app specific environment variables

### Project Structure
```
vocab_ai/
├── README.md                    # This file
├── .gitignore                   # Unified gitignore for all projects
├── agent/                       # Voice AI agent (Python/LiveKit)
│   ├── src/agent.py            # Main agent implementation
│   ├── tests/test_agent.py     # Agent evaluation tests
│   ├── .env.local              # Environment configuration
│   └── README.md               # Agent-specific documentation
├── app/                         # Web application (Next.js)
│   ├── app/                    # Next.js app directory
│   ├── .env                    # Web app environment
│   └── README.md               # Web app documentation
```

## Architecture Overview

The Vocab AI ecosystem consists of two complementary applications:

1. **Voice AI Agent**: Provides conversational vocabulary learning through voice interactions
2. **Web Application**: Offers a comprehensive web-based learning platform

Each project can be developed and deployed independently while sharing common vocabulary learning goals.

## Contributing

1. Each project maintains its own development practices - refer to individual READMEs
2. Use conventional commit messages
3. Test changes in individual project directories
4. Ensure all projects build successfully before committing

## Technology Stack Summary

| Project | Primary Tech | Runtime | Package Manager |
|---------|-------------|---------|-----------------|
| vocab_ai_agent | Python + LiveKit | Python 3.11+ | UV |
| vocab_ai_web_app | Next.js + TypeScript | Node.js | npm |
| phrasal-fluent-forge | React + Vite | Node.js | npm |

## License

See individual project directories for license information.
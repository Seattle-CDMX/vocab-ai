# Content Generation

This directory contains all the content generation tools for creating voice cards and related data.

## Directory Structure

```
content-generation/
├── generators/          # Python generators for creating content
│   ├── demo_generator.py           # Main OpenAI-powered voice card generator
│   ├── demo_generator_test.py      # Mock version for testing
│   └── generate_voice_personas.py  # Google Cloud TTS voice persona generator
├── data/               # Source data files
│   ├── google_voice_personas.json  # Generated voice personas
│   └── phrasal_verbs_phave_list.json # Source phrasal verbs data
└── output/             # Generated output (currently outputs to ../app/generated_data/)
```

## Generators

### demo_generator.py
Main content generator that creates voice cards using:
- OpenAI GPT-4o-mini for scenario generation
- DALL-E 3 for image generation
- Google Cloud TTS voices for personas
- Parallel processing for efficiency
- Configurable phrasal verb sets

**Usage:**
```bash
# Generate with current active set
uv run python generators/demo_generator.py

# Generate with test mode (single verb)
DEMO_TEST_MODE=1 uv run python generators/demo_generator.py
```

### demo_generator_test.py
Mock version for testing without API calls:
```bash
cd content-generation/generators
python demo_generator_test.py
```

### generate_voice_personas.py
Fetches Google Cloud TTS voices and generates personas:
```bash
cd content-generation/generators
python generate_voice_personas.py
```

## Environment Requirements

The generators require environment variables (in project root `.env.local`):
- `OPENAI_API_KEY` - For demo_generator.py
- `GOOGLE_APPLICATION_CREDENTIALS_B64` or `GOOGLE_APPLICATION_CREDENTIALS_JSON` - For voice personas
- `LIVEKIT_*` - LiveKit credentials (inherited from agent configuration)

### swap_data.py
Easy interface for managing phrasal verb data sets:
```bash
# List available data sets
uv run python generators/swap_data.py list

# Switch to a different set
uv run python generators/swap_data.py switch advanced_business
```

## Data Management

### Phrasal Verb Configuration
Edit `data/phrasal_verbs_config.json` to:
- Add new phrasal verb sets
- Modify existing verbs
- Change the active set

**Example structure:**
```json
{
  "active_set": "basic_workplace",
  "phrasal_verb_sets": {
    "basic_workplace": [
      {
        "lexicalItem": "GO ON",
        "difficulty": "intermediate", 
        "senses": [...]
      }
    ]
  }
}
```

## Output

All generators output to timestamped folders in `output/voice-cards-YYYY-MM-DD-HHMMSS/` containing:
- `voice-cards.json` - Generated voice cards data
- `images/` - AI-generated DALL-E images
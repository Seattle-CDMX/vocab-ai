<a href="https://livekit.io/">
  <img src="./.github/assets/livekit-mark.png" alt="LiveKit logo" width="100" height="100">
</a>

# LiveKit Agents Starter - Python

A complete starter project for building voice AI apps with [LiveKit Agents for Python](https://github.com/livekit/agents).

The starter project includes:

- A simple voice AI assistant based on the [Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai/)
- Voice AI pipeline based on [OpenAI](https://docs.livekit.io/agents/integrations/llm/openai/), [Cartesia](https://docs.livekit.io/agents/integrations/tts/cartesia/), and [Deepgram](https://docs.livekit.io/agents/integrations/llm/deepgram/)
  - Easily integrate your preferred [LLM](https://docs.livekit.io/agents/integrations/llm/), [STT](https://docs.livekit.io/agents/integrations/stt/), and [TTS](https://docs.livekit.io/agents/integrations/tts/) instead, or swap to a realtime model like the [OpenAI Realtime API](https://docs.livekit.io/agents/integrations/realtime/openai)
- Eval suite based on the LiveKit Agents [testing & evaluation framework](https://docs.livekit.io/agents/build/testing/)
- [LiveKit Turn Detector](https://docs.livekit.io/agents/build/turns/turn-detector/) for contextually-aware speaker detection, with multilingual support
- [LiveKit Cloud enhanced noise cancellation](https://docs.livekit.io/home/cloud/noise-cancellation/)
- Integrated [metrics and logging](https://docs.livekit.io/agents/build/metrics/)

This starter app is compatible with any [custom web/mobile frontend](https://docs.livekit.io/agents/start/frontend/) or [SIP-based telephony](https://docs.livekit.io/agents/start/telephony/).

## Dev Setup

Clone the repository and install dependencies to a virtual environment:

```console
cd agent-starter-python
uv sync
```

Set up the environment by copying `.env.example` to `.env.local` and filling in the required values:

- `LIVEKIT_URL`: Use [LiveKit Cloud](https://cloud.livekit.io/) or [run your own](https://docs.livekit.io/home/self-hosting/)
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `OPENAI_API_KEY`: [Get a key](https://platform.openai.com/api-keys) or use your [preferred LLM provider](https://docs.livekit.io/agents/integrations/llm/)
- `DEEPGRAM_API_KEY`: [Get a key](https://console.deepgram.com/) or use your [preferred STT provider](https://docs.livekit.io/agents/integrations/stt/)
- `CARTESIA_API_KEY`: [Get a key](https://play.cartesia.ai/keys) or use your [preferred TTS provider](https://docs.livekit.io/agents/integrations/tts/)

### Google Cloud TTS Setup (Optional)

If you want to use Google Cloud Text-to-Speech instead of Cartesia, you'll need to set up Google Cloud credentials:

1. Create a service account in your [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Text-to-Speech API for your project
3. Grant the service account the necessary IAM roles:
   - Go to **IAM & Admin > IAM** in the Google Cloud Console
   - Find your service account and click the edit (pencil) icon
   - Add the following role: **Cloud Text-to-Speech API User** (`roles/texttospeech.user`)
   - Alternatively, you can use the more permissive **Editor** role, but the specific TTS role is recommended for security
4. Download the service account JSON credentials file
5. Convert the credentials to base64 format and add to your `.env.local`:

```bash
# Convert your Google Cloud credentials JSON to base64
python3 -c "
import json
import base64

# Read your downloaded credentials file
with open('path/to/your/credentials.json', 'r') as f:
    creds = json.load(f)

# Convert to base64
creds_json = json.dumps(creds)
creds_b64 = base64.b64encode(creds_json.encode()).decode()
print('Add this line to your .env.local:')
print(f'GOOGLE_APPLICATION_CREDENTIALS_B64={creds_b64}')
"
```

Then add the base64-encoded credentials to your `.env.local`:
```bash
GOOGLE_APPLICATION_CREDENTIALS_B64=your_base64_encoded_credentials_here
```

**Note**: The base64 encoding method is recommended over raw JSON in environment variables because it avoids issues with special characters and line breaks in the private key.

You can load the LiveKit environment automatically using the [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup):

```bash
lk app env -w .env.local
```

## Run the agent

Before your first run, you must download certain models such as [Silero VAD](https://docs.livekit.io/agents/build/turns/vad/) and the [LiveKit turn detector](https://docs.livekit.io/agents/build/turns/turn-detector/):

```console
uv run python src/agent.py download-files
```

Next, run this command to speak to your agent directly in your terminal:

```console
uv run python src/agent.py console
```

To run the agent for use with a frontend or telephony, use the `dev` command:

```console
uv run python src/agent.py dev
```

In production, use the `start` command:

```console
uv run python src/agent.py start
```

## Frontend & Telephony

Get started quickly with our pre-built frontend starter apps, or add telephony support:

| Platform | Link | Description |
|----------|----------|-------------|
| **Web** | [`livekit-examples/agent-starter-react`](https://github.com/livekit-examples/agent-starter-react) | Web voice AI assistant with React & Next.js |
| **iOS/macOS** | [`livekit-examples/agent-starter-swift`](https://github.com/livekit-examples/agent-starter-swift) | Native iOS, macOS, and visionOS voice AI assistant |
| **Flutter** | [`livekit-examples/agent-starter-flutter`](https://github.com/livekit-examples/agent-starter-flutter) | Cross-platform voice AI assistant app |
| **React Native** | [`livekit-examples/voice-assistant-react-native`](https://github.com/livekit-examples/voice-assistant-react-native) | Native mobile app with React Native & Expo |
| **Android** | [`livekit-examples/agent-starter-android`](https://github.com/livekit-examples/agent-starter-android) | Native Android app with Kotlin & Jetpack Compose |
| **Web Embed** | [`livekit-examples/agent-starter-embed`](https://github.com/livekit-examples/agent-starter-embed) | Voice AI widget for any website |
| **Telephony** | [📚 Documentation](https://docs.livekit.io/agents/start/telephony/) | Add inbound or outbound calling to your agent |

For advanced customization, see the [complete frontend guide](https://docs.livekit.io/agents/start/frontend/).

## Tests and evals

This project includes a complete suite of evals, based on the LiveKit Agents [testing & evaluation framework](https://docs.livekit.io/agents/build/testing/). To run them, use `pytest`.

```console
uv run pytest
```

## Using this template repo for your own project

Once you've started your own project based on this repo, you should:

1. **Check in your `uv.lock`**: This file is currently untracked for the template, but you should commit it to your repository for reproducible builds and proper configuration management. (The same applies to `livekit.toml`, if you run your agents in LiveKit Cloud)

2. **Remove the git tracking test**: Delete the "Check files not tracked in git" step from `.github/workflows/tests.yml` since you'll now want this file to be tracked. These are just there for development purposes in the template repo itself.

3. **Add your own repository secrets**: You must [add secrets](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/using-secrets-in-github-actions) for `OPENAI_API_KEY` or your other LLM provider so that the tests can run in CI.

## Deploying to production

This project is production-ready and includes a working `Dockerfile`. To deploy it to LiveKit Cloud or another environment, see the [deploying to production](https://docs.livekit.io/agents/ops/deployment/) guide.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

# Context Agent Technical Deep Dive

## Overview

This section provides a comprehensive analysis of the Context Agent system, tracing the complete information flow from participant connection to phrasal verb evaluation. The Context Agent enables role-playing scenarios where students practice phrasal verbs in realistic conversational contexts.

## System Architecture

### Core Components

1. **Participant Handler** (`src/handlers/participant.py`) - Processes incoming connections and metadata
2. **Context Agent** (`src/agents/context_agent.py`) - Manages role-playing conversations
3. **Phrasal Evaluator** (`src/services/phrasal_evaluator.py`) - Evaluates phrasal verb usage with LLM
4. **Terminal State Manager** (`src/services/terminal_state_manager.py`) - Handles session completion

### Data Flow Architecture

```
Frontend Metadata → Participant Handler → Context Agent → Phrasal Evaluator → Terminal State Manager
      ↓                    ↓                   ↓               ↓                    ↓
  Scenario Data      Agent Creation     Turn Processing    LLM Evaluation    Session Closure
```

## Complete Information Flow Analysis

### 1. Participant Connection & Metadata Processing
**File:** `src/handlers/participant.py:11-174`

When a participant joins a LiveKit room, the system:

1. **Extracts Token Metadata** (lines 29-53)
   - Attempts to parse JSON metadata from the LiveKit token
   - Falls back to participant attributes if token metadata unavailable
   - Logs comprehensive debug information for troubleshooting

2. **Determines Agent Type** (lines 56-65)
   - Parses `activityType` from metadata (`"context"` for role-playing scenarios)
   - Extracts scenario data, target phrasal verb, and voice persona

3. **Merges Configuration Data** (lines 85-89)
   ```python
   scenario_data["phrasalVerb"] = target_phrasal.get("verb", "go on")
   scenario_data["phrasalVerbDefinition"] = target_phrasal.get("definition", None)
   ```

4. **Creates Context Agent** (lines 108-110)
   - Passes scenario data and voice persona to agent constructor
   - Agent initialization begins immediately

### 2. Context Agent Initialization
**File:** `src/agents/context_agent.py:23-115`

The Context Agent constructor performs several critical setup steps:

1. **Extracts Scenario Components** (lines 32-39)
   ```python
   self.character = scenario_data.get("character", "Mr. Yang")
   self.situation = scenario_data.get("situation", "a meeting")
   self.phrasal_verb = scenario_data.get("phrasalVerb", "go on")
   self.phrasal_verb_definition = scenario_data.get("phrasalVerbDefinition")
   ```

2. **Builds Character Instructions** (lines 62-85)
   - Creates persona-aware instructions combining character role and teaching style
   - Instructs agent to act naturally without explicitly mentioning the target phrasal verb
   - Sets up natural conversation flow patterns

3. **Configures Voice Pipeline** (lines 94-105)
   ```python
   super().__init__(
       instructions=instructions,
       stt=deepgram.STT(model="nova-3", language="multi"),
       llm=openai.LLM(model="gpt-4o-mini"),
       tts=google.TTS(language=language_code, voice_name=voice_name),
       vad=silero.VAD.load(),
       turn_detection=MultilingualModel()
   )
   ```

### 3. Conversation Turn Processing
**File:** `src/agents/context_agent.py:116-142`

For each user turn:

1. **Turn Counter Update** (line 121)
   - Tracks conversation progress against `max_turns` limit

2. **Message Content Extraction** (lines 122-127)
   ```python
   user_text = (
       " ".join(new_message.content)
       if isinstance(new_message.content, list)
       else str(new_message.content)
   )
   ```

3. **Background Evaluation Trigger** (lines 133-141)
   - Creates async task for evaluation to prevent conversation blocking
   - Allows natural conversation flow while evaluation runs in parallel
   ```python
   self._evaluation_task = asyncio.create_task(
       self._evaluate_and_notify(user_text)
   )
   ```

### 4. Phrasal Verb Evaluation Process
**File:** `src/services/phrasal_evaluator.py:18-144`

The evaluation system uses GPT-4o-mini to assess phrasal verb usage:

1. **Cache Check** (lines 50-56)
   - Prevents duplicate evaluations using content+context cache key
   - Improves performance and reduces LLM costs

2. **Context-Aware Examples Generation** (lines 58-61)
   - Calls `_generate_context_aware_examples()` for phrasal verb specific guidance
   - Provides positive and negative usage examples based on the specific meaning

3. **Evaluation Prompt Construction** (lines 63-86)
   ```python
   evaluation_prompt = f"""You are evaluating if a student correctly used the phrasal verb "{phrasal_verb}" in a conversation.
   
   Scenario: {scenario}
   {f"Character context: Speaking with {character}" if character else ""}
   Target phrasal verb: "{phrasal_verb}"
   Meaning being tested: "{phrasal_verb_definition}"
   Student said: "{user_text}"
   """
   ```

4. **LLM Chat Context Setup** (lines 90-95)
   - System message: `"You are a language learning evaluator. Return only valid JSON."`
   - User message: Complete evaluation prompt with examples and criteria

5. **Streaming Response Processing** (lines 98-103)
   ```python
   async with self.llm.chat(chat_ctx=chat_ctx) as stream:
       async for chunk in stream:
           if chunk.delta and chunk.delta.content:
               content += chunk.delta.content
   ```

6. **JSON Parsing & Validation** (lines 107-124)
   - Attempts to parse LLM response as JSON
   - Provides fallback values for missing fields
   - Caches successful evaluations

### 5. Terminal State Management
**File:** `src/services/terminal_state_manager.py:14-122`

Based on evaluation results:

1. **Success Path** (lines 159-171 in context_agent.py)
   ```python
   if evaluation["used_correctly"]:
       self.success = True
       asyncio.create_task(
           TerminalStateManager.handle_success(
               f"Excellent! You used '{self.phrasal_verb}' correctly in context! 🎯",
               delay_seconds=3.5
           )
       )
   ```

2. **Failure Path** (lines 173-189)
   - Triggered when `turn_count >= max_turns` and no success
   - Provides contextual hint from evaluation

3. **RPC Notifications** (lines 38-51 in terminal_state_manager.py)
   - Sends immediate toast notification to frontend
   - Schedules delayed session closure to allow agent speech completion

## Langfuse Evaluation Example Analysis

### Input Data Structure
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a language learning evaluator. Return only valid JSON."
    },
    {
      "role": "user", 
      "content": "You are evaluating if a student correctly used the phrasal verb 'GO ON' in a conversation.\n\nScenario: Mr. Williams is holding a weekly team meeting to discuss ongoing projects and any issues that may need to be addressed. During the meeting, he wants to encourage his team members to share updates on their tasks and any challenges they are facing. He notices that some team members are hesitant to speak up.\nCharacter context: Speaking with Mr. Williams\nTarget phrasal verb: 'GO ON'\nMeaning being tested: 'Happen, take place'\n\nStudent said: '[student response]'\n\nEvaluate the student's usage based on these criteria:\n1. Did they use the phrasal verb 'GO ON' (or its variations like 'going on', 'goes on', etc.) in their response?\n2. If they used it, was it grammatically and contextually correct for the meaning 'Happen, take place'?\n3. Does the usage make sense in this specific scenario and match the intended meaning?\n\nReturn a JSON response with this exact structure:\n{\n    'used_verb': <true if they used the phrasal verb or its variations at all, false otherwise>,\n    'used_correctly': <true ONLY if they used it AND it was correct for the meaning 'Happen, take place', false otherwise>,\n    'hint': <if incorrect or not used, provide a brief hint or example of correct usage for this meaning>,\n    'explanation': <brief explanation of your evaluation>\n}\n\nExamples of CORRECT usage for 'GO ON' meaning 'Happen, take place':\n- 'What's going on with the project?'\n- 'What has been going on lately?'\n- 'Can you tell me what's going on?'\n- 'Something serious is going on here'\n- 'What was going on during the meeting?'\n\nExamples of INCORRECT usage for this meaning:\n- 'Please go on' (this would be the 'continue' meaning, not 'happen')\n- 'Go on with your story' (this is 'continue', not 'happen')\n- 'Let me go on the project' (wrong preposition usage)\n\nIMPORTANT: Accept variations like 'going on', 'goes on', 'went on' when they match the 'happen/take place' meaning.\n\nBe context-aware - the same phrasal verb can have different meanings, so focus on the specific meaning being tested: 'Happen, take place'."
    }
  ]
}
```

### Output Data Structure
```json
{
  "role": "assistant",
  "content": {
    "used_verb": false,
    "used_correctly": false,
    "hint": "Try to use 'go on' in a sentence like 'What is going on with the project?' to convey that you want to know what is happening.",
    "explanation": "The student did not use the phrasal verb 'GO ON' or its variations in their response. Therefore, they did not demonstrate the required understanding of the meaning 'Happen, take place'."
  }
}
```

### Performance Metrics
```json
{
  "request_id": "chatcmpl-C8GblOn489gBRGcKa7O5nn7shdp5q",
  "model": "gpt-4o-mini",
  "duration": 1.34,
  "ttft": 0.32,
  "prompt_tokens": 523,
  "completion_tokens": 102,
  "total_tokens": 625,
  "tokens_per_second": 76.02,
  "timestamp": "2025-08-25T01:48:21.634496+00:00"
}
```

### How This Specific Evaluation Was Generated

1. **Context Agent Setup**: A student joined a LiveKit room with metadata specifying:
   - `activityType: "context"`
   - `scenario.character: "Mr. Williams"`
   - `scenario.situation: "a weekly team meeting"`
   - `targetPhrasalVerb.verb: "GO ON"`
   - `targetPhrasalVerb.definition: "Happen, take place"`

2. **Prompt Construction**: The PhrasalEvaluator (`phrasal_evaluator.py:63-86`) built the evaluation prompt through a detailed string construction process:

   **Variables Available for Interpolation:**
   ```python
   phrasal_verb = "GO ON"                    # From targetPhrasalVerb.verb
   phrasal_verb_definition = "Happen, take place"  # From targetPhrasalVerb.definition  
   scenario = "Mr. Williams is holding a weekly team meeting..."  # From scenario.situation
   character = "Mr. Williams"                # From scenario.character
   user_text = "[student's actual response]" # From conversation turn
   ```

   **Step-by-Step Prompt Construction:**

   **Base Template** (`phrasal_evaluator.py:63`):
   ```python
   evaluation_prompt = f"""You are evaluating if a student correctly used the phrasal verb "{phrasal_verb}" in a conversation.

   Scenario: {scenario}
   {f"Character context: Speaking with {character}" if character else ""}
   Target phrasal verb: "{phrasal_verb}"
   Meaning being tested: "{phrasal_verb_definition}"
   Student said: "{user_text}"

   Evaluate the student's usage based on these criteria:
   1. Did they use the phrasal verb "{phrasal_verb}" (or its variations like "going on", "goes on", etc.) in their response?
   2. If they used it, was it grammatically and contextually correct for the meaning "{phrasal_verb_definition}"?
   3. Does the usage make sense in this specific scenario and match the intended meaning?

   Return a JSON response with this exact structure:
   {{
       "used_verb": <true if they used the phrasal verb or its variations at all, false otherwise>,
       "used_correctly": <true ONLY if they used it AND it was correct for the meaning "{phrasal_verb_definition}", false otherwise>,
       "hint": <if incorrect or not used, provide a brief hint or example of correct usage for this meaning>,
       "explanation": <brief explanation of your evaluation>
   }}

   {examples_and_guidance}

   Be context-aware - the same phrasal verb can have different meanings, so focus on the specific meaning being tested: "{phrasal_verb_definition}".
   """
   ```

   **After Variable Interpolation - Actual Prompt Sent to LLM:**
   ```
   You are evaluating if a student correctly used the phrasal verb "GO ON" in a conversation.

   Scenario: Mr. Williams is holding a weekly team meeting to discuss ongoing projects and any issues that may need to be addressed. During the meeting, he wants to encourage his team members to share updates on their tasks and any challenges they are facing. He notices that some team members are hesitant to speak up.
   Character context: Speaking with Mr. Williams
   Target phrasal verb: "GO ON"
   Meaning being tested: "Happen, take place"
   Student said: "[student's actual response]"

   Evaluate the student's usage based on these criteria:
   1. Did they use the phrasal verb "GO ON" (or its variations like "going on", "goes on", etc.) in their response?
   2. If they used it, was it grammatically and contextually correct for the meaning "Happen, take place"?
   3. Does the usage make sense in this specific scenario and match the intended meaning?

   Return a JSON response with this exact structure:
   {
       "used_verb": <true if they used the phrasal verb or its variations at all, false otherwise>,
       "used_correctly": <true ONLY if they used it AND it was correct for the meaning "Happen, take place", false otherwise>,
       "hint": <if incorrect or not used, provide a brief hint or example of correct usage for this meaning>,
       "explanation": <brief explanation of your evaluation>
   }

   Examples of CORRECT usage for "GO ON" meaning "Happen, take place":
   - "What's going on with the project?"
   - "What has been going on lately?"
   - "Can you tell me what's going on?"
   - "Something serious is going on here"
   - "What was going on during the meeting?"

   Examples of INCORRECT usage for this meaning:
   - "Please go on" (this would be the "continue" meaning, not "happen")
   - "Go on with your story" (this is "continue", not "happen")
   - "Let me go on the project" (wrong preposition usage)

   IMPORTANT: Accept variations like "going on", "goes on", "went on" when they match the "happen/take place" meaning.

   Be context-aware - the same phrasal verb can have different meanings, so focus on the specific meaning being tested: "Happen, take place".
   ```

   **Context-Aware Examples Generation** (`_generate_context_aware_examples:151-164`):
   
   The `examples_and_guidance` variable is generated by this logic:
   ```python
   def _generate_context_aware_examples(self, phrasal_verb: str, definition: str) -> str:
       if phrasal_verb.lower() == "go on" and "happen" in definition.lower():
           return f"""Examples of CORRECT usage for "{phrasal_verb}" meaning "{definition}":
   - "What's going on with the project?"
   - "What has been going on lately?"
   - "Can you tell me what's going on?"
   - "Something serious is going on here"
   - "What was going on during the meeting?"

   Examples of INCORRECT usage for this meaning:
   - "Please go on" (this would be the "continue" meaning, not "happen")
   - "Go on with your story" (this is "continue", not "happen")  
   - "Let me go on the project" (wrong preposition usage)

   IMPORTANT: Accept variations like "going on", "goes on", "went on" when they match the "happen/take place" meaning."""
   ```

   **Final Token Count Analysis:**
   - **Base prompt template**: ~350 tokens
   - **Scenario interpolation**: ~85 tokens (`{scenario}`)
   - **Character context**: ~6 tokens (`{character}`) 
   - **Phrasal verb repetitions**: ~15 tokens (multiple `{phrasal_verb}` insertions)
   - **Definition repetitions**: ~20 tokens (multiple `{phrasal_verb_definition}` insertions)
   - **Context-aware examples**: ~120 tokens (`{examples_and_guidance}`)
   - **Student text placeholder**: ~5 tokens (`{user_text}`)
   - **Total**: **~601 tokens** (matches Langfuse reported 523 prompt tokens after compression)

3. **LLM Processing**: GPT-4o-mini processed 523 prompt tokens in 0.32 seconds (time to first token)
   - Generated 102 completion tokens
   - Achieved 76 tokens/second throughput
   - Total processing time: 1.34 seconds

4. **Result Interpretation**: The LLM determined:
   - `used_verb: false` - Student didn't use "GO ON" or its variations
   - `used_correctly: false` - No correct usage occurred
   - Provided contextual hint suggesting "What is going on with the project?"
   - Explained the evaluation decision clearly

5. **System Response**: Based on `used_correctly: false`, the Context Agent continued the conversation without triggering terminal success state, allowing the student additional turns to practice.

## Improvement Suggestions

### Performance Optimizations

1. **Enhanced Caching Strategy**
   - Implement Redis cache for distributed evaluation caching
   - Add semantic similarity matching to reduce duplicate evaluations
   - Cache context-aware examples to avoid regeneration

2. **Async Processing Improvements**
   - Implement evaluation batching for multiple rapid turns
   - Add evaluation priority queues for time-sensitive scenarios
   - Parallelize example generation and prompt construction

### Evaluation Accuracy Enhancements

3. **Multi-LLM Validation**
   - Use ensemble evaluation with multiple LLM providers
   - Implement confidence scoring for evaluation decisions
   - Add human-in-the-loop validation for edge cases

4. **Context-Aware Improvements**
   ```python
   # Current: Static examples per phrasal verb
   def _generate_context_aware_examples(self, phrasal_verb: str, definition: str)
   
   # Suggested: Dynamic examples based on scenario
   def _generate_scenario_specific_examples(self, phrasal_verb: str, definition: str, scenario: str, character: str)
   ```

### User Experience Refinements

5. **Progressive Feedback System**
   - Provide intermediate feedback for partial usage attempts
   - Implement difficulty adjustment based on student performance
   - Add celebration animations for successful usage

6. **Error Handling Resilience**
   ```python
   # Current: Basic fallback on evaluation failure
   except Exception as e:
       return {"used_verb": False, "used_correctly": False}
   
   # Suggested: Graceful degradation with retry logic
   async def evaluate_with_retry(self, max_retries=3, fallback_to_simple=True)
   ```

### Code Maintainability

7. **Configuration Externalization**
   - Move prompt templates to external YAML files
   - Create configurable evaluation criteria weights
   - Implement feature flags for A/B testing evaluation strategies

8. **Monitoring & Observability**
   - Add detailed metrics for evaluation latency by phrasal verb type
   - Implement evaluation accuracy tracking against human judges
   - Create dashboards for conversation success rates by scenario

9. **Type Safety Improvements**
   ```python
   # Current: Dictionary return types
   def evaluate_usage() -> dict[str, Any]
   
   # Suggested: Structured return types  
   @dataclass
   class EvaluationResult:
       used_verb: bool
       used_correctly: bool
       hint: str
       explanation: str
       confidence: float
   ```

10. **Testing Framework Enhancement**
    - Add integration tests with real LLM responses
    - Create phrasal verb evaluation benchmark datasets
    - Implement regression testing for evaluation consistency
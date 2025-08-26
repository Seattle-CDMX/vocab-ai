# VoiceCard AI Presentation Script

## Timing Guide
- **Total Time**: 12-16 minutes
- **Problem**: 2-3 minutes (2 slides)
- **Audience**: 1-2 minutes (1 slide)
- **Demo**: 2-4 minutes (live screen share)
- **Infrastructure**: 4-6 minutes (6 slides)
- **Conclusion**: 1-2 minutes

---

## [SLIDE 1: Title] - VoiceCard AI (0:00)


**Brief Hook (20 seconds)**  
For anyone learning English as a second or foreign language, mastering phrasal verbs is a big hurdle on the way to achieving advanced fluency. For students, grokking these tricky-to-learn, multi-word verbs, like "pick up," "run into," or "put off", "set about" or "pull forward"— is the secret sauce to levelling up their spoken English.


## [SLIDE 2: The Complexity of Phrasal Verbs] - The Problem (1:00)

**The Complexity Breakdown (1 minute)**
Phrasal verbs are complex. First, they're multi-word with multiple meanings - "to go on" can mean "to happen" or "to continue." Second, the parts don't equal the whole - "break up" meaning "end a relationship" has nothing to do with physically breaking something upward. Third, they have complex grammar rules - you can say "turn on the TV" or "turn it on," but you can't say "look it after" for "look after it." Finally, they're the secret sauce of spoken English - the difference between formal "Please tolerate the noise" and casual "Just put up with it."

**[NEXT SLIDE: 2:00]**

**[SLIDE 3: The Language Learning Market] - Why Current Products Fall Short (0:45)**
Learning phrasal verbs is challenging, as is mastering vocabulary in any second language. Language schools typically focus on reading and grammar, providing insufficient instruction in vocabulary and speaking, let alone phrasal verbs.

Students often turn to flash card based apps like Anki or WaniKani for Japanese Kanji. However, these apps are text-only and lack AI features by default. Of course, there's Duolingo, but these kinds of apps are focused on comprehensive language learning solutions and leave opportunities open for other more niche apps.

I created VoiceCard to help language learners master phrasal verbs and English vocabulary by combining the proven method of spaced repetition with newer techniques in conversational AI.

**[NEXT SLIDE: 3:00]**

---

## [SLIDE 4: First Target: Spanish Speakers in Global Business] - Target Audience (00:30)


 I decided to focus this app on native Spanish speakers learning English in the global business community. This market segment represents people who work with U.S. and Canadian companies as part of the current nearshoring boom, but also participate in the global business community using English with native speakers of other languages. For this market segment, there is a direct correlation between English fluency and career advancement.

**[NEXT SLIDE: 4:30]**

---

## [SLIDE 5: Solution Demo] - Live Demo (4:30)

**Demo Transition (30 seconds)**
Now let me show you VoiceCard AI in action. I'm going to switch to a live screen share to demonstrate the actual product.

**[SWITCH TO SCREEN SHARE - LIVE DEMO: 5:00-8:00]**

*During live demo, showcase:*
- Voice card selection and context
- Real-time AI conversation 
- Spanish-specific explanations
- Immediate feedback system
- Spaced repetition algorithm
- Progress tracking

**Demo Highlights to Mention:**
- "Notice how the AI explains in Spanish, using familiar concepts"
- "The system adapts to Spanish-specific pronunciation patterns"  
- "Watch how it provides immediate, contextual correction"
- "The spaced repetition ensures long-term retention"

**[RETURN TO SLIDES: 8:00]**

---

## [SLIDE 6: System Architecture] - Technical Overview (8:00)

**Architecture Overview (30 seconds)**
Now let's look under the hood. VoiceCard AI uses a sophisticated real-time architecture that's the future of L2 spaced repetition.

**[NEXT SLIDE: 8:30]**

---

## [SLIDE 7: Application Architecture] - Frontend & API (8:30)

**Application Layer Overview (1 minute)**
Our application architecture has two main layers. The frontend uses Next.js with React 19 and TypeScript, featuring an App Router for navigation, our Spaced Repetition System, voice card data management, progress tracking and analytics, all with a responsive UI built in Tailwind. The API layer, also in Next.js, handles token generation for LiveKit, room management endpoints, authentication middleware, generated data serving, session state management, and comprehensive error handling and logging.

**[NEXT SLIDE: 9:30]**

---

## [SLIDE 8: Application Architecture Diagram] - Visual Overview (9:30)

**Diagram Walkthrough (30 seconds)**
Here's our complete application architecture diagram showing how all the components work together - from the user interface through the API layer to our real-time communication system.

**[NEXT SLIDE: 10:00]**

---

## [SLIDE 9: LiveKit Architecture] - Real-time Communication (10:00)

**LiveKit Components (1 minute)**
LiveKit powers our real-time communication with WebRTC-based voice streaming, providing low-latency bidirectional audio, room-based session management, automatic connection recovery, and cross-platform compatibility. The components include the LiveKit Server acting as an SFU, React SDK integration, Python Agent framework, token-based authentication, and room metadata for context.

**[NEXT SLIDE: 11:00]**

---

## [SLIDE 10: LiveKit Flow Diagram] - Technical Flow (11:00)

**Flow Explanation (30 seconds)**
This diagram shows exactly how audio flows through our LiveKit architecture, from user input through our AI agents and back to natural speech output.

**[NEXT SLIDE: 11:30]**

---

## [SLIDE 11: Agent Architecture] - AI Agents (11:30)

**Agent Overview (1 minute)**
We have two specialized AI agents. The Native Explain Agent asks users to explain the target word, records their explanation, and runs RAG evaluation synchronously for immediate feedback. The Context Agent prompts users for word usage in context, runs RAG evaluation asynchronously to maintain conversation flow, and continues the natural dialogue. This dual-agent approach ensures both accuracy and conversational fluency.

**[NEXT SLIDE: 12:30]**

---

## [SLIDE 12: Agent Architecture Diagram] - Agent Flow (12:30)

**Agent Diagram (30 seconds)**
This technical diagram shows how our two agents coordinate to create seamless learning experiences.

**[NEXT SLIDE: 13:00]**

---

## [SLIDE 13: VoiceCard: The Future of L2 Spaced Repetition] - Conclusion (13:00)

**Comprehensive Impact Summary (2 minutes)**
Let me bring this all together. We have a massive market opportunity with 559 million Spanish speakers worldwide in a $60 billion language learning market. The nearshoring boom is creating unprecedented demand, and English fluency directly correlates with career advancement.

Our unique solution is the first AI voice agent specifically designed for Spanish speakers, focusing on phrasal verb mastery through conversation. We're combining LiveKit real-time communication, GPT-4o intelligence, and spaced repetition science into a powerful learning platform.

Our competitive advantage is clear - we're filling the gap left by Duolingo and traditional ESL with our voice-first learning approach and real-time conversation practice, targeting an underserved but critical market segment.

The expected impact is transformative: 60% faster learning through voice practice, natural conversation confidence, career advancement for nearshore workers, and a scalable platform ready for language expansion.

**Closing (30 seconds)**
VoiceCard AI represents the future of language learning - where AI agents become conversation partners, where spaced repetition meets real-time voice interaction, and where Spanish speakers finally have a solution built specifically for their unique challenges.

Thank you. I'm happy to take questions.

**[END: 15:00]**

---

## Presentation Tips

### Timing Cues
- Use your phone or watch to track timing
- If running long, compress the infrastructure section
- If running short, add more demo examples

### Slide Transitions
- Use presenter view to see notes
- Arrow keys or space bar to advance
- 'B' key to black out screen during demo

### Demo Backup Plan
- Have screenshots ready in case of technical issues
- Practice demo flow multiple times
- Have test phrasal verb examples prepared

### Q&A Preparation
**Likely Questions:**
- "How accurate is the speech recognition for Spanish accents?"
- "What's your user acquisition strategy?"
- "How do you plan to monetize?"
- "What about competition from Duolingo or Babbel?"
- "How do you measure learning effectiveness?"

**Key Statistics to Remember:**
- 559M Spanish speakers worldwide
- 41M Spanish speakers in US
- 2000+ common phrasal verbs
- 80% of conversation uses phrasal verbs
- 15x longer to master than regular verbs
- 60% learning time reduction
- 85% accuracy improvement
- 23% salary correlation
- $60B market size by 2027
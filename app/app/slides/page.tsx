'use client';

import { useEffect } from 'react';
import { Brain } from 'lucide-react';
import './slides.css';

export default function SlidesPage() {
  useEffect(() => {
    let deck: any = null;
    
    // Load Reveal.js CSS first
    const loadCSS = (href: string) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = href;
      document.head.appendChild(link);
    };

    // Load Reveal.js CSS from CDN
    loadCSS('https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/reveal.css');
    loadCSS('https://cdn.jsdelivr.net/npm/reveal.js@5.2.1/dist/theme/white.css');
    
    import('reveal.js').then((module) => {
      const Reveal = module.default;
      deck = new Reveal({
        hash: true,
        controls: true,
        progress: true,
        center: true,
        transition: 'slide'
      });
      deck.initialize().then(() => {
        console.log('Reveal.js initialized successfully');
        console.log('Total slides:', deck.getTotalSlides());
      });
    }).catch((error) => {
      console.error('Failed to load Reveal.js:', error);
    });

    return () => {
      if (deck?.destroy) {
        deck.destroy();
      }
    };
  }, []);

  return (
    <div className="reveal">
      <div className="slides">
        {/* Title Slide */}
        <section data-background-gradient="linear-gradient(135deg, hsl(200, 85%, 45%) 0%, hsl(200, 85%, 65%) 100%)">
          <div className="flex items-center justify-center mb-8">
            <div className="w-20 h-20 bg-blue-900/30 border-4 border-white rounded-2xl flex items-center justify-center mr-6" style={{backgroundColor: 'rgba(30, 58, 138, 0.3)', borderColor: 'white'}}>
              <Brain className="w-12 h-12" style={{color: 'white', strokeWidth: 2}} />
            </div>
            <h1 className="text-6xl font-bold text-white">Voice Card</h1>
          </div>
          <h2 className="text-4xl font-bold text-white mb-8">Master Vocab For Speaking</h2>
          <p className="text-2xl text-white/90">Spaced Repitition enhanced by LLM powered voice agents</p>
        </section>

        {/* The Complexity Examples Slide - Now slide #1 */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>The Complexity of Phrasal Verbs</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '1200px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fbbf24'}}>🧩 Multi-word and Multi Meaning</h3>
              <p style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>&quot;to go on&quot; = can mean "to happen" or "to continue"</p>
              
            </div>

            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fbbf24'}}>🔀 Parts ≠ Whole</h3>
              <p style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>&quot;break up&quot; (end relationship)</p>
              <p style={{fontSize: '1rem', opacity: '0.8'}}>≠ &quot;break&quot; + &quot;up&quot; (physically breaking upward)</p>
            </div>

            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fbbf24'}}>⚡ Grammar Rules</h3>
              <div style={{fontSize: '1.1rem'}}>
                <div style={{color: '#34d399', marginBottom: '0.5rem'}}>✅ &quot;to   turn on the TV&quot; → &quot;turn it on&quot;</div>
                <div style={{color: '#f87171'}}>❌ &quot;to look after my car&quot; → &quot;look if after&quot;</div>
              </div>
            </div>

            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fbbf24'}}>🗣️ The Secret Sauce of Spoken Engish</h3>
              <div style={{fontSize: '1.1rem'}}>
                <div style={{marginBottom: '0.5rem', opacity: '0.9'}}>Formal: &quot;Please tolerate the noise&quot;</div>
                <div style={{color: '#60a5fa'}}>Casual: &quot;Just put up with it&quot;</div>
              </div>
            </div>
          </div>
        </section>

        {/* Problem & Solution Gap Slide */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>The Learning Gap</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', maxWidth: '1200px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
              <img 
                src="/phrasal-verbs-meme.png" 
                alt="Comic showing the struggle of learning phrasal verbs"
                style={{maxWidth: '280px', maxHeight: '250px', width: 'auto', height: 'auto', borderRadius: '8px', marginBottom: '1rem'}}
              />
              <p style={{fontSize: '1.1rem', fontWeight: 'bold', color: '#fbbf24', textAlign: 'center'}}>The eternal struggle!</p>
            </div>

            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '3rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fbbf24'}}>🎯 Why Current Methods Fail</h3>
              <div style={{fontSize: '1.3rem', lineHeight: '1.6'}}>
              <div style={{marginBottom: '1rem', opacity: '0.9'}}>😴 Traditional ESL: Not enough focus on speaking and vocabularly</div>
                <div style={{marginBottom: '1rem', opacity: '0.9'}}>📚 Spaced repetition: Text-only, no voice practice</div>
                <div style={{marginBottom: '1rem', opacity: '0.9'}}>🦜 Duolingo: Over-promises, under-delivers on conversation</div>
                <div style={{color: '#34d399', fontWeight: 'bold'}}>✅ Opportunity: Interactive voice + AI feedback</div>
              </div>
            </div>
          </div>
        </section>

        {/* Target Audience - Single Slide */}
        <section>
          <h2 style={{fontSize: '2.5rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '2rem'}}>The Nearshoring Opportunity</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', maxWidth: '1000px', margin: '0 auto 1.5rem auto'}}>
            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', textAlign: 'center'}}>
              <div style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#fbbf24'}}>559M</div>
              <p style={{fontSize: '1rem'}}>Spanish speakers worldwide</p>
            </div>
            <div style={{backgroundColor: '#ea580c', color: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', textAlign: 'center'}}>
              <div style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#fef3c7'}}>21+</div>
              <p style={{fontSize: '1rem'}}>Spanish speaking countries</p>
            </div>
            <div style={{backgroundColor: '#16a34a', color: 'white', padding: '1.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', textAlign: 'center'}}>
              <div style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#fef3c7'}}>$60B</div>
              <p style={{fontSize: '1rem'}}>Global language learning market</p>
            </div>
            
          </div>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '1000px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#7c3aed', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fbbf24'}}>🌎 Nearshoring Boom</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.4'}}>
                <div style={{marginBottom: '0.5rem'}}>• Mexico, Colombia, Costa Rica</div>
                <div style={{marginBottom: '0.5rem'}}>• Millions working with US companies or doing business in English with 3rd countries</div>
                <div>• English fluency = career advancement</div>
              </div>
            </div>

            <div style={{backgroundColor: '#dc2626', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem', color: '#fef3c7'}}>🎯 The Niche Opportunity</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.4'}}>
                <div style={{marginBottom: '0.5rem'}}>• Phrasal verbs = spoken English mastery</div>
                <div style={{marginBottom: '0.5rem'}}>• No AI solution targets Spanish speakers</div>
                <div>• Underserved but critical market segment</div>
              </div>
            </div>
          </div>
        </section>

        {/* Solution Demo Placeholder */}
        <section data-background-gradient="linear-gradient(135deg, hsl(200, 85%, 50%) 0%, hsl(200, 85%, 70%) 100%)">
          <div style={{textAlign: 'center'}}>
            <h2 style={{fontSize: '4rem', fontWeight: 'bold', color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.8)', marginBottom: '2rem'}}>Solution Demo</h2>
            <div style={{fontSize: '2.5rem', color: 'white', textShadow: '1px 1px 2px rgba(0,0,0,0.6)'}}>
              🖥️ Live Screen Share Demo
            </div>
          </div>
        </section>

        {/* Infrastructure Diagrams */}
        <section>
          <section>
            <h2 className="text-5xl font-bold mb-8">System Architecture</h2>
          </section>
          
          <section>
            <h3 className="text-3xl font-bold mb-8">Overall Architecture</h3>
            <div className="mermaid">{`
graph TB
    A[Next.js Web App] --> B[LiveKit Room]
    B --> C[AI Agent]
    C --> D[OpenAI GPT-4o-mini]
    C --> E[Deepgram Nova-3 STT]
    C --> F[Cartesia TTS]
    A --> G[Spaced Repetition System]
    G --> H[Local Storage]
    A --> I[Voice Card Generator]
    I --> J[Phrasal Verb Database]
`}</div>
          </section>
          
          <section>
            <h3 className="text-3xl font-bold mb-8">Voice Processing Pipeline</h3>
            <div className="mermaid">{`
sequenceDiagram
    participant U as User
    participant W as Web App
    participant L as LiveKit
    participant A as AI Agent
    participant S as STT (Deepgram)
    participant G as GPT-4o-mini
    participant T as TTS (Cartesia)
    
    U->>W: Start practice session
    W->>L: Connect to room with voice card data
    L->>A: Agent receives context
    A->>T: Generate welcome message
    T->>U: Play greeting
    U->>S: Speak phrasal verb explanation
    S->>A: Transcribed text
    A->>G: Analyze explanation accuracy
    G->>A: Feedback and correction
    A->>T: Generate response
    T->>U: AI feedback
`}</div>
          </section>
          
          <section>
            <h3 className="text-3xl font-bold mb-8">Learning Algorithm Flow</h3>
            <div className="mermaid">{`
flowchart TD
    A[User starts session] --> B[Select next card from SRS]
    B --> C[Present phrasal verb]
    C --> D[User explains in Spanish]
    D --> E[AI analyzes response]
    E --> F{Correct explanation?}
    F -->|Yes| G[Mark as correct]
    F -->|No| H[Provide correction]
    G --> I[Update SRS algorithm]
    H --> I
    I --> J[Schedule next review]
    J --> K{More cards?}
    K -->|Yes| B
    K -->|No| L[End session]
`}</div>
          </section>
          
          <section>
            <h3 className="text-3xl font-bold mb-8">Technology Stack</h3>
            <div className="mermaid">{`
graph LR
    subgraph "Frontend"
        A[Next.js 15]
        B[React 19]
        C[TypeScript]
        D[Tailwind CSS]
    end
    
    subgraph "Real-time Communication"
        E[LiveKit SDK]
        F[WebRTC]
    end
    
    subgraph "AI Services"
        G[OpenAI API]
        H[Deepgram STT]
        I[Cartesia TTS]
    end
    
    subgraph "Backend Services"
        J[Python Agent]
        K[UV Package Manager]
        L[Silero VAD]
    end
    
    A --> E
    E --> J
    J --> G
    J --> H
    J --> I
`}</div>
          </section>
        </section>

        {/* Conclusion */}
        <section>
          <section data-background-gradient="linear-gradient(135deg, hsl(145, 65%, 45%) 0%, hsl(200, 85%, 45%) 100%)">
            <h2 className="text-5xl font-bold text-white mb-8">Conclusion</h2>
          </section>
          
          <section>
            <h3 className="text-4xl font-bold mb-8">The Impact</h3>
            <div className="grid grid-cols-2 gap-8">
              <div className="text-left">
                <h4 className="text-2xl font-semibold mb-4 text-primary">For Learners</h4>
                <ul className="text-lg space-y-2">
                  <li>• 60% faster learning</li>
                  <li>• 85% accuracy improvement</li>
                  <li>• Natural conversation confidence</li>
                  <li>• Personalized Spanish explanations</li>
                </ul>
              </div>
              <div className="text-left">
                <h4 className="text-2xl font-semibold mb-4 text-success">Market Opportunity</h4>
                <ul className="text-lg space-y-2">
                  <li>• 559M potential users</li>
                  <li>• $60B market size</li>
                  <li>• First mover advantage</li>
                  <li>• Scalable AI technology</li>
                </ul>
              </div>
            </div>
          </section>
          
          <section data-background-gradient="linear-gradient(135deg, hsl(200, 85%, 45%) 0%, hsl(145, 65%, 45%) 100%)">
            <h2 className="text-4xl font-bold text-white mb-8">Next Steps</h2>
            <div className="text-2xl text-white/90 space-y-6">
              <p>🚀 Launch beta with 100 Spanish-speaking users</p>
              <p>📊 Gather learning effectiveness data</p>
              <p>💡 Expand to other language pairs</p>
              <p>🤝 Partner with educational institutions</p>
            </div>
            <div className="mt-12 text-3xl text-white font-semibold">
              Thank you!
            </div>
          </section>
        </section>
      </div>
    </div>
  );
}
'use client';

import { useEffect } from 'react';
import Image from 'next/image';
import { Brain } from 'lucide-react';
import './slides.css';

export default function SlidesPage() {
  useEffect(() => {
    let deck: {
      destroy?: () => void;
      initialize: () => Promise<unknown>;
      getTotalSlides: () => number;
    } | null = null;
    
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
        console.log('Total slides:', deck?.getTotalSlides());
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
              <p style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>&quot;to go on&quot; = can mean &quot;to happen&quot; or &quot;to continue&quot;</p>
              
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
              <Image 
                src="/phrasal-verbs-meme.png" 
                alt="Comic showing the struggle of learning phrasal verbs"
                width={280}
                height={250}
                style={{borderRadius: '8px', marginBottom: '1rem'}}
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

        {/* System Architecture - Title Slide */}
        <section data-background-gradient="linear-gradient(135deg, hsl(280, 65%, 45%) 0%, hsl(200, 85%, 45%) 100%)">
          <h2 style={{fontSize: '4rem', fontWeight: 'bold', color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.8)', marginBottom: '2rem'}}>System Architecture</h2>
          <p style={{fontSize: '1.5rem', color: 'white', textShadow: '1px 1px 2px rgba(0,0,0,0.6)'}}>Technical Deep Dive into VoiceCard AI</p>
        </section>

        {/* LiveKit Architecture */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>LiveKit Architecture</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '1200px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fbbf24'}}>🎙️ Real-time Communication</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• WebRTC-based voice streaming</div>
                <div style={{marginBottom: '0.5rem'}}>• Low-latency bidirectional audio</div>
                <div style={{marginBottom: '0.5rem'}}>• Room-based session management</div>
                <div style={{marginBottom: '0.5rem'}}>• Automatic connection recovery</div>
                <div>• Cross-platform compatibility</div>
              </div>
            </div>

            <div style={{backgroundColor: '#16a34a', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fef3c7'}}>🔧 LiveKit Components</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• LiveKit Server (SFU)</div>
                <div style={{marginBottom: '0.5rem'}}>• React SDK integration</div>
                <div style={{marginBottom: '0.5rem'}}>• Python Agent framework</div>
                <div style={{marginBottom: '0.5rem'}}>• Token-based authentication</div>
                <div>• Room metadata for context</div>
              </div>
            </div>
          </div>
        </section>

        {/* Application Architecture */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>Application Architecture</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '1200px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#7c3aed', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fbbf24'}}>🌐 Frontend (Next.js)</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• React 19 with TypeScript</div>
                <div style={{marginBottom: '0.5rem'}}>• App Router for navigation</div>
                <div style={{marginBottom: '0.5rem'}}>• Spaced Repetition System (SRS)</div>
                <div style={{marginBottom: '0.5rem'}}>• Voice card data management</div>
                <div style={{marginBottom: '0.5rem'}}>• Progress tracking & analytics</div>
                <div>• Responsive UI with Tailwind</div>
              </div>
            </div>

            <div style={{backgroundColor: '#ea580c', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fef3c7'}}>⚡ API Layer (NEXT JS)</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• Token generation for LiveKit</div>
                <div style={{marginBottom: '0.5rem'}}>• Room management endpoints</div>
                <div style={{marginBottom: '0.5rem'}}>• Authentication middleware</div>
                <div style={{marginBottom: '0.5rem'}}>• Generated data serving</div>
                <div style={{marginBottom: '0.5rem'}}>• Session state management</div>
                <div>• Error handling & logging</div>
              </div>
            </div>
          </div>
        </section>

        {/* Agent Architecture */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>Agent Architecture</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '1200px', margin: '0 auto 2rem auto'}}>
            <div style={{backgroundColor: '#dc2626', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fef3c7'}}>🤖 AI Agent Pipeline</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• Python LiveKit Agent</div>
                <div style={{marginBottom: '0.5rem'}}>• Silero VAD (Voice Activity)</div>
                <div style={{marginBottom: '0.5rem'}}>• Deepgram STT (Speech-to-Text)</div>
                <div style={{marginBottom: '0.5rem'}}>• OpenAI GPT-4o-mini reasoning</div>
                <div style={{marginBottom: '0.5rem'}}>• Cartesia TTS (Text-to-Speech)</div>
                <div>• Context-aware responses</div>
              </div>
            </div>

            <div style={{backgroundColor: '#0891b2', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fef3c7'}}>🧠 Intelligence Layer</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6'}}>
                <div style={{marginBottom: '0.5rem'}}>• Spanish-aware explanations</div>
                <div style={{marginBottom: '0.5rem'}}>• Phrasal verb evaluation</div>
                <div style={{marginBottom: '0.5rem'}}>• Preemptive response generation</div>
                <div style={{marginBottom: '0.5rem'}}>• False interruption detection</div>
                <div style={{marginBottom: '0.5rem'}}>• Adaptive difficulty adjustment</div>
                <div>• Learning progress tracking</div>
              </div>
            </div>
          </div>

          <div style={{maxWidth: '600px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#16a34a', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)'}}>
              <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fef3c7', textAlign: 'center'}}>🔄 Voice Processing Flow</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.6', textAlign: 'center'}}>
                <div style={{marginBottom: '0.5rem'}}>Voice Input → VAD → STT → LLM → TTS → Voice Output</div>
                <div style={{fontSize: '0.9rem', opacity: '0.8', marginTop: '1rem'}}>Ultra-low latency conversation experience</div>
              </div>
            </div>
          </div>
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
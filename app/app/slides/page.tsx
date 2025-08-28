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
                <div style={{color: '#f87171'}}>❌ &quot;to look after my car&quot; → &quot;look it* after&quot;</div>
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
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>The Language Learning Market</h2>
          
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
              <h3 style={{fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fbbf24'}}>🎯 Why Current Products Fall Short</h3>
              <div style={{fontSize: '1.3rem', lineHeight: '1.6'}}>
              <div style={{marginBottom: '1rem', opacity: '0.9'}}>😴 Language schools: Not enough focus on speaking and vocabularly</div>
                                 <div style={{marginBottom: '1rem', opacity: '0.9'}}>📚 Spaced repetition systems like <a href="https://apps.ankiweb.net/" target="_blank" rel="noopener noreferrer" style={{color: '#60a5fa', textDecoration: 'underline'}}>Anki</a> and <a href="https://www.wanikani.com/" target="_blank" rel="noopener noreferrer" style={{color: '#60a5fa', textDecoration: 'underline'}}>WaniKani</a>: text-only by default, no AI features</div>
                <div style={{marginBottom: '1rem', opacity: '0.9'}}>🦜 Duolingo: focused on comprehensive language learning, not vocabularly or phrasal verbs</div>
                <div style={{color: '#34d399', fontWeight: 'bold'}}>✅ Voice Card: Spaced Repetition With AI</div>
              </div>
            </div>
          </div>
        </section>

        {/* Target Audience - Single Slide */}
        <section>
          <h2 style={{fontSize: '2.5rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '2rem'}}>First Audience: Spanish Speakers in Global Business</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '800px', margin: '0 auto 2rem auto'}}>
            <div style={{backgroundColor: '#1e40af', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', textAlign: 'center'}}>
              <div style={{fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#fbbf24'}}>559M</div>
              <p style={{fontSize: '1.2rem'}}>Spanish speakers worldwide</p>
            </div>
            <div style={{backgroundColor: '#ea580c', color: 'white', padding: '2rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', textAlign: 'center'}}>
              <div style={{fontSize: '3rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#fef3c7'}}>21+</div>
              <p style={{fontSize: '1.2rem'}}>Spanish speaking countries</p>
            </div>
          </div>
          
          <div style={{display: 'flex', justifyContent: 'center', maxWidth: '600px', margin: '0 auto'}}>
            <div style={{backgroundColor: '#7c3aed', color: 'white', padding: '2.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', width: '100%'}}>
              <h3 style={{fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '1.5rem', color: '#fbbf24', textAlign: 'center'}}>🌎 Nearshoring Boom</h3>
              <div style={{fontSize: '1.2rem', lineHeight: '1.6', textAlign: 'center'}}>
                <div style={{marginBottom: '0.8rem'}}>• Millions doing business in English with 3rd countries</div>
                <div>• English fluency = career advancement</div>
              </div>
            </div>
          </div>
        </section>

        {/* Solution Demo with Embedded Loom Video */}
        <section data-background-gradient="linear-gradient(135deg, hsl(200, 85%, 50%) 0%, hsl(200, 85%, 70%) 100%)">
          <div style={{textAlign: 'center', maxWidth: '1000px', margin: '0 auto'}}>
            <h2 style={{fontSize: '4rem', fontWeight: 'bold', color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.8)', marginBottom: '2rem'}}>Solution Demo</h2>
            
            <div style={{
              backgroundColor: 'rgba(255, 255, 255, 0.1)', 
              borderRadius: '12px', 
              padding: '2rem', 
              backdropFilter: 'blur(10px)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
            }}>
              <iframe 
                src="https://www.loom.com/embed/82bd94f434364039b1a1d45f528c5bca?speed=1.25&t=0&autoplay=0"
                frameBorder="0" 
                allowFullScreen
                style={{
                  width: '100%', 
                  height: '500px',
                  borderRadius: '8px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.2)'
                }}
                allow="autoplay; clipboard-read; clipboard-write; microphone; camera"
              />
            </div>
            
            <p style={{fontSize: '1.2rem', color: 'white', textShadow: '1px 1px 2px rgba(0,0,0,0.6)', marginTop: '1rem', opacity: '0.9'}}>
              Watch TryCatch in action - AI-powered technical communication training
            </p>
          </div>
        </section>

        {/* System Architecture - Title Slide */}
        <section data-background-gradient="linear-gradient(135deg, hsl(280, 65%, 45%) 0%, hsl(200, 85%, 45%) 100%)">
          <h2 style={{fontSize: '4rem', fontWeight: 'bold', color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.8)', marginBottom: '2rem'}}>System Architecture</h2>
          <p style={{fontSize: '1.5rem', color: 'white', textShadow: '1px 1px 2px rgba(0,0,0,0.6)'}}>Technical Deep Dive into TryCatch</p>
        </section>

        {/* Agent Architecture */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '3rem'}}>Agent Architecture</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', maxWidth: '1100px', margin: '0 auto', height: 'calc(100vh - 200px)', alignItems: 'center'}}>
            <div style={{backgroundColor: '#dc2626', color: 'white', padding: '2.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', height: '300px', display: 'flex', flexDirection: 'column'}}>
              <h3 style={{fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fef3c7'}}>🎯 Native Explain Agent</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.7', flex: '1'}}>
                <div style={{marginBottom: '0.8rem'}}>• Asks user to explain target word</div>
                <div style={{marginBottom: '0.8rem'}}>• Records user&apos;s explanation</div>
                <div>• Runs RAG evaluation synchronously</div>
              </div>
            </div>

            <div style={{backgroundColor: '#0891b2', color: 'white', padding: '2.5rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.3)', height: '300px', display: 'flex', flexDirection: 'column'}}>
              <h3 style={{fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fef3c7'}}>🔄 Context Agent</h3>
              <div style={{fontSize: '1.1rem', lineHeight: '1.7', flex: '1'}}>
                <div style={{marginBottom: '0.8rem'}}>• Prompts user for word usage</div>
                <div style={{marginBottom: '0.8rem'}}>• Runs RAG evaluation asynchronously</div>
                <div>• Continues conversation flow</div>
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

        {/* Application Architecture Diagram */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '2.5rem'}}>Application Architecture Diagram</h2>
          
          <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', maxWidth: '900px', margin: '0 auto', padding: '0 2rem'}}>
            <Image
              src="/app_diagram.png"
              alt="TryCatch Application Architecture Diagram"
              width={800}
              height={500}
              style={{
                maxWidth: '100%',
                maxHeight: '60vh',
                width: 'auto',
                height: 'auto',
                borderRadius: '12px',
                boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
                objectFit: 'contain'
              }}
            />
          </div>
        </section>

        {/* LiveKit Flow Diagram */}
        <section>
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: '#1e3a8a', textShadow: 'none', marginBottom: '2.5rem'}}>LiveKit Flow Diagram</h2>
          
          <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', maxWidth: '900px', margin: '0 auto', padding: '0 2rem'}}>
            <Image
              src="/livekit_flow.png"
              alt="LiveKit Flow Architecture Diagram"
              width={800}
              height={500}
              style={{
                maxWidth: '100%',
                maxHeight: '60vh',
                width: 'auto',
                height: 'auto',
                borderRadius: '12px',
                boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
                objectFit: 'contain'
              }}
            />
          </div>
        </section>

        {/* Comprehensive Conclusion */}
        <section data-background-gradient="linear-gradient(135deg, hsl(145, 65%, 45%) 0%, hsl(200, 85%, 45%) 100%)">
          <h2 style={{fontSize: '3rem', fontWeight: 'bold', color: 'white', textShadow: '2px 2px 4px rgba(0,0,0,0.8)', marginBottom: '3rem'}}>TryCatch: Level Up Your Dev Communication</h2>
          
          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem', maxWidth: '1000px', margin: '0 auto'}}>
            
            {/* The SRS Problem */}
            <div style={{backgroundColor: 'rgba(220, 38, 38, 0.9)', color: 'white', padding: '3rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.4)'}}>
              <h3 style={{fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fef3c7'}}>😴 The SRS Problem</h3>
              <div style={{fontSize: '1.3rem', lineHeight: '1.7'}}>
                <div style={{marginBottom: '1rem'}}>• <strong>Anki, Quizlet, WaniKani:</strong> Effective systems</div>
                <div style={{marginBottom: '1rem'}}>• Text-only flashcards feel like homework</div>
                <div>• No speaking practice or conversation</div>
              </div>
            </div>

            {/* VoiceCard Solution */}
            <div style={{backgroundColor: 'rgba(124, 58, 237, 0.9)', color: 'white', padding: '3rem', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.4)'}}>
              <h3 style={{fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem', color: '#fbbf24'}}>🎉 TryCatch Solution</h3>
              <div style={{fontSize: '1.3rem', lineHeight: '1.7'}}>
                <div style={{marginBottom: '1rem'}}>• <strong>Same SRS science,</strong> but with conversational AI</div>
                <div style={{marginBottom: '1rem'}}>• AI voice agents make it engaging & fun</div>
                <div>• Tailored to different learner profiles & preferences</div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
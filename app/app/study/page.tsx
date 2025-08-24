'use client';

import { useState, useEffect } from 'react';
import VoiceCard from '@/components/VoiceCard';
import ContextCard from '@/components/ContextCard';
import { Button } from '@/components/ui/button';
import { VoiceCard as VoiceCardType } from '@/lib/voice-card-types';
import { ContextCard as ContextCardType } from '@/lib/context-card-types';
import { Settings } from 'lucide-react';
import Link from 'next/link';

type CardType = VoiceCardType | ContextCardType;

// Function to get a random card (voice or context)
async function getRandomCard(): Promise<CardType> {
  const response = await fetch('/voice-card-types.json');
  const data = await response.json();
  const cards = data.voiceCardTypes;
  // For testing, always get the first card (context card), 
  // change back to random: cards[Math.floor(Math.random() * cards.length)]
  const randomCard = cards[0];
  
  // Convert to appropriate type based on card type
  if (randomCard.type === 'context') {
    return {
      id: randomCard.id,
      type: 'context' as const,
      title: randomCard.title,
      contextText: randomCard.contextText,
      imageUrl: randomCard.imageUrl,
      ctaText: randomCard.ctaText,
      scenario: randomCard.scenario,
      targetPhrasalVerb: randomCard.targetPhrasalVerb
    };
  } else {
    // Default to voice card
    return randomCard as VoiceCardType;
  }
}

export default function VocabularyPracticePage() {
  // Start with null and load card after mount to avoid hydration issues
  const [currentCard, setCurrentCard] = useState<CardType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Load a random card after component mounts
    const loadCard = async () => {
      try {
        const card = await getRandomCard();
        setCurrentCard(card);
      } catch (error) {
        console.error('Failed to load card:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadCard();
  }, []);
  
  const [level] = useState(1);
  const [score, setScore] = useState(0);
  const [currentCardNumber] = useState(6); // Starting at card 6 as shown in the image
  const [totalCards] = useState(20);
  const [verbsStudying] = useState(5);

  const handleAnswer = async (correct: boolean) => {
    if (correct) {
      setScore(prev => prev + 1);
    }
    
    // Get a new random card for the next practice
    try {
      const card = await getRandomCard();
      setCurrentCard(card);
    } catch (error) {
      console.error('Failed to load new card:', error);
    }
    
    // In a real app, you would advance to the next card or end the session
    console.log('Answer recorded:', correct ? 'Correct' : 'Incorrect');
  };

  const handleReset = async () => {
    try {
      const card = await getRandomCard();
      setCurrentCard(card);
    } catch (error) {
      console.error('Failed to load new card:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link href="/admin">
            <Button variant="ghost" className="flex items-center gap-2">
              <Settings className="w-4 h-4" />
              Admin
            </Button>
          </Link>
          
          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{level}</div>
              <div className="text-xs text-gray-600">Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{score}</div>
              <div className="text-xs text-gray-600">Score</div>
            </div>
            <div className="hidden sm:flex h-6 w-px bg-gray-300" />
            <div className="text-center">
              <div className="text-sm font-semibold">Cards: {currentCardNumber}/{totalCards}</div>
              <div className="text-xs text-gray-600">Progress</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-semibold">Verbs: {verbsStudying}/{verbsStudying}</div>
              <div className="text-xs text-gray-600">Studying</div>
            </div>
          </div>

          <div className="w-20"></div> {/* Spacer to center the stats */}
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="max-w-2xl mx-auto">
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${(currentCardNumber / totalCards) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Vocabulary Practice Card */}
        {isLoading ? (
          <div className="max-w-2xl mx-auto text-center py-12">
            <div className="text-lg text-gray-600">Loading practice card...</div>
          </div>
        ) : currentCard ? (
          currentCard.type === 'context' ? (
            <ContextCard
              contextCard={currentCard as ContextCardType}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          ) : (
            <VoiceCard
              voiceCard={currentCard as VoiceCardType}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          )
        ) : (
          <div className="max-w-2xl mx-auto text-center py-12">
            <div className="text-lg text-red-600">Failed to load practice card. Please refresh the page.</div>
          </div>
        )}

        {/* Card Counter */}
        <div className="text-center mt-6">
          <span className="text-gray-600">
            Card {currentCardNumber} of {totalCards}
          </span>
        </div>
      </div>
    </div>
  );
}
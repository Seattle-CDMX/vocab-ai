'use client';

import { useState, useEffect } from 'react';
import VoiceCard from '@/components/VoiceCard';
import { Button } from '@/components/ui/button';
import { getRandomVoiceCard, VoiceCard as VoiceCardType } from '@/lib/voice-card-types';
import { Settings } from 'lucide-react';
import Link from 'next/link';

export default function VocabularyPracticePage() {
  // Start with null and load voice card after mount to avoid hydration issues
  const [currentVoiceCard, setCurrentVoiceCard] = useState<VoiceCardType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    // Load a random voice card after component mounts
    const loadVoiceCard = async () => {
      try {
        const voiceCard = await getRandomVoiceCard();
        setCurrentVoiceCard(voiceCard);
      } catch (error) {
        console.error('Failed to load voice card:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadVoiceCard();
  }, []);
  
  const [level] = useState(1);
  const [score, setScore] = useState(0);
  const [currentCard] = useState(6); // Starting at card 6 as shown in the image
  const [totalCards] = useState(20);
  const [verbsStudying] = useState(5);

  const handleAnswer = async (correct: boolean) => {
    if (correct) {
      setScore(prev => prev + 1);
    }
    
    // Get a new random voice card for the next practice
    try {
      const voiceCard = await getRandomVoiceCard();
      setCurrentVoiceCard(voiceCard);
    } catch (error) {
      console.error('Failed to load new voice card:', error);
    }
    
    // In a real app, you would advance to the next card or end the session
    console.log('Answer recorded:', correct ? 'Correct' : 'Incorrect');
  };

  const handleReset = async () => {
    try {
      const voiceCard = await getRandomVoiceCard();
      setCurrentVoiceCard(voiceCard);
    } catch (error) {
      console.error('Failed to load new voice card:', error);
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
              <div className="text-sm font-semibold">Cards: {currentCard}/{totalCards}</div>
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
                style={{ width: `${(currentCard / totalCards) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Vocabulary Practice Card */}
        {isLoading ? (
          <div className="max-w-2xl mx-auto text-center py-12">
            <div className="text-lg text-gray-600">Loading voice card...</div>
          </div>
        ) : currentVoiceCard ? (
          <VoiceCard
            voiceCard={currentVoiceCard}
            onAnswer={handleAnswer}
            onReset={handleReset}
          />
        ) : (
          <div className="max-w-2xl mx-auto text-center py-12">
            <div className="text-lg text-red-600">Failed to load voice card. Please refresh the page.</div>
          </div>
        )}

        {/* Card Counter */}
        <div className="text-center mt-6">
          <span className="text-gray-600">
            Card {currentCard} of {totalCards}
          </span>
        </div>
      </div>
    </div>
  );
}
'use client';

import { useState, useEffect } from 'react';
import VoiceCard from '@/components/VoiceCard';
import { Button } from '@/components/ui/button';
import { getRandomLexicalItem, TARGET_LEXICAL_ITEMS } from '@/lib/lexical-items';
import { Settings } from 'lucide-react';
import Link from 'next/link';

export default function VocabularyPracticePage() {
  // Fix hydration mismatch by using first item consistently, then randomize on client
  const [currentItem, setCurrentItem] = useState(TARGET_LEXICAL_ITEMS[0]);
  
  useEffect(() => {
    // Set a random item after component mounts to avoid hydration mismatch
    setCurrentItem(getRandomLexicalItem());
  }, []);
  const [level] = useState(1);
  const [score, setScore] = useState(0);
  const [currentCard] = useState(6); // Starting at card 6 as shown in the image
  const [totalCards] = useState(20);
  const [verbsStudying] = useState(5);

  const handleAnswer = (correct: boolean) => {
    if (correct) {
      setScore(prev => prev + 1);
    }
    
    // Get a new random lexical item for the next practice
    setCurrentItem(getRandomLexicalItem());
    
    // In a real app, you would advance to the next card or end the session
    console.log('Answer recorded:', correct ? 'Correct' : 'Incorrect');
  };

  const handleReset = () => {
    setCurrentItem(getRandomLexicalItem());
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
        <VoiceCard
          phrasal={currentItem}
          onAnswer={handleAnswer}
          onReset={handleReset}
        />

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
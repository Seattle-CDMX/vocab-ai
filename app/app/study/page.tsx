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

// Cache for loaded data
let cachedData: { voiceCardTypes: CardType[]; generatedAt?: string } | null = null;

// Function to load voice card data
async function loadVoiceCardData() {
  if (cachedData) return cachedData;
  
  try {
    // Load generated data (now the only source)
    const generatedResponse = await fetch('/api/generated-data?latest=true');
    if (generatedResponse.ok) {
      cachedData = await generatedResponse.json();
      console.log('Using generated voice card data from:', cachedData?.generatedAt);
      return cachedData;
    } else {
      throw new Error('Generated data not found');
    }
  } catch (error) {
    console.error('Failed to load voice card data:', error);
    throw error;
  }
}

// Function to get a card by index (sequential order)
async function getCardByIndex(index: number): Promise<CardType | null> {
  const data = await loadVoiceCardData();
  if (!data) return null;
  const cards = data.voiceCardTypes;
  
  if (index >= cards.length || index < 0) {
    return null; // End of deck or invalid index
  }
  
  const card = cards[index];
  
  // Handle generated images (only for context cards)
  if ('imageUrl' in card && card.imageUrl && card.imageUrl.startsWith('/generated_data/images/')) {
    try {
      const imageResponse = await fetch('/api/generated-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ imagePath: card.imageUrl })
      });
      if (imageResponse.ok) {
        const { image } = await imageResponse.json();
        card.imageUrl = image;
      }
    } catch (error) {
      console.error('Failed to load generated image:', error);
    }
  }
  
  // Convert to appropriate type based on card type
  if (card.type === 'context') {
    return card as ContextCardType;
  } else {
    // Default to voice card
    return card as VoiceCardType;
  }
}

export default function VocabularyPracticePage() {
  // Start with null and load card after mount to avoid hydration issues
  const [currentCard, setCurrentCard] = useState<CardType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [totalCards, setTotalCards] = useState(0);
  
  useEffect(() => {
    // Load the first card after component mounts
    const loadFirstCard = async () => {
      try {
        const data = await loadVoiceCardData();
        if (!data) {
          console.error('Failed to load voice card data');
          return;
        }
        const cardCount = data.voiceCardTypes.length;
        setTotalCards(cardCount);
        
        const card = await getCardByIndex(0);
        setCurrentCard(card);
      } catch (error) {
        console.error('Failed to load card:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadFirstCard();
  }, []);
  
  const [level] = useState(1);
  const [score, setScore] = useState(0);
  const [verbsStudying] = useState(5);

  const handleAnswer = async (correct: boolean) => {
    if (correct) {
      setScore(prev => prev + 1);
    }
    
    // Move to the next card in sequence
    const nextIndex = currentCardIndex + 1;
    
    if (nextIndex >= totalCards) {
      // End of deck reached
      console.log('All cards completed! Final score:', score + (correct ? 1 : 0));
      alert(`Congratulations! You've completed all ${totalCards} cards. Final score: ${score + (correct ? 1 : 0)}/${totalCards}`);
      return;
    }
    
    try {
      const nextCard = await getCardByIndex(nextIndex);
      if (nextCard) {
        setCurrentCard(nextCard);
        setCurrentCardIndex(nextIndex);
        console.log(`Advanced to card ${nextIndex + 1}/${totalCards}:`, nextCard.title);
      }
    } catch (error) {
      console.error('Failed to load next card:', error);
    }
    
    console.log('Answer recorded:', correct ? 'Correct' : 'Incorrect');
  };

  const handleReset = async () => {
    try {
      const card = await getCardByIndex(0);
      setCurrentCard(card);
      setCurrentCardIndex(0);
      console.log('Reset to first card');
    } catch (error) {
      console.error('Failed to reset to first card:', error);
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
              <div className="text-sm font-semibold">Cards: {currentCardIndex + 1}/{totalCards}</div>
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
                style={{ width: `${totalCards > 0 ? ((currentCardIndex + 1) / totalCards) * 100 : 0}%` }}
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
            Card {currentCardIndex + 1} of {totalCards}
          </span>
        </div>
      </div>
    </div>
  );
}
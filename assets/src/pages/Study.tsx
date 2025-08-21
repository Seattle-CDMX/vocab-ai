import { useState } from "react";
import { Button } from "@/components/ui/button";
import ChatCard from "@/components/ChatCard";
import VoiceCard from "@/components/VoiceCard";
import ContextCard from "@/components/ContextCard";
import DialogueCard from "@/components/DialogueCard";
import ProgressBar from "@/components/ProgressBar";
import { ArrowLeft, Settings } from "lucide-react";
import { useNavigate } from "react-router-dom";

// Sample data - in a real app this would come from a backend
const samplePhrasalVerbs = [
  {
    id: "1",
    phrasal: "break down",
    definition: "to stop working (machines, vehicles); to lose control emotionally",
    example: "My car broke down on the highway this morning.",
    difficulty: "beginner" as const
  },
  {
    id: "2", 
    phrasal: "put off",
    definition: "to postpone or delay something",
    example: "I decided to put off the meeting until next week.",
    difficulty: "beginner" as const
  },
  {
    id: "3",
    phrasal: "run into",
    definition: "to meet someone unexpectedly; to encounter a problem",
    example: "I ran into my old teacher at the grocery store.",
    difficulty: "intermediate" as const
  },
  {
    id: "4",
    phrasal: "get along with",
    definition: "to have a good relationship with someone",
    example: "She gets along with her coworkers very well.",
    difficulty: "intermediate" as const
  },
  {
    id: "5",
    phrasal: "come up with",
    definition: "to think of an idea or solution",
    example: "We need to come up with a better plan for the project.",
    difficulty: "advanced" as const
  }
] as const;

// Card types for this study session
 type CardType = 'chat' | 'voice' | 'context' | 'dialogue';
 type SessionItem = { type: CardType; phrasal: typeof samplePhrasalVerbs[number] };

 function shuffle<T>(arr: T[]): T[] {
   const a = [...arr];
   for (let i = a.length - 1; i > 0; i--) {
     const j = Math.floor(Math.random() * (i + 1));
     [a[i], a[j]] = [a[j], a[i]];
   }
   return a;
 }

const Study = () => {
  const navigate = useNavigate();
  const [currentCard, setCurrentCard] = useState(0);
  const [score, setScore] = useState(0);
  const [level] = useState(1);

  const [queue] = useState(() => {
    const items: SessionItem[] = samplePhrasalVerbs.flatMap((pv) => [
      { type: 'chat', phrasal: pv },
      { type: 'voice', phrasal: pv },
      { type: 'context', phrasal: pv },
      { type: 'dialogue', phrasal: pv },
    ]);
    return shuffle(items);
  });

  const totalCards = queue.length;
  const verbsCount = new Set(samplePhrasalVerbs.map(v => v.id)).size;

  const handleAnswer = (correct: boolean) => {
    if (correct) {
      setScore((s) => s + 1);
    }
    
    // Move to next card
    if (currentCard < totalCards - 1) {
      setCurrentCard((i) => i + 1);
    } else {
      // Session complete
      alert(`Session complete! Score: ${correct ? score + 1 : score}/${totalCards}`);
      navigate('/');
    }
  };

  const handleReset = () => {
    setCurrentCard(0);
    setScore(0);
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-study-bg to-primary/5">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button 
            variant="ghost" 
            onClick={() => navigate('/')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Button>
          
          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{level}</div>
              <div className="text-xs text-muted-foreground">Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-success">{score}</div>
              <div className="text-xs text-muted-foreground">Score</div>
            </div>
            <div className="hidden sm:flex h-6 w-px bg-border" />
            <div className="text-center">
              <div className="text-sm font-semibold">Cards: {currentCard + 1}/{totalCards}</div>
              <div className="text-xs text-muted-foreground">Progress</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-semibold">Verbs: {verbsCount}/{verbsCount}</div>
              <div className="text-xs text-muted-foreground">Studying</div>
            </div>
          </div>

          <Button variant="ghost" size="sm">
            <Settings className="w-4 h-4" />
          </Button>
        </div>

        {/* Progress */}
        <div className="mb-8">
          <ProgressBar 
            current={currentCard + 1} 
            total={totalCards}
            className="max-w-2xl mx-auto"
          />
        </div>

        {/* Study Card */}
        {queue.length > 0 && (
          queue[currentCard].type === 'chat' ? (
            <ChatCard
              phrasal={queue[currentCard].phrasal}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          ) : queue[currentCard].type === 'voice' ? (
            <VoiceCard
              phrasal={queue[currentCard].phrasal}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          ) : queue[currentCard].type === 'context' ? (
            <ContextCard
              phrasal={queue[currentCard].phrasal}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          ) : (
            <DialogueCard
              phrasal={queue[currentCard].phrasal}
              onAnswer={handleAnswer}
              onReset={handleReset}
            />
          )
        )}


        {/* Card Counter */}
        <div className="text-center mt-6">
          <span className="text-muted-foreground">
            Card {currentCard + 1} of {totalCards}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Study;
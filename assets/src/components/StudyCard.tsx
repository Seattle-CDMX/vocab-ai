import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Volume2, RotateCcw, Check, X } from "lucide-react";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

interface StudyCardProps {
  phrasal: PhrasalVerb;
  onAnswer: (correct: boolean) => void;
  showAnswer: boolean;
  onShowAnswer: () => void;
  onReset: () => void;
}

const StudyCard = ({ phrasal, onAnswer, showAnswer, onShowAnswer, onReset }: StudyCardProps) => {
  const [isFlipped, setIsFlipped] = useState(false);

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
    if (!showAnswer) {
      onShowAnswer();
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'border-success bg-success/5';
      case 'intermediate': return 'border-warning bg-warning/5';
      case 'advanced': return 'border-destructive bg-destructive/5';
      default: return 'border-border';
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card className={`relative overflow-hidden transition-all duration-300 ${
        isFlipped ? 'animate-card-flip' : ''
      } ${getDifficultyColor(phrasal.difficulty)}`}>
        
        {/* Difficulty Badge */}
        <div className="absolute top-4 right-4">
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            phrasal.difficulty === 'beginner' ? 'bg-success/10 text-success' :
            phrasal.difficulty === 'intermediate' ? 'bg-warning/10 text-warning' :
            'bg-destructive/10 text-destructive'
          }`}>
            {phrasal.difficulty}
          </span>
        </div>

        <div className="p-8">
          {!showAnswer ? (
            /* Question Side */
            <div className="text-center space-y-6">
              <div className="space-y-4">
                <h2 className="text-3xl font-bold text-primary">
                  {phrasal.phrasal}
                </h2>
                <p className="text-muted-foreground">
                  What does this phrasal verb mean?
                </p>
              </div>
              
              <div className="bg-study-bg rounded-lg p-4">
                <p className="text-foreground italic">
                  "{phrasal.example.replace(phrasal.phrasal, '___')}"
                </p>
              </div>

              <Button 
                variant="study" 
                size="lg" 
                onClick={handleFlip}
                className="w-full"
              >
                Show Answer
              </Button>
            </div>
          ) : (
            /* Answer Side */
            <div className="space-y-6">
              <div className="text-center space-y-4">
                <h2 className="text-2xl font-bold text-primary">
                  {phrasal.phrasal}
                </h2>
                <div className="bg-primary/5 rounded-lg p-4 border border-primary/20">
                  <p className="text-lg font-medium text-foreground">
                    {phrasal.definition}
                  </p>
                </div>
              </div>

              <div className="bg-study-bg rounded-lg p-4">
                <p className="text-foreground">
                  <strong>Example:</strong> {phrasal.example}
                </p>
              </div>

              <div className="flex gap-3">
                <Button 
                  variant="destructive" 
                  size="lg" 
                  onClick={() => onAnswer(false)}
                  className="flex-1"
                >
                  <X className="w-5 h-5 mr-2" />
                  Hard
                </Button>
                <Button 
                  variant="warning" 
                  size="lg" 
                  onClick={() => onAnswer(false)}
                  className="flex-1"
                >
                  <RotateCcw className="w-5 h-5 mr-2" />
                  Again
                </Button>
                <Button 
                  variant="success" 
                  size="lg" 
                  onClick={() => onAnswer(true)}
                  className="flex-1"
                >
                  <Check className="w-5 h-5 mr-2" />
                  Easy
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Audio Button */}
        <Button 
          variant="ghost" 
          size="sm" 
          className="absolute bottom-4 left-4"
          onClick={() => {
            // Text-to-speech would go here
            console.log('Playing audio for:', phrasal.phrasal);
          }}
        >
          <Volume2 className="w-4 h-4" />
        </Button>
      </Card>
    </div>
  );
};

export default StudyCard;
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Mic, MicOff, Volume2, RotateCcw, Check, X, MessageCircle } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  status: 'locked' | 'learning' | 'reviewing' | 'mastered';
  level: number;
}

// Sample data (would be fetched based on ID in real app)
const phrasalVerbsData: PhrasalVerb[] = [
  {
    id: "1",
    phrasal: "break down",
    definition: "to stop working (machines, vehicles); to lose control emotionally",
    example: "My car broke down on the highway this morning.",
    difficulty: "beginner",
    status: "mastered",
    level: 1
  },
  {
    id: "2", 
    phrasal: "put off",
    definition: "to postpone or delay something",
    example: "I decided to put off the meeting until next week.",
    difficulty: "beginner",
    status: "reviewing",
    level: 1
  },
  {
    id: "3",
    phrasal: "run into",
    definition: "to meet someone unexpectedly; to encounter a problem",
    example: "I ran into my old teacher at the grocery store.",
    difficulty: "intermediate",
    status: "learning",
    level: 2
  }
];

const FlashCard = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [isListening, setIsListening] = useState(false);
  const [showAnswer, setShowAnswer] = useState(false);
  const [conversationMode, setConversationMode] = useState(false);
  const [messages, setMessages] = useState<Array<{role: 'user' | 'ai', content: string}>>([]);

  const verb = phrasalVerbsData.find(v => v.id === id);

  if (!verb) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Phrasal verb not found</h1>
          <Button onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
        </div>
      </div>
    );
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'border-success bg-success/5';
      case 'intermediate': return 'border-warning bg-warning/5';
      case 'advanced': return 'border-destructive bg-destructive/5';
      default: return 'border-border';
    }
  };

  const handleVoiceToggle = () => {
    setIsListening(!isListening);
    if (!isListening) {
      // Start voice recognition - integrate with LiveKit here
      console.log('Starting voice recognition...');
      // Placeholder for LiveKit integration
    } else {
      // Stop voice recognition
      console.log('Stopping voice recognition...');
    }
  };

  const handlePlayAudio = () => {
    // Text-to-speech for the phrasal verb
    console.log('Playing audio for:', verb.phrasal);
    // This would integrate with TTS
  };

  const startConversation = () => {
    setConversationMode(true);
    setMessages([
      {
        role: 'ai',
        content: `Hi! Let's practice "${verb.phrasal}". Can you use it in a sentence?`
      }
    ]);
  };

  const handleAnswer = (correct: boolean) => {
    // Navigate to next flashcard or back to dashboard
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-study-bg to-primary/5">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button 
            variant="ghost" 
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Button>
          
          <div className="flex items-center gap-4">
            <Badge 
              variant={verb.difficulty === 'beginner' ? 'secondary' : 
                     verb.difficulty === 'intermediate' ? 'outline' : 'destructive'}
            >
              {verb.difficulty}
            </Badge>
            <div className="text-sm text-muted-foreground">Level {verb.level}</div>
          </div>
        </div>

        <div className="max-w-2xl mx-auto">
          {!conversationMode ? (
            /* Flash Card Mode */
            <Card className={`relative overflow-hidden transition-all duration-300 ${getDifficultyColor(verb.difficulty)}`}>
              <div className="p-8">
                {!showAnswer ? (
                  /* Question Side */
                  <div className="text-center space-y-6">
                    <div className="space-y-4">
                      <h2 className="text-4xl font-bold text-primary animate-fade-in">
                        {verb.phrasal}
                      </h2>
                      <p className="text-muted-foreground">
                        What does this phrasal verb mean?
                      </p>
                    </div>
                    
                    <div className="bg-study-bg rounded-lg p-4">
                      <p className="text-foreground italic">
                        "{verb.example.replace(verb.phrasal, '___')}"
                      </p>
                    </div>

                    <div className="flex gap-3 justify-center">
                      <Button 
                        variant="study" 
                        size="lg" 
                        onClick={() => setShowAnswer(true)}
                        className="flex-1 max-w-xs"
                      >
                        Show Answer
                      </Button>
                    </div>

                    <div className="flex gap-3 justify-center">
                      <Button 
                        variant="outline" 
                        onClick={startConversation}
                        className="flex items-center gap-2"
                      >
                        <MessageCircle className="w-4 h-4" />
                        Practice Speaking
                      </Button>
                    </div>
                  </div>
                ) : (
                  /* Answer Side */
                  <div className="space-y-6 animate-fade-in">
                    <div className="text-center space-y-4">
                      <h2 className="text-3xl font-bold text-primary">
                        {verb.phrasal}
                      </h2>
                      <div className="bg-primary/5 rounded-lg p-4 border border-primary/20">
                        <p className="text-lg font-medium text-foreground">
                          {verb.definition}
                        </p>
                      </div>
                    </div>

                    <div className="bg-study-bg rounded-lg p-4">
                      <p className="text-foreground">
                        <strong>Example:</strong> {verb.example}
                      </p>
                    </div>

                    <div className="flex gap-3">
                      <Button 
                        variant="destructive" 
                        size="lg" 
                        onClick={() => handleAnswer(false)}
                        className="flex-1"
                      >
                        <X className="w-5 h-5 mr-2" />
                        Hard
                      </Button>
                      <Button 
                        variant="warning" 
                        size="lg" 
                        onClick={() => handleAnswer(false)}
                        className="flex-1"
                      >
                        <RotateCcw className="w-5 h-5 mr-2" />
                        Again
                      </Button>
                      <Button 
                        variant="success" 
                        size="lg" 
                        onClick={() => handleAnswer(true)}
                        className="flex-1"
                      >
                        <Check className="w-5 h-5 mr-2" />
                        Easy
                      </Button>
                    </div>

                    <div className="text-center">
                      <Button 
                        variant="outline" 
                        onClick={startConversation}
                        className="flex items-center gap-2"
                      >
                        <MessageCircle className="w-4 h-4" />
                        Practice with AI
                      </Button>
                    </div>
                  </div>
                )}

                {/* Voice Controls */}
                <div className="absolute bottom-4 left-4 flex gap-2">
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={handlePlayAudio}
                  >
                    <Volume2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </Card>
          ) : (
            /* Conversation Mode */
            <div className="space-y-4">
              <Card className="p-6">
                <div className="text-center mb-4">
                  <h2 className="text-2xl font-bold text-primary mb-2">{verb.phrasal}</h2>
                  <p className="text-muted-foreground">Practice conversation mode</p>
                </div>

                {/* Chat Messages */}
                <div className="space-y-3 mb-6 max-h-60 overflow-y-auto">
                  {messages.map((message, index) => (
                    <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`rounded-lg p-3 max-w-xs ${
                        message.role === 'user' 
                          ? 'bg-primary text-primary-foreground' 
                          : 'bg-muted text-foreground'
                      }`}>
                        {message.content}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Voice Control */}
                <div className="flex justify-center gap-4">
                  <Button
                    variant={isListening ? "destructive" : "study"}
                    size="lg"
                    onClick={handleVoiceToggle}
                    className="flex items-center gap-2"
                  >
                    {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                    {isListening ? 'Stop Listening' : 'Start Speaking'}
                  </Button>
                </div>

                <div className="text-center mt-4">
                  <Button 
                    variant="ghost" 
                    onClick={() => setConversationMode(false)}
                  >
                    Back to Flash Card
                  </Button>
                </div>
              </Card>

              {/* LiveKit Integration Ready */}
              <Card className="p-4 bg-primary/5 border-primary/20">
                <div className="text-center text-sm text-muted-foreground">
                  🎯 Ready for LiveKit Agent Integration
                  <br />
                  Voice conversation will be powered by AI agents
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlashCard;
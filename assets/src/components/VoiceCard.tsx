import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Mic } from "lucide-react";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: "beginner" | "intermediate" | "advanced";
}

interface VoiceCardProps {
  phrasal: PhrasalVerb;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

const VoiceCard = ({ phrasal, onAnswer, onReset }: VoiceCardProps) => {
  const [recording, setRecording] = useState(false);

  const toggle = () => setRecording((r) => !r);

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Meaning (Español) — {phrasal.phrasal}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-muted-foreground space-y-2 mb-6">
          <p>Explica en español el significado del phrasal verb. La IA te dirá si lo hiciste bien.</p>
          <p>Habla con tus propias palabras y, si quieres, añade 1 ejemplo sencillo.</p>
        </div>
        <div className="flex flex-col items-center gap-4 py-6">
          <button
            onClick={toggle}
            aria-pressed={recording}
            className={`relative h-20 w-20 rounded-full grid place-items-center text-primary-foreground shadow-lg transition-transform duration-200 focus:outline-none focus:ring-2 focus:ring-primary ${recording ? "scale-105" : "scale-100"} bg-primary`}
          >
            <span
              className={`absolute inset-0 rounded-full ${recording ? "animate-pulse ring-8 ring-primary/30" : "ring-0"}`}
              aria-hidden
            />
            <Mic className="w-8 h-8" />
          </button>
          <div className="text-xs text-muted-foreground min-h-4">
            {recording ? "Listening... speak now." : "Idle. Click mic to begin."}
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">
          LiveKit integration coming next — UI is ready.
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => onAnswer(false)}>Skip</Button>
          <Button variant="success" onClick={() => onAnswer(true)}>Finish</Button>
          {onReset && (
            <Button variant="ghost" onClick={onReset}>Reset</Button>
          )}
        </div>
      </CardFooter>
    </Card>
  );
};

export default VoiceCard;

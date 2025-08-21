import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Headphones, Mic, Pause, Play, Send } from "lucide-react";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: "beginner" | "intermediate" | "advanced";
}

interface DialogueCardProps {
  phrasal: PhrasalVerb;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

const DialogueCard = ({ phrasal, onAnswer, onReset }: DialogueCardProps) => {
  const [playing, setPlaying] = useState(false);
  const [explanation, setExplanation] = useState("");

  const togglePlay = () => setPlaying((p) => !p);

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Dialogue Comprehension — {phrasal.phrasal}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-muted-foreground space-y-2 mb-6">
          <p>
            Listen to the dialogue. Then either talk to the agent or write what the
            dialogue was about and how "{phrasal.phrasal}" is used in context.
          </p>
        </div>

        {/* Audio playback button (placeholder for real audio) */}
        <div className="flex flex-col items-center gap-3 py-4">
          <button
            onClick={togglePlay}
            aria-pressed={playing}
            className={`relative h-16 w-16 rounded-full grid place-items-center text-primary-foreground shadow-lg transition-transform duration-200 focus:outline-none focus:ring-2 focus:ring-primary ${playing ? "scale-105" : "scale-100"} bg-primary`}
          >
            <span
              className={`absolute inset-0 rounded-full ${playing ? "animate-pulse ring-8 ring-primary/30" : "ring-0"}`}
              aria-hidden
            />
            {playing ? <Pause className="w-7 h-7" /> : <Play className="w-7 h-7" />}
          </button>
          <div className="text-xs text-muted-foreground min-h-4 flex items-center gap-2">
            <Headphones className="w-3.5 h-3.5" />
            {playing ? "Playing dialogue..." : "Tap to play dialogue"}
          </div>
        </div>

        {/* Text explanation input */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Explain in your own words</label>
          <textarea
            className="w-full rounded-md border bg-background p-3 text-sm outline-none focus:ring-2 focus:ring-primary"
            rows={4}
            placeholder={`Explain the dialogue and how "${phrasal.phrasal}" is used...`}
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
          />
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">Voice agent integration coming next — UI is ready.</div>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={() => onAnswer(false)}>Skip</Button>
          <Button variant="secondary" onClick={() => { /* TODO: start agent convo */ }}>
            <Mic className="w-4 h-4 mr-2" /> Talk to Agent
          </Button>
          <Button variant="success" onClick={() => onAnswer(true)} disabled={!explanation.trim()}>
            <Send className="w-4 h-4 mr-2" /> Submit
          </Button>
          {onReset && (
            <Button variant="ghost" onClick={onReset}>Reset</Button>
          )}
        </div>
      </CardFooter>
    </Card>
  );
};

export default DialogueCard;

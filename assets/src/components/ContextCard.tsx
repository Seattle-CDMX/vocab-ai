
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Lightbulb, Mic } from "lucide-react";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: "beginner" | "intermediate" | "advanced";
}

interface ContextCardProps {
  phrasal: PhrasalVerb;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

const ContextCard = ({ phrasal, onAnswer, onReset }: ContextCardProps) => {

  const scenario =
    phrasal.phrasal.toLowerCase() === "go on"
      ? "Mr. Yang has paused and is waiting. Politely ask him to continue using the correct phrasal verb."
      : `You need to speak with Mr. Yang. Use "${phrasal.phrasal}" naturally to move the conversation forward.`;

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-primary" />
          In-Context — {phrasal.phrasal}
          <Badge variant="secondary" className="ml-2">Scenario</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="rounded-xl px-3 py-2 bg-muted text-foreground">
            <p className="text-sm leading-relaxed">{scenario}</p>
          </div>
          <div className="rounded-lg overflow-hidden border">
            <img
              src="/placeholder.svg"
              alt={`Context for speaking with Mr. Yang about "${phrasal.phrasal}"`}
              loading="lazy"
              className="w-full h-40 object-cover"
            />
          </div>
          <div className="pt-2">
            <Button variant="study" className="hover-scale">
              <Mic className="w-4 h-4 mr-2" />
              Talk to Mr. Yang
            </Button>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">
          Practice using the verb in a real situation.
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => onAnswer(false)}>Skip</Button>
          <Button variant="success" onClick={() => onAnswer(true)}>Complete</Button>
          {onReset && (
            <Button variant="ghost" onClick={onReset}>Reset</Button>
          )}
        </div>
      </CardFooter>
    </Card>
  );
};

export default ContextCard;


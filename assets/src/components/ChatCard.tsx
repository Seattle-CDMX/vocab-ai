import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import { Mic, Send } from "lucide-react";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: "beginner" | "intermediate" | "advanced";
}

interface ChatCardProps {
  phrasal: PhrasalVerb;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

const ChatCard = ({ phrasal, onAnswer, onReset }: ChatCardProps) => {
  const [messages, setMessages] = useState<{ from: "tutor" | "you"; text: string }[]>([
    {
      from: "tutor",
      text: `Pronunciation practice for "${phrasal.phrasal}". Record yourself saying it, or use it in a super simple sentence.`,
    },
  ]);
  
  const [recording, setRecording] = useState(false);

  const send = () => {
    setMessages((m) => [...m, { from: "you", text: "🎤 Audio clip sent" }]);
    setRecording(false);
    // Stubbed AI reply
    setTimeout(() => {
      setMessages((m) => [
        ...m,
        {
          from: "tutor",
          text:
            "Nice try! Consider its meaning: " +
            phrasal.definition +
            ". Example: " +
            phrasal.example,
        },
      ]);
    }, 400);
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mic className="w-5 h-5 text-primary" />
          Pronunciation — {phrasal.phrasal}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-72 overflow-auto pr-1">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.from === "you" ? "justify-end" : "justify-start"}`}>
              <div
                className={
                  m.from === "you"
                    ? "rounded-xl px-3 py-2 bg-primary text-primary-foreground"
                    : "rounded-xl px-3 py-2 bg-muted text-foreground"
                }
              >
                <span className="text-sm leading-relaxed">{m.text}</span>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-center gap-2">
          <Button
            variant="outline"
            onClick={() => setRecording((r) => !r)}
            aria-pressed={recording}
            aria-label={recording ? "Stop recording" : "Start recording"}
            className={`relative ${recording ? "animate-pulse" : ""}`}
          >
            <Mic className="w-4 h-4 mr-2" />
            {recording ? "Recording..." : "Record"}
          </Button>
          <Button variant="study" onClick={send} aria-label="Send audio clip">
            <Send className="w-4 h-4 mr-2" />
            Send clip
          </Button>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">
          Practicing multiple meanings. You'll be assessed on clarity and usage.
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

export default ChatCard;

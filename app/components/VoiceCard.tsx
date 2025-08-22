'use client';

import { useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Mic, MicOff } from "lucide-react";
import { Room } from 'livekit-client';

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
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [roomInstance] = useState(() => new Room());

  const connectToLiveKit = async () => {
    if (isConnecting || isConnected) return;
    
    setIsConnecting(true);
    try {
      // Generate a unique room name for this phrasal verb practice session
      const roomName = `vocab-practice-${phrasal.id}-${Date.now()}`;
      const userName = `student-${Date.now()}`;
      
      console.log('Connecting to LiveKit for phrasal verb practice:', phrasal.phrasal);
      
      const resp = await fetch(`/api/token?room=${roomName}&username=${userName}`);
      const data = await resp.json();
      
      if (data.token) {
        await roomInstance.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, data.token);
        setIsConnected(true);
        console.log('Connected to LiveKit for vocab practice');
      } else {
        console.error('Failed to get token:', data.error);
      }
    } catch (e) {
      console.error('Connection error:', e);
    } finally {
      setIsConnecting(false);
    }
  };

  const disconnectFromLiveKit = async () => {
    try {
      await roomInstance.disconnect();
      setIsConnected(false);
      console.log('Disconnected from LiveKit');
    } catch (e) {
      console.error('Disconnect error:', e);
    }
  };

  const handleMicToggle = () => {
    if (isConnected) {
      disconnectFromLiveKit();
    } else {
      connectToLiveKit();
    }
  };

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
            onClick={handleMicToggle}
            disabled={isConnecting}
            aria-pressed={isConnected}
            className={`relative h-20 w-20 rounded-full grid place-items-center text-white shadow-lg transition-transform duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              isConnected 
                ? "scale-105 bg-red-600 hover:bg-red-700" 
                : isConnecting
                ? "scale-100 bg-gray-400"
                : "scale-100 bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {isConnected && (
              <span
                className="absolute inset-0 rounded-full animate-pulse ring-8 ring-red-600/30"
                aria-hidden
              />
            )}
            {isConnecting ? (
              <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : isConnected ? (
              <MicOff className="w-8 h-8" />
            ) : (
              <Mic className="w-8 h-8" />
            )}
          </button>
          <div className="text-xs text-muted-foreground min-h-4 text-center">
            {isConnecting 
              ? "Connecting to AI teacher..." 
              : isConnected 
              ? "Connected! Speaking with AI teacher." 
              : "Idle. Click mic to connect to AI teacher."}
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-between">
        <div className="text-xs text-muted-foreground">
          {isConnected ? "LiveKit connection active" : "Ready to connect to LiveKit"}
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
'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Mic, MicOff } from "lucide-react";
import { Room } from 'livekit-client';
import { RoomAudioRenderer, StartAudio, RoomContext } from '@livekit/components-react';
import '@livekit/components-styles';
import { VoiceCard as VoiceCardType } from '@/lib/voice-card-types';
import { toast } from 'sonner';

interface VoiceCardProps {
  voiceCard: VoiceCardType;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

const VoiceCard = ({ voiceCard, onAnswer, onReset }: VoiceCardProps) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [roomInstance] = useState(() => new Room());

  // Set up RPC handler for toast notifications
  useEffect(() => {
    if (!isConnected || !roomInstance) return;

    const handleRPC = async (data: any) => {
      console.log('🎯 [VoiceCard] Received RPC:', data);
      console.log('🎯 [VoiceCard] ✅ Handler called for show_toast method, processing payload...');
      
      try {
        const payload = JSON.parse(data.payload);
        console.log('🎯 [VoiceCard] Parsed payload:', payload);
        
        if (payload.type === 'success') {
          console.log('🎯 [VoiceCard] Showing SUCCESS toast:', payload.message);
          toast.success(payload.message, {
            duration: 4000,
            style: {
              background: '#10b981',
              color: 'white',
            },
          });
          console.log('🎯 [VoiceCard] SUCCESS toast.success() called');
        } else if (payload.type === 'error') {
          console.log('🎯 [VoiceCard] Showing ERROR toast:', payload.message);
          toast.error(payload.message, {
            duration: 5000,
            style: {
              background: '#ef4444',
              color: 'white',
            },
          });
          console.log('🎯 [VoiceCard] ERROR toast.error() called');
        } else {
          console.log('🎯 [VoiceCard] ❌ Unknown payload type:', payload.type);
        }
        
        // Send response back to agent
        return JSON.stringify({ status: 'ok' });
      } catch (e) {
        console.error('🎯 [VoiceCard] Failed to parse RPC payload:', e);
        console.error('🎯 [VoiceCard] Raw payload was:', data.payload);
        return JSON.stringify({ status: 'error', message: 'Failed to parse payload' });
      }
    };

    // Register RPC handler
    roomInstance.localParticipant.registerRpcMethod('show_toast', handleRPC);
    console.log('🎯 [VoiceCard] RPC handler registered for show_toast');

    return () => {
      // Cleanup RPC handler on unmount or disconnect
      roomInstance.localParticipant.unregisterRpcMethod('show_toast');
    };
  }, [isConnected, roomInstance]);

  const connectToLiveKit = async () => {
    if (isConnecting || isConnected) return;
    
    setIsConnecting(true);
    try {
      // Generate a unique room name for this voice card practice session
      const roomName = `vocab-practice-${voiceCard.id}-${Date.now()}`;
      const userName = `student-${Date.now()}`;
      
      console.log('🎯 [VoiceCard] Connecting to LiveKit for voice card practice:', voiceCard.title);
      console.log('🎯 [VoiceCard] Voice card data to be sent:', voiceCard);
      
      // Encode voice card data for URL transmission
      const encodedVoiceCardData = encodeURIComponent(JSON.stringify(voiceCard));
      const resp = await fetch(`/api/token?room=${roomName}&username=${userName}&voiceCardData=${encodedVoiceCardData}`);
      const data = await resp.json();
      
      if (data.token) {
        console.log('🎯 [VoiceCard] Token received with voice card data embedded, connecting to room:', roomName);
        await roomInstance.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, data.token);
        console.log('🎯 [VoiceCard] Connected to LiveKit room successfully');
        console.log('🎯 [VoiceCard] Voice card data was passed via token metadata - no need to set attributes');
        
        // Enable microphone for user responses (audio only, no camera)
        await roomInstance.localParticipant.setMicrophoneEnabled(true);
        console.log('🎯 [VoiceCard] Microphone enabled (audio only)');
        
        setIsConnected(true);
        console.log('🎯 [VoiceCard] ✅ COMPLETE: Connected to LiveKit with voice card data embedded in token for:', voiceCard.targetPhrasalVerb.verb);
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
        <CardTitle>Meaning (Español) — {voiceCard.targetPhrasalVerb.verb}</CardTitle>
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
        
        {/* LiveKit Audio Components - Essential for hearing the agent */}
        {isConnected && (
          <RoomContext.Provider value={roomInstance}>
            <RoomAudioRenderer />
            <StartAudio label="Enable audio for AI teacher" />
          </RoomContext.Provider>
        )}
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
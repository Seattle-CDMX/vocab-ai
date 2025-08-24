'use client';

import { useState, useEffect } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Mic, MicOff, MessageCircle } from "lucide-react";
import { Room } from 'livekit-client';
import { RoomAudioRenderer, StartAudio, RoomContext } from '@livekit/components-react';
import '@livekit/components-styles';
import { ContextCard as ContextCardType } from '@/lib/context-card-types';
import { toast } from 'sonner';

interface ContextCardProps {
  contextCard: ContextCardType;
  onAnswer: (correct: boolean) => void;
  onReset?: () => void;
}

interface RPCData {
  payload: string;
}

const ContextCard = ({ contextCard, onAnswer, onReset }: ContextCardProps) => {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [roomInstance] = useState(() => new Room());

  // Set up RPC handler for toast notifications
  useEffect(() => {
    if (!isConnected || !roomInstance) return;

    const handleRPC = async (data: RPCData) => {
      console.log('🎯 [ContextCard] Received RPC:', data);
      
      try {
        const payload = JSON.parse(data.payload);
        console.log('🎯 [ContextCard] Parsed payload:', payload);
        
        if (payload.type === 'success') {
          console.log('🎯 [ContextCard] Showing SUCCESS toast:', payload.message);
          toast.success(payload.message, {
            duration: 4000,
            style: {
              background: '#10b981',
              color: 'white',
            },
          });
          // Mark as completed if success
          if (payload.message.includes('correctly')) {
            setTimeout(() => onAnswer(true), 2000);
          }
        } else if (payload.type === 'error') {
          console.log('🎯 [ContextCard] Showing ERROR toast:', payload.message);
          toast.error(payload.message, {
            duration: 5000,
            style: {
              background: '#ef4444',
              color: 'white',
            },
          });
          // Mark as failed if out of turns
          if (payload.message.includes('Out of turns')) {
            setTimeout(() => onAnswer(false), 2000);
          }
        }
        
        // Send response back to agent
        return JSON.stringify({ status: 'ok' });
      } catch (e) {
        console.error('🎯 [ContextCard] Failed to parse RPC payload:', e);
        return JSON.stringify({ status: 'error', message: 'Failed to parse payload' });
      }
    };

    // Register RPC handler
    roomInstance.localParticipant.registerRpcMethod('show_toast', handleRPC);
    console.log('🎯 [ContextCard] RPC handler registered for show_toast');

    return () => {
      // Cleanup RPC handler on unmount or disconnect
      roomInstance.localParticipant.unregisterRpcMethod('show_toast');
    };
  }, [isConnected, roomInstance, onAnswer]);

  const connectToLiveKit = async () => {
    if (isConnecting || isConnected) return;
    
    setIsConnecting(true);
    try {
      // Generate a unique room name for this context practice session
      const roomName = `context-practice-${contextCard.id}-${Date.now()}`;
      const userName = `student-${Date.now()}`;
      
      console.log('🎯 [ContextCard] Connecting to LiveKit for context practice:', contextCard.title);
      console.log('🎯 [ContextCard] Context card data to be sent:', contextCard);
      
      // Prepare metadata with activity type and scenario
      const metadata = {
        activityType: 'context',
        scenario: contextCard.scenario,
        targetPhrasalVerb: contextCard.targetPhrasalVerb
      };
      
      // Encode metadata for URL transmission
      const encodedMetadata = encodeURIComponent(JSON.stringify(metadata));
      const resp = await fetch(`/api/token?room=${roomName}&username=${userName}&metadata=${encodedMetadata}`);
      const data = await resp.json();
      
      if (data.token) {
        console.log('🎯 [ContextCard] Token received with context metadata, connecting to room:', roomName);
        await roomInstance.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, data.token);
        console.log('🎯 [ContextCard] Connected to LiveKit room successfully');
        
        // Enable microphone for user responses (audio only, no camera)
        await roomInstance.localParticipant.setMicrophoneEnabled(true);
        console.log('🎯 [ContextCard] Microphone enabled for context conversation');
        
        setIsConnected(true);
        console.log('🎯 [ContextCard] ✅ COMPLETE: Connected to LiveKit with context scenario for:', contextCard.scenario.character);
      } else {
        console.error('Failed to get token:', data.error);
        toast.error('Failed to connect to practice session');
      }
    } catch (e) {
      console.error('Connection error:', e);
      toast.error('Connection error. Please try again.');
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
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5 text-primary" />
          In-Context — {contextCard.targetPhrasalVerb.verb}
          <span className="ml-auto text-sm font-normal text-muted-foreground">Scenario</span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="rounded-xl px-4 py-3 bg-muted text-foreground">
            <p className="text-sm leading-relaxed">{contextCard.contextText}</p>
          </div>
          
          {contextCard.imageUrl && (
            <div className="rounded-lg overflow-hidden border">
              <img
                src={contextCard.imageUrl}
                alt={`Context for ${contextCard.scenario.character}`}
                loading="lazy"
                className="w-full h-48 object-cover"
              />
            </div>
          )}
          
          <div className="flex flex-col items-center gap-4 py-6">
            <button
              onClick={handleMicToggle}
              disabled={isConnecting}
              aria-pressed={isConnected}
              className={`relative h-20 w-20 rounded-full grid place-items-center text-white shadow-lg transition-transform duration-200 focus:outline-none focus:ring-2 focus:ring-primary ${
                isConnected 
                  ? "scale-105 bg-red-600 hover:bg-red-700" 
                  : isConnecting
                  ? "scale-100 bg-gray-400"
                  : "scale-100 bg-primary hover:bg-primary/90"
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
            
            <div className="text-center">
              <div className="text-sm font-medium">
                {isConnecting 
                  ? `Connecting to ${contextCard.scenario.character}...` 
                  : isConnected 
                  ? `Speaking with ${contextCard.scenario.character}` 
                  : contextCard.ctaText}
              </div>
              <div className="text-xs text-muted-foreground mt-1">
                {isConnected 
                  ? `Use "${contextCard.targetPhrasalVerb.verb}" naturally in conversation` 
                  : "Click to start conversation"}
              </div>
            </div>
          </div>
        </div>
        
        {/* LiveKit Audio Components - Essential for hearing the agent */}
        {isConnected && (
          <RoomContext.Provider value={roomInstance}>
            <RoomAudioRenderer />
            <StartAudio label={`Enable audio for ${contextCard.scenario.character}`} />
          </RoomContext.Provider>
        )}
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
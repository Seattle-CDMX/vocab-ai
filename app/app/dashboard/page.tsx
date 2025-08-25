'use client';

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, BarChart3 } from "lucide-react";
import { useRouter } from "next/navigation";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  srsLevel: number;
}

interface JsonPhrasalVerb {
  id: number;
  verb: string;
  senses: Array<{
    senseNumber: number;
    definition: string;
    confidencePercent: number;
    examples: string[];
  }>;
}

const convertPhrasalVerbData = (jsonData: JsonPhrasalVerb[]): PhrasalVerb[] => {
  return jsonData.slice(0, 50).map((verb) => {
    const primarySense = verb.senses[0];
    const confidence = primarySense.confidencePercent;
    
    let difficulty: 'beginner' | 'intermediate' | 'advanced';
    if (confidence >= 70) {
      difficulty = 'beginner';
    } else if (confidence >= 40) {
      difficulty = 'intermediate';
    } else {
      difficulty = 'advanced';
    }
    
    const random = Math.random();
    let srsLevel: number;
    if (random < 0.7) {
      srsLevel = 0;
    } else if (random < 0.85) {
      srsLevel = Math.floor(Math.random() * 3) + 1;
    } else if (random < 0.95) {
      srsLevel = Math.floor(Math.random() * 3) + 4;
    } else {
      srsLevel = Math.floor(Math.random() * 3) + 7;
    }
    
    return {
      id: verb.id.toString(),
      phrasal: verb.verb.toLowerCase(),
      definition: primarySense.definition,
      example: primarySense.examples[0] || `Example with ${verb.verb.toLowerCase()}.`,
      difficulty,
      srsLevel
    };
  });
};

const PhrasalVerbCard = ({ verb, onClick }: { verb: PhrasalVerb; onClick: () => void }) => {
  const getNeuronGrowth = (level: number) => {
    if (level === 0) return 'bg-muted text-muted-foreground border-border';
    
    switch (true) {
      case level >= 8: return 'bg-green-500/20 text-green-700 border-green-500/40 shadow-md';
      case level >= 6: return 'bg-blue-500/20 text-blue-700 border-blue-500/40 shadow-sm';
      case level >= 4: return 'bg-yellow-500/20 text-yellow-700 border-yellow-500/40';
      case level >= 2: return 'bg-orange-500/20 text-orange-700 border-orange-500/40';
      default: return 'bg-red-500/20 text-red-700 border-red-500/40';
    }
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return <Badge variant="secondary" className="text-xs">B</Badge>;
      case 'intermediate': return <Badge variant="outline" className="text-xs">I</Badge>;
      case 'advanced': return <Badge variant="destructive" className="text-xs">A</Badge>;
      default: return null;
    }
  };

  const getNeuronIcon = (level: number) => {
    if (level === 0) return '🔒';
    const neurons = ['🌱', '🌿', '🌳', '⚡', '🧠', '💫', '✨', '🌟', '💎'];
    return neurons[level - 1] || '🌱';
  };

  return (
    <Card 
      className={`relative cursor-pointer transition-all duration-200 hover:scale-105 hover:shadow-lg border-2 ${getNeuronGrowth(verb.srsLevel)} ${
        verb.srsLevel === 0 ? 'cursor-not-allowed opacity-60' : ''
      }`}
      onClick={verb.srsLevel !== 0 ? onClick : undefined}
    >
      <div className="p-4 text-center space-y-2">
        <div className="absolute top-2 left-2 text-xs font-bold bg-background/80 rounded px-1">
          {verb.srsLevel === 0 ? 'L🔒' : `L${verb.srsLevel}`}
        </div>
        
        <div className="absolute top-2 right-2">
          {getDifficultyBadge(verb.difficulty)}
        </div>

        <div className="text-2xl mb-2">
          {getNeuronIcon(verb.srsLevel)}
        </div>

        <div className="font-bold text-sm leading-tight">
          {verb.phrasal}
        </div>

        <div className="text-xs font-medium">
          {verb.srsLevel === 0 ? 'Locked' : `Level ${verb.srsLevel}`}
        </div>
      </div>
    </Card>
  );
};

export default function Dashboard() {
  const router = useRouter();
  const [processedVerbs, setProcessedVerbs] = useState<PhrasalVerb[]>([]);

  useEffect(() => {
    fetch('/phrasal_verbs.json')
      .then(response => response.json())
      .then(data => {
        const converted = convertPhrasalVerbData(data as JsonPhrasalVerb[]);
        setProcessedVerbs(converted);
      })
      .catch(error => console.error('Error loading phrasal verbs:', error));
  }, []);

  const getStats = () => {
    const total = processedVerbs.length;
    const locked = processedVerbs.filter(v => v.srsLevel === 0).length;
    const unlocked = total - locked;
    
    return { total, locked, unlocked };
  };

  const stats = getStats();

  const handleVerbClick = (verb: PhrasalVerb) => {
    if (verb.srsLevel > 0) {
      router.push(`/study?verb=${verb.id}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => router.push('/')}
              className="flex items-center gap-2"
            >
              <Brain className="w-5 h-5" />
              VoiceCard
            </Button>
            <h1 className="text-3xl font-bold text-foreground">Phrasal Verb Dashboard</h1>
          </div>
          
          <div className="flex gap-3">
            <Button variant="outline" size="sm">
              <BarChart3 className="w-4 h-4 mr-2" />
              Stats
            </Button>
            <Button onClick={() => router.push('/study')}>
              Start Session
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-primary mb-2">{stats.total}</div>
            <div className="text-sm text-muted-foreground">Total Phrasal Verbs</div>
          </Card>
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">{stats.unlocked}</div>
            <div className="text-sm text-muted-foreground">Unlocked</div>
          </Card>
          <Card className="p-6 text-center">
            <div className="text-3xl font-bold text-muted-foreground mb-2">{stats.locked}</div>
            <div className="text-sm text-muted-foreground">Locked</div>
          </Card>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
          {processedVerbs.map((verb) => (
            <PhrasalVerbCard
              key={verb.id}
              verb={verb}
              onClick={() => handleVerbClick(verb)}
            />
          ))}
        </div>

        {processedVerbs.length === 0 && (
          <div className="text-center py-12">
            <div className="text-muted-foreground">Loading phrasal verbs...</div>
          </div>
        )}
      </div>
    </div>
  );
}
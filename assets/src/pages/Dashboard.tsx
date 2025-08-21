import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Brain, Search, Filter, Mic, Volume2, BarChart3, Settings } from "lucide-react";
import { useNavigate } from "react-router-dom";
import phrasalVerbsData from "../../phrasal_verbs.json";

interface PhrasalVerb {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  srsLevel: number; // 0 = locked, 1-9 = neuron growth levels
  nextReview?: Date;
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

// Function to convert JSON data to our PhrasalVerb format
const convertPhrasalVerbData = (jsonData: JsonPhrasalVerb[]): PhrasalVerb[] => {
  return jsonData.map((verb, index) => {
    const primarySense = verb.senses[0]; // Use the first sense as primary
    const confidence = primarySense.confidencePercent;
    
    // Assign difficulty based on confidence percentage
    let difficulty: 'beginner' | 'intermediate' | 'advanced';
    if (confidence >= 70) {
      difficulty = 'beginner';
    } else if (confidence >= 40) {
      difficulty = 'intermediate';
    } else {
      difficulty = 'advanced';
    }
    
    // Assign SRS levels - most should be locked (0), some unlocked at various levels
    let srsLevel: number;
    const random = Math.random();
    if (random < 0.7) {
      srsLevel = 0; // 70% locked
    } else if (random < 0.85) {
      srsLevel = Math.floor(Math.random() * 3) + 1; // 15% at levels 1-3
    } else if (random < 0.95) {
      srsLevel = Math.floor(Math.random() * 3) + 4; // 10% at levels 4-6
    } else {
      srsLevel = Math.floor(Math.random() * 3) + 7; // 5% at levels 7-9
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
    
    // Neuron growth visualization - gets brighter/more vibrant as it grows
    const intensity = Math.min(level * 10 + 10, 100);
    switch (true) {
      case level >= 8: return 'bg-success text-success-foreground border-success shadow-md'; // Fully grown
      case level >= 6: return 'bg-primary text-primary-foreground border-primary shadow-sm'; // Strong growth
      case level >= 4: return 'bg-warning text-warning-foreground border-warning'; // Growing
      case level >= 2: return 'bg-orange-500/20 text-orange-700 border-orange-500/40'; // Early growth
      default: return 'bg-red-500/20 text-red-700 border-red-500/40'; // Just started
    }
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return <Badge variant="secondary" className="text-xs">B</Badge>;
      case 'intermediate': return <Badge variant="outline" className="text-xs bg-warning/10">I</Badge>;
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
        {/* SRS Level indicator */}
        <div className="absolute top-2 left-2 text-xs font-bold bg-background/80 rounded px-1">
          {verb.srsLevel === 0 ? 'L🔒' : `L${verb.srsLevel}`}
        </div>
        
        {/* Difficulty badge */}
        <div className="absolute top-2 right-2">
          {getDifficultyBadge(verb.difficulty)}
        </div>

        {/* Neuron growth icon */}
        <div className="text-2xl mb-2">
          {getNeuronIcon(verb.srsLevel)}
        </div>

        {/* Phrasal verb */}
        <div className="font-bold text-sm leading-tight">
          {verb.phrasal}
        </div>

        {/* Level indicator */}
        <div className="text-xs font-medium">
          {verb.srsLevel === 0 ? 'Locked' : `Level ${verb.srsLevel}`}
        </div>
      </div>
    </Card>
  );
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [filterLevel, setFilterLevel] = useState<string>("all");
  const [filterDifficulty, setFilterDifficulty] = useState<string>("all");
  const [processedVerbs, setProcessedVerbs] = useState<PhrasalVerb[]>([]);

  useEffect(() => {
    // Convert JSON data to our format on component mount
    const converted = convertPhrasalVerbData(phrasalVerbsData as JsonPhrasalVerb[]);
    setProcessedVerbs(converted);
  }, []);

  const filteredVerbs = processedVerbs.filter(verb => {
    const matchesSearch = verb.phrasal.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         verb.definition.toLowerCase().includes(searchTerm.toLowerCase());
    
    let matchesLevel = true;
    if (filterLevel === "locked") {
      matchesLevel = verb.srsLevel === 0;
    } else if (filterLevel === "early") {
      matchesLevel = verb.srsLevel >= 1 && verb.srsLevel <= 3;
    } else if (filterLevel === "mid") {
      matchesLevel = verb.srsLevel >= 4 && verb.srsLevel <= 6;
    } else if (filterLevel === "advanced") {
      matchesLevel = verb.srsLevel >= 7 && verb.srsLevel <= 9;
    }
    
    const matchesDifficulty = filterDifficulty === "all" || verb.difficulty === filterDifficulty;
    
    return matchesSearch && matchesLevel && matchesDifficulty;
  });

  const getStats = () => {
    const total = processedVerbs.length;
    const locked = processedVerbs.filter(v => v.srsLevel === 0).length;
    const levelCounts = Array.from({length: 9}, (_, i) => ({
      level: i + 1,
      count: processedVerbs.filter(v => v.srsLevel === i + 1).length
    }));

    return { total, locked, levelCounts };
  };

  const stats = getStats();

  const handleVerbClick = (verb: PhrasalVerb) => {
    // Navigate to flash card mode for this specific verb
    if (verb.srsLevel > 0) {
      navigate(`/flashcard/${verb.id}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-study-bg to-primary/5">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              className="flex items-center gap-2"
            >
              <Brain className="w-5 h-5" />
              PhrasalMaster
            </Button>
            <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          </div>
          
          <div className="flex gap-3">
            <Button variant="outline" size="sm">
              <BarChart3 className="w-4 h-4 mr-2" />
              Stats
            </Button>
            <Button variant="study" onClick={() => navigate('/study')}>
              Start Session
            </Button>
          </div>
        </div>

        {/* Stats Overview - Neuron Growth Levels */}
        <div className="grid grid-cols-5 md:grid-cols-11 gap-2 mb-8">
          <Card className="p-3 text-center border-border">
            <div className="text-lg font-bold text-foreground">{stats.total}</div>
            <div className="text-xs text-muted-foreground">Total</div>
          </Card>
          <Card className="p-3 text-center border-border bg-muted/20">
            <div className="text-lg font-bold text-muted-foreground">{stats.locked}</div>
            <div className="text-xs text-muted-foreground">🔒</div>
          </Card>
          {stats.levelCounts.map(({ level, count }) => {
            const getCardStyle = (level: number) => {
              switch (true) {
                case level >= 8: return 'border-success/30 bg-success/5 text-success';
                case level >= 6: return 'border-primary/30 bg-primary/5 text-primary';
                case level >= 4: return 'border-warning/30 bg-warning/5 text-warning';
                case level >= 2: return 'border-orange-500/30 bg-orange-500/5 text-orange-600';
                default: return 'border-red-500/30 bg-red-500/5 text-red-600';
              }
            };

            return (
              <Card key={level} className={`p-3 text-center ${getCardStyle(level)}`}>
                <div className="text-lg font-bold">{count}</div>
                <div className="text-xs text-muted-foreground">L{level}</div>
              </Card>
            );
          })}
        </div>

        {/* Filters and Search */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search phrasal verbs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Tabs value={filterLevel} onValueChange={(value) => {
              if (value === "1") {
                // Show L1-3, filter in the component logic
                setFilterLevel("early");
              } else if (value === "4") {
                setFilterLevel("mid");
              } else if (value === "7") {
                setFilterLevel("advanced");
              } else {
                setFilterLevel(value);
              }
            }} className="w-auto">
              <TabsList className="grid-cols-6">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="locked">🔒</TabsTrigger>
                <TabsTrigger value="1">L1-3</TabsTrigger>
                <TabsTrigger value="4">L4-6</TabsTrigger>
                <TabsTrigger value="7">L7-9</TabsTrigger>
              </TabsList>
            </Tabs>

            <Tabs value={filterDifficulty} onValueChange={setFilterDifficulty} className="w-auto">
              <TabsList>
                <TabsTrigger value="all">All Levels</TabsTrigger>
                <TabsTrigger value="beginner">Beginner</TabsTrigger>
                <TabsTrigger value="intermediate">Intermediate</TabsTrigger>
                <TabsTrigger value="advanced">Advanced</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>

        {/* Phrasal Verbs Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
          {filteredVerbs.map((verb) => (
            <PhrasalVerbCard
              key={verb.id}
              verb={verb}
              onClick={() => handleVerbClick(verb)}
            />
          ))}
        </div>

        {filteredVerbs.length === 0 && (
          <div className="text-center py-12">
            <div className="text-muted-foreground">No phrasal verbs found matching your criteria.</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
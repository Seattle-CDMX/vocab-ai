export type ActivityType = 'voice' | 'context';

export interface ContextScenario {
  character: string;
  situation: string;
  phrasalVerb: string;
  contextText: string;
  maxTurns?: number;
}

export interface ContextCard {
  id: string;
  type: 'context';
  title: string;
  contextText: string;
  imageUrl: string;
  ctaText: string;
  scenario: ContextScenario;
  targetPhrasalVerb: {
    verb: string;
    definition: string;
    example: string;
  };
}

interface VoiceCardData {
  id: string;
  type: string;
  title: string;
  targetPhrasalVerb: {
    verb: string;
    senses: Array<{
      senseNumber: number;
      definition: string;
      examples: string[];
    }>;
  };
}

export interface TokenMetadata {
  activityType: ActivityType;
  scenario?: ContextScenario;
  voiceCardData?: VoiceCardData;
}
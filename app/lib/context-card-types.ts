export type ActivityType = 'voice' | 'context';

export interface VoicePersona {
  voice: {
    name: string;
    language_code: string;
    language_name: string;
    gender: string;
    voice_type: string;
  };
  persona: {
    name: string;
    teaching_style: string;
    expertise: string;
    personality_traits: string[];
    preferred_contexts: string[];
  };
}

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
  targetLexicalItem: {
    lexicalItem: string;
    definition: string;
    example: string;
  };
  voicePersona: VoicePersona;
}

interface VoiceCardData {
  id: string;
  type: string;
  title: string;
  targetLexicalItem: {
    lexicalItem: string;
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
  targetLexicalItem?: {
    lexicalItem: string;
    definition: string;
    example: string;
  };
  voicePersona?: VoicePersona;
  voiceCardData?: VoiceCardData;
}
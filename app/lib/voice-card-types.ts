export interface VoiceCardSense {
  senseNumber: number;
  definition: string;
  examples: string[];
}

export interface VoiceCardLexicalItem {
  lexicalItem: string;
  senses: VoiceCardSense[];
}

export interface VoiceCard {
  id: string;
  type: string;
  title: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  targetLexicalItem: VoiceCardLexicalItem;
}

export interface VoiceCardTypesData {
  voiceCardTypes: VoiceCard[];
  metadata: {
    version: string;
    totalCards: number;
    supportedTypes: string[];
    defaultType: string;
  };
}

// Cache for the voice card data
let voiceCardData: VoiceCardTypesData | null = null;

// Load voice card types from generated data API
export async function loadVoiceCardTypes(): Promise<VoiceCardTypesData> {
  if (voiceCardData) {
    return voiceCardData;
  }
  
  try {
    const response = await fetch('/api/generated-data?latest=true');
    if (!response.ok) {
      throw new Error(`Failed to load voice card types: ${response.statusText}`);
    }
    voiceCardData = await response.json();
    if (!voiceCardData) {
      throw new Error('Failed to parse voice card data');
    }
    return voiceCardData;
  } catch (error) {
    console.error('Error loading voice card types:', error);
    throw error;
  }
}

// Get all voice cards
export async function getAllVoiceCards(): Promise<VoiceCard[]> {
  const data = await loadVoiceCardTypes();
  return data.voiceCardTypes;
}

// Get a random voice card
export async function getRandomVoiceCard(): Promise<VoiceCard> {
  const cards = await getAllVoiceCards();
  const randomIndex = Math.floor(Math.random() * cards.length);
  return cards[randomIndex];
}

// Get voice cards by type
export async function getVoiceCardsByType(type: string): Promise<VoiceCard[]> {
  const cards = await getAllVoiceCards();
  return cards.filter(card => card.type === type);
}

// Get voice cards by difficulty
export async function getVoiceCardsByDifficulty(difficulty: "beginner" | "intermediate" | "advanced"): Promise<VoiceCard[]> {
  const cards = await getAllVoiceCards();
  return cards.filter(card => card.difficulty === difficulty);
}

// Get a specific voice card by ID
export async function getVoiceCardById(id: string): Promise<VoiceCard | undefined> {
  const cards = await getAllVoiceCards();
  return cards.find(card => card.id === id);
}

// Get supported types
export async function getSupportedTypes(): Promise<string[]> {
  const data = await loadVoiceCardTypes();
  return data.metadata.supportedTypes;
}
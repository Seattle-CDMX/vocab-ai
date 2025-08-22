export interface LexicalItem {
  id: string;
  phrasal: string;
  definition: string;
  example: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  senses?: string[];
}

// Hardcoded target lexical items for vocabulary practice
export const TARGET_LEXICAL_ITEMS: LexicalItem[] = [
  {
    id: "get-along-with",
    phrasal: "get along with",
    definition: "to have a good relationship with someone",
    example: "She gets along with her coworkers very well.",
    difficulty: "intermediate",
    senses: [
      "tener una buena relación con alguien",
      "llevarse bien con",
      "caerse bien mutuamente",
      "mantener armonía con otra persona"
    ]
  },
  {
    id: "break-down",
    phrasal: "break down",
    definition: "to stop working (machines, vehicles); to lose control emotionally",
    example: "My car broke down on the highway this morning.",
    difficulty: "beginner",
    senses: [
      "dejar de funcionar (máquinas, vehículos)",
      "averiarse",
      "perder el control emocional",
      "colapsar emocionalmente"
    ]
  },
  {
    id: "put-off",
    phrasal: "put off",
    definition: "to postpone or delay something",
    example: "I decided to put off the meeting until next week.",
    difficulty: "beginner",
    senses: [
      "posponer algo",
      "aplazar",
      "retrasar una actividad",
      "diferir una tarea"
    ]
  },
  {
    id: "run-into",
    phrasal: "run into",
    definition: "to meet someone unexpectedly; to encounter a problem",
    example: "I ran into my old teacher at the grocery store.",
    difficulty: "intermediate",
    senses: [
      "encontrarse con alguien por casualidad",
      "toparse con",
      "encontrar un problema inesperadamente",
      "chocar contra algo"
    ]
  },
  {
    id: "come-up-with",
    phrasal: "come up with",
    definition: "to think of an idea or solution",
    example: "We need to come up with a better plan for the project.",
    difficulty: "advanced",
    senses: [
      "pensar en una idea o solución",
      "idear",
      "crear un plan",
      "inventar una solución"
    ]
  }
];

// Get a random lexical item for practice
export function getRandomLexicalItem(): LexicalItem {
  const randomIndex = Math.floor(Math.random() * TARGET_LEXICAL_ITEMS.length);
  return TARGET_LEXICAL_ITEMS[randomIndex];
}

// Get a specific lexical item by ID
export function getLexicalItemById(id: string): LexicalItem | undefined {
  return TARGET_LEXICAL_ITEMS.find(item => item.id === id);
}
export interface Phoneme {
  ipa: string;
  example: string;
  category: 'front' | 'central' | 'back' | 'schwa' | 'syllabic';
  position: {
    angle: number; // degrees from top
    distance: number; // from center (0-1)
  };
  audioFile: string;
}

export const phonemes: Phoneme[] = [
  // Central schwa - at center
  {
    ipa: 'ə',
    example: 'Schwa',
    category: 'schwa',
    position: { angle: 0, distance: 0 },
    audioFile: '/sounds/schwa.mp3'
  },
  
  // Front vowels (blue - top left)
  {
    ipa: 'i',
    example: 'lean team',
    category: 'front',
    position: { angle: 240, distance: 1.0 },
    audioFile: '/sounds/lean_team.mp3'
  },
  {
    ipa: 'ɪ',
    example: 'git commit',
    category: 'front',
    position: { angle: 220, distance: 0.8 },
    audioFile: '/sounds/git_commit.mp3'
  },
  {
    ipa: 'ɛ',
    example: 'ed tech',
    category: 'front',
    position: { angle: 200, distance: 0.8},
    audioFile: '/sounds/ed_tech.mp3'
  },
  {
    ipa: 'eɪ',
    example: 'say array',
    category: 'front',
    position: { angle: 180, distance: 0.75 },
    audioFile: '/sounds/say_array.mp3'
  },
  {
    ipa: 'æ',
    example: 'flask app',
    category: 'front',
    position: { angle: 170, distance: 1.0 },
    audioFile: '/sounds/flask_app.mp3'
  },
  // Back vowels (purple - clockwise from top right)
  {
    ipa: 'u',
    example: 'Bluetooth',
    category: 'back',
    position: { angle: -80, distance: 1.0 },
    audioFile: '/sounds/bluetooth.mp3'
  },
  {
    ipa: 'ʊ',
    example: 'hook',
    category: 'back',
    position: { angle: -50, distance: 0.8 },
    audioFile: '/sounds/hook.mp3'
  },
  {
    ipa: 'aʊ',
    example: 'cloud',
    category: 'back',
    position: { angle: -20, distance: 0.85 },
    audioFile: '/sounds/cloud.mp3'
  },
  {
    ipa: 'oʊ',
    example: 'node',
    category: 'back',
    position: { angle: 10, distance: 0.75 },
    audioFile: '/sounds/node.mp3'
  },
  {
    ipa: 'ɔɪ',
    example: 'deploy',
    category: 'back',
    position: { angle: 40, distance: 0.9 },
    audioFile: '/sounds/deploy.mp3'
  },
  {
    ipa: 'aɪ',
    example: 'byte',
    category: 'back',
    position: { angle: 70, distance: 0.85 },
    audioFile: '/sounds/byte.mp3'
  },
  {
    ipa: 'ɑ',
    example: 'Java doc',
    category: 'back',
    position: { angle: 100, distance: 1.0 },
    audioFile: '/sounds/javadoc.mp3'
  },
  {
    ipa: 'l',
    example: 'long poll',
    category: 'syllabic',
    position: { angle: 135, distance: 1.0 },
    audioFile: '/sounds/long_poll.mp3'
  },
  
  // Central vowels
  {
    ipa: 'ʌ',
    example: 'bug hunt',
    category: 'central',
    position: { angle: 100, distance: 0.1 },
    audioFile: '/sounds/bug_hunt.mp3'
  },
  {
    ipa: 'ɝ',
    example: 'server',
    category: 'syllabic',
    position: { angle: 135, distance: 0.6 },
    audioFile: '/sounds/server.mp3'
  },
  
];
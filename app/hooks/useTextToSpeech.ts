import { useCallback } from 'react';

export const useTextToSpeech = () => {
  const playAudio = useCallback(async (audioFile: string) => {
    try {
      const audio = new Audio(audioFile);
      audio.volume = 0.8;
      await audio.play();
    } catch (error) {
      console.error('Error playing audio file:', error);
    }
  }, []);

  return { playAudio };
};
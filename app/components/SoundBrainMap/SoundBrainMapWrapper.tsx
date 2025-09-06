'use client';

import VowelNeuronVisualizationDirect from "./VowelNeuronVisualizationDirect";

interface SoundBrainMapWrapperProps {
  className?: string;
}

export default function SoundBrainMapWrapper({ className = "" }: SoundBrainMapWrapperProps) {
  return <VowelNeuronVisualizationDirect className={className} />;
}
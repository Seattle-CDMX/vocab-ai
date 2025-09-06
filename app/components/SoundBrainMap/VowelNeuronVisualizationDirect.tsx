'use client';

import { useEffect, useRef } from 'react';
import { phonemes, Phoneme } from '@/lib/phonemes';
import { useTextToSpeech } from '@/hooks/useTextToSpeech';
import type p5 from 'p5';

interface NeuronNode {
  phoneme: Phoneme;
  x: number;
  y: number;
  originalX: number;
  originalY: number;
  radius: number;
  isHovered: boolean;
  isDragging: boolean;
  isReturning: boolean;
  pulsePhase: number;
  returnStartTime: number;
  dendrites: { angle: number; length: number }[];
}

interface SoundBrainMapDirectProps {
  className?: string;
}

export default function VowelNeuronVisualizationDirect({ className = "" }: SoundBrainMapDirectProps) {
  const sketchRef = useRef<HTMLDivElement>(null);
  const p5InstanceRef = useRef<p5 | null>(null);
  const { playAudio } = useTextToSpeech();

  useEffect(() => {
    if (!sketchRef.current) return;

    const loadP5AndSketch = async () => {
      try {
        // Dynamically import p5.js to avoid SSR issues
        const p5Module = await import('p5');
        const p5 = p5Module.default;

        const sketch = (p: p5) => {
          const state = {
            nodes: [] as NeuronNode[],
            centerX: 0,
            centerY: 0,
            maxRadius: 0,
            dragOffset: { x: 0, y: 0 },
            draggedNode: null as NeuronNode | null,
            brainImage: null as p5.Image | null,
          };

          const generateDendrites = (count: number) => {
            return Array.from({ length: count }, () => ({
              angle: p.random(p.TWO_PI),
              length: p.random(15, 30)
            }));
          };

          const calculateExactPosition = (phoneme: Phoneme) => {
            const angle = p.radians(phoneme.position.angle);
            const distance = Math.max(80, phoneme.position.distance * state.maxRadius);
            
            return {
              x: state.centerX + Math.cos(angle) * distance,
              y: state.centerY + Math.sin(angle) * distance
            };
          };

          const drawBrain = (x: number, y: number, size: number, isHovered: boolean) => {
            const scale = isHovered ? 1.05 : 1;
            const currentSize = size * scale;
            
            p.push();
            p.translate(x, y);
            p.scale(scale);
            
            if (state.brainImage && state.brainImage.width > 0) {
              // Only draw if image is fully loaded
              p.imageMode(p.CENTER);
              p.tint(255, 255);
              p.image(state.brainImage, 0, 0, currentSize * 2, currentSize * 2);
              p.noTint();
            } else {
              // Fallback: simple circle while image loads
              p.colorMode(p.HSB, 360, 100, 100);
              p.fill(320, 45, 88);
              p.stroke(320, 55, 82);
              p.strokeWeight(2);
              p.ellipse(0, 0, currentSize * 1.5, currentSize * 1.5);
            }
            
            p.pop();
            
            // Brain stem/connection lines to neurons
            p.colorMode(p.RGB, 255);
            p.stroke(255, 180, 220, 120);
            p.strokeWeight(2);
            
            state.nodes.forEach(node => {
              if (node.phoneme.category !== 'schwa') {
                // Draw neural pathway
                const steps = 15;
                for (let i = 0; i < steps; i++) {
                  const t = i / steps;
                  const waveOffset = Math.sin(t * p.PI * 2 + p.frameCount * 0.05) * 5;
                  const pathX = p.lerp(x, node.x, t) + waveOffset;
                  const pathY = p.lerp(y, node.y, t);
                  
                  if (i < steps - 1) {
                    const nextT = (i + 1) / steps;
                    const nextWaveOffset = Math.sin(nextT * p.PI * 2 + p.frameCount * 0.05) * 5;
                    const nextPathX = p.lerp(x, node.x, nextT) + nextWaveOffset;
                    const nextPathY = p.lerp(y, node.y, nextT);
                    
                    const alpha = 150 * (1 - t * 0.7);
                    p.stroke(255, 180, 220, alpha);
                    p.line(pathX, pathY, nextPathX, nextPathY);
                  }
                }
              }
            });
          };

          const drawNeuron = (node: NeuronNode) => {
            const { phoneme, x, y, radius, isHovered, pulsePhase, dendrites, isDragging, isReturning } = node;
            
            // Handle return animation
            if (isReturning && !isDragging) {
              const elapsed = p.millis() - node.returnStartTime;
              const duration = 800;
              const progress = Math.min(elapsed / duration, 1);
              const easedProgress = 1 - Math.pow(1 - progress, 3);
              
              node.x = p.lerp(node.x, node.originalX, easedProgress);
              node.y = p.lerp(node.y, node.originalY, easedProgress);
              
              if (progress >= 1) {
                node.isReturning = false;
                node.x = node.originalX;
                node.y = node.originalY;
              }
            }
            
            const pulseScale = isDragging ? 1.2 : (1 + 0.08 * Math.sin(p.frameCount * 0.04 + pulsePhase));
            const currentRadius = radius * (isHovered ? 1.3 : pulseScale);
            
            // Get neuron color based on category
            let fillColor: [number, number, number];
            
            switch (phoneme.category) {
              case 'front':
                fillColor = [195, 90, 80]; // Blue neurons
                break;
              case 'back':
                fillColor = [280, 80, 85]; // Purple neurons
                break;
              case 'central':
                fillColor = [50, 85, 85]; // Yellow neurons
                break;
              case 'syllabic':
                fillColor = [0, 0, 20]; // Dark gray/black neurons
                break;
              default:
                fillColor = [260, 85, 80];
            }
            
            p.colorMode(p.HSB, 360, 100, 100);
            const neuronColor = p.color(fillColor[0], fillColor[1], fillColor[2]);
            
            // Draw dendrites (neural branches)
            p.stroke(fillColor[0], fillColor[1] - 20, fillColor[2] - 10);
            p.strokeWeight(2);
            
            dendrites.forEach(dendrite => {
              const endX = x + Math.cos(dendrite.angle) * dendrite.length;
              const endY = y + Math.sin(dendrite.angle) * dendrite.length;
              
              // Draw branched dendrite
              p.line(x, y, endX, endY);
              
              // Small branches
              const branchAngle1 = dendrite.angle + 0.5;
              const branchAngle2 = dendrite.angle - 0.5;
              const branchLength = dendrite.length * 0.3;
              
              p.line(endX, endY, 
                     endX + Math.cos(branchAngle1) * branchLength,
                     endY + Math.sin(branchAngle1) * branchLength);
              p.line(endX, endY,
                     endX + Math.cos(branchAngle2) * branchLength,
                     endY + Math.sin(branchAngle2) * branchLength);
            });
            
            // Draw neuron cell body
            p.fill(neuronColor);
            p.stroke(fillColor[0], fillColor[1] + 10, fillColor[2] + 15);
            p.strokeWeight(2);
            p.circle(x, y, currentRadius * 2);
            
            // Nucleus
            p.fill(fillColor[0], fillColor[1] + 20, fillColor[2] - 20);
            p.noStroke();
            p.circle(x, y, currentRadius * 0.6);
            
            // Draw text
            p.colorMode(p.RGB, 255);
            p.fill(255, 255, 255);
            p.noStroke();
            p.textAlign(p.CENTER, p.CENTER);
            
            // IPA symbol
            p.textSize(isHovered ? 16 : 12);
            p.textStyle(p.BOLD);
            p.text(phoneme.ipa, x, y - 5);
            
            // Example word
            p.textSize(isHovered ? 10 : 8);
            p.textStyle(p.NORMAL);
            p.text(phoneme.example, x, y + 8);
          };

          p.setup = () => {
            // Create full screen canvas
            const canvas = p.createCanvas(p.windowWidth, p.windowHeight);
            canvas.parent(sketchRef.current!);
            
            // Load the brain image
            p.loadImage('/images/brain.png', (img) => {
              state.brainImage = img;
              console.log('Brain image loaded successfully');
            }, (err) => {
              console.log('Failed to load brain image:', err);
            });
            
            state.centerX = p.width / 2;
            state.centerY = p.height / 2;
            state.maxRadius = Math.min(p.width, p.height) * 0.3;
            
            // Initialize neurons
            state.nodes = [];
            
            // Add schwa first (brain at center)
            const schwa = phonemes.find(ph => ph.category === 'schwa')!;
            state.nodes.push({
              phoneme: schwa,
              x: state.centerX,
              y: state.centerY,
              originalX: state.centerX,
              originalY: state.centerY,
              radius: 60,
              isHovered: false,
              isDragging: false,
              isReturning: false,
              pulsePhase: p.random(p.TWO_PI),
              returnStartTime: 0,
              dendrites: []
            });
            
            phonemes.forEach(phoneme => {
              if (phoneme.category !== 'schwa') {
                const position = calculateExactPosition(phoneme);
                
                state.nodes.push({
                  phoneme,
                  x: position.x,
                  y: position.y,
                  originalX: position.x,
                  originalY: position.y,
                  radius: 25,
                  isHovered: false,
                  isDragging: false,
                  isReturning: false,
                  pulsePhase: p.random(p.TWO_PI),
                  returnStartTime: 0,
                  dendrites: generateDendrites(p.random(4, 8))
                });
              }
            });
          };

          p.draw = () => {
            // Dark neural background with subtle gradient
            for (let i = 0; i <= p.height; i++) {
              const inter = p.map(i, 0, p.height, 0, 1);
              const c = p.lerpColor(p.color(15, 15, 25), p.color(25, 20, 35), inter);
              p.stroke(c);
              p.line(0, i, p.width, i);
            }
            
            // Update node states
            state.nodes.forEach(node => {
              const distance = p.dist(p.mouseX, p.mouseY, node.x, node.y);
              node.isHovered = distance < node.radius * 1.5 && !state.draggedNode;
              
              // Handle return animation
              if (node.isReturning && !node.isDragging) {
                const elapsed = p.millis() - node.returnStartTime;
                const duration = 800;
                const progress = Math.min(elapsed / duration, 1);
                const easedProgress = 1 - Math.pow(1 - progress, 3);
                
                node.x = p.lerp(node.x, node.originalX, easedProgress);
                node.y = p.lerp(node.y, node.originalY, easedProgress);
                
                if (progress >= 1) {
                  node.isReturning = false;
                  node.x = node.originalX;
                  node.y = node.originalY;
                }
              }
            });
            
            // Draw brain (schwa)
            const schwaNode = state.nodes.find(n => n.phoneme.category === 'schwa')!;
            if (schwaNode) {
              drawBrain(schwaNode.x, schwaNode.y, schwaNode.radius, schwaNode.isHovered);
            }
            
            // Draw neurons
            state.nodes.forEach(node => {
              if (node.phoneme.category !== 'schwa') {
                drawNeuron(node);
              }
            });
            
            // Draw schwa text over brain
            if (schwaNode) {
              p.fill(255, 255, 255);
              p.noStroke();
              p.textAlign(p.CENTER, p.CENTER);
              p.textSize(schwaNode.isHovered ? 20 : 16);
              p.textStyle(p.BOLD);
              p.text('ə', schwaNode.x, schwaNode.y - 10);
              p.textSize(schwaNode.isHovered ? 14 : 11);
              p.textStyle(p.NORMAL);
              p.text('Schwa', schwaNode.x, schwaNode.y + 15);
            }
            
            // Draw title
            p.fill(255, 255, 255, 220);
            p.textAlign(p.CENTER, p.TOP);
            p.textSize(Math.min(28, p.width / 25));
            p.textStyle(p.BOLD);
            p.text('The Sound Brain Map', state.centerX, 25);
            
            p.textSize(Math.min(16, p.width / 40));
            p.textStyle(p.NORMAL);
            p.fill(200, 200, 255, 180);
            p.text('Vowel and vowel-like sounds of English', state.centerX, 55);
          };

          // Mouse interaction handlers
          p.mousePressed = () => {
            for (const node of state.nodes) {
              const distance = p.dist(p.mouseX, p.mouseY, node.x, node.y);
              if (distance < node.radius * 1.5) {
                state.draggedNode = node;
                node.isDragging = true;
                node.isReturning = false;
                state.dragOffset.x = p.mouseX - node.x;
                state.dragOffset.y = p.mouseY - node.y;
                break;
              }
            }
          };

          p.mouseDragged = () => {
            if (state.draggedNode) {
              state.draggedNode.x = p.mouseX - state.dragOffset.x;
              state.draggedNode.y = p.mouseY - state.dragOffset.y;
            }
          };

          p.mouseReleased = () => {
            if (state.draggedNode) {
              // Start return animation
              state.draggedNode.isDragging = false;
              state.draggedNode.isReturning = true;
              state.draggedNode.returnStartTime = p.millis();
              state.draggedNode = null;
            }
          };

          p.mouseClicked = () => {
            // Only trigger click if not dragging
            if (!state.draggedNode) {
              for (const node of state.nodes) {
                const distance = p.dist(p.mouseX, p.mouseY, node.x, node.y);
                if (distance < node.radius * 1.5) {
                  playAudio(node.phoneme.audioFile);
                  break;
                }
              }
            }
          };

          p.windowResized = () => {
            p.resizeCanvas(p.windowWidth, p.windowHeight);
            state.centerX = p.width / 2;
            state.centerY = p.height / 2;
            state.maxRadius = Math.min(p.width, p.height) * 0.3;
            
            // Reposition schwa
            const schwaNode = state.nodes.find(n => n.phoneme.category === 'schwa')!;
            if (schwaNode) {
              schwaNode.x = schwaNode.originalX = state.centerX;
              schwaNode.y = schwaNode.originalY = state.centerY;
            }
            
            // Reposition other nodes using exact positions
            state.nodes.forEach(node => {
              if (node.phoneme.category !== 'schwa') {
                const position = calculateExactPosition(node.phoneme);
                node.x = node.originalX = position.x;
                node.y = node.originalY = position.y;
              }
            });
          };
        };

        p5InstanceRef.current = new p5(sketch);
      } catch (error) {
        console.error('Failed to load p5.js:', error);
      }
    };

    loadP5AndSketch();

    return () => {
      if (p5InstanceRef.current) {
        p5InstanceRef.current.remove();
        p5InstanceRef.current = null;
      }
    };
  }, [playAudio]);

  return (
    <div 
      ref={sketchRef} 
      className={`w-full h-full ${className}`}
      style={{ position: 'fixed', top: 0, left: 0, zIndex: 0 }}
    />
  );
}
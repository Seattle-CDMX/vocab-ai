#!/usr/bin/env python3
"""
Google Voice Personas Generator
Fetches premium Google Cloud TTS voices and generates culturally appropriate personas
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Any
import random
from datetime import datetime

from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv(".env.local")

OUTPUT_FILE = Path(__file__).parent / "google_voice_personas.json"

class VoicePersonasGenerator:
    def __init__(self):
        # Initialize Google Cloud TTS client
        # Note: Requires GOOGLE_APPLICATION_CREDENTIALS environment variable
        self.client = texttospeech.TextToSpeechClient()
        self.used_names = set()
        
    def fetch_premium_voices(self) -> List[Dict]:
        """Fetch all premium voices from Google Cloud TTS"""
        try:
            # List all available voices
            voices = self.client.list_voices()
            
            premium_voices = []
            for voice in voices.voices:
                voice_name = voice.name
                language_code = voice.language_codes[0] if voice.language_codes else ""
                
                # Filter for premium voices (Neural2, WaveNet, Chirp3-HD, Studio)
                if any(premium in voice_name for premium in ['Neural2', 'Wavenet', 'Chirp3-HD', 'Studio']):
                    premium_voices.append({
                        'name': voice_name,
                        'language_code': language_code,
                        'language_name': self.get_language_name(language_code),
                        'gender': voice.ssml_gender.name,
                        'voice_type': self.get_voice_type(voice_name)
                    })
            
            return premium_voices
            
        except Exception as e:
            print(f"Error fetching voices from Google Cloud: {e}")
            print("Falling back to hardcoded premium voices list...")
            return self.get_fallback_premium_voices()
    
    def get_fallback_premium_voices(self) -> List[Dict]:
        """Fallback premium voices if API is not available"""
        return [
            # English (US)
            {'name': 'en-US-Neural2-A', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-C', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-D', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-E', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-F', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-G', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-H', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-I', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Neural2-J', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-US-Wavenet-A', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            {'name': 'en-US-Wavenet-B', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            {'name': 'en-US-Wavenet-C', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'en-US-Studio-O', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'FEMALE', 'voice_type': 'Studio'},
            {'name': 'en-US-Studio-Q', 'language_code': 'en-US', 'language_name': 'English (US)', 'gender': 'MALE', 'voice_type': 'Studio'},
            
            # English (UK)
            {'name': 'en-GB-Neural2-A', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-GB-Neural2-B', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-GB-Neural2-C', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-GB-Neural2-D', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-GB-Wavenet-A', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'en-GB-Wavenet-B', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            {'name': 'en-GB-Studio-B', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'MALE', 'voice_type': 'Studio'},
            {'name': 'en-GB-Studio-C', 'language_code': 'en-GB', 'language_name': 'English (UK)', 'gender': 'FEMALE', 'voice_type': 'Studio'},
            
            # English (AU)
            {'name': 'en-AU-Neural2-A', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-AU-Neural2-B', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-AU-Neural2-C', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'en-AU-Neural2-D', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'en-AU-Wavenet-A', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'en-AU-Wavenet-B', 'language_code': 'en-AU', 'language_name': 'English (Australia)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            
            # French
            {'name': 'fr-FR-Neural2-A', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'fr-FR-Neural2-B', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'fr-FR-Neural2-C', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'fr-FR-Neural2-D', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'fr-FR-Wavenet-A', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'fr-FR-Wavenet-B', 'language_code': 'fr-FR', 'language_name': 'French (France)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            
            # German
            {'name': 'de-DE-Neural2-A', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'de-DE-Neural2-B', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'de-DE-Neural2-C', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'de-DE-Neural2-D', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'de-DE-Wavenet-A', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'de-DE-Wavenet-B', 'language_code': 'de-DE', 'language_name': 'German (Germany)', 'voice_type': 'WaveNet', 'gender': 'MALE'},
            
            # Spanish
            {'name': 'es-ES-Neural2-A', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'es-ES-Neural2-B', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'es-ES-Neural2-C', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'es-ES-Neural2-D', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'es-ES-Wavenet-B', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            {'name': 'es-ES-Wavenet-C', 'language_code': 'es-ES', 'language_name': 'Spanish (Spain)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            
            # Italian
            {'name': 'it-IT-Neural2-A', 'language_code': 'it-IT', 'language_name': 'Italian (Italy)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'it-IT-Neural2-C', 'language_code': 'it-IT', 'language_name': 'Italian (Italy)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'it-IT-Wavenet-A', 'language_code': 'it-IT', 'language_name': 'Italian (Italy)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'it-IT-Wavenet-C', 'language_code': 'it-IT', 'language_name': 'Italian (Italy)', 'gender': 'MALE', 'voice_type': 'WaveNet'},
            
            # Japanese
            {'name': 'ja-JP-Neural2-B', 'language_code': 'ja-JP', 'language_name': 'Japanese (Japan)', 'gender': 'FEMALE', 'voice_type': 'Neural2'},
            {'name': 'ja-JP-Neural2-C', 'language_code': 'ja-JP', 'language_name': 'Japanese (Japan)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'ja-JP-Neural2-D', 'language_code': 'ja-JP', 'language_name': 'Japanese (Japan)', 'gender': 'MALE', 'voice_type': 'Neural2'},
            {'name': 'ja-JP-Wavenet-A', 'language_code': 'ja-JP', 'language_name': 'Japanese (Japan)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
            {'name': 'ja-JP-Wavenet-B', 'language_code': 'ja-JP', 'language_name': 'Japanese (Japan)', 'gender': 'FEMALE', 'voice_type': 'WaveNet'},
        ]
    
    def get_language_name(self, language_code: str) -> str:
        """Get human-readable language name from language code"""
        language_map = {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)', 
            'en-AU': 'English (Australia)',
            'en-IN': 'English (India)',
            'fr-FR': 'French (France)',
            'fr-CA': 'French (Canada)',
            'de-DE': 'German (Germany)',
            'es-ES': 'Spanish (Spain)',
            'es-US': 'Spanish (US)',
            'it-IT': 'Italian (Italy)',
            'pt-BR': 'Portuguese (Brazil)',
            'pt-PT': 'Portuguese (Portugal)',
            'ja-JP': 'Japanese (Japan)',
            'ko-KR': 'Korean (South Korea)',
            'zh-CN': 'Chinese (Mandarin, China)',
            'zh-TW': 'Chinese (Taiwan)',
            'hi-IN': 'Hindi (India)',
            'ar-XA': 'Arabic',
            'ru-RU': 'Russian (Russia)',
            'nl-NL': 'Dutch (Netherlands)',
            'sv-SE': 'Swedish (Sweden)',
            'no-NO': 'Norwegian (Norway)',
            'da-DK': 'Danish (Denmark)',
            'pl-PL': 'Polish (Poland)',
        }
        return language_map.get(language_code, language_code)
    
    def get_voice_type(self, voice_name: str) -> str:
        """Extract voice type from voice name"""
        if 'Chirp3-HD' in voice_name:
            return 'Chirp3-HD'
        elif 'Neural2' in voice_name:
            return 'Neural2'
        elif 'Wavenet' in voice_name:
            return 'WaveNet'
        elif 'Studio' in voice_name:
            return 'Studio'
        else:
            return 'Standard'
    
    def generate_persona_name(self, language_code: str, gender: str) -> str:
        """Generate culturally appropriate names"""
        
        # Names database organized by language and gender
        names_db = {
            'en-US': {
                'MALE': ['Dr. Williams', 'Mr. Johnson', 'Prof. Davis', 'Mr. Anderson', 'Dr. Brown', 'Mr. Wilson', 'Prof. Miller', 'Dr. Garcia', 'Mr. Martinez', 'Prof. Robinson'],
                'FEMALE': ['Dr. Smith', 'Ms. Johnson', 'Prof. Williams', 'Ms. Brown', 'Dr. Jones', 'Ms. Garcia', 'Prof. Miller', 'Dr. Davis', 'Ms. Rodriguez', 'Prof. Wilson']
            },
            'en-GB': {
                'MALE': ['Mr. Thompson', 'Dr. Clarke', 'Prof. Hamilton', 'Mr. Richardson', 'Dr. Fletcher', 'Mr. Ashworth', 'Prof. Pemberton', 'Dr. Whitfield', 'Mr. Sterling', 'Prof. Blackwood'],
                'FEMALE': ['Ms. Bennett', 'Dr. Hamilton', 'Prof. Clarke', 'Ms. Crawford', 'Dr. Whitmore', 'Ms. Ashford', 'Prof. Sterling', 'Dr. Pemberton', 'Ms. Blackwell', 'Prof. Richardson']
            },
            'en-AU': {
                'MALE': ['Mr. Campbell', 'Dr. Mitchell', 'Prof. Henderson', 'Mr. O\'Brien', 'Dr. Sullivan', 'Mr. Fraser', 'Prof. McKenzie', 'Dr. Morrison', 'Mr. Stewart', 'Prof. Cameron'],
                'FEMALE': ['Ms. Mitchell', 'Dr. Campbell', 'Prof. Henderson', 'Ms. Fraser', 'Dr. Sullivan', 'Ms. McKenzie', 'Prof. Morrison', 'Dr. Stewart', 'Ms. Cameron', 'Prof. O\'Brien']
            },
            'fr-FR': {
                'MALE': ['M. Dubois', 'Dr. Laurent', 'Prof. Moreau', 'M. Bernard', 'Dr. Petit', 'M. Durand', 'Prof. Leroy', 'Dr. Moreau', 'M. Simon', 'Prof. Michel'],
                'FEMALE': ['Mme. Laurent', 'Dr. Dubois', 'Prof. Moreau', 'Mme. Bernard', 'Dr. Martin', 'Mme. Petit', 'Prof. Durand', 'Dr. Leroy', 'Mme. Robert', 'Prof. Simon']
            },
            'de-DE': {
                'MALE': ['Herr Schmidt', 'Dr. Mueller', 'Prof. Weber', 'Herr Wagner', 'Dr. Becker', 'Herr Schulz', 'Prof. Hoffmann', 'Dr. Schaefer', 'Herr Koch', 'Prof. Richter'],
                'FEMALE': ['Frau Mueller', 'Dr. Schmidt', 'Prof. Weber', 'Frau Wagner', 'Dr. Fischer', 'Frau Becker', 'Prof. Schulz', 'Dr. Hoffmann', 'Frau Meyer', 'Prof. Koch']
            },
            'es-ES': {
                'MALE': ['Sr. Garcia', 'Dr. Rodriguez', 'Prof. Martinez', 'Sr. Lopez', 'Dr. Gonzalez', 'Sr. Perez', 'Prof. Sanchez', 'Dr. Ramirez', 'Sr. Cruz', 'Prof. Flores'],
                'FEMALE': ['Sra. Rodriguez', 'Dra. Garcia', 'Prof. Martinez', 'Sra. Lopez', 'Dra. Gonzalez', 'Sra. Perez', 'Prof. Sanchez', 'Dra. Ramirez', 'Sra. Torres', 'Prof. Flores']
            },
            'it-IT': {
                'MALE': ['Sig. Rossi', 'Dr. Ferrari', 'Prof. Esposito', 'Sig. Bianchi', 'Dr. Romano', 'Sig. Gallo', 'Prof. Conti', 'Dr. Bruno', 'Sig. Ricci', 'Prof. Barbieri'],
                'FEMALE': ['Sig.ra Ferrari', 'Dott.ssa Rossi', 'Prof. Esposito', 'Sig.ra Bianchi', 'Dott.ssa Romano', 'Sig.ra Gallo', 'Prof. Conti', 'Dott.ssa Bruno', 'Sig.ra Ricci', 'Prof. Barbieri']
            },
            'ja-JP': {
                'MALE': ['田中先生', '佐藤博士', '鈴木教授', '高橋先生', '伊藤博士', '渡辺教授', '中村先生', '小林博士', '加藤教授', '吉田先生'],
                'FEMALE': ['佐藤先生', '田中博士', '鈴木教授', '高橋先生', '伊藤博士', '渡辺教授', '中村先生', '小林博士', '加藤教授', '吉田先生']
            }
        }
        
        # Default to English US if language not found
        lang_key = language_code if language_code in names_db else 'en-US'
        available_names = names_db[lang_key][gender]
        
        # Filter out already used names
        unused_names = [name for name in available_names if name not in self.used_names]
        
        if not unused_names:
            # If all names are used, reset and reuse
            self.used_names.clear()
            unused_names = available_names
        
        selected_name = random.choice(unused_names)
        self.used_names.add(selected_name)
        
        return selected_name
    
    def generate_persona(self, voice: Dict) -> Dict:
        """Generate a complete persona for a voice"""
        name = self.generate_persona_name(voice['language_code'], voice['gender'])
        
        # Teaching styles and personalities
        teaching_styles = [
            "patient and encouraging", "direct and practical", "enthusiastic and energetic",
            "calm and methodical", "friendly and conversational", "professional and precise",
            "warm and supportive", "clear and structured", "engaging and interactive", "thorough and detailed"
        ]
        
        expertise_areas = [
            "business communication", "workplace interactions", "professional presentations",
            "email writing", "meeting facilitation", "client relations", "team management",
            "project coordination", "cross-cultural communication", "negotiation skills"
        ]
        
        return {
            'voice': voice,
            'persona': {
                'name': name,
                'teaching_style': random.choice(teaching_styles),
                'expertise': random.choice(expertise_areas),
                'personality_traits': random.sample([
                    'patient', 'encouraging', 'professional', 'friendly', 'knowledgeable',
                    'supportive', 'clear', 'engaging', 'thorough', 'practical', 'warm', 'direct'
                ], 3),
                'preferred_contexts': random.sample([
                    'meetings', 'presentations', 'emails', 'phone calls', 'interviews',
                    'networking events', 'team discussions', 'client meetings', 'workshops', 'training sessions'
                ], 3)
            }
        }
    
    def generate_all_personas(self):
        """Generate personas for all premium voices"""
        print("Fetching premium voices from Google Cloud TTS...")
        premium_voices = self.fetch_premium_voices()
        
        print(f"Found {len(premium_voices)} premium voices")
        print("Generating personas...")
        
        personas = []
        for voice in premium_voices:
            persona = self.generate_persona(voice)
            personas.append(persona)
            print(f"Generated persona: {persona['persona']['name']} ({voice['name']})")
        
        # Create output structure
        output = {
            'generated_at': str(datetime.now().isoformat()),
            'total_personas': len(personas),
            'personas': personas,
            'metadata': {
                'generator': 'generate_voice_personas.py',
                'version': '1.0.0',
                'description': 'Google Cloud TTS premium voice personas for vocabulary learning'
            }
        }
        
        # Save to file
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nPersona generation complete!")
        print(f"Output saved to: {OUTPUT_FILE}")
        print(f"Total personas generated: {len(personas)}")
        
        return OUTPUT_FILE

def main():
    """Main entry point"""
    generator = VoicePersonasGenerator()
    generator.generate_all_personas()

if __name__ == "__main__":
    main()
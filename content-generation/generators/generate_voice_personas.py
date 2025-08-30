#!/usr/bin/env python3
"""
Google Voice Personas Generator
Fetches premium Google Cloud TTS voices and generates culturally appropriate personas
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "agent" / "src"))
from config.credentials import parse_google_credentials

load_dotenv(Path(__file__).parent.parent.parent / "agent" / ".env.local")

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "google_voice_personas.json"


class VoicePersonasGenerator:
    def __init__(self):
        # Initialize Google Cloud TTS client with same credentials as agent
        credentials_info = parse_google_credentials()
        if not credentials_info:
            raise ValueError(
                "Google Cloud credentials not found. Set GOOGLE_APPLICATION_CREDENTIALS_B64 or GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable."
            )

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        self.used_names = set()
        print(
            "✅ Successfully initialized Google Cloud TTS client with agent credentials"
        )

    def fetch_premium_voices(self) -> List[Dict]:
        """Fetch only CHIRP 3 HD voices from Google Cloud TTS - FAIL FAST if API fails"""
        print("🔍 Fetching real CHIRP 3 HD voices from Google Cloud TTS API...")

        try:
            # List all available voices
            voices = self.client.list_voices()

            chirp3_hd_voices = []
            for voice in voices.voices:
                voice_name = voice.name
                language_code = voice.language_codes[0] if voice.language_codes else ""

                # Filter for CHIRP 3 HD voices only
                if "Chirp3-HD" in voice_name:
                    chirp3_hd_voices.append(
                        {
                            "name": voice_name,
                            "language_code": language_code,
                            "language_name": self.get_language_name(language_code),
                            "gender": voice.ssml_gender.name,
                            "voice_type": self.get_voice_type(voice_name),
                        }
                    )

            if not chirp3_hd_voices:
                raise ValueError(
                    "No CHIRP 3 HD voices found in Google Cloud TTS API response"
                )

            print(
                f"✅ Successfully fetched {len(chirp3_hd_voices)} real CHIRP 3 HD voices from Google Cloud"
            )
            return chirp3_hd_voices

        except Exception as e:
            print(f"❌ FAILED to fetch voices from Google Cloud TTS API: {e}")
            print(
                "🚫 NO FALLBACK - Script requires real voice data from Google Cloud API"
            )
            print("💡 Check your Google Cloud credentials and API access")
            raise RuntimeError(
                f"Cannot generate voice personas without real Google Cloud TTS voices. API Error: {e}"
            )

    def get_language_name(self, language_code: str) -> str:
        """Get human-readable language name from language code"""
        language_map = {
            "en-US": "English (US)",
            "en-GB": "English (UK)",
            "en-AU": "English (Australia)",
            "en-IN": "English (India)",
            "fr-FR": "French (France)",
            "fr-CA": "French (Canada)",
            "de-DE": "German (Germany)",
            "es-ES": "Spanish (Spain)",
            "es-US": "Spanish (US)",
            "it-IT": "Italian (Italy)",
            "pt-BR": "Portuguese (Brazil)",
            "pt-PT": "Portuguese (Portugal)",
            "ja-JP": "Japanese (Japan)",
            "ko-KR": "Korean (South Korea)",
            "zh-CN": "Chinese (Mandarin, China)",
            "zh-TW": "Chinese (Taiwan)",
            "hi-IN": "Hindi (India)",
            "ar-XA": "Arabic",
            "ru-RU": "Russian (Russia)",
            "nl-NL": "Dutch (Netherlands)",
            "sv-SE": "Swedish (Sweden)",
            "no-NO": "Norwegian (Norway)",
            "da-DK": "Danish (Denmark)",
            "pl-PL": "Polish (Poland)",
        }
        return language_map.get(language_code, language_code)

    def get_voice_type(self, voice_name: str) -> str:
        """Extract voice type from voice name"""
        if "Chirp3-HD" in voice_name:
            return "Chirp3-HD"
        elif "Neural2" in voice_name:
            return "Neural2"
        elif "Wavenet" in voice_name:
            return "WaveNet"
        elif "Studio" in voice_name:
            return "Studio"
        else:
            return "Standard"

    def generate_persona_name(self, language_code: str, gender: str) -> str:
        """Generate culturally appropriate names"""

        # Names database organized by language and gender
        names_db = {
            "en-US": {
                "MALE": [
                    "Dr. Williams",
                    "Mr. Johnson",
                    "Prof. Davis",
                    "Mr. Anderson",
                    "Dr. Brown",
                    "Mr. Wilson",
                    "Prof. Miller",
                    "Dr. Garcia",
                    "Mr. Martinez",
                    "Prof. Robinson",
                ],
                "FEMALE": [
                    "Dr. Smith",
                    "Ms. Johnson",
                    "Prof. Williams",
                    "Ms. Brown",
                    "Dr. Jones",
                    "Ms. Garcia",
                    "Prof. Miller",
                    "Dr. Davis",
                    "Ms. Rodriguez",
                    "Prof. Wilson",
                ],
            },
            "en-GB": {
                "MALE": [
                    "Mr. Thompson",
                    "Dr. Clarke",
                    "Prof. Hamilton",
                    "Mr. Richardson",
                    "Dr. Fletcher",
                    "Mr. Ashworth",
                    "Prof. Pemberton",
                    "Dr. Whitfield",
                    "Mr. Sterling",
                    "Prof. Blackwood",
                ],
                "FEMALE": [
                    "Ms. Bennett",
                    "Dr. Hamilton",
                    "Prof. Clarke",
                    "Ms. Crawford",
                    "Dr. Whitmore",
                    "Ms. Ashford",
                    "Prof. Sterling",
                    "Dr. Pemberton",
                    "Ms. Blackwell",
                    "Prof. Richardson",
                ],
            },
            "en-AU": {
                "MALE": [
                    "Mr. Campbell",
                    "Dr. Mitchell",
                    "Prof. Henderson",
                    "Mr. O'Brien",
                    "Dr. Sullivan",
                    "Mr. Fraser",
                    "Prof. McKenzie",
                    "Dr. Morrison",
                    "Mr. Stewart",
                    "Prof. Cameron",
                ],
                "FEMALE": [
                    "Ms. Mitchell",
                    "Dr. Campbell",
                    "Prof. Henderson",
                    "Ms. Fraser",
                    "Dr. Sullivan",
                    "Ms. McKenzie",
                    "Prof. Morrison",
                    "Dr. Stewart",
                    "Ms. Cameron",
                    "Prof. O'Brien",
                ],
            },
            "fr-FR": {
                "MALE": [
                    "M. Dubois",
                    "Dr. Laurent",
                    "Prof. Moreau",
                    "M. Bernard",
                    "Dr. Petit",
                    "M. Durand",
                    "Prof. Leroy",
                    "Dr. Moreau",
                    "M. Simon",
                    "Prof. Michel",
                ],
                "FEMALE": [
                    "Mme. Laurent",
                    "Dr. Dubois",
                    "Prof. Moreau",
                    "Mme. Bernard",
                    "Dr. Martin",
                    "Mme. Petit",
                    "Prof. Durand",
                    "Dr. Leroy",
                    "Mme. Robert",
                    "Prof. Simon",
                ],
            },
            "de-DE": {
                "MALE": [
                    "Herr Schmidt",
                    "Dr. Mueller",
                    "Prof. Weber",
                    "Herr Wagner",
                    "Dr. Becker",
                    "Herr Schulz",
                    "Prof. Hoffmann",
                    "Dr. Schaefer",
                    "Herr Koch",
                    "Prof. Richter",
                ],
                "FEMALE": [
                    "Frau Mueller",
                    "Dr. Schmidt",
                    "Prof. Weber",
                    "Frau Wagner",
                    "Dr. Fischer",
                    "Frau Becker",
                    "Prof. Schulz",
                    "Dr. Hoffmann",
                    "Frau Meyer",
                    "Prof. Koch",
                ],
            },
            "es-ES": {
                "MALE": [
                    "Sr. Garcia",
                    "Dr. Rodriguez",
                    "Prof. Martinez",
                    "Sr. Lopez",
                    "Dr. Gonzalez",
                    "Sr. Perez",
                    "Prof. Sanchez",
                    "Dr. Ramirez",
                    "Sr. Cruz",
                    "Prof. Flores",
                ],
                "FEMALE": [
                    "Sra. Rodriguez",
                    "Dra. Garcia",
                    "Prof. Martinez",
                    "Sra. Lopez",
                    "Dra. Gonzalez",
                    "Sra. Perez",
                    "Prof. Sanchez",
                    "Dra. Ramirez",
                    "Sra. Torres",
                    "Prof. Flores",
                ],
            },
            "it-IT": {
                "MALE": [
                    "Sig. Rossi",
                    "Dr. Ferrari",
                    "Prof. Esposito",
                    "Sig. Bianchi",
                    "Dr. Romano",
                    "Sig. Gallo",
                    "Prof. Conti",
                    "Dr. Bruno",
                    "Sig. Ricci",
                    "Prof. Barbieri",
                ],
                "FEMALE": [
                    "Sig.ra Ferrari",
                    "Dott.ssa Rossi",
                    "Prof. Esposito",
                    "Sig.ra Bianchi",
                    "Dott.ssa Romano",
                    "Sig.ra Gallo",
                    "Prof. Conti",
                    "Dott.ssa Bruno",
                    "Sig.ra Ricci",
                    "Prof. Barbieri",
                ],
            },
            "ja-JP": {
                "MALE": [
                    "田中先生",
                    "佐藤博士",
                    "鈴木教授",
                    "高橋先生",
                    "伊藤博士",
                    "渡辺教授",
                    "中村先生",
                    "小林博士",
                    "加藤教授",
                    "吉田先生",
                ],
                "FEMALE": [
                    "佐藤先生",
                    "田中博士",
                    "鈴木教授",
                    "高橋先生",
                    "伊藤博士",
                    "渡辺教授",
                    "中村先生",
                    "小林博士",
                    "加藤教授",
                    "吉田先生",
                ],
            },
        }

        # Default to English US if language not found
        lang_key = language_code if language_code in names_db else "en-US"
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
        name = self.generate_persona_name(voice["language_code"], voice["gender"])

        # Teaching styles and personalities
        teaching_styles = [
            "patient and encouraging",
            "direct and practical",
            "enthusiastic and energetic",
            "calm and methodical",
            "friendly and conversational",
            "professional and precise",
            "warm and supportive",
            "clear and structured",
            "engaging and interactive",
            "thorough and detailed",
        ]

        expertise_areas = [
            "business communication",
            "workplace interactions",
            "professional presentations",
            "email writing",
            "meeting facilitation",
            "client relations",
            "team management",
            "project coordination",
            "cross-cultural communication",
            "negotiation skills",
        ]

        return {
            "voice": voice,
            "persona": {
                "name": name,
                "teaching_style": random.choice(teaching_styles),
                "expertise": random.choice(expertise_areas),
                "personality_traits": random.sample(
                    [
                        "patient",
                        "encouraging",
                        "professional",
                        "friendly",
                        "knowledgeable",
                        "supportive",
                        "clear",
                        "engaging",
                        "thorough",
                        "practical",
                        "warm",
                        "direct",
                    ],
                    3,
                ),
                "preferred_contexts": random.sample(
                    [
                        "meetings",
                        "presentations",
                        "emails",
                        "phone calls",
                        "interviews",
                        "networking events",
                        "team discussions",
                        "client meetings",
                        "workshops",
                        "training sessions",
                    ],
                    3,
                ),
            },
        }

    def generate_all_personas(self):
        """Generate personas for all CHIRP 3 HD voices"""
        print("Fetching CHIRP 3 HD voices from Google Cloud TTS...")
        chirp3_hd_voices = self.fetch_premium_voices()

        print(f"Found {len(chirp3_hd_voices)} CHIRP 3 HD voices")
        print("Generating personas...")

        personas = []
        for voice in chirp3_hd_voices:
            persona = self.generate_persona(voice)
            personas.append(persona)
            print(f"Generated persona: {persona['persona']['name']} ({voice['name']})")

        # Create output structure
        output = {
            "generated_at": str(datetime.now().isoformat()),
            "total_personas": len(personas),
            "personas": personas,
            "metadata": {
                "generator": "generate_voice_personas.py",
                "version": "2.0.0",
                "description": "Google Cloud TTS CHIRP 3 HD voice personas for vocabulary learning",
            },
        }

        # Save to file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print("\nPersona generation complete!")
        print(f"Output saved to: {OUTPUT_FILE}")
        print(f"Total personas generated: {len(personas)}")

        return OUTPUT_FILE


def main():
    """Main entry point"""
    generator = VoicePersonasGenerator()
    generator.generate_all_personas()


if __name__ == "__main__":
    main()

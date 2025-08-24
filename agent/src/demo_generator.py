#!/usr/bin/env python3
"""
Demo Generator for Voice Card Types
Generates enhanced voice card data with OpenAI-powered content and images
"""

import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import base64
import httpx
import random

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(".env.local")

PHRASAL_VERBS_PATH = Path(__file__).parent.parent.parent / "app" / "public" / "phrasal_verbs.json"
VOICE_PERSONAS_PATH = Path(__file__).parent / "google_voice_personas.json"
OUTPUT_DIR = Path(__file__).parent.parent / "generated_data"
IMAGES_DIR = OUTPUT_DIR / "images"

class DemoGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        self.voice_personas = self.load_voice_personas()
        self.used_personas = set()
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        OUTPUT_DIR.mkdir(exist_ok=True)
        IMAGES_DIR.mkdir(exist_ok=True)
        
    def load_phrasal_verbs(self) -> List[Dict]:
        """Load phrasal verbs from JSON file"""
        with open(PHRASAL_VERBS_PATH, 'r') as f:
            data = json.load(f)
        return data
    
    def load_voice_personas(self) -> List[Dict]:
        """Load voice personas from JSON file"""
        try:
            with open(VOICE_PERSONAS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['personas']
        except Exception as e:
            print(f"Error loading voice personas: {e}")
            return []
    
    def get_random_persona(self) -> Dict:
        """Get a random voice persona, avoiding recently used ones"""
        if not self.voice_personas:
            return self.get_fallback_persona()
        
        # Filter out recently used personas
        available_personas = [
            p for p in self.voice_personas 
            if p['persona']['name'] not in self.used_personas
        ]
        
        # If all personas are used, reset and reuse
        if not available_personas:
            self.used_personas.clear()
            available_personas = self.voice_personas
        
        selected_persona = random.choice(available_personas)
        self.used_personas.add(selected_persona['persona']['name'])
        
        return selected_persona
    
    def get_fallback_persona(self) -> Dict:
        """Fallback persona if voice personas file is not available"""
        return {
            'voice': {
                'name': 'en-US-Neural2-A',
                'language_code': 'en-US',
                'language_name': 'English (US)',
                'gender': 'MALE',
                'voice_type': 'Neural2'
            },
            'persona': {
                'name': 'Mr. Johnson',
                'teaching_style': 'professional and clear',
                'expertise': 'business communication',
                'personality_traits': ['professional', 'clear', 'supportive'],
                'preferred_contexts': ['meetings', 'presentations', 'emails']
            }
        }
    
    def get_selected_verbs(self, verbs: List[Dict]) -> List[Dict]:
        """Get first 5 and last 5 phrasal verbs"""
        # For testing: just use the first verb
        if os.getenv("DEMO_TEST_MODE") == "1":
            return verbs[:1]
        
        first_five = verbs[:5]
        last_five = verbs[-5:]
        return first_five + last_five
    
    async def generate_workplace_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Generate a workplace-appropriate scenario using OpenAI"""
        prompt = f"""
        You are {persona['persona']['name']}, a {persona['persona']['expertise']} expert. Create a realistic workplace scenario for practicing the phrasal verb "{verb['verb']}".
        
        The phrasal verb means: {verb['senses'][0]['definition']}
        Example usage: {verb['senses'][0]['examples'][0] if verb['senses'][0]['examples'] else 'N/A'}
        
        Generate a JSON response with:
        {{
            "scenario_title": "Brief title for the scenario",
            "character_name": "Professional character name (e.g., Ms. Chen, Dr. Smith)",
            "character_role": "Their role (e.g., Project Manager, Department Head)",
            "situation": "Detailed workplace situation where this phrasal verb would naturally be used",
            "conversation_starter": "How the character begins the conversation",
            "expected_usage": "How the learner should use the phrasal verb in response",
            "difficulty": "beginner/intermediate/advanced",
            "business_context": "Specific business context (meeting, email discussion, presentation, etc.)",
            "learning_tip": "A helpful tip for remembering this phrasal verb",
            "alternative_scenarios": ["2-3 other workplace situations where this verb applies"]
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a business English expert creating workplace learning scenarios."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating scenario for {verb['verb']}: {e}")
            return self.get_fallback_scenario(verb, persona)
    
    def get_fallback_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Fallback scenario if API fails"""
        return {
            "scenario_title": f"Practice {verb['verb']}",
            "character_name": persona['persona']['name'],
            "character_role": "Team Lead",
            "situation": f"A workplace situation to practice {verb['verb']}",
            "conversation_starter": "Let's discuss this matter.",
            "expected_usage": f"Use '{verb['verb']}' naturally in conversation",
            "difficulty": "intermediate",
            "business_context": "Team meeting",
            "learning_tip": f"Remember: {verb['senses'][0]['definition']}",
            "alternative_scenarios": ["Meeting discussion", "Email follow-up", "Project planning"]
        }
    
    async def generate_image(self, verb: Dict, scenario: Dict) -> str:
        """Generate an image using DALL-E and save locally"""
        image_prompt = f"""
        Professional office setting showing a {scenario['business_context']} scenario.
        Include a diverse business professional in a modern workplace.
        Style: Clean, modern, corporate photography.
        No text or words in the image.
        Convey the action of "{verb['verb']}" through body language and context.
        """
        
        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Download and save image locally
            image_filename = f"{verb['verb'].lower().replace(' ', '-')}-{self.timestamp}.png"
            image_path = IMAGES_DIR / image_filename
            
            async with httpx.AsyncClient() as client:
                img_response = await client.get(image_url)
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
            
            return f"/generated_data/images/{image_filename}"
            
        except Exception as e:
            print(f"Error generating image for {verb['verb']}: {e}")
            return "/placeholder.svg"
    
    async def generate_native_explain_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Generate a native explanation scenario using OpenAI"""
        primary_sense = verb['senses'][0]
        
        prompt = f"""
        You are {persona['persona']['name']}, a {persona['persona']['expertise']} expert with a {persona['persona']['teaching_style']} teaching style.
        
        Create an educational explanation for the phrasal verb "{verb['verb']}" that focuses on helping learners understand its meaning and usage.
        
        The phrasal verb has these senses:
        {json.dumps(verb['senses'], indent=2)}
        
        Generate a JSON response with:
        {{
            "explanation_approach": "How you'll explain this phrasal verb (e.g., 'step-by-step breakdown', 'real-world examples', 'comparative method')",
            "main_definition": "Clear, simple definition of the primary meaning",
            "key_teaching_points": ["3-4 important points to remember about this phrasal verb"],
            "usage_examples": ["3 practical examples showing different contexts"],
            "common_mistakes": ["2-3 common errors learners make with this phrasal verb"],
            "memory_tips": ["2 helpful tips for remembering this phrasal verb"],
            "difficulty_level": "beginner/intermediate/advanced",
            "teaching_personality": "Brief description of your teaching personality based on your traits"
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are {persona['persona']['name']}, an expert language teacher with these traits: {', '.join(persona['persona']['personality_traits'])}. Your teaching style is {persona['persona']['teaching_style']}."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating native explain scenario for {verb['verb']}: {e}")
            return self.get_fallback_native_explain(verb, persona)
    
    def get_fallback_native_explain(self, verb: Dict, persona: Dict) -> Dict:
        """Fallback native explain scenario if API fails"""
        primary_sense = verb['senses'][0]
        return {
            "explanation_approach": "step-by-step breakdown",
            "main_definition": primary_sense['definition'],
            "key_teaching_points": [f"'{verb['verb']}' means {primary_sense['definition']}", "Can be used in both formal and informal contexts", "Pay attention to preposition usage"],
            "usage_examples": primary_sense['examples'][:3] if len(primary_sense['examples']) >= 3 else primary_sense['examples'] + [f"Let me {verb['verb'].lower()} this matter."],
            "common_mistakes": ["Using the wrong preposition", "Confusing with similar phrasal verbs"],
            "memory_tips": [f"Think of {verb['verb'].lower()} as {primary_sense['definition'].lower()}", "Practice with real workplace situations"],
            "difficulty_level": "intermediate",
            "teaching_personality": persona['persona']['teaching_style']
        }
    
    async def create_native_explain_card(self, verb: Dict) -> Dict:
        """Create a native explain card with voice persona"""
        persona = self.get_random_persona()
        scenario = await self.generate_native_explain_scenario(verb, persona)
        
        # Use the first sense as the primary definition
        primary_sense = verb['senses'][0]
        
        native_explain_card = {
            "id": f"native-explain-{verb['verb'].lower().replace(' ', '-')}-{self.timestamp}",
            "type": "native_explain",
            "title": f"Explain: {verb['verb']}",
            "difficulty": scenario['difficulty_level'],
            "targetPhrasalVerb": {
                "verb": verb['verb'],
                "senses": verb['senses']
            },
            "teachingScenario": {
                "teacher": persona['persona']['name'],
                "approach": scenario['explanation_approach'],
                "mainDefinition": scenario['main_definition'],
                "keyTeachingPoints": scenario['key_teaching_points'],
                "usageExamples": scenario['usage_examples'],
                "commonMistakes": scenario['common_mistakes'],
                "memoryTips": scenario['memory_tips'],
                "teachingPersonality": scenario['teaching_personality']
            },
            "voicePersona": persona,
            "metadata": {
                "originalId": verb['id'],
                "generatedAt": self.timestamp,
                "cardType": "native_explain"
            }
        }
        
        return native_explain_card
    
    async def create_situation_card(self, verb: Dict) -> Dict:
        """Create a situation/context card with voice persona"""
        persona = self.get_random_persona()
        scenario = await self.generate_workplace_scenario(verb, persona)
        image_path = await self.generate_image(verb, scenario)
        
        # Use the first sense as the primary definition
        primary_sense = verb['senses'][0]
        
        situation_card = {
            "id": f"context-{verb['verb'].lower().replace(' ', '-')}-{self.timestamp}",
            "type": "context",
            "title": f"In-Context — {verb['verb']}",
            "difficulty": scenario['difficulty'],
            "contextText": f"You're speaking with {scenario['character_name']}, {scenario['character_role']}. {scenario['situation']}",
            "imageUrl": image_path,
            "ctaText": f"Talk to {scenario['character_name']}",
            "scenario": {
                "character": scenario['character_name'],
                "role": scenario['character_role'],
                "situation": scenario['situation'],
                "phrasalVerb": verb['verb'].lower(),
                "contextText": scenario['situation'],
                "conversationStarter": scenario['conversation_starter'],
                "expectedUsage": scenario['expected_usage'],
                "businessContext": scenario['business_context'],
                "maxTurns": 5
            },
            "targetPhrasalVerb": {
                "verb": verb['verb'],
                "definition": primary_sense['definition'],
                "confidence": primary_sense['confidencePercent'],
                "examples": primary_sense['examples'] + [scenario['expected_usage']],
                "learningTip": scenario['learning_tip'],
                "alternativeScenarios": scenario['alternative_scenarios']
            },
            "voicePersona": persona,
            "metadata": {
                "originalId": verb['id'],
                "generatedAt": self.timestamp,
                "allSenses": verb['senses'],
                "cardType": "context"
            }
        }
        
        return situation_card
    
    async def generate_all_cards(self):
        """Main generation process"""
        print(f"Starting demo generation at {self.timestamp}")
        
        # Load and select verbs
        all_verbs = self.load_phrasal_verbs()
        selected_verbs = self.get_selected_verbs(all_verbs)
        
        print(f"Processing {len(selected_verbs)} phrasal verbs...")
        
        # Generate voice cards (1 native explain + 1 situation per verb = 20 total)
        voice_cards = []
        for i, verb in enumerate(selected_verbs):
            print(f"Processing {i+1}/{len(selected_verbs)}: {verb['verb']}")
            
            # Create 1 native explain card
            print(f"  - Generating native explain card...")
            native_card = await self.create_native_explain_card(verb)
            voice_cards.append(native_card)
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
            # Create 1 situation card
            print(f"  - Generating situation card...")
            situation_card = await self.create_situation_card(verb)
            voice_cards.append(situation_card)
            
            # Small delay to avoid rate limits
            await asyncio.sleep(1)
        
        # Separate cards by type for statistics
        native_explains = [card for card in voice_cards if card['type'] == 'native_explain']
        situations = [card for card in voice_cards if card['type'] == 'context']
        
        # Create output structure
        output = {
            "generatedAt": self.timestamp,
            "totalCards": len(voice_cards),
            "nativeExplainCards": len(native_explains),
            "situationCards": len(situations),
            "voiceCardTypes": voice_cards,
            "metadata": {
                "generator": "demo_generator.py",
                "version": "2.0.0",
                "phrasalVerbsProcessed": [v['verb'] for v in selected_verbs],
                "voicePersonasUsed": len(self.used_personas),
                "cardStructure": "1 native_explain + 1 context per phrasal verb"
            }
        }
        
        # Save to timestamped file
        output_file = OUTPUT_DIR / f"voice-cards-{self.timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nGeneration complete!")
        print(f"Total cards generated: {len(voice_cards)}")
        print(f"  - Native explain cards: {len(native_explains)}")
        print(f"  - Situation cards: {len(situations)}")
        print(f"Voice personas used: {len(self.used_personas)}")
        print(f"Output saved to: {output_file}")
        print(f"Images saved to: {IMAGES_DIR}")
        
        # Also create a symlink to latest for easy access
        latest_link = OUTPUT_DIR / "voice-cards-latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(output_file.name)
        print(f"Latest symlink created: {latest_link}")
        
        return output_file

async def main():
    """Main entry point"""
    generator = DemoGenerator()
    await generator.generate_all_cards()

if __name__ == "__main__":
    asyncio.run(main())
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

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(".env.local")

PHRASAL_VERBS_PATH = Path(__file__).parent.parent.parent / "app" / "public" / "phrasal_verbs.json"
OUTPUT_DIR = Path(__file__).parent.parent / "generated_data"
IMAGES_DIR = OUTPUT_DIR / "images"

class DemoGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
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
    
    def get_selected_verbs(self, verbs: List[Dict]) -> List[Dict]:
        """Get first 5 and last 5 phrasal verbs"""
        first_five = verbs[:5]
        last_five = verbs[-5:]
        return first_five + last_five
    
    async def generate_workplace_scenario(self, verb: Dict) -> Dict:
        """Generate a workplace-appropriate scenario using OpenAI"""
        prompt = f"""
        Create a realistic workplace scenario for practicing the phrasal verb "{verb['verb']}".
        
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
            return self.get_fallback_scenario(verb)
    
    def get_fallback_scenario(self, verb: Dict) -> Dict:
        """Fallback scenario if API fails"""
        return {
            "scenario_title": f"Practice {verb['verb']}",
            "character_name": "Mr. Johnson",
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
    
    async def create_voice_card(self, verb: Dict, index: int) -> Dict:
        """Create an enhanced voice card with all data"""
        scenario = await self.generate_workplace_scenario(verb)
        image_path = await self.generate_image(verb, scenario)
        
        # Use the first sense as the primary definition
        primary_sense = verb['senses'][0]
        
        voice_card = {
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
            "metadata": {
                "originalId": verb['id'],
                "generatedAt": self.timestamp,
                "allSenses": verb['senses']
            }
        }
        
        return voice_card
    
    async def generate_all_cards(self):
        """Main generation process"""
        print(f"Starting demo generation at {self.timestamp}")
        
        # Load and select verbs
        all_verbs = self.load_phrasal_verbs()
        selected_verbs = self.get_selected_verbs(all_verbs)
        
        print(f"Processing {len(selected_verbs)} phrasal verbs...")
        
        # Generate voice cards
        voice_cards = []
        for i, verb in enumerate(selected_verbs):
            print(f"Processing {i+1}/{len(selected_verbs)}: {verb['verb']}")
            card = await self.create_voice_card(verb, i)
            voice_cards.append(card)
            
            # Small delay to avoid rate limits
            await asyncio.sleep(1)
        
        # Create output structure
        output = {
            "generatedAt": self.timestamp,
            "totalCards": len(voice_cards),
            "voiceCardTypes": voice_cards,
            "metadata": {
                "generator": "demo_generator.py",
                "version": "1.0.0",
                "phrasalVerbsProcessed": [v['verb'] for v in selected_verbs]
            }
        }
        
        # Save to timestamped file
        output_file = OUTPUT_DIR / f"voice-cards-{self.timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nGeneration complete!")
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
#!/usr/bin/env python3
"""
Demo Generator for Voice Card Types
Generates enhanced voice card data with OpenAI-powered content and images
"""

import asyncio
import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(".env.local")

PHRASAL_VERBS_PATH = Path(__file__).parent.parent.parent / "app" / "public" / "phrasal_verbs.json"
VOICE_PERSONAS_PATH = Path(__file__).parent / "google_voice_personas.json"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "app" / "generated_data"
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
        with open(PHRASAL_VERBS_PATH) as f:
            data = json.load(f)
        return data

    def load_voice_personas(self) -> List[Dict]:
        """Load voice personas from JSON file"""
        try:
            with open(VOICE_PERSONAS_PATH, encoding='utf-8') as f:
                data = json.load(f)
            return data['personas']
        except Exception as e:
            print(f"Error loading voice personas: {e}")
            return []

    def get_culturally_appropriate_name(self, language_code: str, gender: str) -> Dict:
        """Get culturally appropriate name based on voice language and gender"""
        name_mappings = {
            'en-US': {'MALE': ['Mr. Johnson', 'Mr. Smith', 'Mr. Davis', 'Mr. Williams'], 'FEMALE': ['Ms. Johnson', 'Ms. Smith', 'Ms. Davis', 'Ms. Williams']},
            'en-GB': {'MALE': ['Mr. Thompson', 'Mr. Clarke', 'Mr. Brown', 'Mr. Wilson'], 'FEMALE': ['Ms. Thompson', 'Ms. Clarke', 'Ms. Brown', 'Ms. Wilson']},
            'en-AU': {'MALE': ['Mr. Anderson', 'Mr. Campbell', 'Mr. Fraser', 'Mr. Stewart'], 'FEMALE': ['Ms. Anderson', 'Ms. Campbell', 'Ms. Fraser', 'Ms. Stewart']},
            'en-CA': {'MALE': ['Mr. MacDonald', 'Mr. Taylor', 'Mr. Miller', 'Mr. White'], 'FEMALE': ['Ms. MacDonald', 'Ms. Taylor', 'Ms. Miller', 'Ms. White']},
            'en-IN': {'MALE': ['Mr. Sharma', 'Mr. Patel', 'Mr. Singh', 'Mr. Kumar'], 'FEMALE': ['Ms. Sharma', 'Ms. Patel', 'Ms. Singh', 'Ms. Kumar']},
            'es-ES': {'MALE': ['Mr. García', 'Mr. Martínez', 'Mr. López', 'Mr. Rodríguez'], 'FEMALE': ['Ms. García', 'Ms. Martínez', 'Ms. López', 'Ms. Rodríguez']},
            'es-MX': {'MALE': ['Mr. Hernández', 'Mr. González', 'Mr. Pérez', 'Mr. Sánchez'], 'FEMALE': ['Ms. Hernández', 'Ms. González', 'Ms. Pérez', 'Ms. Sánchez']},
            'es-US': {'MALE': ['Mr. Hernández', 'Mr. González', 'Mr. Pérez', 'Mr. Sánchez'], 'FEMALE': ['Ms. Hernández', 'Ms. González', 'Ms. Pérez', 'Ms. Sánchez']},
            'fr-FR': {'MALE': ['Mr. Dubois', 'Mr. Moreau', 'Mr. Laurent', 'Mr. Simon'], 'FEMALE': ['Ms. Dubois', 'Ms. Moreau', 'Ms. Laurent', 'Ms. Simon']},
            'de-DE': {'MALE': ['Mr. Müller', 'Mr. Schmidt', 'Mr. Weber', 'Mr. Fischer'], 'FEMALE': ['Ms. Müller', 'Ms. Schmidt', 'Ms. Weber', 'Ms. Fischer']},
            'it-IT': {'MALE': ['Mr. Rossi', 'Mr. Bianchi', 'Mr. Ferrari', 'Mr. Romano'], 'FEMALE': ['Ms. Rossi', 'Ms. Bianchi', 'Ms. Ferrari', 'Ms. Romano']},
            'pt-BR': {'MALE': ['Mr. Silva', 'Mr. Santos', 'Mr. Oliveira', 'Mr. Pereira'], 'FEMALE': ['Ms. Silva', 'Ms. Santos', 'Ms. Oliveira', 'Ms. Pereira']},
            'ja-JP': {'MALE': ['Mr. Tanaka', 'Mr. Sato', 'Mr. Suzuki', 'Mr. Takahashi'], 'FEMALE': ['Ms. Tanaka', 'Ms. Sato', 'Ms. Suzuki', 'Ms. Takahashi']},
            'ko-KR': {'MALE': ['Mr. Kim', 'Mr. Lee', 'Mr. Park', 'Mr. Choi'], 'FEMALE': ['Ms. Kim', 'Ms. Lee', 'Ms. Park', 'Ms. Choi']},
            'zh-CN': {'MALE': ['Mr. Wang', 'Mr. Li', 'Mr. Zhang', 'Mr. Liu'], 'FEMALE': ['Ms. Wang', 'Ms. Li', 'Ms. Zhang', 'Ms. Liu']},
            'cmn-CN': {'MALE': ['Mr. Wang', 'Mr. Li', 'Mr. Zhang', 'Mr. Liu'], 'FEMALE': ['Ms. Wang', 'Ms. Li', 'Ms. Zhang', 'Ms. Liu']},
            'hi-IN': {'MALE': ['Mr. Sharma', 'Mr. Patel', 'Mr. Singh', 'Mr. Kumar'], 'FEMALE': ['Ms. Sharma', 'Ms. Patel', 'Ms. Singh', 'Ms. Kumar']},
            'ar-XA': {'MALE': ['Mr. Ahmed', 'Mr. Mohammed', 'Mr. Ali', 'Mr. Hassan'], 'FEMALE': ['Ms. Fatima', 'Ms. Aisha', 'Ms. Zeinab', 'Ms. Mariam']},
            'ru-RU': {'MALE': ['Mr. Petrov', 'Mr. Ivanov', 'Mr. Smirnov', 'Mr. Kuznetsov'], 'FEMALE': ['Ms. Petrova', 'Ms. Ivanova', 'Ms. Smirnova', 'Ms. Kuznetsova']},
            'nl-NL': {'MALE': ['Mr. de Jong', 'Mr. Jansen', 'Mr. de Vries', 'Mr. van den Berg'], 'FEMALE': ['Ms. de Jong', 'Ms. Jansen', 'Ms. de Vries', 'Ms. van den Berg']},
            'sv-SE': {'MALE': ['Mr. Andersson', 'Mr. Johansson', 'Mr. Karlsson', 'Mr. Nilsson'], 'FEMALE': ['Ms. Andersson', 'Ms. Johansson', 'Ms. Karlsson', 'Ms. Nilsson']},
            'th-TH': {'MALE': ['Mr. Somchai', 'Mr. Somsak', 'Mr. Sombat', 'Mr. Somkid'], 'FEMALE': ['Ms. Siriporn', 'Ms. Somjit', 'Ms. Sirikul', 'Ms. Somying']},
            'vi-VN': {'MALE': ['Mr. Nguyen', 'Mr. Tran', 'Mr. Le', 'Mr. Pham'], 'FEMALE': ['Ms. Nguyen', 'Ms. Tran', 'Ms. Le', 'Ms. Pham']},
            'bn-IN': {'MALE': ['Mr. Rahman', 'Mr. Ahmed', 'Mr. Khan', 'Mr. Islam'], 'FEMALE': ['Ms. Rahman', 'Ms. Ahmed', 'Ms. Khan', 'Ms. Islam']},
            'ur-IN': {'MALE': ['Mr. Khan', 'Mr. Ahmed', 'Mr. Ali', 'Mr. Shah'], 'FEMALE': ['Ms. Khan', 'Ms. Ahmed', 'Ms. Ali', 'Ms. Shah']},
            'ml-IN': {'MALE': ['Mr. Nair', 'Mr. Pillai', 'Mr. Menon', 'Mr. Kumar'], 'FEMALE': ['Ms. Nair', 'Ms. Pillai', 'Ms. Menon', 'Ms. Kumar']},
            'uk-UA': {'MALE': ['Mr. Kovalenko', 'Mr. Bondarenko', 'Mr. Tkachenko', 'Mr. Koval'], 'FEMALE': ['Ms. Kovalenko', 'Ms. Bondarenko', 'Ms. Tkachenko', 'Ms. Koval']},
        }
        
        # Use base language code if specific variant not found
        base_lang = language_code.split('-')[0]
        if language_code not in name_mappings and base_lang == 'en':
            language_code = 'en-US'
        elif language_code not in name_mappings:
            for key in name_mappings.keys():
                if key.startswith(base_lang):
                    language_code = key
                    break
            else:
                language_code = 'en-US'  # fallback
        
        names = name_mappings.get(language_code, name_mappings['en-US'])
        available_names = names.get(gender, names['MALE'])
        
        # Track used names to avoid repeats
        if not hasattr(self, 'used_names'):
            self.used_names = set()
        
        # Filter out used names
        unused_names = [name for name in available_names if name not in self.used_names]
        if not unused_names:
            self.used_names.clear()  # Reset if all used
            unused_names = available_names
            
        selected_name = random.choice(unused_names)
        self.used_names.add(selected_name)
        
        return {
            'name': selected_name,
            'cultural_background': self.get_cultural_background(language_code),
            'language_region': language_code
        }

    def get_cultural_background(self, language_code: str) -> str:
        """Get cultural background description for image generation"""
        backgrounds = {
            'en-US': 'American professional',
            'en-GB': 'British professional', 
            'en-AU': 'Australian professional',
            'en-CA': 'Canadian professional',
            'en-IN': 'Indian professional',
            'es-ES': 'Spanish professional',
            'es-MX': 'Mexican professional', 
            'fr-FR': 'French professional',
            'de-DE': 'German professional',
            'it-IT': 'Italian professional',
            'pt-BR': 'Brazilian professional',
            'ja-JP': 'Japanese professional',
            'ko-KR': 'Korean professional',
            'zh-CN': 'Chinese professional',
            'cmn-CN': 'Chinese professional',
            'hi-IN': 'Indian professional',
            'ar-XA': 'Middle Eastern professional',
            'ru-RU': 'Russian professional',
            'nl-NL': 'Dutch professional',
            'sv-SE': 'Swedish professional',
        }
        return backgrounds.get(language_code, 'international professional')

    def get_random_persona(self) -> Dict:
        """Get a random voice persona with culturally appropriate name"""
        if not self.voice_personas:
            return self.get_fallback_persona()

        # Filter out recently used personas
        available_personas = [
            p for p in self.voice_personas
            if p['voice']['name'] not in self.used_personas
        ]

        # If all personas are used, reset and reuse
        if not available_personas:
            self.used_personas.clear()
            available_personas = self.voice_personas

        selected_persona = random.choice(available_personas)
        self.used_personas.add(selected_persona['voice']['name'])

        # Generate culturally appropriate name
        name_info = self.get_culturally_appropriate_name(
            selected_persona['voice']['language_code'],
            selected_persona['voice']['gender']
        )
        
        # Update persona with culturally appropriate name
        selected_persona['persona']['name'] = name_info['name']
        selected_persona['cultural_info'] = {
            'background': name_info['cultural_background'],
            'language_region': name_info['language_region']
        }

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
        """Get first 3 and last 3 phrasal verbs for faster testing"""
        # For testing: just use the first verb
        if os.getenv("DEMO_TEST_MODE") == "1":
            return verbs[:1]

        # Use first 3 and last 3 for faster generation (6 total cards)
        first_three = verbs[:3]
        last_three = verbs[-3:]
        return first_three + last_three

    async def generate_workplace_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Generate a workplace-appropriate scenario using OpenAI"""
        prompt = f"""
        You are {persona['persona']['name']}, a {persona['persona']['expertise']} expert. Create a realistic workplace scenario for practicing the phrasal verb "{verb['verb']}".
        
        The phrasal verb means: {verb['senses'][0]['definition']}
        Example usage: {verb['senses'][0]['examples'][0] if verb['senses'][0]['examples'] else 'N/A'}
        
        Generate a JSON response with:
        {{
            "scenario_title": "Brief title for the scenario",
            "character_name": "{persona['persona']['name']}",
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

            scenario_data = json.loads(response.choices[0].message.content)
            # Ensure character name matches persona name exactly
            scenario_data["character_name"] = persona['persona']['name']
            return scenario_data
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

    async def generate_image(self, verb: Dict, scenario: Dict, persona: Dict) -> str:
        """Generate an image using DALL-E and save locally with cultural coherence"""
        cultural_background = persona.get('cultural_info', {}).get('background', 'international professional')
        character_name = scenario['character_name']
        
        image_prompt = f"""
        Friendly, approachable office setting with a {scenario['business_context']} scenario.
        Feature a {cultural_background} as the main character ({character_name}) in the center of the image,
        with warm smile and engaging expression in a bright, modern workplace.
        The main character should clearly represent their cultural background in appearance.
        Include other diverse business professionals collaborating in the background.
        Style: Natural, bright, welcoming photography with soft lighting and warm colors.
        Show people being collaborative, friendly, and approachable - not overly formal or stiff.
        Capture a sense of positive energy and learning atmosphere.
        No text or words in the image.
        Convey the action of "{verb['verb']}" through natural body language and friendly interaction.
        Focus on the {cultural_background} as the primary subject.
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

            # Download and save image locally (simple filename, overwrite existing)
            image_filename = f"{verb['verb'].lower().replace(' ', '-')}.png"
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
            "id": f"native-explain-{verb['verb'].lower().replace(' ', '-')}",
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
        image_path = await self.generate_image(verb, scenario, persona)

        # Use the first sense as the primary definition
        primary_sense = verb['senses'][0]

        situation_card = {
            "id": f"context-{verb['verb'].lower().replace(' ', '-')}",
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

    async def generate_card_batch(self, verb: Dict, verb_index: int, total_verbs: int) -> List[Dict]:
        """Generate both cards for a single verb in parallel"""
        print(f"Processing {verb_index+1}/{total_verbs}: {verb['verb']}")
        
        # Create both cards concurrently
        native_task = asyncio.create_task(self.create_native_explain_card(verb))
        situation_task = asyncio.create_task(self.create_situation_card(verb))
        
        # Wait for both cards to complete
        native_card, situation_card = await asyncio.gather(native_task, situation_task)
        
        print(f"  ✅ Completed both cards for {verb['verb']}")
        return [native_card, situation_card]

    async def generate_all_cards(self):
        """Main generation process with parallel processing"""
        print(f"Starting parallel demo generation at {self.timestamp}")

        # Load and select verbs
        all_verbs = self.load_phrasal_verbs()
        selected_verbs = self.get_selected_verbs(all_verbs)

        print(f"Processing {len(selected_verbs)} phrasal verbs in parallel...")

        # Create tasks for all verbs (each task generates 2 cards)
        batch_tasks = [
            self.generate_card_batch(verb, i, len(selected_verbs)) 
            for i, verb in enumerate(selected_verbs)
        ]

        # Execute all batches concurrently with a semaphore to control concurrency
        semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent verb processing batches
        
        async def limited_batch(task):
            async with semaphore:
                return await task
        
        print("🚀 Generating all cards concurrently...")
        batch_results = await asyncio.gather(*[limited_batch(task) for task in batch_tasks])
        
        # Flatten results
        voice_cards = []
        for batch in batch_results:
            voice_cards.extend(batch)

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
                "version": "2.1.0",
                "phrasalVerbsProcessed": [v['verb'] for v in selected_verbs],
                "voicePersonasUsed": len(self.used_personas),
                "cardStructure": "1 native_explain + 1 context per phrasal verb",
                "generationMode": "parallel"
            }
        }

        # Save to simple filename (overwrite existing)
        output_file = OUTPUT_DIR / "voice-cards.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print("\n🎉 Parallel generation complete!")
        print(f"Total cards generated: {len(voice_cards)}")
        print(f"  - Native explain cards: {len(native_explains)}")
        print(f"  - Situation cards: {len(situations)}")
        print(f"Voice personas used: {len(self.used_personas)}")
        print(f"Output saved to: {output_file}")
        print(f"Images saved to: {IMAGES_DIR}")

        return output_file

async def main():
    """Main entry point"""
    generator = DemoGenerator()
    await generator.generate_all_cards()

if __name__ == "__main__":
    asyncio.run(main())

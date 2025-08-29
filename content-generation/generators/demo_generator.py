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

load_dotenv(Path(__file__).parent.parent / ".env.local")

VOICE_PERSONAS_PATH = Path(__file__).parent.parent / "data" / "google_voice_personas.json"
PHRASAL_VERBS_CONFIG_PATH = Path(__file__).parent.parent / "data" / "phrasal_verbs_config.json"


class DemoGenerator:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        self.output_dir = Path(__file__).parent.parent / "output" / f"voice-cards-{self.timestamp}"
        self.images_dir = self.output_dir / "images"
        self.voice_personas = self.load_voice_personas()
        self.used_personas = set()
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(exist_ok=True)

    def load_phrasal_verbs_from_config(self) -> List[Dict]:
        """Load phrasal verbs from configuration file"""
        try:
            with open(PHRASAL_VERBS_CONFIG_PATH) as f:
                config = json.load(f)
            
            active_set = config.get("active_set", "basic_workplace")
            phrasal_verbs = config["phrasal_verb_sets"][active_set]
            
            print(f"📚 Loaded phrasal verb set: '{active_set}' ({len(phrasal_verbs)} verbs)")
            return phrasal_verbs
            
        except Exception as e:
            print(f"⚠️  Error loading phrasal verbs config: {e}")
            print("🔄 Falling back to hardcoded verbs")
            return self.get_fallback_phrasal_verbs()
    
    def get_fallback_phrasal_verbs(self) -> List[Dict]:
        """Fallback phrasal verbs if config file fails"""
        return [
            {
                "lexicalItem": "GO ON",
                "difficulty": "intermediate",
                "senses": [
                    {
                        "senseNumber": 1,
                        "definition": "Happen, take place",
                        "examples": [
                            "There is a debate going on right now between the two parties."
                        ]
                    }
                ]
            }
        ]

    def load_voice_personas(self) -> List[Dict]:
        """Load voice personas from JSON file"""
        try:
            with open(VOICE_PERSONAS_PATH, encoding="utf-8") as f:
                data = json.load(f)
            return data["personas"]
        except Exception as e:
            print(f"Error loading voice personas: {e}")
            return []

    def get_culturally_appropriate_name(self, language_code: str, gender: str) -> Dict:
        """Get culturally appropriate name based on voice language and gender"""
        name_mappings = {
            "en-US": {
                "MALE": ["Mr. Johnson", "Mr. Smith", "Mr. Davis", "Mr. Williams"],
                "FEMALE": ["Ms. Johnson", "Ms. Smith", "Ms. Davis", "Ms. Williams"],
            },
            "en-GB": {
                "MALE": ["Mr. Thompson", "Mr. Clarke", "Mr. Brown", "Mr. Wilson"],
                "FEMALE": ["Ms. Thompson", "Ms. Clarke", "Ms. Brown", "Ms. Wilson"],
            },
            "en-AU": {
                "MALE": ["Mr. Anderson", "Mr. Campbell", "Mr. Fraser", "Mr. Stewart"],
                "FEMALE": ["Ms. Anderson", "Ms. Campbell", "Ms. Fraser", "Ms. Stewart"],
            },
            "en-CA": {
                "MALE": ["Mr. MacDonald", "Mr. Taylor", "Mr. Miller", "Mr. White"],
                "FEMALE": ["Ms. MacDonald", "Ms. Taylor", "Ms. Miller", "Ms. White"],
            },
            "en-IN": {
                "MALE": ["Mr. Sharma", "Mr. Patel", "Mr. Singh", "Mr. Kumar"],
                "FEMALE": ["Ms. Sharma", "Ms. Patel", "Ms. Singh", "Ms. Kumar"],
            },
            "es-ES": {
                "MALE": ["Mr. García", "Mr. Martínez", "Mr. López", "Mr. Rodríguez"],
                "FEMALE": ["Ms. García", "Ms. Martínez", "Ms. López", "Ms. Rodríguez"],
            },
            "es-MX": {
                "MALE": ["Mr. Hernández", "Mr. González", "Mr. Pérez", "Mr. Sánchez"],
                "FEMALE": ["Ms. Hernández", "Ms. González", "Ms. Pérez", "Ms. Sánchez"],
            },
            "es-US": {
                "MALE": ["Mr. Hernández", "Mr. González", "Mr. Pérez", "Mr. Sánchez"],
                "FEMALE": ["Ms. Hernández", "Ms. González", "Ms. Pérez", "Ms. Sánchez"],
            },
            "fr-FR": {
                "MALE": ["Mr. Dubois", "Mr. Moreau", "Mr. Laurent", "Mr. Simon"],
                "FEMALE": ["Ms. Dubois", "Ms. Moreau", "Ms. Laurent", "Ms. Simon"],
            },
            "de-DE": {
                "MALE": ["Mr. Müller", "Mr. Schmidt", "Mr. Weber", "Mr. Fischer"],
                "FEMALE": ["Ms. Müller", "Ms. Schmidt", "Ms. Weber", "Ms. Fischer"],
            },
            "it-IT": {
                "MALE": ["Mr. Rossi", "Mr. Bianchi", "Mr. Ferrari", "Mr. Romano"],
                "FEMALE": ["Ms. Rossi", "Ms. Bianchi", "Ms. Ferrari", "Ms. Romano"],
            },
            "pt-BR": {
                "MALE": ["Mr. Silva", "Mr. Santos", "Mr. Oliveira", "Mr. Pereira"],
                "FEMALE": ["Ms. Silva", "Ms. Santos", "Ms. Oliveira", "Ms. Pereira"],
            },
            "ja-JP": {
                "MALE": ["Mr. Tanaka", "Mr. Sato", "Mr. Suzuki", "Mr. Takahashi"],
                "FEMALE": ["Ms. Tanaka", "Ms. Sato", "Ms. Suzuki", "Ms. Takahashi"],
            },
            "ko-KR": {
                "MALE": ["Mr. Kim", "Mr. Lee", "Mr. Park", "Mr. Choi"],
                "FEMALE": ["Ms. Kim", "Ms. Lee", "Ms. Park", "Ms. Choi"],
            },
            "zh-CN": {
                "MALE": ["Mr. Wang", "Mr. Li", "Mr. Zhang", "Mr. Liu"],
                "FEMALE": ["Ms. Wang", "Ms. Li", "Ms. Zhang", "Ms. Liu"],
            },
            "cmn-CN": {
                "MALE": ["Mr. Wang", "Mr. Li", "Mr. Zhang", "Mr. Liu"],
                "FEMALE": ["Ms. Wang", "Ms. Li", "Ms. Zhang", "Ms. Liu"],
            },
            "hi-IN": {
                "MALE": ["Mr. Sharma", "Mr. Patel", "Mr. Singh", "Mr. Kumar"],
                "FEMALE": ["Ms. Sharma", "Ms. Patel", "Ms. Singh", "Ms. Kumar"],
            },
            "ar-XA": {
                "MALE": ["Mr. Ahmed", "Mr. Mohammed", "Mr. Ali", "Mr. Hassan"],
                "FEMALE": ["Ms. Fatima", "Ms. Aisha", "Ms. Zeinab", "Ms. Mariam"],
            },
            "ru-RU": {
                "MALE": ["Mr. Petrov", "Mr. Ivanov", "Mr. Smirnov", "Mr. Kuznetsov"],
                "FEMALE": [
                    "Ms. Petrova",
                    "Ms. Ivanova",
                    "Ms. Smirnova",
                    "Ms. Kuznetsova",
                ],
            },
            "nl-NL": {
                "MALE": [
                    "Mr. de Jong",
                    "Mr. Jansen",
                    "Mr. de Vries",
                    "Mr. van den Berg",
                ],
                "FEMALE": [
                    "Ms. de Jong",
                    "Ms. Jansen",
                    "Ms. de Vries",
                    "Ms. van den Berg",
                ],
            },
            "sv-SE": {
                "MALE": [
                    "Mr. Andersson",
                    "Mr. Johansson",
                    "Mr. Karlsson",
                    "Mr. Nilsson",
                ],
                "FEMALE": [
                    "Ms. Andersson",
                    "Ms. Johansson",
                    "Ms. Karlsson",
                    "Ms. Nilsson",
                ],
            },
            "th-TH": {
                "MALE": ["Mr. Somchai", "Mr. Somsak", "Mr. Sombat", "Mr. Somkid"],
                "FEMALE": ["Ms. Siriporn", "Ms. Somjit", "Ms. Sirikul", "Ms. Somying"],
            },
            "vi-VN": {
                "MALE": ["Mr. Nguyen", "Mr. Tran", "Mr. Le", "Mr. Pham"],
                "FEMALE": ["Ms. Nguyen", "Ms. Tran", "Ms. Le", "Ms. Pham"],
            },
            "bn-IN": {
                "MALE": ["Mr. Rahman", "Mr. Ahmed", "Mr. Khan", "Mr. Islam"],
                "FEMALE": ["Ms. Rahman", "Ms. Ahmed", "Ms. Khan", "Ms. Islam"],
            },
            "ur-IN": {
                "MALE": ["Mr. Khan", "Mr. Ahmed", "Mr. Ali", "Mr. Shah"],
                "FEMALE": ["Ms. Khan", "Ms. Ahmed", "Ms. Ali", "Ms. Shah"],
            },
            "ml-IN": {
                "MALE": ["Mr. Nair", "Mr. Pillai", "Mr. Menon", "Mr. Kumar"],
                "FEMALE": ["Ms. Nair", "Ms. Pillai", "Ms. Menon", "Ms. Kumar"],
            },
            "uk-UA": {
                "MALE": [
                    "Mr. Kovalenko",
                    "Mr. Bondarenko",
                    "Mr. Tkachenko",
                    "Mr. Koval",
                ],
                "FEMALE": [
                    "Ms. Kovalenko",
                    "Ms. Bondarenko",
                    "Ms. Tkachenko",
                    "Ms. Koval",
                ],
            },
        }

        # Use base language code if specific variant not found
        base_lang = language_code.split("-")[0]
        if language_code not in name_mappings and base_lang == "en":
            language_code = "en-US"
        elif language_code not in name_mappings:
            for key in name_mappings.keys():
                if key.startswith(base_lang):
                    language_code = key
                    break
            else:
                language_code = "en-US"  # fallback

        names = name_mappings.get(language_code, name_mappings["en-US"])
        available_names = names.get(gender, names["MALE"])

        # Track used names to avoid repeats
        if not hasattr(self, "used_names"):
            self.used_names = set()

        # Filter out used names
        unused_names = [name for name in available_names if name not in self.used_names]
        if not unused_names:
            self.used_names.clear()  # Reset if all used
            unused_names = available_names

        selected_name = random.choice(unused_names)
        self.used_names.add(selected_name)

        return {
            "name": selected_name,
            "cultural_background": self.get_cultural_background(language_code),
            "language_region": language_code,
        }

    def get_cultural_background(self, language_code: str) -> str:
        """Get cultural background description for image generation"""
        backgrounds = {
            "en-US": "American professional",
            "en-GB": "British professional",
            "en-AU": "Australian professional",
            "en-CA": "Canadian professional",
            "en-IN": "Indian professional",
            "es-ES": "Spanish professional",
            "es-MX": "Mexican professional",
            "fr-FR": "French professional",
            "de-DE": "German professional",
            "it-IT": "Italian professional",
            "pt-BR": "Brazilian professional",
            "ja-JP": "Japanese professional",
            "ko-KR": "Korean professional",
            "zh-CN": "Chinese professional",
            "cmn-CN": "Chinese professional",
            "hi-IN": "Indian professional",
            "ar-XA": "Middle Eastern professional",
            "ru-RU": "Russian professional",
            "nl-NL": "Dutch professional",
            "sv-SE": "Swedish professional",
        }
        return backgrounds.get(language_code, "international professional")

    def get_random_persona(self) -> Dict:
        """Get a random voice persona with culturally appropriate name"""
        if not self.voice_personas:
            return self.get_fallback_persona()

        # Filter out recently used personas
        available_personas = [
            p
            for p in self.voice_personas
            if p["voice"]["name"] not in self.used_personas
        ]

        # If all personas are used, reset and reuse
        if not available_personas:
            self.used_personas.clear()
            available_personas = self.voice_personas

        selected_persona = random.choice(available_personas)
        self.used_personas.add(selected_persona["voice"]["name"])

        # Generate culturally appropriate name
        name_info = self.get_culturally_appropriate_name(
            selected_persona["voice"]["language_code"],
            selected_persona["voice"]["gender"],
        )

        # Update persona with culturally appropriate name and tech role
        selected_persona["persona"]["name"] = name_info["name"]
        selected_persona["cultural_info"] = {
            "background": name_info["cultural_background"],
            "language_region": name_info["language_region"],
        }
        
        # Override with tech-focused expertise and contexts
        tech_roles = [
            "Senior Software Engineer",
            "Tech Lead", 
            "Engineering Manager",
            "CTO",
            "Product Manager",
            "DevOps Engineer",
            "QA Lead",
            "Scrum Master"
        ]
        
        tech_teaching_styles = [
            "direct and technical",
            "collaborative and supportive", 
            "methodical and thorough",
            "practical and hands-on",
            "clear and structured",
            "patient and encouraging"
        ]
        
        tech_contexts = [
            "code reviews",
            "sprint planning", 
            "technical discussions",
            "architecture meetings",
            "deployment planning",
            "incident response",
            "team retrospectives"
        ]
        
        tech_traits = [
            "analytical",
            "problem-solving",
            "collaborative", 
            "detail-oriented",
            "supportive",
            "technical",
            "clear",
            "patient"
        ]
        
        selected_persona["persona"]["expertise"] = random.choice(tech_roles)
        selected_persona["persona"]["teaching_style"] = random.choice(tech_teaching_styles)
        selected_persona["persona"]["personality_traits"] = random.sample(tech_traits, 3)
        selected_persona["persona"]["preferred_contexts"] = random.sample(tech_contexts, 3)

        return selected_persona

    def get_fallback_persona(self) -> Dict:
        """Fallback persona if voice personas file is not available"""
        return {
            "voice": {
                "name": "en-US-Neural2-A",
                "language_code": "en-US",
                "language_name": "English (US)",
                "gender": "MALE",
                "voice_type": "Neural2",
            },
            "persona": {
                "name": "Mr. Johnson",
                "teaching_style": "clear and structured",
                "expertise": "Senior Software Engineer",
                "personality_traits": ["technical", "clear", "supportive"],
                "preferred_contexts": ["code reviews", "technical discussions", "sprint planning"],
            },
        }

    def get_selected_verbs(self, verbs: List[Dict]) -> List[Dict]:
        """Get all hardcoded phrasal verbs or just one for testing"""
        # For testing: just use the first verb
        if os.getenv("DEMO_TEST_MODE") == "1":
            return verbs[:1]

        # Use all hardcoded verbs
        return verbs

    async def generate_workplace_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Generate a developer-focused workplace scenario using OpenAI"""
        cefr_level = verb["difficulty"]
        prompt = f"""
        You are {persona["persona"]["name"]}, a {persona["persona"]["expertise"]} in a software development company. Create a realistic tech workplace scenario for practicing the phrasal verb "{verb["lexicalItem"]}".
        
        The phrasal verb means: {verb["senses"][0]["definition"]}
        Example usage: {verb["senses"][0]["examples"][0] if verb["senses"][0]["examples"] else "N/A"}
        
        IMPORTANT: This is for developers learning English. The scenario should involve:
        - Software development concepts (pull requests, deployments, code reviews, sprints, etc.)
        - Tech team roles (developers, QA, DevOps, product managers, etc.)  
        - Real situations developers face (debugging, releases, architecture decisions, etc.)
        
        Language difficulty should match CEFR level {cefr_level}:
        - A2: Simple, direct sentences with basic tech vocabulary
        - B1: Clear explanations with common development terminology  
        - B2: More complex scenarios with advanced technical concepts
        
        Generate a JSON response with:
        {{
            "scenario_title": "Brief title for the tech scenario",
            "character_name": "{persona["persona"]["name"]}",
            "character_role": "Their tech role (e.g., Senior Developer, Tech Lead, CTO, Product Manager)",
            "situation": "Detailed tech situation where this phrasal verb would naturally be used (mention specific dev concepts like pull requests, deployments, code reviews, etc.)",
            "conversation_starter": "How the character begins the conversation (use tech context)",
            "expected_usage": "How the developer should use the phrasal verb in response (with tech context)",
            "difficulty": "{cefr_level}",
            "business_context": "Specific tech context (code review, sprint planning, deployment, incident response, etc.)",
            "learning_tip": "A helpful tip for remembering this phrasal verb in tech contexts",
            "alternative_scenarios": ["2-3 other tech situations where this verb applies"]
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an English teacher specializing in technical English for software developers. Create realistic scenarios that developers would encounter in their daily work.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            scenario_data = json.loads(response.choices[0].message.content)
            # Ensure character name matches persona name exactly
            scenario_data["character_name"] = persona["persona"]["name"]
            return scenario_data
        except Exception as e:
            print(f"Error generating scenario for {verb['verb']}: {e}")
            return self.get_fallback_scenario(verb, persona)

    def get_fallback_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Fallback scenario if API fails"""
        return {
            "scenario_title": f"Practice {verb['lexicalItem']}",
            "character_name": persona["persona"]["name"],
            "character_role": "Team Lead",
            "situation": f"A workplace situation to practice {verb['lexicalItem']}",
            "conversation_starter": "Let's discuss this matter.",
            "expected_usage": f"Use '{verb['lexicalItem']}' naturally in conversation",
            "difficulty": verb["difficulty"],
            "business_context": "Team meeting",
            "learning_tip": f"Remember: {verb['senses'][0]['definition']}",
            "alternative_scenarios": [
                "Meeting discussion",
                "Email follow-up",
                "Project planning",
            ],
        }

    async def generate_image(self, verb: Dict, scenario: Dict, persona: Dict) -> str:
        """Generate a cartoon-style tech-themed image using DALL-E"""
        tech_role = scenario["character_role"]
        business_context = scenario["business_context"]

        # Create tech-specific visual elements based on the phrasal verb and context
        tech_elements = {
            "PULL IN": "code merge visualization, git branches coming together, pull request interface",
            "BREAK DOWN": "user story cards, task breakdown diagrams, agile planning board",
            "ROLL OUT": "deployment pipeline, progress bars, feature flags, server infrastructure", 
            "FALL BACK": "system architecture diagram, backup servers, rollback buttons, monitoring dashboards"
        }
        
        specific_tech_element = tech_elements.get(verb["lexicalItem"], "computer screens, code, tech workspace")

        image_prompt = f"""
        Cartoon-style illustration of a friendly tech workspace scene.
        
        Main character: A cheerful, cartoon-style {tech_role} with a warm, approachable expression.
        Setting: Modern, colorful tech office with a fun, startup-like vibe.
        
        Tech elements in the scene:
        - {specific_tech_element}
        - Multiple monitors showing code, dashboards, or development tools
        - Modern tech gadgets, laptops, mechanical keyboards
        - Whiteboards with diagrams, sticky notes, or planning boards
        - Plants, coffee cups, and friendly office décor
        
        Visual style:
        - Bright, cartoon/animated illustration style (like Pixar or modern tech company illustrations)
        - Vibrant but professional colors (blues, greens, purples with orange/yellow accents)
        - Clean, modern flat design with subtle gradients
        - Friendly, non-intimidating atmosphere
        - Tech-forward but approachable aesthetic
        
        Context: {business_context} scenario
        Action: Visual representation of "{verb["lexicalItem"]}" in a tech context
        
        No text or words in the image.
        No photorealistic people - keep it cartoon/illustration style.
        Focus on creating a welcoming, modern tech environment that developers would recognize and enjoy.
        """

        try:
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

            # Download and save image locally to timestamped folder
            image_filename = f"{verb['lexicalItem'].lower().replace(' ', '-')}.png"
            image_path = self.images_dir / image_filename

            async with httpx.AsyncClient() as client:
                img_response = await client.get(image_url)
                with open(image_path, "wb") as f:
                    f.write(img_response.content)

            return f"images/{image_filename}"

        except Exception as e:
            print(f"Error generating image for {verb['lexicalItem']}: {e}")
            return "/placeholder.svg"

    async def generate_native_explain_scenario(self, verb: Dict, persona: Dict) -> Dict:
        """Generate a native explanation scenario using OpenAI"""
        prompt = f"""
        You are {persona["persona"]["name"]}, a {persona["persona"]["expertise"]} expert with a {persona["persona"]["teaching_style"]} teaching style.
        
        Create an educational explanation for the phrasal verb "{verb["lexicalItem"]}" that focuses on helping learners understand its meaning and usage.
        
        The phrasal verb has these senses:
        {json.dumps(verb["senses"], indent=2)}
        
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
                    {
                        "role": "system",
                        "content": f"You are {persona['persona']['name']}, an expert language teacher with these traits: {', '.join(persona['persona']['personality_traits'])}. Your teaching style is {persona['persona']['teaching_style']}.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating native explain scenario for {verb['lexicalItem']}: {e}")
            return self.get_fallback_native_explain(verb, persona)

    def get_fallback_native_explain(self, verb: Dict, persona: Dict) -> Dict:
        """Fallback native explain scenario if API fails"""
        primary_sense = verb["senses"][0]
        return {
            "explanation_approach": "step-by-step breakdown",
            "main_definition": primary_sense["definition"],
            "key_teaching_points": [
                f"'{verb['lexicalItem']}' means {primary_sense['definition']}",
                "Can be used in both formal and informal contexts",
                "Pay attention to preposition usage",
            ],
            "usage_examples": primary_sense["examples"][:3]
            if len(primary_sense["examples"]) >= 3
            else primary_sense["examples"]
            + [f"Let me {verb['lexicalItem'].lower()} this matter."],
            "common_mistakes": [
                "Using the wrong preposition",
                "Confusing with similar phrasal verbs",
            ],
            "memory_tips": [
                f"Think of {verb['lexicalItem'].lower()} as {primary_sense['definition'].lower()}",
                "Practice with real workplace situations",
            ],
            "difficulty_level": verb["difficulty"],
            "teaching_personality": persona["persona"]["teaching_style"],
        }

    async def create_native_explain_card(self, verb: Dict) -> Dict:
        """Create a native explain card with voice persona"""
        native_explain_card = {
            "id": f"native-explain-{verb['lexicalItem'].lower().replace(' ', '-')}",
            "type": "native_explain",
            "title": f"Explain: {verb['lexicalItem']}",
            "difficulty": verb["difficulty"],
            "targetLexicalItem": {
                "lexicalItem": verb["lexicalItem"],
                "senses": verb["senses"]
            }
        }

        return native_explain_card

    async def create_situation_card(self, verb: Dict) -> Dict:
        """Create a situation/context card with voice persona"""
        persona = self.get_random_persona()
        scenario = await self.generate_workplace_scenario(verb, persona)
        image_path = await self.generate_image(verb, scenario, persona)

        # Use the first sense as the primary definition
        primary_sense = verb["senses"][0]

        situation_card = {
            "id": f"context-{verb['lexicalItem'].lower().replace(' ', '-')}",
            "type": "context",
            "title": f"In-Context: {verb['lexicalItem']}",
            "difficulty": verb["difficulty"],
            "contextText": f"You're speaking with {scenario['character_name']}, {scenario['character_role']}. {scenario['situation']}",
            "imageUrl": image_path,
            "ctaText": f"Talk to {scenario['character_name']}",
            "scenario": {
                "character": scenario["character_name"],
                "role": scenario["character_role"],
                "situation": scenario["situation"],
                "phrasalVerb": verb["lexicalItem"].lower(),
                "contextText": scenario["situation"],
                "conversationStarter": scenario["conversation_starter"],
                "maxTurns": 5
            },
            "targetLexicalItem": {
                "lexicalItem": verb["lexicalItem"],
                "definition": primary_sense["definition"],
                "examples": primary_sense["examples"] + [scenario["expected_usage"]]
            },
            "voicePersona": {
                **persona,
                "scenarioRole": {
                    "character": scenario["character_name"],
                    "role": scenario["character_role"],
                    "teachingApproach": persona["persona"]["teaching_style"],
                    "expertise": persona["persona"]["expertise"],
                    "conversationStyle": f"As {scenario['character_name']}, they will use a {persona['persona']['teaching_style']} approach to help learners practice the phrasal verb '{verb['lexicalItem']}' in a {scenario['business_context']} context."
                }
            }
        }

        return situation_card

    async def generate_card_batch(
        self, verb: Dict, verb_index: int, total_verbs: int
    ) -> List[Dict]:
        """Generate both cards for a single verb in parallel"""
        print(f"Processing {verb_index + 1}/{total_verbs}: {verb['lexicalItem']}")

        # Create both cards concurrently
        native_task = asyncio.create_task(self.create_native_explain_card(verb))
        situation_task = asyncio.create_task(self.create_situation_card(verb))

        # Wait for both cards to complete
        native_card, situation_card = await asyncio.gather(native_task, situation_task)

        print(f"  ✅ Completed both cards for {verb['lexicalItem']}")
        return [native_card, situation_card]

    async def generate_all_cards(self):
        """Main generation process with parallel processing"""
        print(f"Starting parallel demo generation at {self.timestamp}")

        # Load verbs from config
        all_verbs = self.load_phrasal_verbs_from_config()
        selected_verbs = self.get_selected_verbs(all_verbs)

        print(f"Processing {len(selected_verbs)} phrasal verbs in parallel...")

        # Create tasks for all verbs (each task generates 2 cards)
        batch_tasks = [
            self.generate_card_batch(verb, i, len(selected_verbs))
            for i, verb in enumerate(selected_verbs)
        ]

        # Execute all batches concurrently with a semaphore to control concurrency
        semaphore = asyncio.Semaphore(
            3
        )  # Limit to 3 concurrent verb processing batches

        async def limited_batch(task):
            async with semaphore:
                return await task

        print("🚀 Generating all cards concurrently...")
        batch_results = await asyncio.gather(
            *[limited_batch(task) for task in batch_tasks]
        )

        # Flatten results
        voice_cards = []
        for batch in batch_results:
            voice_cards.extend(batch)

        # Separate cards by type for statistics
        native_explains = [
            card for card in voice_cards if card["type"] == "native_explain"
        ]
        situations = [card for card in voice_cards if card["type"] == "context"]

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
                "phrasalVerbsProcessed": [v["lexicalItem"] for v in selected_verbs],
                "voicePersonasUsed": len(self.used_personas),
                "cardStructure": "1 native_explain + 1 context per phrasal verb",
                "generationMode": "parallel",
            },
        }

        # Save to timestamped folder
        output_file = self.output_dir / "voice-cards.json"
        with open(output_file, "w") as f:
            json.dump(output, f, indent=2)

        print("\n🎉 Parallel generation complete!")
        print(f"Total cards generated: {len(voice_cards)}")
        print(f"  - Native explain cards: {len(native_explains)}")
        print(f"  - Situation cards: {len(situations)}")
        print(f"Voice personas used: {len(self.used_personas)}")
        print(f"Output saved to: {output_file}")
        print(f"Images saved to: {self.images_dir}")

        return output_file


async def main():
    """Main entry point"""
    generator = DemoGenerator()
    await generator.generate_all_cards()


if __name__ == "__main__":
    asyncio.run(main())

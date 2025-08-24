#!/usr/bin/env python3
"""
Test version of Demo Generator without API calls
Generates mock data for testing the system integration
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

PHRASAL_VERBS_PATH = Path(__file__).parent.parent.parent / "app" / "public" / "phrasal_verbs.json"
OUTPUT_DIR = Path(__file__).parent.parent / "generated_data"
IMAGES_DIR = OUTPUT_DIR / "images"

class MockDemoGenerator:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
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

    def get_selected_verbs(self, verbs: List[Dict]) -> List[Dict]:
        """Get first 5 and last 5 phrasal verbs"""
        first_five = verbs[:5]
        last_five = verbs[-5:]
        return first_five + last_five

    def generate_mock_scenario(self, verb: Dict) -> Dict:
        """Generate a mock workplace scenario"""
        scenarios = {
            "GO ON": {
                "scenario_title": "Team Meeting Continuation",
                "character_name": "Ms. Chen",
                "character_role": "Project Manager",
                "situation": "You're in a team meeting discussing project updates. Ms. Chen paused to check her notes and now wants to continue the discussion.",
                "conversation_starter": "Sorry for the pause. Now, about the timeline for the next phase...",
                "expected_usage": "Please go on, I'm very interested in hearing about the timeline.",
                "difficulty": "intermediate",
                "business_context": "Team meeting",
                "learning_tip": "Use 'go on' to encourage someone to continue speaking or to indicate continuation.",
                "alternative_scenarios": ["Presentation Q&A", "One-on-one review", "Conference call"]
            },
            "PICK UP": {
                "scenario_title": "Task Assignment",
                "character_name": "Mr. Johnson",
                "character_role": "Department Head",
                "situation": "Mr. Johnson needs someone to collect important documents from the client's office on their way to the meeting.",
                "conversation_starter": "I need someone to get the contracts from the client's office before our 3 PM meeting.",
                "expected_usage": "I can pick up the contracts on my way to the meeting.",
                "difficulty": "beginner",
                "business_context": "Task delegation",
                "learning_tip": "'Pick up' means to collect or get something from somewhere.",
                "alternative_scenarios": ["Office supplies run", "Client materials", "Lunch order"]
            }
        }

        # Default scenario for verbs not in the mock data
        default = {
            "scenario_title": f"Practice {verb['verb']}",
            "character_name": "Dr. Smith",
            "character_role": "Senior Consultant",
            "situation": f"A workplace situation where '{verb['verb']}' would be naturally used in conversation.",
            "conversation_starter": "Let's discuss this matter further.",
            "expected_usage": f"I'll {verb['verb'].lower()} with that approach.",
            "difficulty": "intermediate",
            "business_context": "Business discussion",
            "learning_tip": f"Remember: {verb['senses'][0]['definition']}",
            "alternative_scenarios": ["Team meeting", "Email discussion", "Project planning"]
        }

        return scenarios.get(verb['verb'], default)

    def create_mock_image(self, verb: Dict) -> str:
        """Create a placeholder for image (in real version, this would generate an image)"""
        # In the test version, we'll just return placeholder
        # In production, this would call DALL-E API
        return "/placeholder.svg"

    def create_voice_card(self, verb: Dict, index: int) -> Dict:
        """Create a voice card with mock data"""
        scenario = self.generate_mock_scenario(verb)
        image_path = self.create_mock_image(verb)

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

    def generate_all_cards(self):
        """Main generation process"""
        print(f"Starting mock demo generation at {self.timestamp}")

        # Load and select verbs
        all_verbs = self.load_phrasal_verbs()
        selected_verbs = self.get_selected_verbs(all_verbs)

        print(f"Processing {len(selected_verbs)} phrasal verbs...")
        print(f"Selected verbs: {[v['verb'] for v in selected_verbs]}")

        # Generate voice cards
        voice_cards = []
        for i, verb in enumerate(selected_verbs):
            print(f"Processing {i+1}/{len(selected_verbs)}: {verb['verb']}")
            card = self.create_voice_card(verb, i)
            voice_cards.append(card)

        # Create output structure
        output = {
            "generatedAt": self.timestamp,
            "totalCards": len(voice_cards),
            "voiceCardTypes": voice_cards,
            "metadata": {
                "generator": "demo_generator_test.py",
                "version": "1.0.0-test",
                "phrasalVerbsProcessed": [v['verb'] for v in selected_verbs],
                "testMode": True
            }
        }

        # Save to timestamped file
        output_file = OUTPUT_DIR / f"voice-cards-{self.timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)

        print("\nMock generation complete!")
        print(f"Output saved to: {output_file}")

        # Also create a symlink to latest for easy access
        latest_link = OUTPUT_DIR / "voice-cards-latest.json"
        if latest_link.exists():
            latest_link.unlink()
        latest_link.symlink_to(output_file.name)
        print(f"Latest symlink created: {latest_link}")

        return output_file

def main():
    """Main entry point"""
    generator = MockDemoGenerator()
    generator.generate_all_cards()

if __name__ == "__main__":
    main()

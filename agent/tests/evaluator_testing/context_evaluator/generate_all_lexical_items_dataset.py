#!/usr/bin/env python3
"""
Generate comprehensive test datasets for all lexical items from voice-cards.json.
Creates 25 test cases per lexical item (100 total) with expected feedback for wrong answers.
"""

import json
import os
import asyncio
from typing import List, Dict, Any
from pathlib import Path


class ComprehensiveLexicalItemDatasetGenerator:
    """Generate comprehensive test cases for all lexical items with contextual feedback."""
    
    def __init__(self):
        # Load extracted lexical items data
        self.lexical_items = self.load_lexical_items()
        
    def load_lexical_items(self) -> Dict[str, Any]:
        """Load extracted lexical items data."""
        data_path = os.path.join(os.path.dirname(__file__), "lexical_items_extracted.json")
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Please run extract_lexical_items.py first to generate {data_path}")
        
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📁 Loaded {data['total_lexical_items']} lexical items from {data_path}")
        return data["lexical_items"]
    
    def generate_test_cases_for_lexical_item(self, lexical_item: str, item_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate 25 comprehensive test cases for a single lexical item (100 total across 4 items)."""
        
        scenario_data = item_data["scenario"]
        definition = item_data["definition"]
        examples = item_data["examples"]
        
        print(f"🎯 Generating test cases for {lexical_item.upper()}")
        print(f"   Context: {scenario_data['character']} in {scenario_data['situation'][:50]}...")
        
        test_cases = []
        
        # Scaled down to 25 cases per lexical item (proportional distribution)
        # 1. Correct usage cases (5 cases) - contextually appropriate  
        correct_responses = self.generate_correct_responses(lexical_item, definition, scenario_data)[:5]
        
        # 2. Wrong sense cases (7 cases) - using lexical item but wrong meaning
        wrong_sense_responses = self.generate_wrong_sense_responses(lexical_item, definition)[:7]
        
        # 3. Incomplete cases (4 cases) - fragments and hesitations
        incomplete_responses = self.generate_incomplete_responses(lexical_item)[:4]
        
        # 4. No usage cases (4 cases) - correct concept but different words
        no_usage_responses = self.generate_no_usage_responses(definition)[:4]
        
        # 5. Spanish response cases (3 cases) - users responding in Spanish
        spanish_responses = self.generate_spanish_responses(definition)[:3]
        
        # 6. Grammatical error cases (2 cases) - using lexical item with grammar errors
        grammatical_error_responses = self.generate_grammatical_error_responses(lexical_item)[:2]
        
        # Build all test cases with expected outcomes and feedback
        categories = [
            ("correct", correct_responses, True, True, "easy", ""),
            ("wrong_sense", wrong_sense_responses, False, True, "medium", self.get_wrong_sense_feedback),
            ("incomplete", incomplete_responses, False, True, "hard", self.get_incomplete_feedback),
            ("no_usage", no_usage_responses, False, False, "easy", self.get_no_usage_feedback),
            ("spanish_response", spanish_responses, False, False, "hard", self.get_spanish_response_feedback),
            ("grammatical_error", grammatical_error_responses, False, True, "hard", self.get_grammatical_error_feedback)
        ]
        
        for category, responses, used_correctly, used_verb, difficulty, feedback_generator in categories:
            for response in responses:
                # Generate expected feedback for incorrect responses
                expected_feedback = ""
                if not used_correctly:
                    if callable(feedback_generator):
                        expected_feedback = feedback_generator(response, lexical_item, definition, scenario_data)
                    else:
                        expected_feedback = feedback_generator
                
                test_case = {
                    "input": {
                        "user_text": response,
                        "phrasal_verb": lexical_item.lower(),  # Keep backward compatibility
                        "phrasal_verb_definition": definition,
                        "scenario": scenario_data["situation"],
                        "character": scenario_data["character"],
                        "phrasal_verb_examples": examples
                    },
                    "expected_output": {
                        "used_correctly": used_correctly,
                        "used_verb": used_verb,
                        "expected_feedback": expected_feedback
                    },
                    "metadata": {
                        "category": category,
                        "difficulty": difficulty,
                        "lexical_item": lexical_item,
                        "scenario_character": scenario_data["character"],
                        "notes": self.get_category_notes(category)
                    }
                }
                test_cases.append(test_case)
        
        print(f"   Generated {len(test_cases)} test cases for {lexical_item}")
        return test_cases
    
    def generate_correct_responses(self, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> List[str]:
        """Generate contextually appropriate correct usage responses."""
        # Create professional, contextually appropriate responses
        base_templates = [
            f"Let's {lexical_item.lower()} the latest updates from the main branch",
            f"We should {lexical_item.lower()} these changes before proceeding", 
            f"Can we {lexical_item.lower()} the necessary components for this feature?",
            f"I think we need to {lexical_item.lower()} this into our current workflow",
            f"How about we {lexical_item.lower()} the required dependencies?",
            f"Should we {lexical_item.lower()} these modifications into the release?",
            f"Let's {lexical_item.lower()} all the relevant documentation",
            f"We can {lexical_item.lower()} this enhancement into the next sprint",
            f"I suggest we {lexical_item.lower()} these improvements systematically",
            f"Could you help me {lexical_item.lower()} the necessary resources?",
            f"We need to {lexical_item.lower()} the updated configurations",
            f"Let me {lexical_item.lower()} what we discussed in the last meeting"
        ]
        
        return base_templates
    
    def generate_wrong_sense_responses(self, lexical_item: str, definition: str) -> List[str]:
        """Generate responses using the lexical item but with wrong meanings."""
        # Create responses that use the lexical item but in wrong contexts/senses
        wrong_sense_templates = []
        
        if "pull in" in lexical_item.lower():
            wrong_sense_templates = [
                "The car needs to pull in to the parking space",
                "Let's pull in to the gas station for fuel",
                "The train will pull in to the station soon",
                "We should pull in our marketing budget this quarter",
                "The police officer asked us to pull in to the curb",
                "The boat needs to pull in to the harbor",
                "Can you pull in the fishing net from the water?",
                "The company decided to pull in external consultants",
                "We need to pull in our spending on office supplies",
                "The manager wants to pull in the team's autonomy",
                "Let's pull in to the drive-through for lunch",
                "The airplane will pull in to the gate shortly",
                "We should pull in the outdoor furniture before it rains",
                "The farmer needs to pull in the harvest equipment",
                "Can you pull in your car closer to the building?"
            ]
        elif "break down" in lexical_item.lower():
            wrong_sense_templates = [
                "The server might break down under heavy load",
                "My laptop tends to break down during updates",
                "The build system breaks down every Friday",
                "I'm breaking down under all this pressure",
                "The deployment pipeline breaks down regularly",
                "Our monitoring system breaks down during peak hours",
                "The database connection breaks down frequently",
                "The CI/CD process breaks down with large deployments",
                "Don't break down on me now, we need to finish this",
                "The legacy code is starting to break down",
                "The architecture breaks down when you scale it",
                "I feel like I'm going to break down with this workload",
                "The testing framework breaks down with complex data",
                "The team lead is breaking down from the stress",
                "These old systems are breaking down over time"
            ]
        elif "roll out" in lexical_item.lower():
            wrong_sense_templates = [
                "Let's roll out the red carpet for the new CEO",
                "The baker needs to roll out the pizza dough",
                "We should roll out the yoga mats for the session", 
                "Can you roll out the sleeping bag for camping?",
                "The chef will roll out the pasta dough carefully",
                "Let's roll out the banner for the company event",
                "We need to roll out the carpet for the presentation",
                "The artist wants to roll out the canvas on the floor",
                "Can you roll out the blueprints on the table?",
                "We should roll out the tarp to cover the equipment",
                "The decorator will roll out the fabric for measurements",
                "Let's roll out the poster for the team meeting",
                "We need to roll out the mat for the exercise class",
                "Can you roll out the rope for the climbing activity?",
                "The installer will roll out the flooring material"
            ]
        elif "fall back" in lexical_item.lower():
            wrong_sense_templates = [
                "I need to fall back on my chair to relax",
                "The soldier will fall back from the front line",
                "Let's fall back to our original meeting location",
                "We should fall back to the previous version if needed",
                "The team decided to fall back on their experience",
                "Can you fall back a few steps to make room?",
                "The runner will fall back to conserve energy",
                "We need to fall back to the backup server",
                "The company will fall back on its reserves",
                "Let's fall back to the tried and tested method",
                "The troops were ordered to fall back immediately",
                "We should fall back to manual processing",
                "The player will fall back to defend the goal",
                "Can we fall back to the original plan?",
                "The organization will fall back on volunteers"
            ]
        
        return wrong_sense_templates
    
    def generate_incomplete_responses(self, lexical_item: str) -> List[str]:
        """Generate incomplete/fragment responses."""
        return [
            lexical_item.title(),  # Just the lexical item
            f"We {lexical_item.lower()}",  # Incomplete sentence
            f"Let's... {lexical_item.lower()}",  # Hesitation pattern
            f"{lexical_item.title()} it, you know?",  # Informal/slang
            f"{' '.join(lexical_item.split()[:-1])}ing here" if ' ' in lexical_item else f"{lexical_item.lower()}ing here",  # Fragment
            f"To {lexical_item.lower()}",  # Infinitive only
            f"{lexical_item.title()} what?",  # Question fragment
            f"Yeah, {lexical_item.lower()}"  # Affirmative fragment
        ]
    
    def generate_no_usage_responses(self, definition: str) -> List[str]:
        """Generate responses with correct concept but different vocabulary."""
        # Map definitions to alternative vocabulary
        alternatives = {
            "include": ["incorporate", "integrate", "add", "merge", "combine", "bring in", "insert", "embed"],
            "divide": ["split", "separate", "partition", "segment", "decompose", "fragment", "break apart", "dissect"],
            "deploy": ["release", "launch", "distribute", "publish", "implement", "deliver", "install", "activate"], 
            "return": ["revert", "go back", "restore", "reset", "switch back", "retreat", "recover", "restore"]
        }
        
        # Find the most appropriate alternatives based on definition
        chosen_alternatives = []
        for key, values in alternatives.items():
            if key.lower() in definition.lower():
                chosen_alternatives.extend(values[:8])
                break
        
        if not chosen_alternatives:
            chosen_alternatives = ["organize", "manage", "handle", "process", "coordinate", "arrange", "execute", "implement"]
        
        return [
            f"Let's {alt} these requirements into smaller pieces" for alt in chosen_alternatives
        ]
    
    def generate_spanish_responses(self, definition: str) -> List[str]:
        """Generate Spanish responses for English conversation context."""
        # Create Spanish responses that would be conceptually correct but wrong language
        spanish_responses = [
            "Vamos a incluir eso en el proyecto",  # "Let's include that in the project"
            "Podemos incorporar estos cambios",  # "We can incorporate these changes"
            "Deberíamos dividir esto en partes",  # "We should divide this into parts" 
            "¿Podemos separar esta tarea grande?",  # "Can we separate this big task?"
            "Sí, vamos a organizar esto mejor",  # "Yes, let's organize this better"
            "Mejor implementamos esto paso a paso"  # "Better we implement this step by step"
        ]
        return spanish_responses
    
    def generate_grammatical_error_responses(self, lexical_item: str) -> List[str]:
        """Generate grammatically incorrect usage of the lexical item."""
        parts = lexical_item.lower().split()
        if len(parts) == 2:
            verb, particle = parts
            return [
                f"{particle} {verb} we should this task",  # Word order issues
                f"We are {verb} {particle} the story",  # Wrong tense form
                f"{verb.title()} {particle}s are needed here",  # Wrong pluralization
                f"I will {verb}ed {particle} this feature",  # Wrong past form
                f"Let's {verb} it {particle} it",  # Repetition/stutter
                f"We {verb} {particle} can this"  # Mixed up grammar
            ]
        else:
            return [
                f"We are {lexical_item.lower()} the project",
                f"{lexical_item.title()}ing is needed here", 
                f"I will {lexical_item.lower()}ed this",
                f"Let's {lexical_item.lower()} it it",
                f"We {lexical_item.lower()} should this",
                f"{lexical_item.lower()} we can this"
            ]
    
    def get_wrong_sense_feedback(self, response: str, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> str:
        """Generate feedback for wrong sense usage."""
        return f"This usage refers to a different meaning of '{lexical_item}' rather than '{definition}'. In {scenario_data['situation'][:30]}..., try using it to mean '{definition}'."
    
    def get_incomplete_feedback(self, response: str, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> str:
        """Generate feedback for incomplete usage."""
        return f"This response is incomplete or too informal for a professional {scenario_data['role']} context. Try forming a complete sentence using '{lexical_item}' to {definition.lower()}."
    
    def get_no_usage_feedback(self, response: str, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> str:
        """Generate feedback for no usage."""
        return f"Good concept! However, try using the specific phrase '{lexical_item}' in your response. For example: 'Let's {lexical_item.lower()} these requirements.'"
    
    def get_spanish_response_feedback(self, response: str, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> str:
        """Generate feedback for Spanish responses."""
        return f"Please respond in English during this English conversation practice. Try using '{lexical_item}' to express your idea."
    
    def get_grammatical_error_feedback(self, response: str, lexical_item: str, definition: str, scenario_data: Dict[str, Any]) -> str:
        """Generate feedback for grammatical errors."""
        return f"You're using '{lexical_item}' but there's a grammatical error. Try: 'Let's {lexical_item.lower()} this requirement' or similar correct form."
    
    def get_category_notes(self, category: str) -> str:
        """Get explanatory notes for each category."""
        notes = {
            "correct": "Proper usage of lexical item with appropriate meaning and context",
            "wrong_sense": "Uses lexical item but with wrong meaning/sense for the context",
            "incomplete": "Uses lexical item but in incomplete or fragment sentences", 
            "no_usage": "Correct concept but doesn't use the target lexical item",
            "spanish_response": "User responds in Spanish during English conversation - wrong context",
            "grammatical_error": "Uses lexical item but with grammatical errors or awkward construction"
        }
        return notes.get(category, "")
    
    def save_combined_dataset(self, all_test_data: Dict[str, Any]) -> str:
        """Save all test cases for all lexical items to a single JSON file."""
        filename = "all_lexical_items_comprehensive_test_cases.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_test_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {all_test_data['total_cases']} test cases saved to {filepath}")
        return filepath
    
    async def generate_dataset_for_item_async(self, lexical_item: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dataset for a single lexical item asynchronously."""
        print(f"🎯 Starting {lexical_item.upper()} generation...")
        # Run the CPU-bound work in a thread pool
        test_cases = await asyncio.to_thread(
            self.generate_test_cases_for_lexical_item, lexical_item, item_data
        )
        print(f"✅ Completed {lexical_item.upper()}: {len(test_cases)} cases")
        
        # Count by category
        category_counts = {}
        difficulty_counts = {}
        for case in test_cases:
            cat = case["metadata"]["category"]
            diff = case["metadata"]["difficulty"]
            category_counts[cat] = category_counts.get(cat, 0) + 1
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        return {
            "lexical_item": lexical_item.lower(),
            "scenario_info": {
                "character": item_data["scenario"]["character"],
                "role": item_data["scenario"]["role"],
                "situation": item_data["scenario"]["situation"],
                "definition": item_data["definition"],
                "context": item_data["scenario"]["context_text"],
                "conversation_starter": item_data["scenario"]["conversation_starter"],
                "examples": item_data["examples"]
            },
            "total_cases": len(test_cases),
            "category_breakdown": category_counts,
            "difficulty_breakdown": difficulty_counts,
            "test_cases": test_cases
        }

    async def generate_all_datasets_async(self) -> str:
        """Generate comprehensive datasets for all lexical items in parallel."""
        print(f"🚀 Generating comprehensive datasets for {len(self.lexical_items)} lexical items in parallel...")
        
        # Create tasks for all lexical items
        tasks = [
            self.generate_dataset_for_item_async(lexical_item, item_data)
            for lexical_item, item_data in self.lexical_items.items()
        ]
        
        # Run all tasks concurrently
        lexical_item_datasets = await asyncio.gather(*tasks)
        
        # Combine all test cases and calculate totals
        all_test_cases = []
        lexical_items_data = {}
        total_category_counts = {}
        total_difficulty_counts = {}
        
        for item_dataset in lexical_item_datasets:
            lexical_item = item_dataset["lexical_item"]
            lexical_items_data[lexical_item] = {
                "scenario_info": item_dataset["scenario_info"],
                "total_cases": item_dataset["total_cases"],
                "category_breakdown": item_dataset["category_breakdown"],
                "difficulty_breakdown": item_dataset["difficulty_breakdown"]
            }
            
            # Add test cases to master list
            all_test_cases.extend(item_dataset["test_cases"])
            
            # Aggregate category counts
            for category, count in item_dataset["category_breakdown"].items():
                total_category_counts[category] = total_category_counts.get(category, 0) + count
            
            # Aggregate difficulty counts  
            for difficulty, count in item_dataset["difficulty_breakdown"].items():
                total_difficulty_counts[difficulty] = total_difficulty_counts.get(difficulty, 0) + count
        
        # Create combined dataset
        combined_dataset = {
            "dataset_name": "all-lexical-items-comprehensive",
            "description": f"Comprehensive test dataset for all {len(self.lexical_items)} lexical items with expected feedback",
            "total_cases": len(all_test_cases),
            "total_lexical_items": len(self.lexical_items),
            "category_breakdown": total_category_counts,
            "difficulty_breakdown": total_difficulty_counts,
            "lexical_items": lexical_items_data,
            "test_cases": all_test_cases,
            "generated_at": "2025-08-29",
            "generator": "Comprehensive dataset generator for ContextEvaluator with feedback"
        }
        
        # Save to single file
        filepath = await asyncio.to_thread(self.save_combined_dataset, combined_dataset)
        
        print(f"\n🎉 Generated {len(all_test_cases)} total test cases across {len(self.lexical_items)} lexical items!")
        return filepath

    def generate_all_datasets(self) -> str:
        """Generate comprehensive datasets for all lexical items (sync wrapper)."""
        return asyncio.run(self.generate_all_datasets_async())


def main():
    """Generate comprehensive test datasets for all lexical items."""
    try:
        generator = ComprehensiveLexicalItemDatasetGenerator()
        generated_file = generator.generate_all_datasets()
        
        print(f"\n📊 COMPREHENSIVE DATASET GENERATION COMPLETE")
        print(f"✅ Generated single file:")
        print(f"   📁 {os.path.basename(generated_file)}")
        
        print(f"\n🎯 Next steps:")
        print(f"   1. Upload dataset to Langfuse using upload_to_langfuse.py")
        print(f"   2. Run comprehensive evaluation using test framework")
        print(f"   3. Analyze accuracy across all lexical items")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating datasets: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
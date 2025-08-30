#!/usr/bin/env python3
"""
Extract all lexical items and their scenario data from voice-cards.json.
This script analyzes the voice-cards data and prepares it for comprehensive test generation.
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path


def extract_lexical_items() -> Dict[str, Any]:
    """Extract all lexical items and their context scenarios from voice-cards.json."""
    # Load voice-cards.json
    voice_cards_path = Path(__file__).parent.parent.parent.parent / "app" / "generated_data" / "voice-cards.json"
    
    if not voice_cards_path.exists():
        raise FileNotFoundError(f"voice-cards.json not found at {voice_cards_path}")
    
    with open(voice_cards_path, 'r', encoding='utf-8') as f:
        voice_cards_data = json.load(f)
    
    print(f"📁 Loaded voice-cards.json from {voice_cards_path}")
    print(f"📊 Total cards: {voice_cards_data['totalCards']}")
    
    # Extract unique lexical items and their context scenarios
    lexical_items = {}
    
    for card in voice_cards_data["voiceCardTypes"]:
        # We want context cards (not native_explain) for scenario data
        if card["type"] == "context":
            lexical_item = card["targetLexicalItem"]["lexicalItem"]
            definition = card["targetLexicalItem"]["definition"]
            examples = card["targetLexicalItem"]["examples"]
            
            # Extract scenario data
            scenario = card["scenario"]
            voice_persona = card.get("voicePersona", {})
            
            lexical_items[lexical_item] = {
                "lexical_item": lexical_item.lower(),  # Store in lowercase for consistency
                "definition": definition,
                "examples": examples,
                "scenario": {
                    "character": scenario["character"],
                    "role": scenario["role"],
                    "situation": scenario["situation"],
                    "context_text": scenario["contextText"],
                    "conversation_starter": scenario["conversationStarter"],
                    "max_turns": scenario["maxTurns"]
                },
                "voice_persona": voice_persona,
                "difficulty": card["difficulty"]
            }
    
    return {
        "total_lexical_items": len(lexical_items),
        "lexical_items": lexical_items,
        "extracted_at": "2025-08-29",
        "source_file": str(voice_cards_path)
    }


def save_lexical_items_data(data: Dict[str, Any], filename: str = "lexical_items_extracted.json"):
    """Save extracted lexical items data to JSON file."""
    output_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted data saved to {output_path}")
    return output_path


def print_summary(data: Dict[str, Any]):
    """Print a summary of extracted lexical items."""
    print(f"\n🎯 Extracted {data['total_lexical_items']} lexical items:")
    
    for item_name, item_data in data["lexical_items"].items():
        print(f"\n📝 {item_name}")
        print(f"   Definition: {item_data['definition']}")
        print(f"   Character: {item_data['scenario']['character']} ({item_data['scenario']['role']})")
        print(f"   Situation: {item_data['scenario']['situation'][:70]}...")
        print(f"   Examples: {len(item_data['examples'])} provided")
        print(f"   Difficulty: {item_data['difficulty']}")


def main():
    """Extract and display lexical items from voice-cards.json."""
    try:
        print("🔍 Extracting lexical items from voice-cards.json...")
        
        # Extract lexical items
        data = extract_lexical_items()
        
        # Print summary
        print_summary(data)
        
        # Save to file
        output_path = save_lexical_items_data(data)
        
        print(f"\n✅ Extraction complete!")
        print(f"📋 Ready for comprehensive test generation across {data['total_lexical_items']} lexical items")
        print(f"📁 Data saved to: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error extracting lexical items: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
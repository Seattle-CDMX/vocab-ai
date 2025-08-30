#!/usr/bin/env python3
"""
Simple script to swap phrasal verb data sets
"""

import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "data" / "phrasal_verbs_config.json"

def load_config():
    """Load the current configuration"""
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config):
    """Save the configuration"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def list_available_sets():
    """List all available phrasal verb sets"""
    config = load_config()
    current_set = config["active_set"]
    
    print("\n📚 Available Phrasal Verb Sets:")
    print("=" * 40)
    
    for set_name, verbs in config["phrasal_verb_sets"].items():
        status = "🟢 ACTIVE" if set_name == current_set else "⚪"
        verb_list = [v["lexicalItem"] for v in verbs]
        print(f"{status} {set_name}")
        print(f"   📝 {len(verbs)} verbs: {', '.join(verb_list)}")
        print()

def switch_set(target_set):
    """Switch to a different phrasal verb set"""
    config = load_config()
    
    if target_set not in config["phrasal_verb_sets"]:
        print(f"❌ Error: Set '{target_set}' not found!")
        print("Available sets:", list(config["phrasal_verb_sets"].keys()))
        return False
    
    config["active_set"] = target_set
    save_config(config)
    
    verb_count = len(config["phrasal_verb_sets"][target_set])
    print(f"✅ Switched to '{target_set}' ({verb_count} verbs)")
    return True

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python swap_data.py list                    # List available sets")
        print("  python swap_data.py switch <set_name>       # Switch to a set")
        print()
        list_available_sets()
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_available_sets()
    elif command == "switch":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify a set name")
            print("Usage: python swap_data.py switch <set_name>")
            return
        
        target_set = sys.argv[2]
        if switch_set(target_set):
            print(f"🚀 Ready to generate cards with '{target_set}' set!")
            print("Run: uv run python generators/demo_generator.py")
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: list, switch")

if __name__ == "__main__":
    main()
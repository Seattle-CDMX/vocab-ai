import os
import yaml


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from a YAML file.
    
    Args:
        prompt_name: The name of the prompt file (without .yaml extension)
        
    Returns:
        The prompt text as a string
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        yaml.YAMLError: If there's an error parsing the YAML
    """
    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to get to the project root, then into prompts
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), "prompts")
    
    prompt_file = os.path.join(prompts_dir, f"{prompt_name}.yaml")
    
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        
    # Expect the YAML to have a 'prompt' key
    if 'prompt' not in data:
        raise ValueError(f"Prompt file {prompt_file} must contain a 'prompt' key")
        
    return data['prompt']
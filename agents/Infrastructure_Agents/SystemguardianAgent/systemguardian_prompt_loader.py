# systemguardian_prompt_loader.py

from .systemguardian_config import load_guardian_prompt

def get_systemguardian_prompt():
    return load_guardian_prompt()

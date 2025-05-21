# agent_suggester.py – Hauptmodul für GPT-gestützte Agentenvorschläge

import os
from agents.General_Agents.AgentSuggester.agent_suggester_prompt import generate_agent_suggestion_prompt
from agents.General_Agents.AgentSuggester.agent_suggester_log import log_suggestion
from modules.utils.json_loader import load_config
from modules.reasoning_intelligenz.structure_content_loader import get_all_structure_blocks
from modules.ai_intelligenz.gpt_response_parser import parse_gpt_response
from openai import ChatCompletion

AGENT_KEYWORDS = load_config("agent_keyword_map.json")

def suggest_agents_for_structure():
    structure_blocks = get_all_structure_blocks()
    prompt = generate_agent_suggestion_prompt(structure_blocks, AGENT_KEYWORDS)
    response = ChatCompletion.create(
        model="gpt-4o",
        messages=prompt
    )
    parsed = parse_gpt_response(response.choices[0].message.content)
    log_suggestion(parsed)
    return parsed

# agent_suggester_router.py – Aufruf über Chainlit, Telegram oder Trigger

from agents.General_Agents.AgentSuggester.agent_suggester import suggest_agents_for_structure

def handle_agent_suggestion_request():
    return suggest_agents_for_structure()

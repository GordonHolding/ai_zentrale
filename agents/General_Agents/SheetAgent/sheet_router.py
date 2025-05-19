# sheet_router.py – GPT-Router für SheetAgent-Anfragen

from agents.General_Agents.SheetAgent.sheet_agent import handle_sheet_request

def route_sheet_action(context: dict):
    template_key = context.get("template")
    variables = context.get("variables", {})
    output_format = context.get("output_format", "sheet")
    return handle_sheet_request(template_key, variables, output_format)

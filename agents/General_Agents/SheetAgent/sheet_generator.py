# sheet_generator.py – erstellt Tabelleninhalte basierend auf Template

def generate_sheet_data(template: dict, variables: dict) -> list:
    headers = template.get("headers", [])
    rows = []

    for entry in template.get("rows", []):
        row = []
        for col in headers:
            value = entry.get(col, "")
            for var, replacement in variables.items():
                value = value.replace(f"[{var.upper()}]", replacement)
            row.append(value)
        rows.append(row)

    return [headers] + rows

# deadline_checker.py – prüft, ob Fristen überschritten oder bald fällig sind

from datetime import datetime, timedelta
from modules.reasoning_intelligenz.calendar_reader import get_all_deadlines

def check_deadlines():
    today = datetime.today().date()
    upcoming_days = 3
    warnings = []

    for deadline in get_all_deadlines():
        try:
            due = datetime.strptime(deadline["due_date"], "%Y-%m-%d").date()
            delta = (due - today).days
            if delta < 0:
                warnings.append(f"⏰ Überfällig: {deadline['key']} (seit {abs(delta)} Tagen) – {deadline['source']}")
            elif 0 <= delta <= upcoming_days:
                warnings.append(f"⚠️ Bald fällig: {deadline['key']} (in {delta} Tagen) – {deadline['source']}")
        except Exception:
            continue

    return warnings

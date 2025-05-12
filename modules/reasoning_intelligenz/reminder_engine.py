def get_reminders(events):
    return [e for e in events if "Reminder" in e.get("summary", "")]

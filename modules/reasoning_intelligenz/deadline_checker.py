def check_deadlines(entries):
    from datetime import datetime
    today = datetime.now().date()
    return [entry for entry in entries if 'deadline' in entry and datetime.strptime(entry['deadline'], "%Y-%m-%d").date() <= today]

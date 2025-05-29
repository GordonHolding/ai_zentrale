# memory_triggers.py – Triggerlogik für MemoryAgent

import datetime
from agents.Infrastructure_Agents.MemoryAgent import memory_log
from agents.Infrastructure_Agents.MemoryAgent import memory_config
from agents.Infrastructure_Agents.MemoryAgent import memory_agent
from modules.output_infrastruktur import drive_indexer

# 📌 Trigger bei Systemstart – Initialisierung des Memory Logs
def trigger_on_startup():
    timestamp = datetime.datetime.now().isoformat()
    memory_log.log_system_start(entries=[
        f"[MemoryAgent] Initialisiert um {timestamp}",
        "Trigger: trigger_on_startup()",
        "Status: GPT-Memory und Verlaufsprotokoll aktiv"
    ])
    print("✅ MemoryAgent bereit (Startup Trigger)")

# 🔁 Trigger bei neuer GPT-Nachricht (z. B. Chainlit oder Routing)
def trigger_on_gpt_message(user_id: str, user_message: str, gpt_reply: str):
    memory_agent.log_user_message(user_id, user_message)
    memory_agent.log_assistant_reply(user_id, gpt_reply)
    log_routing(user_id, user_message, gpt_reply)

# 🧾 GPT-Verlaufs-Log
def log_routing(user_id, user_message, gpt_reply):
    routing_log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "agent": "MemoryAgent",
        "trigger": "trigger_on_gpt_message",
        "user_id": user_id,
        "input": user_message[:100],
        "output": gpt_reply[:100]
    }
    drive_indexer.append_to_log("driveagent_routing_log.json", routing_log)

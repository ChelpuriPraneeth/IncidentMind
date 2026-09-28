import os
from dotenv import load_dotenv

load_dotenv()

from app.services.agent_service import investigate_incident

incident = """
Payments API is returning 503 errors after today's deployment.
API latency increased to 5.2 seconds.
Database CPU is at 94%.
Several customers cannot complete payments.
"""

result = investigate_incident(incident)

print("\n================ INCIDENT =================")
print(result["incident"])

print("\n============= PAST MEMORIES ===============")
for memory in result["memories"]:
    print("\n- " + memory)

print("\n=============== AI ANALYSIS ===============")
print(result["analysis"])
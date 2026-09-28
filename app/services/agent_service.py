import os

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()


# ============================================================
# Configuration
# ============================================================

BANK_ID = "incidentmind_final"
MODEL = "openai/gpt-oss-120b"


# ============================================================
# Clients
# ============================================================

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# Investigate Incident
# ============================================================

def investigate_incident(
    incident: str,
    incident_id: str,
    service: str,
    severity: str,
    reported_at: str,
) -> dict:

    incident_context = f"""
Incident ID: {incident_id}
Service: {service}
Severity: {severity}
Reported At: {reported_at}

Incident Description:
{incident}
"""

    # --------------------------------------------------------
    # 1. Recall relevant historical incidents
    # --------------------------------------------------------

    memory_result = hindsight.recall(
        bank_id=BANK_ID,
        query=incident_context,
        max_tokens=4000,
        budget="mid",
    )

    # --------------------------------------------------------
    # 2. Remove duplicate memories
    # --------------------------------------------------------

    memories = []
    seen = set()

    for memory in memory_result.results:

        text = memory.text.strip()

        if text and text not in seen:
            memories.append(text)
            seen.add(text)

    # --------------------------------------------------------
    # 3. Prepare historical context
    # --------------------------------------------------------

    memory_context = "\n\n".join(memories)

    if not memory_context:
        memory_context = "No relevant historical incidents found."

    # --------------------------------------------------------
    # 4. AI reasoning prompt
    # --------------------------------------------------------

    prompt = f"""
You are IncidentMind, an AI production incident response engineer.

CURRENT INCIDENT
{incident_context}

RELEVANT HISTORICAL MEMORIES
{memory_context}

Analyze this incident using historical evidence.

Return exactly these sections:

1. Incident Summary
2. Relevant Historical Incidents
3. Possible Root Causes
4. Recommended Investigation
5. Recommended Resolution
6. Why the Historical Memory Matters

Rules:

- Clearly separate facts from hypotheses.
- Do not claim a root cause is confirmed without evidence.
- Do not invent logs, metrics, infrastructure details, or events.
- Use historical incidents as evidence, not proof.
- Give practical investigation steps.
- Prefer previously successful resolutions when the evidence supports them.
- Mention uncertainty when the evidence is incomplete.
"""

    # --------------------------------------------------------
    # 5. Groq reasoning
    # --------------------------------------------------------

    response = groq.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful production incident "
                    "response engineer."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_completion_tokens=1500,
    )

    answer = response.choices[0].message.content

    # --------------------------------------------------------
    # 6. Return result
    # --------------------------------------------------------

    return {
        "incident_id": incident_id,
        "service": service,
        "severity": severity,
        "reported_at": reported_at,
        "incident": incident,
        "memory_count": len(memories),
        "memories": memories,
        "analysis": answer,
    }


# ============================================================
# Record Resolution / Learn
# ============================================================

def record_resolution(
    incident: str,
    incident_id: str,
    service: str,
    severity: str,
    resolution: str,
    successful: bool,
    engineer_note: str = "",
    reported_at: str = "",
) -> dict:

    outcome = "SUCCESSFUL" if successful else "UNSUCCESSFUL"

    # --------------------------------------------------------
    # Learning record
    # --------------------------------------------------------

    memory = f"""
Production incident learning record.

Incident ID:
{incident_id}

Service:
{service}

Severity:
{severity}

Reported At:
{reported_at}

Incident:
{incident}

Resolution Attempted:
{resolution}

Outcome:
{outcome}

Engineer Note:
{engineer_note if engineer_note else "No additional note provided."}

Learning:
This incident and its outcome should be considered when investigating
future incidents with similar symptoms, service behavior, and deployment
patterns.
"""

    # --------------------------------------------------------
    # Store learning in Hindsight
    # --------------------------------------------------------

    hindsight.retain(
        bank_id=BANK_ID,
        content=memory.strip(),
    )

    return {
        "status": "stored",
        "incident_id": incident_id,
        "service": service,
        "severity": severity,
        "reported_at": reported_at,
        "outcome": outcome,
        "message": "Resolution outcome stored in long-term memory.",
    }
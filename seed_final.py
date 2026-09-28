import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "incidentmind_final"

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

try:
    client.create_bank(
        bank_id=BANK_ID,
        name="IncidentMind Final",
        background=(
            "Production incident history covering root causes, "
            "successful resolutions, and engineering lessons."
        ),
    )
except Exception:
    pass

incidents = [
"""Incident ID: INC-2041
Service: payments-api
Severity: CRITICAL
Incident: Payment API returned 503 errors after a deployment.
Root cause: Database connection leak exhausted the connection pool.
Resolution: Rolled back the deployment and fixed connection handling.
Outcome: SUCCESSFUL
Lesson: Monitor connection-pool metrics after releases.""",

"""Incident ID: INC-2087
Service: orders-api
Severity: HIGH
Incident: Order search latency increased after a schema migration.
Root cause: Missing index on customer_id.
Resolution: Added the index and verified the query plan.
Outcome: SUCCESSFUL
Lesson: Validate critical indexes after migrations.""",

"""Incident ID: INC-2134
Service: auth-service
Severity: CRITICAL
Incident: Users could not authenticate after a security configuration update.
Root cause: Incorrect JWT signing configuration.
Resolution: Restored the previous configuration and redeployed.
Outcome: SUCCESSFUL
Lesson: Validate authentication configuration before production rollout.""",

"""Incident ID: INC-2198
Service: inventory-api
Severity: HIGH
Incident: Inventory requests timed out during traffic increase.
Root cause: Redis failure caused heavy database fallback.
Resolution: Restored Redis capacity and increased database resources.
Outcome: SUCCESSFUL
Lesson: Monitor cache health and database fallback load together.""",

"""Incident ID: INC-2240
Service: notification-api
Severity: MEDIUM
Incident: Email notifications were delayed after a worker deployment.
Root cause: Message queue backlog.
Resolution: Scaled workers and corrected concurrency settings.
Outcome: SUCCESSFUL
Lesson: Monitor queue depth after worker deployments.""",

"""Incident ID: INC-2315
Service: payments-api
Severity: HIGH
Incident: Payment latency increased with intermittent 503 responses.
Root cause: A new query caused excessive database scans.
Resolution: Optimized the query and added a supporting index.
Outcome: SUCCESSFUL
Lesson: Compare query plans before and after payment-service releases."""
]

print("Creating final demo memory...")

for incident in incidents:
    client.retain(
        bank_id=BANK_ID,
        content=incident
    )

print("FINAL DEMO BANK READY")
print(BANK_ID)

client.close()
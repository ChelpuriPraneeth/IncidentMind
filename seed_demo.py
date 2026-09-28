import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = "incidentmind_demo"

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

try:
    client.create_bank(
        bank_id=BANK_ID,
        name="IncidentMind Demo",
        background=(
            "Production incident history including symptoms, root causes, "
            "resolutions, outcomes, and engineering lessons."
        ),
    )
except Exception:
    pass


incidents = [

    """
Incident ID: INC-2041
Service: payments-api
Severity: CRITICAL

Incident:
Payment requests began returning 503 errors after a deployment.
Database CPU increased sharply and request latency increased.

Root cause:
A database connection leak in the new release exhausted the connection pool.

Resolution:
Rolled back the deployment and fixed connection handling.

Outcome:
SUCCESSFUL

Engineer lesson:
Always compare connection-pool metrics before and after major releases.
""",

    """
Incident ID: INC-2087
Service: orders-api
Severity: HIGH

Incident:
Order search latency increased significantly after a schema migration.

Root cause:
A frequently queried customer_id column was missing its database index.

Resolution:
Added the missing index and verified the query execution plan.

Outcome:
SUCCESSFUL

Engineer lesson:
Validate critical indexes after every database migration.
""",

    """
Incident ID: INC-2134
Service: auth-service
Severity: CRITICAL

Incident:
Users received authentication failures after a security configuration update.

Root cause:
The JWT signing configuration was changed incorrectly during deployment.

Resolution:
Restored the previous signing configuration and redeployed.

Outcome:
SUCCESSFUL

Engineer lesson:
Validate authentication configuration in staging before production rollout.
""",

    """
Incident ID: INC-2198
Service: inventory-service
Severity: HIGH

Incident:
Inventory API requests timed out during a traffic increase.

Root cause:
Redis cache nodes became unavailable and requests fell back to expensive database queries.

Resolution:
Restored Redis capacity and temporarily increased database resources.

Outcome:
SUCCESSFUL

Engineer lesson:
Monitor cache availability and database fallback load together.
""",

    """
Incident ID: INC-2240
Service: notification-api
Severity: MEDIUM

Incident:
Email notifications were delayed by more than 20 minutes.

Root cause:
The message queue accumulated a large backlog after a worker deployment.

Resolution:
Scaled workers, cleared the backlog, and corrected worker concurrency settings.

Outcome:
SUCCESSFUL

Engineer lesson:
Monitor queue depth immediately after worker deployments.
""",

    """
Incident ID: INC-2315
Service: payments-api
Severity: CRITICAL

Incident:
Payment API latency increased and intermittent 503 responses appeared after a release.

Root cause:
A new payment query caused excessive database scans.

Resolution:
Optimized the query, added a supporting index, and rolled back the release temporarily.

Outcome:
SUCCESSFUL

Engineer lesson:
Compare database query plans before and after payment-service releases.
""",

]

print("Seeding IncidentMind demo memory...")

for incident in incidents:
    client.retain(
        bank_id=BANK_ID,
        content=incident.strip(),
    )
    print("Stored:", incident.split("Incident ID: ")[1].split("\n")[0])

print()
print("DEMO MEMORY READY")
print("Bank:", BANK_ID)

client.close()
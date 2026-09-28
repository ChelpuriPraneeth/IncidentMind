import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

BANK_ID = "incidentmind"

print("Creating memory bank...")

client.create_bank(
    bank_id=BANK_ID,
    name="IncidentMind",
    background="Memory for production incidents, root causes, resolutions, and lessons learned.",
)

print("Storing incident...")

client.retain(
    bank_id=BANK_ID,
    content=(
        "Incident INC-1001 affected payments-api. "
        "API latency increased to 4.8 seconds and database CPU reached 91%. "
        "Root cause was a missing database index on orders.customer_id after deployment. "
        "The team added the index and rolled back the deployment. "
        "The resolution successfully restored normal latency."
    ),
)

print("Recalling memory...")

result = client.recall(
    bank_id=BANK_ID,
    query="What happened in the previous payments API incident and how was it fixed?",
)

for memory in result.results:
    print("\nMEMORY:")
    print(memory.text)

print("\nHINDSIGHT TEST SUCCESS")
client.close()
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

BANK_ID = "feedbackos"


print("Connecting to Hindsight...")

# Create our memory bank
client.create_bank(
    bank_id=BANK_ID,
    name="FeedbackOS"
)

print("Memory bank created!")

# Store our first customer feedback
client.retain(
    bank_id=BANK_ID,
    content=(
        "Customer Sarah Chen reported that she could not find "
        "the report export option in the product."
    ),
    context="Customer product feedback"
)

print("Feedback stored!")

# Search the memory
result = client.recall(
    bank_id=BANK_ID,
    query="What problem did Sarah Chen have with the product?"
)

print("\n--- HINDSIGHT RECALL ---")

for memory in result.results:
    print(memory.text)

print("\nHindsight test complete!")
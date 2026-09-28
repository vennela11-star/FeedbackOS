import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()


class FeedbackMemory:
    def __init__(self):
        self.bank_id = os.getenv("HINDSIGHT_BANK_ID", "feedbackos")

        self.client = Hindsight(
            base_url=os.getenv("HINDSIGHT_API_URL"),
            api_key=os.getenv("HINDSIGHT_API_KEY"),
        )

    def remember_feedback(self, feedback_text: str):
        return self.client.retain(
            bank_id=self.bank_id,
            content=feedback_text,
            context="Customer product feedback",
        )

    def recall_related_feedback(self, query: str):
        return self.client.recall(
            bank_id=self.bank_id,
            query=query,
        )

    def close(self):
        """
        Close the Hindsight client's HTTP resources.
        """
        try:
            self.client.close()
        except Exception:
            pass
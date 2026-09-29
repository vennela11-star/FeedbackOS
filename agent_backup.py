from groq import Groq
from dotenv import load_dotenv
import os

from memory import FeedbackMemory
from models import Feedback


load_dotenv()


class FeedbackOSAgent:

    def __init__(self):
        self.memory = FeedbackMemory()

        self.llm = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def add_feedback(self, feedback: Feedback):
        memory_text = feedback.to_memory_text()

        self.memory.remember_feedback(memory_text)

        return {
            "status": "stored",
            "feedback": feedback.message,
        }

    def analyze(self, question: str):
        memories = self.memory.recall_related_feedback(question)

        context = "\n\n".join(
            memory.text for memory in memories.results
        )

        prompt = f"""
You are FeedbackOS, an AI product-feedback analyst.

Analyze customer feedback across time.

Historical feedback:
{context}

Product team's question:
{question}

Identify:
1. Recurring themes
2. Important customer problems
3. Evidence from the feedback
4. Whether the issue appears to be increasing, decreasing, or unclear
5. Important contradictions

Do not invent evidence that is not present.

Give a concise answer for a product team.
"""

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return response.choices[0].message.content
    
    def close(self):
        self.memory.close()
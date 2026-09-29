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

        if not memories.results:
            return "No relevant customer feedback was found in memory."

        context_parts = []

        for memory in memories.results:
            context_parts.append(memory.text)

        context = "\n\n--- FEEDBACK RECORD ---\n\n".join(context_parts)

        prompt = f"""
You are FeedbackOS, an AI customer-feedback intelligence agent.

Your job is to analyze historical customer feedback using ONLY
the feedback records supplied below.

IMPORTANT RULES:

1. Never invent a customer, date, product change, event, or result.
2. Never assume that a product update happened unless a customer
   explicitly mentions it.
3. Treat every feedback record as independent evidence.
4. Pay close attention to dates and customer names.
5. Distinguish FACTS from INFERENCES.
6. If the evidence is insufficient, say "Unclear from the available feedback."
7. Do not turn an inference into a fact.
8. When counting customers, count distinct customer names only.
9. When describing a trend, explain which dated feedback supports it.
10. Do not recommend a solution unless you clearly label it as a
    recommendation rather than customer evidence.

Your analysis should focus on PROBLEM EVOLUTION:

- What problem appeared first?
- Which customers experienced it?
- Did the same problem appear repeatedly?
- What changed later?
- Did later feedback indicate improvement?
- Did a new problem appear afterward?
- What remains uncertain?
- What should the product team investigate next?

CUSTOMER FEEDBACK FROM HINDSIGHT:

{context}

PRODUCT TEAM QUESTION:

{question}

Return the answer using exactly these sections:

## 1. First Problem

State the earliest recurring problem and cite the relevant
customer and date from the supplied feedback.

## 2. Customers Affected

List the distinct customers who reported that problem.

## 3. Problem Evolution

Explain chronologically how the feedback changed over time.

## 4. Evidence of Improvement

State whether later feedback shows improvement.

Separate:
- Direct evidence
- Inference

## 5. New Problems

Identify any new problem that appeared later.

## 6. Contradictions or Uncertainty

Identify conflicting feedback or anything that cannot be
determined from the available records.

## 7. Recommended Investigation

Give practical recommendations for the product team.
Clearly label these as recommendations, not facts.

Remember:
The customer feedback is the source of truth.
Do not invent missing information.
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
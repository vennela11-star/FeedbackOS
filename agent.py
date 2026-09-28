import os

from dotenv import load_dotenv
from groq import Groq

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

        self.memory.remember_feedback(
            memory_text
        )

        return {
            "status": "stored",
            "feedback": feedback.message,
        }

    def analyze(self, question: str):

        memories = self.memory.recall_related_feedback(
            question
        )

        if not memories.results:
            return "No related customer feedback was found."

        context_parts = []

        for memory in memories.results:
            context_parts.append(memory.text)

        context = "\n\n--- FEEDBACK RECORD ---\n\n".join(
            context_parts
        )

        prompt = f"""
You are FeedbackOS, an AI product-feedback intelligence agent.

Your job is to analyze customer feedback history and help a product team
understand how customer problems evolve over time.

IMPORTANT EVIDENCE RULES:

- Use ONLY the customer feedback provided below.
- Do not invent customers, dates, product changes, events, or evidence.
- Every factual claim must be supported by the provided feedback.
- Clearly distinguish DIRECT EVIDENCE from INFERENCE.
- If the evidence is insufficient, say "Not enough evidence."
- Do not treat a customer's suggestion as proof that the product team
  implemented it.
- Do not assume that a product change happened unless the feedback explicitly
  says that it happened.
- Do not speculate about why a problem improved or returned.
- Do not assume differences in user roles, permissions, browsers, devices,
  versions, tenants, rollout status, or environments unless the feedback
  explicitly provides evidence for them.
- If the reason for a change is unknown, say:
  "Reason not established by the feedback."
- Pay attention carefully to dates and customer names.
- Identify whether multiple customers experienced the same problem.
- Treat duplicate feedback as duplicate evidence, not as additional
  independent customers.
- Do not automatically assume two similar customer names are the same
  customer.
- If customer identity is uncertain, explicitly say so.
- Do not turn an inference into a fact.
- Keep the chronological order of events accurate.

CUSTOMER FEEDBACK HISTORY:

{context}

PRODUCT TEAM QUESTION:

{question}

Return the analysis using exactly these sections:

## 1. First recurring problem

State the earliest recurring customer problem.

Provide supporting evidence using:
- Customer
- Date
- Feedback

Only call something recurring when the provided evidence shows that
multiple customers reported the same or substantially similar problem.

## 2. Customers affected

List the distinct customers who reported that problem.

Do not count the same customer twice.

If two customer names might refer to the same organization but the feedback
does not establish that, keep them separate and mention the uncertainty.

## 3. Problem evolution

Explain chronologically how the customer feedback changed over time.

Separate:

- Early problem
- Repeated reports
- Direct evidence of improvement
- Later reports
- Newly emerging problems

Do not invent reasons for why the problem changed.

If the reason for a change is unknown, state:

"Reason not established by the feedback."

## 4. Evidence of improvement

Separate the evidence into:

### Direct evidence

Only include statements where a customer directly reports that a previously
reported problem became easier, better, resolved, or otherwise improved.

### Inference

Explain patterns that may suggest improvement, but clearly label them as
inference.

Do not present inference as fact.

If there is no direct evidence of improvement, say:

"Not enough evidence of direct improvement."

## 5. New problems

Identify problems that appeared later in the feedback history.

For each problem provide:

- Problem
- First known date
- Customers reporting it
- Supporting evidence

Do not assume that a later problem replaced an earlier problem unless the
feedback explicitly supports that conclusion.

## 6. Contradictions and uncertainty

Identify:

- Conflicting feedback
- Duplicate feedback
- Missing dates
- Missing customer names
- Uncertain customer identity
- Claims that cannot be verified from the provided feedback
- Any other limitation in the evidence

Do not resolve contradictions by guessing.

## 7. Recommended investigation

Give practical recommendations for the product team to investigate.

IMPORTANT:

Recommendations are NOT customer-stated facts.

Clearly label them as recommendations.

Do not claim that a recommendation has already been implemented.

Keep the answer concise, chronological, and evidence-based.
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

        try:
            self.memory.close()
        except Exception:
            pass
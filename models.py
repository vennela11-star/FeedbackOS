from pydantic import BaseModel


class Feedback(BaseModel):
    customer: str
    date: str
    product: str
    message: str

    def to_memory_text(self):
        return f"""
CUSTOMER: {self.customer}
DATE: {self.date}
PRODUCT: {self.product}
TYPE: customer_feedback
FEEDBACK: {self.message}
""".strip()
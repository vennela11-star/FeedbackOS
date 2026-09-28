from agent import FeedbackOSAgent


agent = FeedbackOSAgent()

try:
    print("FeedbackOS is analyzing the accumulated customer history...\n")

    answer = agent.analyze(
        """
        Analyze the customer feedback history for the Reports feature.

        I want to know:
        1. What recurring problem appeared first?
        2. How many different customers reported it?
        3. What changed later?
        4. Did customer feedback indicate that the original problem improved?
        5. What new problem appeared after the improvement?
        6. What should the product team investigate next?

        Use only evidence found in the recalled customer feedback.
        Clearly separate:
        - Evidence directly stated by customers
        - Inferences based on that evidence
        - Recommendations

        Do not invent product changes, customer details, or events
        that are not present in the recalled feedback.
        """
    )

    print("========== FEEDBACKOS INSIGHT ==========\n")
    print(answer)

finally:
    agent.close()
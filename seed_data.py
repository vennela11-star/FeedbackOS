from agent import FeedbackOSAgent
from models import Feedback


feedback_items = [
    Feedback(
        customer="Acme Corp",
        date="2026-09-04",
        product="Reports",
        message="I couldn't find the CSV export button in Reports."
    ),
    Feedback(
        customer="NovaTech",
        date="2026-09-07",
        product="Reports",
        message="The CSV export option is buried under the three-dot menu."
    ),
    Feedback(
        customer="BrightLabs",
        date="2026-09-10",
        product="Reports",
        message="I had to ask our admin how to download a report as CSV."
    ),
    Feedback(
        customer="Orbit Systems",
        date="2026-09-12",
        product="Reports",
        message="Please make the report export button easier to find."
    ),
    Feedback(
        customer="PixelWorks",
        date="2026-09-13",
        product="Reports",
        message="The export function is useful, but I didn't know where it was."
    ),
    Feedback(
        customer="DataForge",
        date="2026-09-15",
        product="Reports",
        message="The Reports page should have a clearly visible CSV export action."
    ),
    Feedback(
        customer="Acme Corp",
        date="2026-09-23",
        product="Reports",
        message="After the new Reports layout, the CSV export button is much easier to find."
    ),
    Feedback(
        customer="NovaTech",
        date="2026-09-24",
        product="Reports",
        message="I can find the export option immediately now. Much better."
    ),
    Feedback(
        customer="BrightLabs",
        date="2026-09-26",
        product="Reports",
        message="The export button is easy to find now, but CSV downloads are slow."
    ),
    Feedback(
        customer="Orbit Systems",
        date="2026-09-27",
        product="Reports",
        message="I can find CSV export now, but a large report takes too long to download."
    ),
]


agent = FeedbackOSAgent()

try:
    print("Loading customer feedback...\n")

    for feedback in feedback_items:
        result = agent.add_feedback(feedback)

        print(
            f"Stored: {feedback.customer} | "
            f"{feedback.date} | "
            f"{feedback.message}"
        )

    print("\nDataset loaded successfully!")

finally:
    agent.close()
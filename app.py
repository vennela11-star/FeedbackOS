import streamlit as st
from datetime import date

from agent import FeedbackOSAgent
from models import Feedback


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="FeedbackOS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        .hero {
            padding: 1.8rem;
            border-radius: 18px;
            background: linear-gradient(
                135deg,
                #111827 0%,
                #1e293b 100%
            );
            color: white;
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin-bottom: 0.4rem;
            font-size: 2.5rem;
        }

        .hero p {
            color: #cbd5e1;
            font-size: 1.05rem;
        }

        .feature-card {
            padding: 1.2rem;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            background: white;
            min-height: 120px;
        }

        .feature-card h3 {
            margin-bottom: 0.4rem;
        }

        .section-card {
            padding: 1.4rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            background: white;
            margin-bottom: 1rem;
        }

        .success-box {
            padding: 1rem;
            border-radius: 12px;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
        }

        .info-box {
            padding: 1rem;
            border-radius: 12px;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e40af;
        }

        .footer {
            text-align: center;
            color: #64748b;
            padding: 2rem 0;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "agent" not in st.session_state:
    st.session_state.agent = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None


# ---------------------------------------------------------
# AGENT INITIALIZATION
# ---------------------------------------------------------

@st.cache_resource
def get_agent():
    return FeedbackOSAgent()


try:
    agent = get_agent()
except Exception as e:
    st.error("FeedbackOS could not initialize.")
    st.exception(e)
    st.stop()

st.session_state.agent = agent


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🧠 FeedbackOS</h1>
        <p>
            Customer feedback intelligence powered by memory + AI
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# TOP FEATURE CARDS
# ---------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 Memory</h3>
            <p>Long-term customer feedback</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🔎 Evidence</h3>
            <p>Customer + date evidence</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📈 Evolution</h3>
            <p>Problems across time</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🤖 AI Analysis</h3>
            <p>Evidence-based insights</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ FeedbackOS System")

    st.success("🧠 Memory\n\nHindsight")
    st.success("🔎 Retrieval\n\nEnabled")
    st.success("🤖 Analysis\n\nAI-powered")

    st.metric(
        "📊 Analysis Modes",
        "5",
    )

    st.divider()

    st.subheader("How FeedbackOS works")

    st.markdown(
        """
        **🧠 Memory**

        Customer feedback is retained so the system can reason across
        feedback collected at different times.

        **🔎 Evidence**

        Analyses are grounded in feedback recalled from memory.

        **📈 Evolution**

        FeedbackOS examines how customer problems change over time.
        """
    )


# ---------------------------------------------------------
# ADD FEEDBACK
# ---------------------------------------------------------

st.markdown("## ➕ Add Customer Feedback")

st.markdown(
    """
    <div class="section-card">
        Add a new customer feedback record to FeedbackOS memory.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("feedback_form", clear_on_submit=False):

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input(
            "Customer name",
            placeholder="Example: Acme Corp",
        )

    with col2:
        feedback_date = st.date_input(
            "Feedback date",
            value=date.today(),
        )

    product_name = st.text_input(
        "Product",
        placeholder="Example: Reports",
    )

    feedback_message = st.text_area(
        "Customer feedback",
        placeholder=(
            "Example: The CSV export button is difficult to find "
            "because it is hidden under the three-dot menu."
        ),
        height=150,
    )

    submitted = st.form_submit_button(
        "💾 Store Feedback",
        use_container_width=True,
        type="primary",
    )


# ---------------------------------------------------------
# STORE FEEDBACK
# ---------------------------------------------------------

if submitted:

    if not customer_name.strip():
        st.error("Please enter a customer name.")

    elif not product_name.strip():
        st.error("Please enter a product name.")

    elif not feedback_message.strip():
        st.error("Please enter customer feedback.")

    else:

        try:

            feedback = Feedback(
                customer=customer_name.strip(),
                date=str(feedback_date),
                product=product_name.strip(),
                message=feedback_message.strip(),
            )

            result = agent.add_feedback(feedback)

            st.session_state.last_feedback = {
                "customer": customer_name.strip(),
                "product": product_name.strip(),
                "date": str(feedback_date),
                "message": feedback_message.strip(),
            }

            st.success("✅ Feedback successfully stored in FeedbackOS memory.")

            with st.expander("View stored feedback", expanded=True):

                st.write(
                    f"**Customer:** {customer_name.strip()}"
                )

                st.write(
                    f"**Product:** {product_name.strip()}"
                )

                st.write(
                    f"**Date:** {feedback_date}"
                )

                st.write(
                    f"**Feedback:** {feedback_message.strip()}"
                )

        except Exception as e:

            st.error("❌ Feedback could not be stored.")

            st.exception(e)


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

st.markdown("---")

st.markdown("## 🔎 Analyze Customer Feedback")

st.markdown(
    """
    <div class="info-box">
        FeedbackOS searches its accumulated customer feedback and
        generates an evidence-based analysis.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


analysis_modes = {
    "Customer feedback overview": (
        "Give me an overall analysis of the customer feedback. "
        "Identify the earliest recurring problem, affected customers, "
        "problem evolution, evidence of improvement, new problems, "
        "contradictions, uncertainty, and recommended investigation."
    ),

    "Problem evolution": (
        "Analyze how customer problems have evolved over time. "
        "Focus on the chronological sequence of problems, improvements, "
        "and newly emerging problems."
    ),

    "Recurring problems": (
        "Identify the earliest recurring customer problems. "
        "Group feedback from different customers that describes the "
        "same underlying issue."
    ),

    "Evidence of improvement": (
        "Identify direct evidence that previously reported customer "
        "problems improved or were resolved. Clearly separate direct "
        "evidence from inference."
    ),

    "New problems": (
        "Identify problems that appeared later in the customer feedback "
        "history. Explain when they appeared and which customers reported them."
    ),
}


analysis_mode = st.radio(
    "Analysis mode",
    list(analysis_modes.keys()),
    horizontal=True,
)

st.write("")


custom_question = st.text_area(
    "Ask your own question (optional)",
    placeholder=(
        "Example: Which customer problem appears most frequently "
        "and how has it changed over time?"
    ),
    height=100,
)

if custom_question.strip():

    question = custom_question.strip()

else:

    question = analysis_modes[analysis_mode]


if st.button(
    "🧠 Analyze Feedback",
    use_container_width=True,
    type="primary",
):

    with st.spinner("Searching feedback memory and generating analysis..."):

        try:

            result = agent.analyze(question)

            st.session_state.analysis_result = result

        except Exception as e:

            st.session_state.analysis_result = None

            st.error("❌ Analysis failed.")

            st.exception(e)


# ---------------------------------------------------------
# DISPLAY ANALYSIS
# ---------------------------------------------------------

if st.session_state.analysis_result:

    st.markdown("---")

    st.markdown("## 💡 FeedbackOS Insight")

    st.markdown(
        st.session_state.analysis_result
    )



# ---------------------------------------------------------
# DECISION LAYERS
# ---------------------------------------------------------

st.markdown("---")

st.markdown("## 🧭 Decision Layers")

d1, d2, d3 = st.columns(3)

with d1:

    st.markdown(
        """
        ### 🔎 Evidence

        What customers directly reported, including dates
        and customer references.
        """
    )

with d2:

    st.markdown(
        """
        ### 🧠 Inference

        Patterns FeedbackOS identifies from recalled
        customer history.
        """
    )

with d3:

    st.markdown(
        """
        ### 💡 Recommendation

        Potential areas for the product team to investigate.

        Recommendations are not customer-stated facts.
        """
    )


# ---------------------------------------------------------
# WHAT MAKES FEEDBACKOS DIFFERENT
# ---------------------------------------------------------

st.markdown("---")

st.markdown("## What makes FeedbackOS different?")

w1, w2, w3 = st.columns(3)

with w1:

    st.markdown(
        """
        ### 🧠 Memory

        Customer feedback is retained so the system can
        reason across feedback collected at different times.
        """
    )

with w2:

    st.markdown(
        """
        ### 🔎 Evidence

        Analyses are grounded in feedback recalled from
        memory rather than treating every message as an
        isolated event.
        """
    )

with w3:

    st.markdown(
        """
        ### 📈 Evolution

        FeedbackOS examines how customer problems change
        over time, including improvements and newly emerging problems.
        """
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        FeedbackOS • Customer Feedback Intelligence
    </div>
    """,
    unsafe_allow_html=True,
)
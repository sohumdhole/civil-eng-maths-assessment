import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Civil Eng Math Assessment",
    page_icon="🎓",
    layout="wide"
)

# Shared styles and colour config
ATU_TEAL = "#005F73"

st.markdown(f"""
<style>
    /* Styling headers with ATU Teal */
    h1, h2, h3, h4 {{
        color: {ATU_TEAL};
    }}
    /* Simple styling for key buttons if needed */
    div.stButton > button:first-child {{
        background-color: {ATU_TEAL};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

st.title("Civil Engineering Mathematics Assessment Tool")

st.markdown(f"""
Welcome to the companion assessment portal for the **Engineering Mathematics Toolkit**. 
This application is tailored for civil engineering students to rigorously test their applied mathematical knowledge.

[🔗 Visit the Engineering Mathematics Toolkit](https://engineering-mathematics-toolkit-atx8ku78wlsyqoqqrzzgew.streamlit.app/)

### Features
* **📝 Problem Bank**: Explore problems filtered by topic and difficulty level. Drill down into worked solutions and common pitfalls.
* **🎯 Diagnostic Test**: Take a 10-question evaluation to identify your strengths and topics requiring further study.
* **📈 Progress Tracker**: Visualize your attempt history and monitor your subject proficiency.
* **🏫 Lecturer Dashboard**: (For Educators) View aggregated cohort analytics.

---
Please select a module from the **sidebar** to get started.
""")

# Initialize session state globally required variables if they don't exist
if 'tracker_data' not in st.session_state:
    st.session_state.tracker_data = []  # List of dicts: {'topic': ..., 'confidence': ...}
if 'diagnostic_active' not in st.session_state:
    st.session_state.diagnostic_active = False
if 'test_problems' not in st.session_state:
    st.session_state.test_problems = []
if 'test_current_q' not in st.session_state:
    st.session_state.test_current_q = 0
if 'test_responses' not in st.session_state:
    st.session_state.test_responses = []

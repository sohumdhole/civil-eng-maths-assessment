import streamlit as st
import json
import random
import os

# Page config
st.set_page_config(page_title="Problem Bank", page_icon="📝", layout="wide")

ATU_TEAL = "#005F73"
st.markdown(f"""
<style>
    h1, h2, h3, h4 {{ color: {ATU_TEAL}; }}
    div.stButton > button:first-child {{
        background-color: {ATU_TEAL};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_problems():
    try:
        # Resolves via Streamlit Cloud's root cwd, defaulting back if needed
        file_path = "problems.json"
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'problems.json')
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("problems", [])
    except FileNotFoundError:
        st.error("problems.json not found. Please upload it alongside app.py.")
        return []
    except json.JSONDecodeError:
        st.error("Error decoding problems.json. Please check the file format.")
        return []

problems = load_problems()

st.title("📝 Problem Bank")
st.markdown("Filter practice problems by topic and difficulty level.")

if not problems:
    st.info("Waiting for problem data...")
    st.stop()

# Define available filters
topics = sorted(list(set(p.get("topic", "Unknown") for p in problems)))
levels = sorted(list(set(p.get("level", "Unknown") for p in problems)))

# Sidebar filters
st.sidebar.header("Filter Problems")
selected_topic = st.sidebar.selectbox("Select Topic", ["All"] + topics)
selected_level = st.sidebar.selectbox("Select Level", ["All"] + levels)

# Filter logic
filtered_problems = problems
if selected_topic != "All":
    filtered_problems = [p for p in filtered_problems if p.get("topic") == selected_topic]
if selected_level != "All":
    filtered_problems = [p for p in filtered_problems if p.get("level") == selected_level]

if not filtered_problems:
    st.warning("No problems match the selected filters. Please adjust your criteria.")
else:
    # State management for random problem index
    if 'current_problem_idx' not in st.session_state:
        st.session_state.current_problem_idx = 0
    
    # Ensure index is within range of currently filtered problems
    if st.session_state.current_problem_idx >= len(filtered_problems):
        st.session_state.current_problem_idx = 0
        
    current_problem = filtered_problems[st.session_state.current_problem_idx]
    
    st.subheader(f"Topic: {current_problem.get('topic')} | Level: {current_problem.get('level')}")
    st.markdown(f"### {current_problem.get('title', '')}")
    st.markdown(f"**Scenario:** {current_problem.get('scenario')}")
    st.info(f"**Question:** {current_problem.get('question')}")
    
    with st.expander("Show Worked Solution"):
        st.markdown(current_problem.get('worked_solution'))
        if current_problem.get('common_mistake'):
            st.warning(f"**Common Mistake:** {current_problem.get('common_mistake')}")
            
    if st.button("Next Problem"):
        st.session_state.current_problem_idx = random.randint(0, len(filtered_problems)-1)
        st.rerun()

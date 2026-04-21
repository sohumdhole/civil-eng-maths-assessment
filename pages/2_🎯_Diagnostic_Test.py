import streamlit as st
import json
import random
import os
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Diagnostic Test", page_icon="🎯", layout="wide")

ATU_TEAL = "#005F73"
st.markdown(f"""
<style>
    h1, h2, h3, h4 {{ color: {ATU_TEAL}; }}
    div.stButton > button:first-child {{
        background-color: {ATU_TEAL};
        color: white;
    }}
    .stProgress > div > div > div > div {{
        background-color: {ATU_TEAL};
    }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_problems():
    try:
        file_path = "problems.json"
        if not os.path.exists(file_path):
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'problems.json')
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("problems", [])
    except Exception:
        return []

problems = load_problems()

st.title("🎯 Diagnostic Test")

if 'tracker_data' not in st.session_state:
    st.session_state.tracker_data = []

# State management for Diagnostic Test
if 'diagnostic_active' not in st.session_state:
    st.session_state.diagnostic_active = False
if 'test_problems' not in st.session_state:
    st.session_state.test_problems = []
if 'test_current_q' not in st.session_state:
    st.session_state.test_current_q = 0
if 'test_responses' not in st.session_state:
    st.session_state.test_responses = [] # Store tuple of (topic, confidence_level)

def start_diagnostic():
    if not problems:
        st.error("No problems available to start Diagnostic.")
        return
        
    topics = list(set(p.get('topic') for p in problems if p.get('topic')))
    test_set = []
    
    # Try to grab up to 2 problems per topic
    for t in topics:
        topic_problems = [p for p in problems if p.get('topic') == t]
        samples = random.sample(topic_problems, min(2, len(topic_problems)))
        test_set.extend(samples)
        
    # If not enough, pad with randoms to 10
    if len(test_set) < 10 and len(problems) >= 10:
        remaining = [p for p in problems if p not in test_set]
        needed = 10 - len(test_set)
        test_set.extend(random.sample(remaining, min(needed, len(remaining))))
        
    random.shuffle(test_set)
    st.session_state.test_problems = test_set[:10]
    st.session_state.test_current_q = 0
    st.session_state.test_responses = []
    st.session_state.diagnostic_active = True
    st.rerun()

if not st.session_state.diagnostic_active and not st.session_state.test_responses:
    st.markdown("""
    Welcome to the Diagnostic! You will be presented with 10 random problems spanning various topics.
    For each problem, read it and evaluate your confidence in solving it.
    """)
    st.button("Start Diagnostic Test", on_click=start_diagnostic)

elif st.session_state.diagnostic_active:
    total_q = len(st.session_state.test_problems)
    current_q_idx = st.session_state.test_current_q
    
    if current_q_idx < total_q:
        q_data = st.session_state.test_problems[current_q_idx]
        
        # Progress bar
        progress = (current_q_idx) / total_q
        st.progress(progress, text=f"Question {current_q_idx + 1} of {total_q}")
        
        st.subheader(f"Topic: {q_data.get('topic')} ({q_data.get('level')})")
        st.markdown(f"**Scenario:** {q_data.get('scenario')}")
        st.info(f"**Question:** {q_data.get('question')}")
        
        st.write("How confident are you that you can solve this?")
        
        col1, col2, col3 = st.columns(3)
        def log_response(confidence):
            st.session_state.test_responses.append((q_data.get('topic'), confidence))
            st.session_state.tracker_data.append({'topic': q_data.get('topic'), 'confidence': confidence})
            st.session_state.test_current_q += 1

        with col1:
            st.button("Confident", key="conf_1", on_click=log_response, args=("Confident",), use_container_width=True)
        with col2:
            st.button("Unsure", key="conf_2", on_click=log_response, args=("Unsure",), use_container_width=True)
        with col3:
            st.button("No Idea", key="conf_3", on_click=log_response, args=("No Idea",), use_container_width=True)
            
    else:
        # Finished
        st.success("Diagnostic Test Complete!")
        
        # Analyze Responses
        # Map: Confident -> 2, Unsure -> 1, No Idea -> 0 for radar
        score_map = {"Confident": 2, "Unsure": 1, "No Idea": 0}
        
        topic_scores = {}
        topic_counts = {}
        for topic, conf in st.session_state.test_responses:
            topic_scores[topic] = topic_scores.get(topic, 0) + score_map[conf]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
        avg_scores = {t: topic_scores[t] / topic_counts[t] for t in topic_scores}
        
        # Radar Chart
        df_radar = pd.DataFrame(dict(
            r=list(avg_scores.values()),
            theta=list(avg_scores.keys())
        ))
        
        if not df_radar.empty:
            fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 2], markers=True)
            fig.update_traces(fill='toself', line_color=ATU_TEAL)
            fig.update_layout(title="Topic Strength Analysis (0=Weak, 2=Strong)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary Table of Weak Topics
        weak_topics = [t for t, s in avg_scores.items() if s < 1.5]
        if weak_topics:
            st.warning("Based on your responses, we recommend revisiting the following modules:")
            recommendations = []
            for t in weak_topics:
                recommendations.append({"Weak Topic": t, "Recommended Module (Eng. Math Toolkit)": f"Module: {t}"})
            st.table(pd.DataFrame(recommendations))
        else:
            st.success("Great job! You seem confident across the evaluated topics.")
            
        if st.button("Retake Diagnostic"):
            st.session_state.diagnostic_active = False
            st.session_state.test_responses = []
            st.rerun()

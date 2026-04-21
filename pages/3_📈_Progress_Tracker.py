import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Progress Tracker", page_icon="📈", layout="wide")

ATU_TEAL = "#005F73"
st.markdown(f"""
<style>
    h1, h2, h3, h4 {{ color: {ATU_TEAL}; }}
</style>
""", unsafe_allow_html=True)

st.title("📈 Progress Tracker")

if 'tracker_data' not in st.session_state or not st.session_state.tracker_data:
    st.info("You haven't attempted any diagnostic problems yet. Take the diagnostic test to see your progress here!")
    st.stop()

tracker_df = pd.DataFrame(st.session_state.tracker_data)

total_problems = len(tracker_df)
topics_attempted = tracker_df['topic'].nunique()
score_map = {"Confident": 2, "Unsure": 1, "No Idea": 0}
tracker_df['score'] = tracker_df['confidence'].map(score_map)

topic_avg = tracker_df.groupby('topic')['score'].mean().reset_index()
topic_avg = topic_avg.sort_values(by='score', ascending=False)
strongest_topic = topic_avg.iloc[0]['topic'] if not topic_avg.empty else "N/A"
weakest_topic = topic_avg.iloc[-1]['topic'] if not topic_avg.empty else "N/A"

st.subheader("Motivational Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Problems Attempted", total_problems)
col2.metric("Strongest Topic", strongest_topic)
col3.metric("Weakest Topic", weakest_topic)

st.markdown("---")

# Bar Chart of Problems Attempted per Topic
attempt_counts = tracker_df['topic'].value_counts().reset_index()
attempt_counts.columns = ['Topic', 'Attempts']

fig1 = px.bar(
    attempt_counts, 
    x='Topic', 
    y='Attempts', 
    title="Problems Attempted per Topic",
    color_discrete_sequence=[ATU_TEAL]
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("Improvement Trend Tracker")
st.markdown("As you attempt more diagnostic sessions, your confidence profile develops. Keep it up!")

# Breakdown of Confidence Levels per Topic
confidence_dist = tracker_df.groupby(['topic', 'confidence']).size().reset_index(name='count')
fig2 = px.bar(
    confidence_dist,
    x='topic',
    y='count',
    color='confidence',
    title="Confidence Breakdown per Topic",
    barmode='group',
    color_discrete_map={"Confident": "#2ca02c", "Unsure": "#ff7f0e", "No Idea": "#d62728"}
)
st.plotly_chart(fig2, use_container_width=True)

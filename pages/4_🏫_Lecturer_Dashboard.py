import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Lecturer Dashboard", page_icon="🏫", layout="wide")

ATU_TEAL = "#005F73"
st.markdown(f"""
<style>
    h1, h2, h3, h4 {{ color: {ATU_TEAL}; }}
</style>
""", unsafe_allow_html=True)

st.title("🏫 Lecturer Dashboard")
st.markdown("*Aggregated Analytics for Cohort Tracking*")

st.info("ℹ️ **Note:** This dashboard is designed to complement the Engineering Mathematics Toolkit. "
         "Students use that app to learn concepts, and this app to assess and track their progress.")

# Generate Mock Data for 20 Students
@st.cache_data
def get_mock_cohort_data():
    students = [f"Student_{i:02d}" for i in range(1, 21)]
    topics = ["Calculus", "Trigonometry", "Linear Algebra", "Differential Equations", "Probability & Statistics"]
    
    data = []
    for s in students:
        for t in topics:
            # Random average confidence per topic between 0.0 (No Idea) and 2.0 (Confident)
            # Give Differential Equations a naturally lower score for realism
            if t == "Differential Equations":
                score = np.random.normal(0.8, 0.4)
            elif t == "Linear Algebra":
                score = np.random.normal(1.2, 0.5)
            else:
                score = np.random.normal(1.5, 0.4)
            
            score = max(0.0, min(2.0, score))
            data.append({"Student": s, "Topic": t, "Confidence_Score": score})
            
    return pd.DataFrame(data)

df = get_mock_cohort_data()

st.subheader("Cohort Heatmap: Topics vs Students")
pivot_df = df.pivot(index="Topic", columns="Student", values="Confidence_Score")

fig_heat = px.imshow(
    pivot_df,
    labels=dict(x="Student", y="Topic", color="Avg Confidence"),
    color_continuous_scale="RdYlGn",
    title="Heatmap of Student Confidence Scores (0 = Low, 2 = High)"
)
fig_heat.update_xaxes(side="bottom")
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.subheader("Ranked List of Topics Needing Attention")

topic_performance = df.groupby('Topic')['Confidence_Score'].mean().reset_index()
topic_performance = topic_performance.sort_values(by='Confidence_Score', ascending=True)

st.write("Topics ordered from lowest average cohort confidence to highest:")

# Adding a visual bar indicating the score severity
topic_performance['Status'] = topic_performance['Confidence_Score'].apply(
    lambda x: "🚨 Needs Urgent Review" if x < 1.0 else ("⚠️ Needs Practice" if x < 1.5 else "✅ Doing Well")
)
st.dataframe(
    topic_performance.rename(columns={"Confidence_Score": "Average Score (/2.0)"}),
    hide_index=True,
    use_container_width=True
)

st.markdown("""
### Recommendation
Based on the data above, the topics marked **🚨 Needs Urgent Review** should be targeted for intervention in the next lecture, or students should be explicitly directed to revise those modules in the Engineering Mathematics Toolkit.
""")

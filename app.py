import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Dedicated Mentoring System for Students",
    layout="wide",
    page_icon="🎓"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("final_student_recommendations.csv")

# ---------------------------
# STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown(
"<h1 style='text-align:center;color:#4CAF50;'>🎓 Dedicated Mentoring System for Students</h1>",
unsafe_allow_html=True
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("🔍 Filters")

student = st.sidebar.selectbox("Select Student", df['student_id'])

category_filter = st.sidebar.multiselect(
"Filter by Category",
df['Category'].unique(),
default=df['Category'].unique()
)

cluster_filter = st.sidebar.multiselect(
"Filter by Cluster",
df['cluster'].unique(),
default=df['cluster'].unique()
)

filtered_df = df[
(df['Category'].isin(category_filter)) &
(df['cluster'].isin(cluster_filter))
]

student_data = df[df['student_id'] == student]

# ---------------------------
# KPI CARDS
# ---------------------------
st.subheader("📊 Overall Insights")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(filtered_df))
col2.metric("High Risk", len(filtered_df[filtered_df['Category']=="Red"]))
col3.metric("Top Performers", len(filtered_df[filtered_df['Category']=="Green"]))
col4.metric("Avg SRI", round(filtered_df['SRI'].mean(),2))

# ---------------------------
# STUDENT PROFILE
# ---------------------------
st.subheader("👤 Student Profile")
st.dataframe(student_data)

# ---------------------------
# STUDENT SCORES
# ---------------------------
st.subheader("📈 Student Scores")

col1, col2, col3, col4 = st.columns(4)

col1.metric("APS", round(student_data['APS'].values[0],2))
col2.metric("WWS", round(student_data['WWS'].values[0],2))
col3.metric("PTMS", round(student_data['PTMS'].values[0],2))
col4.metric("CRS", round(student_data['CRS'].values[0],2))

col5, col6 = st.columns(2)

col5.metric("SRI", round(student_data['SRI'].values[0],2))
col6.metric("Category", student_data['Category'].values[0])

# ---------------------------
# CATEGORY + CLUSTER GRAPHS
# ---------------------------
st.subheader("📊 Student Distribution")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(3,2.5))
    filtered_df['Category'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Category Distribution")
    st.pyplot(fig, use_container_width=False)

with col2:
    fig2, ax2 = plt.subplots(figsize=(3,2.5))
    ax2.scatter(filtered_df['APS'], filtered_df['WWS'])
    ax2.set_xlabel("APS")
    ax2.set_ylabel("WWS")
    ax2.set_title("Cluster Analysis")
    st.pyplot(fig2, use_container_width=False)

# ---------------------------
# ACTIVITY ANALYSIS
# ---------------------------
st.subheader("📊 Activity Analysis")

col1, col2 = st.columns(2)

with col1:
    fig3, ax3 = plt.subplots(figsize=(3,2.5))
    ax3.scatter(filtered_df['attendance'], filtered_df['APS'])
    ax3.set_xlabel("Attendance")
    ax3.set_ylabel("APS")
    ax3.set_title("Academic Analysis")
    st.pyplot(fig3, use_container_width=False)

with col2:
    fig4, ax4 = plt.subplots(figsize=(3,2.5))
    ax4.scatter(filtered_df['WWS'], filtered_df['SRI'])
    ax4.set_xlabel("WWS")
    ax4.set_ylabel("SRI")
    ax4.set_title("Wellness Analysis")
    st.pyplot(fig4, use_container_width=False)

col3, col4 = st.columns(2)

with col3:
    fig5, ax5 = plt.subplots(figsize=(3,2.5))
    ax5.scatter(filtered_df['PTMS'], filtered_df['APS'])
    ax5.set_xlabel("PTMS")
    ax5.set_ylabel("APS")
    ax5.set_title("Productivity Analysis")
    st.pyplot(fig5, use_container_width=False)

with col4:
    fig6, ax6 = plt.subplots(figsize=(3,2.5))
    ax6.scatter(filtered_df['CRS'], filtered_df['SRI'])
    ax6.set_xlabel("CRS")
    ax6.set_ylabel("SRI")
    ax6.set_title("Career Readiness")
    st.pyplot(fig6, use_container_width=False)

# ---------------------------
# MENTOR RECOMMENDATION
# ---------------------------
st.subheader("👨‍🏫 Mentor Recommendation")

st.success(f"Mentor Type: {student_data['mentor_type'].values[0]}")
st.info(f"Assigned Mentor: {student_data['assigned_mentor'].values[0]}")
st.warning(f"Intervention Plan: {student_data['intervention'].values[0]}")

# ---------------------------
# HIGH RISK STUDENTS
# ---------------------------
st.subheader("🚨 High Risk Students")

risk_df = filtered_df[filtered_df['Category']=="Red"]

st.dataframe(risk_df[['student_id','SRI','Category']])

# ---------------------------
# TOP PERFORMERS
# ---------------------------
st.subheader("🏆 Top Performer Students")

top_df = filtered_df[filtered_df['Category']=="Green"]

st.dataframe(top_df[['student_id','SRI','Category']])

# ---------------------------
# CLUSTER SUMMARY
# ---------------------------
st.subheader("📊 Cluster Summary")

cluster_summary = filtered_df.groupby('cluster')[['APS','WWS','PTMS','CRS','SRI']].mean()

st.dataframe(cluster_summary)

# ---------------------------
# DOWNLOAD
# ---------------------------
st.download_button(
"📥 Download Report",
filtered_df.to_csv(index=False),
"student_report.csv"
)
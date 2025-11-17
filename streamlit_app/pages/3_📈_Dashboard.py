# pages/3_📈_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

st.title("📈 Student Performance Dashboard")

# ---------- Load data ----------
@st.cache_data
def load_data():
    root = Path(__file__).resolve().parent.parent
    data_path = root / "data" / "students_performance.csv"
    df = pd.read_csv(data_path)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Could not find `data/students_performance.csv`.\n\n"
        "Add your dataset (e.g., Kaggle 'StudentsPerformance') to `data/` and reload."
    )
    st.stop()

st.caption(
    f"Data source: **students_performance.csv** (e.g., Kaggle StudentsPerformance dataset) • "
    f"Last refreshed: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**"
)

st.markdown(
    """
    This dashboard lets you explore student exam scores with interactive filters.
    Filters update the **KPIs and charts together**, creating a small analytics product.
    """
)

st.markdown("---")

# ---------- Sidebar Filters ----------
st.sidebar.header("Dashboard Filters")

# Gender filter
gender_col = "gender" if "gender" in df.columns else None
gender_options = (
    sorted(df[gender_col].dropna().unique())
    if gender_col is not None
    else []
)

if gender_col:
    gender_filter = st.sidebar.multiselect(
        "Select gender(s):",
        options=gender_options,
        default=gender_options,
    )
else:
    gender_filter = None

# Test prep filter
prep_col = "test preparation course" if "test preparation course" in df.columns else None
prep_options = (
    sorted(df[prep_col].dropna().unique())
    if prep_col is not None
    else []
)

if prep_col:
    prep_filter = st.sidebar.multiselect(
        "Select test prep status:",
        options=prep_options,
        default=prep_options,
    )
else:
    prep_filter = None

# Math score slider
min_math = int(df["math score"].min())
max_math = int(df["math score"].max())
math_range = st.sidebar.slider(
    "Filter by math score range:",
    min_value=min_math,
    max_value=max_math,
    value=(min_math, max_math),
    step=1,
)

# Apply filters
filtered_df = df.copy()

if gender_col and gender_filter:
    filtered_df = filtered_df[filtered_df[gender_col].isin(gender_filter)]

if prep_col and prep_filter:
    filtered_df = filtered_df[filtered_df[prep_col].isin(prep_filter)]

filtered_df = filtered_df[
    (filtered_df["math score"] >= math_range[0])
    & (filtered_df["math score"] <= math_range[1])
]

st.markdown("### Filtered Data Overview")
st.caption(f"Showing {filtered_df.shape[0]} students after filters.")

# ---------- KPIs ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Number of students", f"{filtered_df.shape[0]}")

with col2:
    st.metric("Avg math score", f"{filtered_df['math score'].mean():.1f}")

with col3:
    st.metric("Avg reading score", f"{filtered_df['reading score'].mean():.1f}")

with col4:
    st.metric("Avg writing score", f"{filtered_df['writing score'].mean():.1f}")

st.markdown("---")

# ---------- Linked Visuals ----------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Average Scores by Subject (Bar Chart)")
    subject_means = {
        "Math": filtered_df["math score"].mean(),
        "Reading": filtered_df["reading score"].mean(),
        "Writing": filtered_df["writing score"].mean(),
    }
    mean_df = pd.DataFrame(
        {"Subject": list(subject_means.keys()), "Average score": list(subject_means.values())}
    )

    fig_subjects = px.bar(
        mean_df,
        x="Subject",
        y="Average score",
        title="Average Exam Scores (Filtered)",
        labels={"Average score": "Average score (points)"},
        range_y=[0, 100],
    )
    st.plotly_chart(fig_subjects, use_container_width=True)

with right_col:
    st.subheader("Reading vs Writing (Scatter, Filtered)")
    fig_scatter = px.scatter(
        filtered_df,
        x="reading score",
        y="writing score",
        color=gender_col if gender_col else None,
        title="Reading vs Writing (Current Filter Selection)",
        labels={
            "reading score": "Reading score (points)",
            "writing score": "Writing score (points)",
        },
        hover_data=filtered_df.columns,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ---------- Narrative Insights ----------
st.subheader("Dashboard Insights & Limitations")

st.markdown(
    """
    **What users can conclude from this dashboard:**

    - The **KPIs** summarize the current filtered subset: how many students and
      their average scores across subjects.  
    - The **Average Scores by Subject** chart shows whether one subject tends to
      have **higher or lower scores** than others under the selected filters.  
    - The **Reading vs Writing scatter** reveals how tightly those scores track
      together and whether certain groups (e.g., by gender or prep status) cluster.  
    - Changing filters (gender, test prep, math score range) updates **all visuals and KPIs**, 
      enabling “what if” explorations.  

    **Limitations:**

    - The dataset is **context-specific** (students from particular schools),
      so patterns may not generalize to all populations.  
    - Some filters can create very **small sample sizes**, making averages less stable.  
    - The dashboard is **descriptive**, not predictive — it doesn’t explain why 
      certain groups perform differently.  
    """
)

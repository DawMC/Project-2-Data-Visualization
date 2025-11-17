# pages/2_📊_Charts_Gallery.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("📊 EDA Gallery — Student Performance Dataset")

# ---------- Load data ----------
@st.cache_data
def load_data():
    """
    Loads StudentsPerformance.csv from the /data folder.
    Expected columns (from classic Kaggle dataset):
      - gender
      - race/ethnicity
      - parental level of education
      - lunch
      - test preparation course
      - math score
      - reading score
      - writing score
    """
    root = Path(__file__).resolve().parent.parent
    data_path = root / "data" / "StudentsPerformance.csv"
    df = pd.read_csv(data_path)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "❌ Could not find `data/StudentsPerformance.csv`.\n\n"
        "Make sure your file is saved as `StudentsPerformance.csv` in the `data/` folder."
    )
    st.stop()

st.caption(f"Rows: {df.shape[0]} • Columns: {df.shape[1]}")

st.markdown(
    """
    This gallery showcases **four different chart types** using the Students Performance dataset.
    Each chart includes:
    - A **question** it explores  
    - A short **“How to read this chart”** explainer  
    - **Observations** based on what the data show  
    """
)

st.divider()

# ======================================================================================
# CHART 1: Histogram — Distribution of Math Scores
# ======================================================================================

st.subheader("Chart 1 — Distribution of Math Scores (Histogram)")
st.markdown("**Question:** How are math scores distributed across students?")

# interactive: user controls number of bins
bins = st.slider("Number of bins for the histogram:", 5, 50, 20)

fig_hist = px.histogram(
    df,
    x="math score",
    nbins=bins,
    title="Distribution of Math Scores",
    labels={"math score": "Math score (points)"},
)
fig_hist.update_layout(bargap=0.05)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown(
    """
    - The **x-axis** shows ranges of math scores (e.g., 40–50, 50–60).  
    - The **y-axis** shows how many students fall into each score range.  
    - Taller bars mean **more students** in that range.  
    - Changing the number of bins makes the bars **wider or narrower**, revealing more or less detail.  
    """
)

st.markdown("**Observations (example patterns you might see):**")
st.markdown(
    """
    - Most students appear in the **middle-to-high score range**, with fewer at the extremes.  
    - You might see a **slight skew** (more students at the high end or low end depending on the class).  
    - Very low or very high scores are relatively **rare**, which suggests the class is not dominated by extreme outliers.  
    """
)

st.divider()

# ======================================================================================
# CHART 2: Box Plot — Math Scores by Test Preparation Course
# ======================================================================================

st.subheader("Chart 2 — Math Scores by Test Preparation Status (Box Plot)")
st.markdown(
    "**Question:** Do students who completed the test preparation course tend to score higher in math?"
)

# Just in case column name slightly differs, we guard it:
if "test preparation course" not in df.columns:
    st.error(
        "Expected column `test preparation course` not found in dataset. "
        "Check the CSV headers or adjust the code."
    )
else:
    prep_col = "test preparation course"

    fig_box = px.box(
        df,
        x=prep_col,
        y="math score",
        title="Math Scores by Test Preparation Status",
        labels={prep_col: "Test preparation course", "math score": "Math score (points)"},
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("**How to read this chart:**")
    st.markdown(
        """
        - Each box represents a **group of students** based on test prep status (e.g., *completed* vs *none*).  
        - The **line inside the box** is the median math score for that group.  
        - The **box edges** show the middle 50% of scores (from the 25th to 75th percentile).  
        - Dots outside the whiskers are **potential outliers** (unusually high or low scores).  
        """
    )

    st.markdown("**Observations (typical findings for this dataset):**")
    st.markdown(
        """
        - Students who **completed** the test preparation course often have a **higher median math score**.  
        - The spread of scores may be **tighter** for one group, indicating more consistent performance.  
        - There are usually a few **outliers** in both groups, showing students who performed very differently from their peers.  
        """
    )

st.divider()

# ======================================================================================
# CHART 3: Scatter Plot — Reading vs Writing Scores by Gender (Interactive)
# ======================================================================================

st.subheader("Chart 3 — Reading vs Writing Scores by Gender (Scatter Plot)")
st.markdown(
    "**Question:** How strongly are reading and writing scores related, and does the pattern look different by gender?"
)

if "gender" not in df.columns:
    st.error(
        "Expected column `gender` not found in dataset. "
        "Check the CSV headers or adjust the code."
    )
else:
    fig_scatter = px.scatter(
        df,
        x="reading score",
        y="writing score",
        color="gender",
        title="Reading vs Writing Scores by Gender",
        labels={
            "reading score": "Reading score (points)",
            "writing score": "Writing score (points)",
            "gender": "Gender",
        },
        hover_data=df.columns,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("**How to read this chart:**")
    st.markdown(
        """
        - Each point represents **one student** in the dataset.  
        - The **x-axis** is the reading score; the **y-axis** is the writing score.  
        - Colors indicate **gender**, so you can see whether groups cluster differently.  
        - Points near a **diagonal line** (bottom-left to top-right) mean similar reading and writing scores.  
        """
    )

    st.markdown("**Observations (typical patterns):**")
    st.markdown(
        """
        - Reading and writing scores tend to be **strongly positively correlated** (students who read well often write well).  
        - Both genders occupy similar regions of the chart, though one gender may slightly **cluster at higher scores**.  
        - A few points may show students who are **much stronger in one skill** than the other (off the diagonal).  
        """
    )

st.divider()

# ======================================================================================
# CHART 4: Bar Chart — Average Math Score by Parental Level of Education
# ======================================================================================

st.subheader("Chart 4 — Average Math Score by Parental Education (Bar Chart)")
st.markdown(
    "**Question:** How does average math performance vary with parental level of education?"
)

if "parental level of education" not in df.columns:
    st.error(
        "Expected column `parental level of education` not found in dataset. "
        "Check the CSV headers or adjust the code."
    )
else:
    parent_col = "parental level of education"

    grouped = (
        df.groupby(parent_col)["math score"]
        .mean()
        .reset_index()
        .sort_values("math score", ascending=False)
    )

    fig_bar = px.bar(
        grouped,
        x=parent_col,
        y="math score",
        title="Average Math Score by Parental Education Level",
        labels={
            parent_col: "Parental level of education",
            "math score": "Average math score (points)",
        },
    )
    fig_bar.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("**How to read this chart:**")
    st.markdown(
        """
        - Each bar represents a **parental education category** (e.g., *bachelor's degree*, *some college*).  
        - The **height of the bar** is the **average math score** of students in that category.  
        - Comparing bar heights helps you see which categories are associated with **higher or lower scores**.  
        - Tilted labels make long category names easier to read.  
        """
    )

    st.markdown("**Observations (common patterns):**")
    st.markdown(
        """
        - Higher parental education levels often line up with **higher average math scores**, but the differences are not extreme.  
        - Some middle categories (like *some college*) may be similar to the top categories, reminding us that **many factors** affect performance.  
        - These patterns are **associations**, not proof that parental education directly causes score differences.  
        """
    )

st.divider()

# ======================================================================================
# ETHICS & LIMITATIONS
# ======================================================================================

st.subheader("Ethics & Limitations")

st.markdown(
    """
    This dataset contains **student exam scores**, which are data about real people.
    Results must be interpreted carefully:

    - The data typically come from a **single context** (a limited group of schools or regions),
      so they may reflect **specific teaching environments and cultural expectations** and
      may not generalize to all students.  
    - Exam scores can be influenced by many factors (teaching quality, test design, resources, stress)
      and may also reflect **structural inequalities**, not just individual ability or effort.  
    - The visualizations here show **descriptive patterns only**. They should **not** be used to:
      - Judge individual students or teachers.  
      - Make broad generalizations about any demographic group.  

    Use these charts as a way to **explore patterns and ask questions**, not to draw strong
    conclusions about cause-and-effect or personal worth.
    """
)

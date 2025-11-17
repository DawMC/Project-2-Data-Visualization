# app.py
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Dawson Cummings • Data Portfolio",
    page_icon="📊",
    layout="wide",
)

# --------- Branding header ----------
st.title("📊 Dawson Cummings — Data Visualization")
st.caption("Multi-page Streamlit app combining a professional bio, an EDA gallery, and an interactive dashboard.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Welcome 👋")
    st.markdown(
        """
        This app doubles as my **professional portfolio** and a small **analytics product**
        built around a student performance dataset (exam scores and background variables).

        Use the sidebar or the navigation bar at the top of the app (Pages) to explore:

        - 📄 **Bio** – a short professional profile + highlights  
        - 📊 **Charts Gallery** – exploratory data analysis with multiple chart types  
        - 📈 **Dashboard** – interactive filters, KPIs, and linked visuals  
        - 🧭 **Future Work** – roadmap & reflections

        """
    )

with col2:
    st.markdown("### Contact")
    st.markdown(
        """
        - Name: **Dawson Cummings**  
        - Email: `dcummin8@msudenver.edu`  
        """
    )
    st.markdown("### App Info")
    st.write(f"Last refreshed: **{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")
    st.write("Built with Streamlit, Pandas, and Plotly.")

st.divider()
st.markdown(
    """
    ### How to Navigate

    - Use the **sidebar or the 'Pages' menu** to switch between Bio, Charts Gallery, Dashboard, and Future Work.
    - On the **Charts Gallery** page, each chart includes:
      - A question it answers  
      - A “How to read this chart” explainer  
      - Key observations  

    - On the **Dashboard** page, use the filters to slice the data and see KPIs & charts update together.
    """
)

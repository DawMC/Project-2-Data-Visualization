# pages/1_📄_Bio.py
import streamlit as st
from pathlib import Path

st.title("📄 Professional Bio")

# Try to load an optional profile image
assets_dir = Path(__file__).resolve().parent.parent / "assets"
profile_path = assets_dir / "profile.jpg"

col1, col2 = st.columns([1, 2])

with col1:
    if profile_path.exists():
        st.image(
            str(profile_path),
            caption="Alt-text: Profile portrait of Dawson Cummings.",
            use_column_width=True,
        )
    else:
        st.info("You can add `assets/profile.jpg` to show a profile image here.")

with col2:
    st.subheader("Hi, I'm Dawson ")
    st.markdown(
        """
        I'm a Computer Science Major with a Business minor. I am graduating in December and will be trying to go
        into the cyber security world once I get out of college. I really enjoy being able to use what I have learned
        to create different visualizations regarding data and making the most out of my education and what I am learning.
        """
    )

st.markdown("---")

st.subheader("Highlights")
st.markdown(
    """
    - 📚 Coursework in **Data Visualization, Statistics, Computer Networks, and Security**  
    - 🐍 Hands-on with **Python, Pandas, NumPy, Plotly, Altair, Streamlit**  
    - 🔐 Exposure to **cryptography, buffer overflow defenses, and secure coding practices**  
    """
)

st.markdown("---")

st.subheader("Visualization Philosophy")
st.markdown(
    """
    I believe that charts shoudl be able to be easily readable and really hone in on a specific question. 
    While also having clear labels and be incredible easy to read. I also understand that especially when 
    it comes to ethics, that there is always bias and limitations whan it comes to these datasets. 

    """
)

st.markdown("---")


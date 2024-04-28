import streamlit as st
from AuthenticationPage import authenticate
from InputPage_CSV import upload_csv
from Emo_dashboard import emo_dashboard

import os
os.chdir("C:\\Users\\Mahadevan Periasamy\\Desktop\\FinalYearProject_ML\\Streamlit\\Final_Project")


######################################## PAGE CONFIGURATION #####################################

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="😃",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

with open('./index.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

######################################## PAGE CONFIGURATION #####################################

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "SignupLoginPage"


def main():

    if st.session_state.current_page == "InputPageCSV":
        upload_csv()
    elif st.session_state.current_page == "Emotion-Dashboard":
        emo_dashboard()
    else:
        authenticate()


if __name__ == "__main__":
    main()

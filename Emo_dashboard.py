import streamlit as st
from streamlit_option_menu import option_menu
import Summary as s
import Reports as r
import os
# os.chdir("P:\PyCharm Selenium Practice\pythonProject\Sentiment Analysis\example app\TestingApp")


################################## EMOTION-DASHBOARD ########################################

def emo_dashboard():
    with st.sidebar:
        def t():
            st.session_state.signout = False
            st.session_state.signedout = False
            st.session_state.username = ''
            st.session_state.current_page = "SignupLoginPage"
            st.cache_data.clear()

        if "signedout" not in st.session_state:
            st.session_state["signedout"] = False
        if 'signout' not in st.session_state:
            st.session_state['signout'] = False

        if st.session_state.signout:
            st.sidebar.text('Username: ' + st.session_state.username)
            st.sidebar.text('Email id: ' + st.session_state.useremail)
            st.sidebar.button('Sign out', on_click=t)

        if st.sidebar.button("Back to Input Page"):
            st.session_state.current_page = "InputPageCSV"
            st.cache_data.clear()

        selected = option_menu(
            menu_title="Main Menu",
            options=["Summary", "Reports"],
            icons=['graph-up-arrow', 'file-earmark-pdf'],
            menu_icon="cast",
            default_index=0,
        )

    if selected == "Summary":
        st.title(":chart_with_upwards_trend: Analysis Summary")
        s.analysis()
    if selected == "Reports":
        st.title(":receipt: Reports")
        r.report_gen()

################################## EMOTION-DASHBOARD ########################################

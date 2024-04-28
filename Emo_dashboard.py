import streamlit as st
from streamlit_option_menu import option_menu
import Summary as s
import InfluencersList as i
import BrandComparison as b
import PDFReport as p
import ExcelReport as e
import os
os.chdir("C:\\Users\\Mahadevan Periasamy\\Desktop\\FinalYearProject_ML\\Streamlit\\Final_Project")

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

        brand_name = st.session_state.get('brand_name')

        with st.expander(f"***{brand_name}***", expanded=True):
            brand_options = ["Summary", "Influencers", "Brand Comparison", "Pdf Report", "Excel Report"]
            selected_option = option_menu(
                menu_title=None,
                options=brand_options,
                icons=['file-earmark-text', 'person-badge', 'tags', 'file-pdf', 'file-excel'],
                menu_icon="chevron-down",
                default_index=0,
            )

    if selected_option == "Summary":
        st.title(":chart_with_upwards_trend: Analysis Summary")
        s.analysis()
    elif selected_option == "Influencers":
        st.title(":bust_in_silhouette: List of Influencers")
        i.gen_influencers_list()
    elif selected_option == "Brand Comparison":
        st.title("⚖️ Compare Brands")
        b.compare_brands()
    if selected_option == "Pdf Report":
        st.title(":page_with_curl: PDF Report")
        p.pdf_report_gen()
    elif selected_option == "Excel Report":
        st.title(":page_facing_up: Excel Report")
        e.excel_report_gen()

################################## EMOTION-DASHBOARD ########################################
import streamlit as st
# from datetime import datetime


# def convert_date_to_RFC_3339(start_date, end_date):
#     start_date_RFC_3339 = datetime.strftime(start_date, "%Y-%m-%dT%H:%M:%SZ")
#     end_dateRFC_3339 = datetime.strftime(end_date, "%Y-%m-%dT%H:%M:%SZ")
#     return start_date_RFC_3339, end_dateRFC_3339

def upload_csv():

    # def t():
    #     st.session_state.signout = False
    #     st.session_state.signedout = False
    #     st.session_state.username = ''
    #     st.session_state.current_page = "SignupLoginPage"
    #     st.cache_data.clear()
    #
    # if "signedout" not in st.session_state:
    #     st.session_state["signedout"] = False
    # if 'signout' not in st.session_state:
    #     st.session_state['signout'] = False
    #
    #
    # # SignOut button
    # st.text('Username: ' + st.session_state.username)
    # st.text('Email id: ' + st.session_state.useremail)
    #
    # if st.session_state.signout:
    #     st.button('Sign out', on_click=t)


    st.title(":label: Brand Analysis")
    #
    # Brand name input
    brand_name = st.text_input(":first_place_medal: Enter Brand Name:")

    # Get start and end dates from user
    # start_date = st.date_input("Start Date")
    # end_date = st.date_input("End Date")
    # converted_start_date, converted_end_date = convert_date_to_RFC_3339(start_date, end_date)

    brand_category = st.selectbox(":first_place_medal: Choose the Brand's Category:", ("Food Category", "Clothing Category", "FootWear Category", "Cosmetics", "Beverages", "Accessories"))

    st.markdown('')

    if st.button("Analyse"):
        if not brand_name:
            st.info("Please! Enter the Brand name to Continue...")
        else:
            st.session_state['brand_name'] = brand_name
            st.session_state['brand_category'] = brand_category

            # st.session_state['start_date'] = converted_start_date
            # st.session_state['end_date'] = converted_end_date

            st.session_state.current_page = "Emotion-Dashboard"
    #
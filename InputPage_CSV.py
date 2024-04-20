import streamlit as st

def upload_csv():
    # st.title("Upload a DataFile In csv format")
    st.title("Brand Analysis")
    #
    # uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    # Brand name input
    brand_name = st.text_input(":first_place_medal: Enter brand name:")
    brand_category = st.selectbox(":first_place_medal: Choose the Brand's Category:", ("Food Category", "Clothing Category", "FootWear Category", "Cosmetics", "Beverages", "Accessories"))

    if st.button("Analyse"):
        if brand_name is not None:
            # Store the uploaded file data in session state
            # csv_data = uploaded_file.getvalue().decode("utf-8")
            # st.session_state['input_csv_data'] = csv_data
            st.session_state['brand_name'] = brand_name
            st.session_state['brand_category'] = brand_category
            st.session_state.current_page = "Emotion-Dashboard"
    else:
        # st.info("Upload a CSV File!")
        st.info("Please! Enter the Brand name to Continue...")
    #

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.current_page = "SignupLoginPage"
        st.cache_data.clear()

    # if "signedout" not in st.session_state:
    #     st.session_state["signedout"] = False
    # if 'signout' not in st.session_state:
    #     st.session_state['signout'] = False

    # SignOut button
    st.text('Username: ' + st.session_state.username)
    st.text('Email id: ' + st.session_state.useremail)

    if st.session_state.signout:
        st.button('Sign out', on_click=t)
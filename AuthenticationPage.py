import streamlit as st
# from streamlit_lottie import st_lottie
import firebase_admin
from firebase_admin import firestore, credentials, auth, storage, db
import os
os.chdir("P:\PyCharm Selenium Practice\pythonProject\Sentiment Analysis\example app\TestingApp")

if not firebase_admin._apps:
    cred = credentials.Certificate("streamlitsentimentapp-firebase-adminsdk-j5ali-11b8fc6f9e.json")
    firebase_admin.initialize_app(cred)

# Save data in real-time database
# ref = db.reference('SentimentAnalysis-Dashboard/')
# users_ref = ref.child('Users')
db = firestore.client()
users_ref = db.collection("Users")

def authenticate():
    st.title("Welcome to :red[Sentiment Analysis] :sunglasses:")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''


    # Log-In Function
    def f():
        try:
            user = auth.get_user_by_email(email)
            # auth.verify_password(password, user.password)
            print(user.uid)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            global Usernm
            Usernm = (user.uid)
            st.session_state.signedout = True
            st.session_state.signout = True
            st.session_state.current_page = "InputPageCSV"
        except firebase_admin.auth.UserNotFoundError:
            st.error("User not found")


    # def s():
    #     st.session_state.signout = False
    #     st.session_state.signedout = False
    #     st.session_state.username = ''
    #     st.cache_data.clear()

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False

    if not st.session_state['signedout']:
        option = st.selectbox("Choose an option:", ("SignUp", "SignIn"))

        # lottie_login = "https://lottie.host/35f22ac9-cb76-4a14-a7cb-4e761535a5c2/Oes5t2dgq9.json"
        # col1, col2, col3 = st.columns([1, 2, 1])
        # with col1:
        #     st.write("")
        # with col2:
        #     st_lottie(lottie_login, speed=1, width=400, height=500, key="login_animation", quality="high")
        # with col3:
        #     st.write("")

        if option == "SignUp":
            with st.form("Sign_Up", clear_on_submit=True):
                st.markdown("**Fill the Form to Register** :balloon:")
                email = st.text_input("Enter email:")
                password = st.text_input("Enter Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                username = st.text_input("Enter your Unique Username")

                if st.form_submit_button('Create my account'):
                    if (len(email) or len(password) or len(confirm_password) or len(username)) == 0:
                        st.error("Please Fill all the fields!!")
                    else:
                        if password != confirm_password:
                            st.error("Passwords do not match")
                        else:
                            try:
                                user = auth.create_user(email=email, password=password, uid=username)
                                # st.session_state.current_page = "InputPage"
                                users_ref.add({
                                    "Email": email,
                                    "username": username
                                })
                                st.success('Account created successfully: {0}'.format(user.uid))
                                st.markdown('Please Login using your email and password')
                                st.balloons()
                            except firebase_admin.auth.EmailAlreadyExistsError:
                                st.error("User already exists with this email")

        elif option == "SignIn":
            with st.form("Sign_In", clear_on_submit=True):
                st.markdown("**Fill the Form to SignIn** :balloon:")
                email = st.text_input("Enter email:")
                password = st.text_input("Enter Password", type="password")
                if st.form_submit_button('Login'):
                    if (len(email) and len(password)) == 0:
                        st.error("Please Fill all the fields!!")
                    else:
                        f()

    # if st.session_state.signout:
    #     st.text('Username: ' + st.session_state.username)
    #     st.text('Email id: ' + st.session_state.useremail)
    #     st.button('Sign out', on_click=s)
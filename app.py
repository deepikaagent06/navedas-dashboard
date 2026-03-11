import streamlit as st
from dashboard import show_dashboard

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():

    # Create two columns
    col1, col2 = st.columns([1,4])

    with col1:
        st.image("governance_logo.jpg", width=1000)

    with col2:
        st.title("Navedas Intelligence")

    st.subheader("Secure Access")

    password = st.text_input("password", type="password")

    if st.button("Login"):

        if password == "2026":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Incorrect Credentials")


if st.session_state.logged_in:
    show_dashboard()
else:

    login()


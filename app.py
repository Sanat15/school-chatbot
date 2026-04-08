import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="School Chatbot", page_icon="🏫")
st.title("🏫 School Chatbot")

# Session state
if "token" not in st.session_state:
    st.session_state.token = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Login form
if not st.session_state.token:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", data={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.session_state.role = response.json()["role"]
            st.rerun()
        else:
            st.error("Invalid username or password")
else:
    st.caption(f"Logged in as {st.session_state.role}")
    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.messages = []
        st.rerun()

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/chat/query",
                    json={"question": prompt},
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                if response.status_code == 200:
                    answer = response.json()["response"]
                else:
                    answer = "Sorry, something went wrong."
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
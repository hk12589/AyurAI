import streamlit as st
import requests

#API_URL = "http://localhost:8000/get_remedy"
API_URL = "http://127.0.0.1:8000/get_remedy"


st.set_page_config(page_title="Ayurveda Remedy Chatbot", layout="centered")
st.title("🪷 Ayurveda Remedy Recommender")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {msg['content']}")

# User input
user_input = st.text_input("Enter your symptoms:", key="user_input")

if st.button("Get Remedy"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Finding remedy..."):
            res = requests.post(API_URL, json={"query": user_input})

        if res.status_code == 200:
            data = res.json()
            if "recommendation" in data:
                bot_reply = data["recommendation"]
            else:
                bot_reply = "No remedy found for given symptoms."

            st.session_state.messages.append({"role": "bot", "content": bot_reply})
        else:
            st.error("Error fetching remedy")

    st.rerun()

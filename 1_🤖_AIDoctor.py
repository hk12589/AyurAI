import streamlit as st
import requests
import re
import app as app
from app import get_remedy, QueryRequest


#API_URL = "http://localhost:8000/get_remedy"
API_URL = "http://127.0.0.1:8000/get_remedy"

st.set_page_config(page_title="Ayurveda Remedy Chatbot", page_icon="🌿",layout="centered")
st.title("🪷 Ayurveda Remedy Recommender")

if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_generator():
    for word in data["recommendation"].split():
        yield word + " "

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
            #res = requests.post(API_URL, json={"query": user_input})
            res = get_remedy(QueryRequest(query=user_input))

        #if res.status_code == 200:
        data = res
        if "recommendation" in data:
            #formatted_output = format_llm_response(data["recommendation"])
            st.write_stream(stream_generator())                
            #bot_reply = formatted_output            
                
        elif "matches" in data:
            matches = data["matches"]
            if matches:
                bot_reply = "Here are the top matches for your symptoms:\n\n"
                for match in matches:
                    bot_reply += f"- **Disease:** {match['disease']}\n"
                    bot_reply += f"  **Dosha:** {match['dosha']}\n"
                    bot_reply += f"  **Remedies:** {match['remedy']}\n\n"
            else:
                bot_reply = "No matching remedies found for your symptoms."
        else:
            bot_reply = "No remedy found for given symptoms."

        st.session_state.messages.append({"role": "bot", "content": data["recommendation"]}) 

    st.rerun()

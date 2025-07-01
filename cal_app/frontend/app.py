import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"  # Change if backend is hosted elsewhere

st.set_page_config(page_title="Calendar Booking Assistant", page_icon="📅")
st.title("📅 Calendar Booking Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "session_state" not in st.session_state:
    st.session_state["session_state"] = {}

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("How can I help you with your calendar today?"):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Send to backend
    payload = {
        "message": prompt,
        "session_state": st.session_state["session_state"]
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        agent_reply = data.get("response", "(No response)")
        st.session_state["session_state"] = data.get("session_state", {})
    except Exception as e:
        agent_reply = f"Error: {e}"

    # Add agent message to history
    st.session_state["messages"].append({"role": "assistant", "content": agent_reply})
    st.rerun()

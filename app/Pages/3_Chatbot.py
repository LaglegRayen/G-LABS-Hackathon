import os
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv
from llama_index.llms.groq import Groq
from llama_index.core import Settings
import uuid

def chatbot():
    # Setup
    nest_asyncio.apply()
    load_dotenv()

    # Configure the LLM
    llm = Groq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_CLOUD_API_KEY"),
        temperature=0.7
    )
    
    # Healthcare-focused system prompt
    SYSTEM_PROMPT = (
        "You are a helpful, professional healthcare assistant. "
        "You provide clear, concise, and medically accurate advice to patients. "
        "Always stay polite and caring. "
        "Avoid diagnosing illnesses; instead, guide users towards best practices, "
        "possible next steps, and suggest seeing healthcare professionals when needed."
    )

    # Session state init
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    if "active_convo" not in st.session_state:
        st.session_state.active_convo = None

    def new_conversation():
        convo_id = f"Chat {len(st.session_state.conversations) + 1}"
        st.session_state.conversations[convo_id] = {
            "messages": []
        }
        st.session_state.active_convo = convo_id
        st.rerun()

    # Sidebar UI
    st.sidebar.title("💬 Conversations")
    if st.sidebar.button("➕ New Conversation"):
        new_conversation()

    if st.session_state.conversations:
        for title in st.session_state.conversations.keys():
            if st.sidebar.button(title, key=title):
                st.session_state.active_convo = title
                st.rerun()

    # Start a new chat
    if st.session_state.active_convo is None:
        st.title("🆕 Start a New Chat")
        st.write("Click 'New Conversation' to start chatting!")

    # Chat interface
    elif st.session_state.active_convo:
        convo = st.session_state.conversations[st.session_state.active_convo]
        st.title(f"💬 {st.session_state.active_convo}")

        # Show previous messages
        for msg in convo["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input chat
        if user_input := st.chat_input("Ask something about your health..."):
            convo["messages"].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\nAssistant:"
                    response = llm.complete(full_prompt).text
                    st.markdown(response)
                    convo["messages"].append({"role": "assistant", "content": response})

def main():
    st.set_page_config(page_title="Healthcare Chatbot", layout="wide")
    chatbot()

if __name__ == "__main__":
    main()

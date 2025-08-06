import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="ApnaChatBot", page_icon="🤖")
st.title("🤖 ApnaChatBot")
st.markdown("Ask anything and get instant AI-powered answers!")

# Get env vars
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = "2025-01-01-preview"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version,
)

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."}
    ]

# Display chat history
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=st.session_state.messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False,
        )

        assistant_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

    except Exception as e:
        st.error(f"❌ Error: {e}")

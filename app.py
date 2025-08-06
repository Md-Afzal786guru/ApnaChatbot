import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

# Load local .env variables (for development)
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="ApnaChatBot", page_icon="🤖")
st.title("🤖 ApnaChatBot")
st.markdown("Ask anything and get instant AI-powered answers!")

# Load environment variables (local or Streamlit Cloud)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY") or st.secrets.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT") or st.secrets.get("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"  # Fixed version used in Azure OpenAI

# Validate credentials
if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY or not AZURE_OPENAI_DEPLOYMENT:
    st.error("❌ Missing Azure OpenAI credentials. Please check your .env file or Streamlit Secrets.")
    st.stop()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant that helps people find information."}
    ]

# Display previous messages (except system)
for msg in st.session_state.messages[1:]:
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
            model=AZURE_OPENAI_DEPLOYMENT,
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

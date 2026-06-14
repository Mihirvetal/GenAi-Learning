import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI

# 1. Setup the Page UI
st.set_page_config(page_title="My AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 My Personal AI Assistant")
st.write("Ask me anything about the candidate's profile based on the loaded data!")

# 2. Initialize System (Cached so it doesn't reload on every message!)
@st.cache_resource(show_spinner=False)
def initialize_system():
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Configure global models
    Settings.embed_model = GoogleGenAIEmbedding(model_name="gemini-embedding-001", api_key=api_key)
    Settings.llm = GoogleGenAI(model="gemini-2.5-flash", api_key=api_key)
    
    # Load the saved index from your notebook storage folder
    storage_context = StorageContext.from_defaults(persist_dir="./notebook/storage")
    index = load_index_from_storage(storage_context)
    
    # Upgrade to Chat Engine to remember conversation history
    return index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Load the engine
with st.spinner("Booting up AI Brain..."):
    chat_engine = initialize_system()

# 3. Initialize Streamlit Chat History State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I've read the profile data. What would you like to know?"}
    ]

# 4. Draw the existing chat messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle New User Input
if prompt := st.chat_input("Ask a question..."):
    
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # The chat engine automatically handles passing the history to Gemini!
            response = chat_engine.chat(prompt)
            st.markdown(response.response)
    
    # Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response.response})
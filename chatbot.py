import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

st.set_page_config(
    page_title="Upcode",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load API key
load_dotenv()
secret_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=secret_key)

# Greeting message
greeting_message = {
    "role": "assistant",
    "content": "Hello! I am your Travel Agent. How Can I Help You Today?"
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": """
            Assume you are a travel agent. You conduct travel programs across the world.
            Respond to queries within 2-3 sentences.
            """
        },
        greeting_message
    ]

# Display chat history (excluding system)
for message in st.session_state["messages"][1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create assistant placeholder
    assistant_message = st.chat_message("assistant").empty()
    full_response = ""

    # Stream assistant response
    stream = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=st.session_state["messages"],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            assistant_message.markdown(full_response + "▌")

    # Finalize assistant message
    assistant_message.markdown(full_response)
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

st.sidebar.write("Upcode")
if st.sidebar.button("Click Me !!"):
    st.sidebar.success("Thank You")
st.sidebar.image("https://tse3.mm.bing.net/th/id/OIP.I9y8uyLrGxrOba8RcFIckQHaBv?pid=Api&P=0&h=180",caption="Learn with Developers")




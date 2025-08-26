import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]


st.set_page_config(
    page_title="Chat GPT",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

hide_streamlit_elements = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)

st.title('How can I help?')

if "chats" not in st.session_state:
    st.session_state.chats = []

# Display previous chat messages in correct order (top to bottom)
for chat in st.session_state.chats:
    st.chat_message(chat['role']).markdown(chat['content'])

prompt = st.chat_input('Ask anything')

if prompt:
    # Immediately display the user's message
    st.chat_message("user").markdown(prompt)
    st.session_state.chats.append({"role": "user", "content": prompt})

    # Create a placeholder for the streaming response
    message_placeholder = st.empty()
    
    # Stream the response
    full_response = ""
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Get streaming response
        stream = openai.chat.completions.create(
            model=st.secrets["OPENAI_MODEL"],
            messages=[
                { "role" : "system","content":"You are an AI agent"},
                *st.session_state.chats,
            ],
            stream=True
        )
        
        # Display streaming response with typing effect
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                # Display with typing cursor
                message_placeholder.markdown(full_response + "▌")
        
        # Remove cursor when complete
        message_placeholder.markdown(full_response)

    # Add the complete response to chat history
    st.session_state.chats.append({"role": "assistant", "content": full_response})
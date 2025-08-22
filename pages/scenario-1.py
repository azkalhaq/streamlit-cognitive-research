import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]


st.set_page_config(
    page_title="Chat GPT",
    page_icon="🤖",
    layout="centered"
)

st.title('How can I help?')

if "chats" not in st.session_state:
    st.session_state.chats = []

prompt = st.chat_input('Ask anything')

if prompt:
    st.session_state.chats.append({
        "role": "user",
        "content": prompt
    })

    # Create a placeholder for the streaming response
    message_placeholder = st.empty()
    
    # Stream the response
    full_response = ""
    with message_placeholder.container():
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Get streaming response
            stream = openai.chat.completions.create(
                model=st.secrets["OPENAI_MODEL"],
                messages=[
                    { "role" : "system","content":"You are an AI agent"},
                    *st.session_state.chats,
                    {"role": "user", "content": prompt}
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
    st.session_state.chats.append({
        "role": "assistant",
        "content": full_response
    })

# Display previous chat messages
for chat in st.session_state.chats[:-1]:  # Exclude the last message as it's already displayed
    st.chat_message(chat['role']).markdown(chat['content'])
import streamlit as st
import openai
import os

openai.api_key = st.secrets["OpenAI_key"]


st.set_page_config(
    page_title="Chat GPT-4o",
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

    assistant = openai.chat.completions.create(
        model="gpt-5",
        messages=[
            { "role" : "system","content":"You are an AI agent"},
            *st.session_state.chats,
            {"role": "user", "content": prompt}
        ]
    )

    st.session_state.chats.append({
        "role": "assistant",
        "content": assistant.choices[0].message.content
    })

    # print(assistant.choices[0].message.content)

for chat in st.session_state.chats:
    st.chat_message(chat['role']).markdown(chat['content'])
    # st.chat_message("assistant").text("Hey, how can I help you?")
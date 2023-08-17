import re

import openai
import streamlit as st


def doc_preprocess(doc: str) -> str:
    doc = doc.strip()
    doc = re.sub(r"[\n]+", "\n", doc)
    doc = doc.strip()
    return doc


with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="chatbot_api_key",
        type="password",
        value=""
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

uploaded_file = st.file_uploader(
    "上传文件，支持.txt和.md",
    type=("txt", "md"),
)

st.title("基于ChatGPT的文档问答")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "How can I help you?"
        },
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("请先添加OpenAI API Key.")
        st.stop()

    if not uploaded_file:
        st.info("请先上传文档.")
        st.stop()

    article = uploaded_file.read().decode()
    article = doc_preprocess(article)

    prompt_with_article = f"Here's an article:\n{article}\n{prompt}"

    openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt_with_article})
    st.chat_message("user").write(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
    )
    msg = response.choices[0].message

    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)

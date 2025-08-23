import streamlit as st
import google.generativeai as genai
import openai
import time
import os

st.set_page_config(
    page_title="Anomali baru",
    page_icon='🐮'
)

st.title("🐮 Chattipus Bottotipus")
st.caption("Sosok anomali mengerikan")

#Visualizing live-like reply ux
def print_char(response):
    for i in response.text:
        yield i
        time.sleep(0.030)

if "msg" not in st.session_state:
    st.session_state.msg = []

def load_state():
    for msg in st.session_state.msg:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

def save_state(role, sentences):
    if role == "user":
        st.session_state.msg.append({"role": "user", "content": sentences})
    elif role == "assistant":
        st.session_state.msg.append({"role": "assistant", "content": sentences})


prompt = st.chat_input("Say Something")
load_state()

#Start initialize Gemini LLM
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        save_state("user", prompt)
        
        response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.write_stream(print_char(response))
        save_state("assistant", response.text)


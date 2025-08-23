import streamlit as st
import google.generativeai as genai
import openai
import time

st.set_page_config(
    page_title="Anomali baru",
    page_icon='🐮'
)

st.title("🐮 Chattipus Bottotipus")
st.caption("Sosok anomali mengerikan")

def print_char(prompt):
    for i in prompt:
        yield i
        time.sleep(0.030)

prompt = st.chat_input("Say Something")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        st.write_stream(print_char(prompt))


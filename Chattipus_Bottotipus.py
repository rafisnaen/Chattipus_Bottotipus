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

prompt = st.chat_input("Say Something")

#Start initialize Gemini LLM
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        
        response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.write_stream(print_char(response))


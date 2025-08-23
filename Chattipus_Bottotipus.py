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

with st.sidebar:

    selected_model = st.selectbox(
        "Pilih anomali",
        ("gemini-2.5-flash", "gpt-3.5-turbo"),
        key="selected_model"
    )
    st.write(f"🐮 Anomali {selected_model} Chatbot")

    #Additional model parameter settings
    temperature = st.slider(
        "Temperature:",
        min_value=0.01,
        max_value=5.00,
        value=0.07,
        step=0.01
    )
    st.caption("min = 0.01 || max = 5.00")

    top_p = st.slider(
        "Top P:",
        min_value=0.01,
        max_value=1.00,
        value=0.95,
        step=0.01
    )
    st.caption("min = 0.01 || max = 1.00")

    top_k = st.slider(
        "Top K:",
        min_value=1,
        max_value=50,
        value=40,
        step=1
    )
    st.caption("min = 1 || max = 50")

    max_tokens = st.slider(
        "Max sequence length:",
        min_value=64,
        max_value=4096,
        value=256,
        step=1
    )
    st.caption("min = 1 || max = 50")

    if selected_model == "gemini-2.5-flash":
        #Start initialize Gemini LLM
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature":temperature,
                "top_p":top_p,
                "top_k":top_k,
                "max_output_tokens":max_tokens,
            }
            )
    else:
        openai.api_key = os.environ["OPENAI_API_KEY"]
        model_name = "gpt-3.5-turbo"


#Session state section
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


#LLM Section
prompt = st.chat_input("Say Something")
load_state()

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
        save_state("user", prompt)
        
        response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.write_stream(print_char(response))
        save_state("assistant", response.text)



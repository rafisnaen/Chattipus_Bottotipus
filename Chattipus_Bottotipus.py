import streamlit as st
import requests
import os

# Init openrouter API
API_KEY = os.environ.get(["OPENROUTER_API_KEY"])
url = "https://openrouter.ai/api/v1/chat/completions"

# openrouter model setup

def openrouter(model, messages, temperature, top_p, top_k, max_tokens):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model, 
        "messages": messages, 
        "temperature": temperature, 
        "top_p": top_p, 
        "top_k": top_k, 
        "max_tokens": max_tokens,
    }
    response = requests.post(url, headers=headers, json=data)

    #Raise HTTP error kalau selain kode 200 (kode 200 == berhasil)
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return response.json()["choices"][0]["message"]["content"] 

st.set_page_config(
    page_title="Anomali baru",
    page_icon='🐮'
)

st.title("🐮 Chattipus Bottotipus")
st.caption("Sosok anomali mengerikan")

#Make sidebar container
with st.sidebar:
     st.header("🐮 Pengaturan anomali")
    
    #selectbox widget
     selected_model = st.selectbox(
          "Pilih anomali",
          ("google/gemini-2.0-flash-exp:free", "openai/gpt-oss-20b:free")
     )

    #caption
     if selected_model == "google/gemini-2.0-flash-exp:free":
        st.caption("🐮 Anomali Gemini Chatbot")
     else:
        st.caption("🐮 Anomali GPT Chatbot")

    #make an expand widget for model response settings
     with st.expander("Advanced settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 1.0)
        top_p = st.slider("Top P",  0.0, 1.0, 1.0)
        top_k = st.slider("Top K", 1, 100, 40)
        max_tokens = st.slider("Max tokens",50,2000,500)
    
#Initialize session state
if "msg" not in st.session_state:
        st.session_state.msg = []

# load session statenya
def load_state():
    for msg in st.session_state.msg:
         with st.chat_message(msg["role"]):
              st.markdown(msg["content"])

# Save session statenya, append list buat di load ketika rerun
def save_state(role, sentences):
    if role == "user":
        st.session_state.msg.append({"role": "user", "content": sentences})
    if role == "assistant":
        st.session_state.msg.append({"role": "assistant", "content": sentences})
# Load the chat
load_state()

# Start prompting
prompt = st.chat_input("Input pertanyaan anomali")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        save_state("user", prompt)
        
        #Add live-like thinking UI

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            #Call openrouter function
            #Kasih riwaya full chat, bukan variabel prompt doang
            response = openrouter(selected_model, st.session_state.msg, temperature, top_p, top_k, max_tokens)

            #Output responnya
            st.markdown(response)
            save_state("assistant", response)
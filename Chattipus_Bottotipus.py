import streamlit as st
import requests
import os
import time

# Init openrouter API
API_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/chat/completions"

# openrouter model setup

def openrouter(model, messages, temperature, top_p, top_k, max_tokens):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    #setup json utk data modelnya
    data = {
        "model": model, 
        "messages": messages, 
        "temperature": temperature, 
        "top_p": top_p, 
        "top_k": top_k, 
        "max_tokens": max_tokens,
    }
    response = requests.post(url, headers=headers, json=data)

    # Raise HTTP error kalau selain kode 200 (kode 200 == berhasil)
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return response.json()["choices"][0]["message"]["content"] 
    
# Make a live-like response dari teks yang dikembalikan oleh open router
def live_like_response(response):
    for i in response:
        yield i
        time.sleep(0.010)


st.set_page_config(
    page_title="Anomali baru",
    page_icon='🐮'
)

st.title("🐮 Chattipus Bottotipus")
st.caption("Sosok anomali mengerikan")


# Init session state, buat list utk nyimpen history chat
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

# Buat sidebar containernya
with st.sidebar:
     st.header("🐮 Pengaturan anomali")
    
    # selectbox widget
     selected_model = st.selectbox(
          "Pilih anomali",
          ("google/gemini-flash-1.5", "openai/gpt-3.5-turbo")
     )

    # caption
     if selected_model == "google/gemini-flash-1.5":
        st.caption("🐮 Anomali Gemini Chatbot")
     else:
        st.caption("🐮 Anomali GPT Chatbot")

    # buat expand widget utk model response settings
     with st.expander("Advanced settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 1.0)
        top_p = st.slider("Top P",  0.0, 1.0, 1.0)
        top_k = st.slider("Top K", 1, 100, 40)
        max_tokens = st.slider("Max tokens",50,2000,500)

    # buat fitur summarize chat
     if st.button("🐄 rangkum dialog"):
        with st.spinner("Merangkum..."):
            save_state("user", "Dengan detail yang ketat, tolong rangkum seluruh chat")
            response = openrouter(selected_model, st.session_state.msg, temperature, top_p, top_k, max_tokens)
            save_state("assistant", response)

# Load chat
load_state()

# Mulai prompting
prompt = st.chat_input("🐄 Input pertanyaan anomali")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        # save promptingan sama rolenya
        save_state("user", prompt)
        
        # Tambahin UI live-like thinking
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            #Call openrouter function
            #Kasih riwaya full chat, bukan variabel prompt doang
            response = openrouter(selected_model, st.session_state.msg, temperature, top_p, top_k, max_tokens)

            #Output responnya
            #Berbeda dengan write,
            #Write stream harus menampilkan respon yang tidak secara langsung dibuat utuh.
            st.write_stream(live_like_response(response))
            # save role sama responnya
            save_state("assistant", response)
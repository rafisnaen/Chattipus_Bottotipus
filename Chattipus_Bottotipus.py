import streamlit as st
import requests
import os
import time
import numpy as np

# Init openrouter API
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# openrouter model setup
def openrouter(model, messages, temperature, top_p, top_k, max_tokens):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
    response = requests.post(OPENROUTER_URL, headers=headers, json=data)

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

# Default project instructions
DEFAULT_INSTRUCTIONS = """Gunakan gaya penulisan yang natural dan sesuai konteks."""

# Initialize project settings di session state
if 'project_settings' not in st.session_state:
    st.session_state.project_settings = {
        'instructions': DEFAULT_INSTRUCTIONS,
        'output_mode': 'Paragraph',
        'preferred_mode': 'None'
    }

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

def openrouter_with_instructions(model, messages, temperature, top_p, top_k, max_tokens):
    # Ambil settings dari session state
    project_settings = st.session_state.get('project_settings', {})
    
    # Dapetin current settings dari state
    current_output_mode = project_settings.get('output_mode', 'Paragraph')
    current_preferred_mode = project_settings.get('preferred_mode', 'None')
    current_instructions = project_settings.get('instructions', DEFAULT_INSTRUCTIONS)
    
    # Variabel format instruksi
    format_instructions = ""
    
    # Instructions untuk Output Mode
    if current_output_mode == "Bullet Points":
        format_instructions = "SELALU gunakan format bullet points (•) atau numbering untuk menyajikan informasi. Buat poin-poin yang jelas dan terstruktur."
    elif current_output_mode == "Code":
        format_instructions = "Sertakan code examples yang relevan. Format kode dengan baik dan berikan penjelasan singkat untuk setiap bagian kode."
    elif current_output_mode == "Structured":
        format_instructions = "Gunakan struktur yang jelas dengan heading, subheading, dan paragraf yang terorganisir. Gunakan pemisah visual jika diperlukan."
    elif current_output_mode == "Detailed Explanation":
        format_instructions = "Berikan penjelasan yang sangat detail dan mendalam. Jelaskan step-by-step dengan contoh konkret."
    else: 
        format_instructions = "Gunakan format paragraf yang mengalir dengan baik. Jelaskan dengan runtut dan kohesif."
    
    # Instructions untuk Preferred Mode  
    mode_instructions = ""
    if current_preferred_mode == "Academic":
        mode_instructions = "Gunakan bahasa akademik yang formal, struktural, dan referensial. Sertakan terminologi teknis yang tepat."
    elif current_preferred_mode == "Casual":
        mode_instructions = "Gunakan bahasa yang santai, mudah dipahami, dan conversational. Hindari jargon teknis yang berlebihan."
    elif current_preferred_mode == "Technical":
        mode_instructions = "Fokus pada aspek teknis, spesifikasi, dan detail implementasi. Gunakan terminologi teknis yang spesifik."
    elif current_preferred_mode == "Simple":
        mode_instructions = "Gunakan bahasa yang sederhana, jelas, dan mudah dimengerti oleh pemula. Hindari kompleksitas yang tidak perlu."
    else: 
        mode_instructions = "Gunakan gaya penulisan yang natural dan sesuai konteks."
    
    # Gabungkan semua instructions
    system_message = {
        "role": "system",
        "content": f"""
        {current_instructions}
        
        FORMAT OUTPUT YANG HARUS DIPATUHI:
        - Format: {current_output_mode}
        - Gaya: {current_preferred_mode}
        
        INSTRUKSI SPESIFIK:
        {format_instructions}
        {mode_instructions}
        
        ATURAN TAMBAHAN:
        - Jelaskan dengan detail, jelas, dan mudah dipahami
        - Berpikir secara step-by-step sebelum memberikan jawaban
        - PASTIKAN untuk selalu mengikuti format {current_output_mode} dan gaya {current_preferred_mode} yang telah ditentukan
        - Jangan mengabaikan preferensi format dan gaya yang diminta
        """
    }
    
    # Sisipkan system message di awal
    enhanced_messages = [system_message] + messages

    # Panggil API seperti biasa
    return openrouter(model, enhanced_messages, temperature, top_p, top_k, max_tokens)

# Buat sidebar containernya
with st.sidebar:
    st.header("🐮 Pengaturan anomali")
    
    # PROJECT SETTINGS EXPANDER
    with st.expander("⚙️ Project Settings", expanded=False):
        # Project Instructions
        project_instructions = st.text_area(
            "Project Instructions:",
            value=st.session_state.project_settings['instructions'],
            height=150,
            help="Instruksi khusus untuk mengatur perilaku AI assistant"
        )
        
        # Preferred Output Mode
        output_mode = st.selectbox(
            "Preferred Output Mode:",
            ["Paragraph", "Bullet Points", "Code", "Structured", "Detailed Explanation"],
            index=["Paragraph", "Bullet Points", "Code", "Structured", "Detailed Explanation"]
            .index(st.session_state.project_settings['output_mode']),
            help="Pilih format output yang diinginkan"
        )
        
        # Preferred Mode (Additional)
        preferred_mode = st.selectbox(
            "Preferred Mode:",
            ["None", "Academic", "Casual", "Technical", "Simple"],
            index=["None", "Academic", "Casual", "Technical", "Simple"]
            .index(st.session_state.project_settings['preferred_mode']),
            help="Pilih gaya penulisan yang diinginkan"
        )
        
        # Save Settings Button
        if st.button("💾 Save Project Settings", use_container_width=True):
            st.session_state.project_settings = {
                'instructions': project_instructions,
                'output_mode': output_mode,
                'preferred_mode': preferred_mode
            }
            st.success("✅ Project settings disimpan!")
    
    # Tampilkan current settings
    st.caption(f"📝 Output: {st.session_state.project_settings['output_mode']}")
    st.caption(f"🎯 Mode: {st.session_state.project_settings['preferred_mode']}")
    
    # selectbox widget
    selected_model = st.selectbox(
        "Pilih anomali",
        ("deepseek/deepseek-chat-v3.1", "openai/gpt-oss-20b")
    )

    # caption
    if selected_model == "deepseek/deepseek-chat-v3.1":
        st.caption("🐮 Anomali Deepseek Chatbot")
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
            response = openrouter_with_instructions(selected_model, st.session_state.msg, temperature, top_p, top_k, max_tokens)
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
            # Call openrouter function
            response = openrouter_with_instructions(selected_model, st.session_state.msg, temperature, top_p, top_k, max_tokens)

            # Output responnya
            st.write_stream(live_like_response(response))
            # save role sama responnya
            save_state("assistant", response)
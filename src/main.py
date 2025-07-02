import streamlit as st
from components.seikyu import seikyu
from components.buttons import set_model_selector
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(page_title="解析アプリ", page_icon="📄")

# ----------------- サイドバー -----------------
st.sidebar.title("設定")

with st.sidebar:
    st.write("モデル")
    
    client_name, model_name = set_model_selector()

# --- メイン画面選択 ---
if "page" not in st.session_state:
    st.session_state.page = None

if st.button("請求書解析アプリ 📄"):
    st.session_state.page = "seikyu"

if st.session_state.page == "seikyu":
    seikyu(
        client_name=client_name,
        model_name=model_name
    )
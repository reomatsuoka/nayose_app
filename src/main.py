import streamlit as st
from components.seikyu import seikyu
from utils.provider import model_names
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(page_title="解析アプリ", page_icon="📄")

# ----------------- サイドバー -----------------
st.sidebar.title("設定")

with st.sidebar:
    st.write("モデル")
    
    # モデル選択用のオプションを作成（グループ別に整理）
    options_list = []
    options_dict = {}
    
    # 各クライアントごとにモデルを追加
    for client in model_names.keys():
        for model in model_names[client].keys():
            display_text = f"{client}: {model}"
            options_list.append(display_text)
            options_dict[display_text] = (client, model)
    
    # セレクトボックスを作成
    selected_option = st.selectbox(
        "モデルを選択",
        options=options_list,
        label_visibility="collapsed",
        placeholder="モデルを選択してください",
        key="model_selector"
    )
    
    # 選択されたモデルを解析
    selected_pair = None
    if selected_option and selected_option != "モデルを選択してください":
        client_name, model_name = options_dict.get(selected_option)

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
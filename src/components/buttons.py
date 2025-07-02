import streamlit as st
from utils.provider import model_names

def set_model_selector():
    # モデル選択用のオプションを作成（グループ別に整理）
    options_list = []
    options_dict = {}
    
    # 各クライアントごとにモデルを追加
    for client in model_names.keys():
        for model in model_names[client].keys():
            display_text = f"{client}: {model}"
            options_list.append(display_text)
            options_dict[display_text] = (client, model_names[client][model])
    
    # セレクトボックスを作成
    selected_option = st.selectbox(
        "モデルを選択",
        options=options_list,
        label_visibility="collapsed",
        placeholder="モデルを選択してください",
        key="model_selector"
    )
    
    if selected_option and selected_option != "モデルを選択してください":
        client_name, model_name = options_dict.get(selected_option)
        return client_name, model_name
    else:
        return None, None
    
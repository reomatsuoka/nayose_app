import streamlit as st
import base64
import toml
from utils.provider import LLMProvider
import io
import zipfile

config = toml.load("config.toml")

def seikyu(
        client_name,
        model_name
):
    st.title("請求書解析アプリ 📄")

    input_files = st.file_uploader("画像を選択してください", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    with st.expander("プロンプト詳細設定", expanded=False):
        system_prompt = st.text_area("システムプロンプト", value=config["prompts"]["system_prompt"])
        user_prompt = st.text_area("ユーザープロンプト", value=config["prompts"]["user_prompt"])

    analyze = st.button("解析する", disabled=(len(input_files) == 0))

    if analyze and input_files:
        client = LLMProvider(
            client_name=client_name,
            model_name=model_name
        ).get_client()

        csv_files_data = []

        for input_file in input_files:
            st.markdown(f"---")
            st.info(f"**{input_file.name}** を解析中...")
            try:
                img_bytes = input_file.read()
                data_url = (
                    "data:image/png;base64," + base64.b64encode(img_bytes).decode("utf-8")
                )

                output_text = client.generate_content_with_image(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    image_url=data_url
                )
                st.write(f"**{input_file.name}** の解析が完了しました。")
                
                header = "請求書番号,発行日,支払期日,合計金額\n"
                csv_data = header + output_text

                file_stem = input_file.name.rsplit('.', 1)[0]
                csv_filename = f"analysis_result_{file_stem}.csv"

                csv_files_data.append((csv_filename, csv_data))

            except Exception as e:
                st.error(f"**{input_file.name}** の解析中にエラーが発生しました。詳細はターミナルログをご確認ください。")
                st.exception(e)

        if csv_files_data:
            st.markdown("---")
            if len(csv_files_data) == 1:
                st.write("解析が完了しました。以下のボタンからCSVがダウンロードできます。")
                file_name, data = csv_files_data[0]
                st.download_button(
                    label="CSVをダウンロード",
                    data=data.encode("utf-8-sig"),
                    file_name=file_name,
                    mime="text/csv",
                )
            else:
                st.write("全ての解析が完了しました。以下のボタンからCSVファイルをまとめたZIPがダウンロードできます。")

                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for file_name, data in csv_files_data:
                        zip_file.writestr(file_name, data.encode("utf-8-sig"))
                
                st.download_button(
                    label=f"CSV (ZIP) をダウンロード",
                    data=zip_buffer.getvalue(),
                    file_name=f"analysis_results.zip",
                    mime="application/zip",
                )
    else:
        st.info("""
            請求書を選択し「解析する」を押してください。\n
            システムプロンプトとユーザープロンプトを変更したい場合は、「プロンプト詳細設定」を展開してください。
        """)
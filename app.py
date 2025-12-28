import streamlit as st
import google.generativeai as genai
import os

# 設定標題
st.title("🕵️‍♂️ IPAS AI 隨身教練")

# 嘗試抓取金鑰 (在 Streamlit Cloud 上會抓 Secrets，在本地會報錯提示)
try:
    # 如果是在 Streamlit Cloud 上，我們從 secrets 抓
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # 如果你在自己電腦跑，不想設定環境變數，暫時可以先寫死在這裡測試
    # 上傳到 GitHub 前記得刪掉，改成空字串或你的安全設定
    api_key = "你的_Gemini_API_Key_填在這裡"

if not api_key:
    st.error("請設定 Google API Key！")
    st.stop()

genai.configure(api_key=api_key)

# 設定 AI 教練大腦
model = genai.GenerativeModel(
    'gemini-1.5-flash', 
    system_instruction="你是一位嚴格的 IPAS AI 考照教練。請出 IPAS 難度的單選題考使用者，並在使用者答錯時給予引導，不要直接給答案。"
)

# 初始化聊天紀錄
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "model",
        "content": "學員你好！我是你的 IPAS 教練。準備好開始刷題了嗎？請輸入『出題』！"
    })

# 顯示歷史訊息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 處理使用者輸入
if prompt := st.chat_input("輸入你的回答..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages
        ])
        response = chat.send_message(prompt)

        st.session_state.messages.append({"role": "model", "content": response.text})
        with st.chat_message("model"):
            st.markdown(response.text)
    except Exception as e:
        st.error(f"連線錯誤：{e}")
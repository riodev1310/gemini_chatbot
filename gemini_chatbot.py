import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Thiết lập cấu hình trang
st.set_page_config(page_title="ChatGPT Clone with Gemini", layout="wide")

# Tiêu đề ứng dụng
st.title("🧠 ChatGPT UI Clone with Streamlit & Gemini")

# Hàm xử lý phản hồi của chatbot
def generate_bot_response(user_input):
    try:
        # Tạo conversation history từ session state
        conversation = [
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in st.session_state.chat_history
        ]
        # Thêm đầu vào hiện tại của người dùng
        conversation.append({"role": "user", "parts": [user_input]})

        # Khởi tạo model Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Tạo nội dung hội thoại để gửi tới API
        chat = model.start_chat(history=conversation)
        response = chat.send_message(user_input)
        
        # Làm sạch phản hồi
        bot_response = response.text.replace("*", "").strip()
        return bot_response
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

# Hàm lưu lịch sử chat vào file JSON
def save_chat_history():
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=2)

# Hàm tải lịch sử chat từ file JSON
def load_chat_history():
    try:
        with open("chat_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Khởi tạo session state để lưu lịch sử chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Hiển thị lịch sử chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận đầu vào từ người dùng
prompt = st.chat_input("Nhập tin nhắn của bạn...")

if prompt:
    # Lưu tin nhắn người dùng vào lịch sử
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gọi hàm generate_bot_response để lấy phản hồi từ Gemini
    response = generate_bot_response(prompt)
    
    # Hiển thị phản hồi của chatbot
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Lưu phản hồi vào lịch sử chat
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Lưu lịch sử chat vào file JSON
    save_chat_history()

# Nút xóa lịch sử chat
if st.button("Xóa lịch sử chat"):
    st.session_state.chat_history = []
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")
    st.rerun()
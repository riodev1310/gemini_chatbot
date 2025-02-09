import streamlit as st 
import google.generativeai as genai

# Khởi tạo session
genai.configure(api_key="api_key_from_ai_studio")

# Lấy model từ Gemini để sử dụng
model = genai.GenerativeModel("gemini-2.0-flash")

if "history" not in st.session_state: 
    st.session_state.history = []

# Tạo hàm mô hình
def generate_bot_response(question):
    response = model.generate_content(question)
    bot_response = response.text.replace("*", "")
    save_conversation(question, bot_response)
    return bot_response

def save_conversation(question, response):
    conversation = {
        "you": question,
        "bot": response
    }
    st.session_state.history.append(conversation)
    # st.write(st.session_state.history)

st.title("Streamlit Chatbot") 

user_question = st.text_input("Question: ")

ask_button = st.button("Ask")

# Xử lý sự kiện khi người dùng click vào nút Ask
if ask_button and user_question:
    bot_response = generate_bot_response(st.session_state.user_question)
    
    # Hiển thị các cuộc đối thoại giữa user và bot
    for conversation in st.session_state.history:
        st.subheader("You: ")
        st.write(conversation["you"])
        st.subheader("Bot: ")
        st.write(conversation["bot"])
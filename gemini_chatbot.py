import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set Streamlit page configuration
st.set_page_config(page_title="Gemini Chatbot", page_icon=":speech_balloon:", layout="wide")

# Store conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to generate a response based on user input and conversation history
def generate_bot_response(user_input):
    # Add user input to conversation history
    st.session_state.history.append(f"You: {user_input}")

    # Combine the conversation history for context
    conversation_history = "\n".join(st.session_state.history)

    # Use the generative model with the conversation history
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(conversation_history)
    bot_response = response.text.replace("*", "")  # Clean up any special characters if needed

    # Add bot response to history
    st.session_state.history.append(f"Bot: {bot_response}")
    return bot_response

# Display chat interface
st.title("Gemini Chatbot")

# Display the input box inside the container
user_message = st.text_input("You:")

# Process the user's message when they click "Ask"
if st.button("Ask"):
    if user_message:
        bot_response = generate_bot_response(user_message)
        
        # Show the updated conversation
        for message in st.session_state.history:
            if message.startswith("You:"):
                st.markdown("### **You:**")
                st.markdown(f"{message[4:]}", unsafe_allow_html=True)
            elif message.startswith("Bot:"):
                st.markdown("### **Bot:**")
                st.markdown(f""" {message[4:]}""", unsafe_allow_html=True)
                st.write("="*130)
    else:
        st.write("Please enter a message.")
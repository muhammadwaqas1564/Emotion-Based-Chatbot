import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate


GOOGLE_API_KEY = 'AIzaSyA0426ezmDuv6_Inx6OLDhRsFERW_VZvmk'
llm = GoogleGenerativeAI(model='gemini-pro', google_api_key=GOOGLE_API_KEY, temperature=0.7)

emoji_map = {
    "happy": "😊",
    "sad": "😢",
    "angry": "😠",
    "excited": "🎉",
    "neutral": "😐",
}

# Function to generate chatbot response based on emotion
def chat_with_emotion(emotion, user_input):
    prompt_template = f"""
    You are a chatbot capable of expressing different emotions in your responses. 
    Respond with a {emotion} tone to the following user message:

    USER MESSAGE: {user_input}

    Your Response (in {emotion} tone):
    """


    prompt = PromptTemplate(template=prompt_template, input_variables=["user_input"])
    prompt_text = prompt.format(user_input=user_input)
    response = llm.invoke(prompt_text)

    return response

# Streamlit app setup
st.title("Emotional Chatbot 🤖")

# Persistent emotion using session state
# "session_state" is a powerful feature that allows you to manage and persist data across user interactions during a session. This is particularly useful for creating interactive applications where you want to maintain state information without requiring the user to re-enter data every time they interact with the app.
if 'emotion' not in st.session_state:
    # Set the default emotion
    st.session_state.emotion = "happy"  

# Select the emotion in the sidebar
# Update the state, when user enter the emotion
emotion = st.sidebar.selectbox("Select an emotion for the chatbot 🤖:", ["happy", "sad", "angry", "excited", "neutral"])
st.session_state.emotion = emotion

# it wil display the selected emotion
st.sidebar.write(f"Selected Emotion: {st.session_state.emotion} {emoji_map[emotion]}")

# Input field for user message
user_input = st.text_input("You:", placeholder="Type your message here...")

# It save the history for displaying
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# When the user sends a message
if st.button("Send"):
    if user_input:
        emotion = st.session_state.emotion
        bot_response = chat_with_emotion(emotion, user_input)

        # Display the conversation
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(f"Chatbot ({emotion}{emoji_map[emotion]}): {bot_response}")

# Display chat history
for message in st.session_state.chat_history:
    st.write(message)

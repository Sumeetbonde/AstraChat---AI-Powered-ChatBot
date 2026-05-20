from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title = "AstraChat",
    page_icon = "https://media.istockphoto.com/id/1309421900/vector/abstract.jpg?s=170667a&w=0&k=20&c=gqazf_Fxz15vGteQrGYqrKCg5raM-fiqhZusJ4QdTnc=", 
    layout="centered"
)
st.title("AstraChat - How can I help you?")

# chat history
chat_history = []


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# show chat history even after page refresh
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]): #message["role"] -> user or assistant
        st.markdown(message["content"])

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.7,
    api_key = os.getenv("GEMINI_API_KEY")
)

# input from user box
user_prompt = st.chat_input("Ask Astra Something...")

# on clicking send button
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({
        "role":"user",
        "content": user_prompt
    })

    response = llm.invoke(
        input=[
            {
                "role": "system",
                "content" : "You are a helpful assistant. Be concise and to the point."
            },
            *st.session_state.chat_history
        ]
    )

    assistant_reponse = response.text.strip()
    st.session_state.chat_history.append(
        {
            "role":"assistant",
            "content": assistant_reponse
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reponse)


# Footer
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #0e1117;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    z-index: 100;
}
</style>

<div class="footer">
    Made with ❤️ by Sumeet
</div>
""", unsafe_allow_html=True)

# flow -> user input -> store in chat history -> send chat history to llm  -> get response -> store in chat history -> show response in UI
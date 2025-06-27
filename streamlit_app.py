import streamlit as st
import requests

st.set_page_config(page_title="Calendar Booking Assistant")

st.title("📅 Calendar Chatbot")

if st.sidebar.button("🔐 Login with Google"):
    st.markdown("[Click here to login](https://calendar-backend-fastapi.onrender.com/api/login)")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "memory" not in st.session_state:
    st.session_state.memory = {}


user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    # Send input to FastAPI backend
    response = requests.post(
        "https://calendar-backend-fastapi.onrender.com/api/chat",
        json={"message": user_input, "memory": st.session_state.memory}
    )
    
    data = response.json()  # ✅ Only call once!

    # ✅ FIRST store updated memory
    st.session_state.memory = data.get("memory", {})

    # Get reply and updated memory from backend
    reply = data.get("response")
    #st.session_state.memory = response.json().get("memory", {})  # ✅ Store updated memory
    
    st.sidebar.title("🧠 Debug Memory")
    st.sidebar.json(st.session_state.memory)
    print("Current memory:", st.session_state.memory)

    # Update chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", reply))

# Show chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑‍💻 {sender}:** {msg}")
    else:
        st.markdown(f"**🤖 {sender}:** {msg}")

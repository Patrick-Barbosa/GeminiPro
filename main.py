import streamlit as st
import google.generativeai as genai


ApiKey = st.secrets["GOOGLE_GEMINI_KEY"]

# Initialize Gemini-Pro
genai.configure(api_key=ApiKey)
model = genai.GenerativeModel('gemini-pro')

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Correção: Garantir a inicialização do 'chat' antes de acessá-lo
if "chat" not in st.session_state:
    st.session_state["chat"] = model.start_chat(history=[])

# Display Form Title
st.title("Teste o Gemini Pro!")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
prompt = st.text_input("Como posso te ajudar?")
if prompt:
    # Display user's last message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt)
    
    # Display last response
    with st.chat_message("assistant"):
        st.markdown(response.text)
import streamlit as st
import os
import google.generativeai as genai

# Configure a API key
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))
model = genai.GenerativeModel('Gemini 1.5 Pro (Preview only)')

# Função para adaptar o papel do modelo para o Streamlit
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Inicializa o histórico de chat no estado da sessão, se ainda não existir
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Exibe o título do formulário
st.title("Testando o Gemini Pro!")

# Exibe mensagens de chat anteriores
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Aceita a próxima mensagem do usuário e adiciona ao contexto
if prompt := st.chat_input("Como posso te ajudar?"):
    # Exibe a última mensagem do usuário
    st.chat_message("user").markdown(prompt)
    
    # Configuração personalizada de geração
    generation_config = genai.types.GenerationConfig(
        temperature=0.3  # Controla a aleatoriedade da geração
    )
    
    # Envia a entrada do usuário para o Gemini e lê a resposta, incluindo a configuração de geração
    response = st.session_state.chat.send_message(prompt, generation_config=generation_config)
    
    # Exibe a última resposta
    with st.chat_message("assistant"):
        st.markdown(response.text)

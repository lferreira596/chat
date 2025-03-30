import streamlit as st
import requests
import uuid

# 🔧 CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Delivery Insights",
    page_icon="🍕",
    layout="centered"
)

# 🎨 ESTILO PERSONALIZADO
st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        h1, h3 {
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .stChatInput input {
            border-radius: 8px !important;
            padding: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 🧑‍🍳 CABEÇALHO
st.markdown("<h1>🍕 Delivery Insights</h1>", unsafe_allow_html=True)
st.markdown("<h3>Converse com a IA e entenda os dados do seu delivery</h3>", unsafe_allow_html=True)

# 📷 IMAGEM DE DESTAQUE
st.image("delivery_banner.webp", use_container_width=True)

# 📌 EXEMPLOS
with st.expander("❓ Exemplos de perguntas"):
    st.markdown("""
    - Qual o ticket médio em São Paulo?
    - Quais produtos mais vendidos no bairro Moema?
    - Quantos pedidos foram feitos em janeiro?
    - Quanto tempo leva a entrega média no Rio de Janeiro?
    """)

# 🔁 RESET
if st.button("🔄 Nova conversa"):
    st.session_state.messages = []
    st.experimental_rerun()

# 🆔 ID de sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔗 Função para chamada da API
def ask_question(question):
    url = "http://20.197.225.152:5000/ask"
    payload = {"question": question}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get("answer", "Resposta vazia.")
        return f"Erro: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Erro de conexão com a API: {e}"

# 💬 Histórico
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"]):
        st.markdown(f"{avatar} {message['content']}")

# 📥 Input do usuário
prompt = st.chat_input("Ex: Qual o ticket médio em São Paulo?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(f"👤 {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("🤖 Pensando..."):
            answer = ask_question(prompt)
            st.markdown(f"🤖 {answer}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Antigravity AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        color: #f8fafc;
        font-weight: 800;
    }
    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .api-hint {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Try importing google-generativeai, handle if not installed
google_ai_installed = False
try:
    import google.generativeai as genai
    google_ai_installed = True
except ImportError:
    pass

# Header
st.title("🤖 Antigravity AI Chatbot")
st.markdown("<p class='subtitle'>Una interfaz web interactiva para chatear con Gemini fuera de la terminal.</p>", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # API Key Input
    api_key = st.text_input("Gemini API Key:", type="password", help="Obtén una clave gratuita en Google AI Studio.")
    st.markdown("[¿No tienes una API Key? Consigue una gratis aquí](https://aistudio.google.com/)", unsafe_allow_html=True)
    
    st.divider()
    
    # Model Selection
    model_option = st.selectbox(
        "Selecciona el modelo:",
        ("gemini-2.5-flash", "gemini-2.5-pro")
    )
    
    # System Prompt customization
    system_instruction = st.text_area(
        "Instrucción del Sistema (Personalidad):",
        value="Eres Antigravity, un asistente de programación inteligente y amigable. Respondes de forma clara, concisa y en español.",
        height=100
    )
    
    st.divider()
    
    # Clear conversation button
    if st.button("🗑️ Limpiar Conversación"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy Antigravity. Introduce tu API Key en la barra lateral para empezar a chatear con la versión real. Mientras tanto, puedo operar en modo de prueba offline."}
    ]

# Display existing chat messages
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # Add to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant", avatar="🤖"):
        # If API key is provided and google-generativeai is installed
        if api_key and google_ai_installed:
            try:
                # Configure API
                genai.configure(api_key=api_key)
                
                # Create Model with system instruction
                model = genai.GenerativeModel(
                    model_name=model_option,
                    system_instruction=system_instruction
                )
                
                # Construct history for the model
                # Format previous messages as chat history for Gemini
                chat = model.start_chat(history=[])
                
                # Send message and stream response
                with st.spinner("Pensando..."):
                    # We send the history manually or just generate content based on conversation
                    # For simplicity in this UI, we can build a prompt with the chat history context
                    context_prompt = ""
                    for msg in st.session_state.messages[:-1]:
                        role_name = "Usuario" if msg["role"] == "user" else "Asistente"
                        context_prompt += f"{role_name}: {msg['content']}\n"
                    context_prompt += f"Usuario: {prompt}\nAsistente:"
                    
                    response = model.generate_content(context_prompt, stream=True)
                    
                    # Stream response to Streamlit UI
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                error_msg = f"❌ Ocurrió un error al conectar con Gemini API:\n```\n{str(e)}\n```\nPor favor verifica tu API Key y tu conexión a internet."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            # Offline/Mock Mode
            response_placeholder = st.empty()
            mock_response = f"**[Modo Offline/Prueba]** Has dicho: '{prompt}'.\n\n*Nota: Para obtener respuestas reales de IA, ingresa una API Key de Gemini válida en la barra lateral.*"
            response_placeholder.markdown(mock_response)
            st.session_state.messages.append({"role": "assistant", "content": mock_response})

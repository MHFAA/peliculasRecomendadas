import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Cargar la clave API desde las variables de entorno
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Verificar si la clave API está disponible
if not OPENAI_API_KEY:
    st.error("⚠️ No se encontró la clave API de OpenAI. Agrega tu clave en Streamlit Cloud o en el archivo .env.")
    st.stop()

# Configurar OpenAI API
openai.api_key = OPENAI_API_KEY

# Función para obtener respuesta del chatbot
def get_response(user_input):
    prompt = f"""
    Actúa como un asistente de ayuda para migrantes y refugiados que llegan a una nueva ciudad. 
    Responde a preguntas sobre alojamiento, trámites legales, empleo, asistencia sanitaria y recursos esenciales.
    La pregunta del usuario es: {user_input}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Cambia a "gpt-3.5-turbo" si prefieres más rapidez y menor costo
            messages=[{"role": "system", "content": "Eres un asistente experto en orientación para migrantes y refugiados."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error en la API: {str(e)}"

# Configuración de la app en Streamlit
st.set_page_config(page_title="Asistente para Migrantes", layout="wide")

st.title("🌍 Chatbot de Ayuda para Migrantes y Refugiados")
st.write("Escribe tu pregunta sobre alojamiento, empleo, trámites o asistencia sanitaria en tu nueva ciudad.")

# Mantener historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial del chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Obtener respuesta del chatbot
    response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(response)


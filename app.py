import streamlit as st
import pickle
from pathlib import Path

st.set_page_config(
    page_title="Streamlit ML App",
    page_icon="🤖",
    layout="centered"
)

# 🔁 Ajusta el nombre si tu archivo se llama distinto
MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.pkl"

st.title("🤖 Streamlit ML App")
st.write("Verificando carga del modelo reutilizado (pickle)...")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    st.success(f"Modelo cargado correctamente ✅: {MODEL_PATH.name}")
    st.write("Tipo de objeto:", type(model))

except Exception as e:
    st.error("❌ No se pudo cargar el modelo.")
    st.write("Ruta intentada:")
    st.code(str(MODEL_PATH))
    st.exception(e)

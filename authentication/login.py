import streamlit as st
from models.professional import Profesional

def authenticate(db, session_state):  
    dni = st.text_input("DNI")
    password = st.text_input("Contraseña", type="password")

    # Alinear el botón de "Iniciar sesión" con los campos de entrada
    if st.button("Iniciar sesión"):
        if Profesional.verify_profesional(db, dni, password):
            session_state.logged_in = True
            session_state.professional_dni = dni  
            st.success("Inicio de sesión exitoso")
            return True
        else:
            st.error("Las credenciales no son correctas. Intente nuevamente.")
            return False

    # Agregar un mensaje para recuperar la contraseña
    st.markdown("**¿Olvidaste tu contraseña?** [Recupérala aquí](#)")
    return False



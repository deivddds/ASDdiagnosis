import streamlit as st
import pandas as pd
from streamlit import session_state
from PIL import Image
from models.database import SessionLocal, Base
from modules import home_page, data_management, new_diagnosis, diagnosis_history, resources_tools, settings
from constants.config import get_text, LANGUAGES
import streamlit as st
from models import Niño
from constants.config import get_text, LANGUAGES
from datetime import date
from sqlalchemy import Insert
import urllib.parse

def prevent_links(text):
    new_text = "\u200B".join(list(text))
    return new_text

def diagnosis_form_create(professional_dni):
    db = SessionLocal()  
    children = db.query(Niño).filter(Niño.dni_profesional == professional_dni).all()
    
    children_dict = {f"{child.nombre} {child.apellidos}": child.id_niño for child in children}
    child_name = st.selectbox('Seleccione el niño:', list(children_dict.keys()))
    child_id = children_dict[child_name]

    module_options = ["Modulo 1", "Modulo 2", "Modulo 3", "Modulo 4"]

    with st.expander("ADOS"):
        # Parte de ADOS
        col1, col2 = st.columns(2)
        with col1:
            module = col1.selectbox('Módulo', module_options)
            reciprocal_social_interaction = col1.number_input('CSR', min_value=0)

        with col2:
            total_score = col2.number_input('Puntuación total ADOS', min_value=0)
            restricted_repetitive_behaviour = col2.number_input('CRRE', min_value=0)

        evaluation_date = st.date_input('Fecha de la evaluación')
        conclusion = st.text_area('Conclusión del evaluador')

    with st.expander("MCHAT"):
        # Parte de M-CHAT
        col1, col2 = st.columns(2)
        with col1:
            total_risk_responses = col1.number_input('Número total de respuestas que indican un posible riesgo', min_value=0)
            mchat_result = col1.text_input('Resultado final del M-CHAT')

        with col2:
            critical_risk_responses = col2.number_input('Número de respuestas que indican un riesgo en preguntas críticas', min_value=0)
            mchat_date = col2.date_input('Fecha de la prueba M-CHAT')

        mchat_observations = st.text_area('Observaciones M-CHAT')

    with st.expander("Diagnóstico Facial"):
        # Adjuntar una foto
        photo_file = st.file_uploader("Cargar Foto", type=['png', 'jpg', 'jpeg'])
        if photo_file is not None:
            image = Image.open(photo_file)
            st.image(image, caption='Foto subida.', use_column_width=True)

    # Retornar los datos del formulario
    return {
        'child_id': child_id,
        'child_name': child_name,
        'module': module,
        'reciprocal_social_interaction': reciprocal_social_interaction,
        'total_score': total_score,
        'restricted_repetitive_behaviour': restricted_repetitive_behaviour,
        'evaluation_date': evaluation_date,
        'conclusion': conclusion,
        'total_risk_responses': total_risk_responses,
        'mchat_result': mchat_result,
        'critical_risk_responses': critical_risk_responses,
        'mchat_date': mchat_date,
        'mchat_observations': mchat_observations,
        'photo_file': photo_file
    }




def is_form_valid():
    # Completar con la lógica de validación del formulario
    pass

def display_new_diagnosis(session_state):
    if session_state.operation_result:
        st.success(session_state.operation_result)
        session_state.operation_result = ""

    db = SessionLocal()
    professional_dni = session_state.professional_dni

    st.sidebar.markdown("___")
    st.sidebar.subheader("Formulario de Nuevo Diagnóstico")

    with st.sidebar:
        with st.form("new_child_form"):
            diagnosis_form_data = diagnosis_form_create(professional_dni)
            diagnosis_result = None
            diagnosis_confidence = None
            if st.form_submit_button("Enviar diagnóstico"):
                with st.spinner('Procesando el diagnóstico...'):
                    # Llamada a la API
                    diagnosis_result, diagnosis_confidence = call_diagnosis_api(diagnosis_form_data['photo_file'])
                    
    # Verificación de que la respuesta de la API fue exitosa
    if diagnosis_result is not None and diagnosis_confidence is not None:
        display_diagnosis_preview(diagnosis_form_data, diagnosis_result, diagnosis_confidence)
    else:
        st.subheader("Formulario de Nuevo Diagnóstico")
        st.markdown("""
            #### Instrucciones para realizar el diagnóstico:
            1. Completa el formulario de diagnóstico en el panel de la izquierda.
            2. Asegúrate de completar todos los campos obligatorios.
            3. Haz clic en "Enviar diagnóstico" para procesar el diagnóstico.
            4. Una vez que el diagnóstico haya sido procesado, los resultados aparecerán aquí.
            """)

def call_diagnosis_api(image_file):
    # Llamada mockeada a la API utilizando la imagen
    diagnosis_result = True
    diagnosis_confidence = 89.3
    return diagnosis_result, diagnosis_confidence


def display_diagnosis_preview(form_data, diagnosis_result, diagnosis_confidence):
    db = SessionLocal() 
    st.subheader("Resultado del diagnostico")
    st.markdown("**Perfil**", unsafe_allow_html=True)
    
    
    child = db.query(Niño).filter(Niño.id_niño == form_data['child_id']).first()

    if child:
        col1, col2 = st.columns([1, 3])
        
        # Mostrar la foto del niño si está disponible
        if form_data['photo_file'] is not None:
            image = Image.open(form_data['photo_file'])
            col1.image(image, use_column_width=True)

        with col2:
            st.markdown(f"<p style='margin-bottom: 0.1rem;'><h4><strong>{child.nombre} {child.apellidos}</strong></h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 0.1rem;'>Fecha de nacimiento: {child.fecha_nacimiento}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 0.1rem;'>Género: {child.genero}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 0.1rem;'>Antecedentes familiares: {child.antecedentes_familiares}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 0.1rem;'>Diagnóstico previo: {child.diagnostico_previo}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin-bottom: 0.1rem;'>Observaciones: {child.observaciones}</p>", unsafe_allow_html=True)


    st.markdown("**Resultado**", unsafe_allow_html=True)

    diagnosis_confidence = prevent_links(f"{diagnosis_confidence}%")

    if diagnosis_result:
        st.markdown(f"""
        <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px; max-width: 500px; margin-bottom:20px;'>
            <div style='display: grid; grid-template-columns: 1fr 1fr;'>
                <p style='margin: 0;'><strong>Diagnóstico</strong></p>
                <p style='margin: 0;'><strong>Confianza</strong></p>
                <h2 style='color: green; margin: 0;'>Positivo</h2>
                <h2 style='margin: 0;'>{diagnosis_confidence}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #f0f0f0; padding: 20px; border-radius: 10px; max-width: 500px;margin-bottom:20px;'>
            <div style='display: grid; grid-template-columns: 1fr 1fr;'>
                <p style='margin: 0;'><strong>Diagnóstico</strong></p>
                <p style='margin: 0;'><strong>Confianza</strong></p>
                <h2 style='color: red; margin: 0;'>Negativo</h2>
                <h2 style='margin: 0;'>{diagnosis_confidence}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**MCHAT**", unsafe_allow_html=True)
    mchat_df = pd.DataFrame(
        {
            "Respuestas riesgo": [form_data['total_risk_responses']],
            "Resultado M-CHAT": [form_data['mchat_result']],
            "Respuestas críticas": [form_data['critical_risk_responses']],
            "Fecha prueba M-CHAT": [form_data['mchat_date']],
            "Observaciones M-CHAT": [form_data['mchat_observations']],
        }
    )

    st.dataframe(
        mchat_df,
        column_config =
        {
            "Respuestas riesgo": st.column_config.ProgressColumn(
                "Respuestas riesgo", 
                min_value=0, 
                max_value=20,  # Asegúrate de cambiar esto a la escala correcta
                format="%f"
            ),
            "Resultado M-CHAT": st.column_config.ProgressColumn(
                "Resultado M-CHAT", 
                min_value=0, 
                max_value=20,  # Asegúrate de cambiar esto a la escala correcta
                format="%f"
            ),
            "Respuestas críticas": st.column_config.ProgressColumn(
                "Respuestas críticas", 
                min_value=0, 
                max_value=20,  # Asegúrate de cambiar esto a la escala correcta
                format="%f"
            ),
        },
        hide_index=True,
    )
   
    st.markdown("**ADOS**", unsafe_allow_html=True)
    ados_df = pd.DataFrame(
        {
            "Módulo": [form_data['module']],
            "PT ADOS": [form_data['total_score']],
            "CSR": [form_data['reciprocal_social_interaction']],
            "CRRE": [form_data['restricted_repetitive_behaviour']],
            "Fecha de evaluación": [form_data['evaluation_date']],
            "Conclusión del evaluador": [form_data['conclusion']],
        }
    )

    st.dataframe(
        ados_df,
        column_config =
        
        {
        "PT ADOS": st.column_config.ProgressColumn(
            "PT ADOS", 
            min_value=0, 
            max_value=20,
            format="%f"
            ),
        "CSR": st.column_config.ProgressColumn(
            "CSR", 
            min_value=0, 
            max_value=16,
            format="%f"
            ),
        "CRRE": st.column_config.ProgressColumn(
            "CRRE", 
            min_value=0, 
            max_value=4,
            format="%f"
            ),
        },
        hide_index=True,
    )


if __name__ == "__main__":
    display_new_diagnosis(session_state)

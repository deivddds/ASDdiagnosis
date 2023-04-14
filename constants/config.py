# -*- coding: utf-8 -*-

# constants/config.py
LANGUAGES = {
    "es": [
        {"label": "Español", "code": "es"},
        {"label": "Inglés", "code": "en"},
    ],
    "en": [
        {"label": "Spanish", "code": "es"},
        {"label": "English", "code": "en"},
    ],
}

TEXTS = {
    "es": {
        "PAGE_TITLES": {"display_settings": "Configuración",},
        "SETTINGS_SECTIONS": {"language": "Idioma","theme": "Tema",},
        "SETTINGS_PROMPTS": {
            "select_language": "Selecciona el idioma",
            "select_theme": "Selecciona el tema",
        },
        "SETTINGS_ACTIONS": {"apply_changes": "Aplicar cambios",},
        "HOME_TITLE": "ADSdiagnosis",
        "HOME_MENU": "Seleccione una opción",
        "HOME_DESCRIPTION": "Herramienta para profesionales en el diagnóstico y seguimiento del Trastorno del Espectro Autista (TEA) en niños.",
        "MENU_ITEMS": {
            "display_home_page": "Página de inicio",
            "display_data_management": "Gestión de datos",
            "display_new_diagnosis": "Nuevo diagnóstico",
            "display_diagnosis_history": "Historial de diagnósticos",
            "display_resources_tools": "Recursos y herramientas",
            "display_settings": "Configuración",
        },
        "SIDEBAR_LINKS": {
            "research": "Investigaciones sobre TEA",
            "communities": "Comunidades y organizaciones",
            "tools_apps": "Herramientas y aplicaciones",
        },
        "USAGE_INSTRUCTIONS": """
Navegue por el menú de la izquierda para acceder a las diferentes secciones y funcionalidades de la aplicación. Utilice los botones de acciones principales para añadir nuevos niños o realizar diagnósticos.
""",
        "AUTHORS_LICENSE": {
            "authors": "Autor y desarrollador: David Molero Peña",
            "email": "Correo electrónico: d.molero@gmail.com",
            "profiles": "Perfiles en redes sociales o sitios web: [Enlaces a perfiles o sitios web]",
            "license": "Licencia: [Información de la licencia y créditos]",
        },
        "DATA_MANAGEMENT_VARIABLES": {
            "child_name": "Nombre del niño",
            "child_surname": "Apellidos del niño",
            "date_of_birth": "Fecha de nacimiento",
            "gender": "Género",
            "family_history": "Antecedentes familiares",
            "previous_diagnosis": "Diagnóstico previo",
            "observations": "Observaciones",
            "color": "Color",
            "child_data_updated_success": "Datos del niño actualizados con éxito",
            "update_child_data": "Actualizar información"
        },
    },
    "en": {
        "PAGE_TITLES": {
            "display_settings": "Settings",
        },
        "SETTINGS_SECTIONS": {
            "language": "Language",
            "theme": "Theme",
        },
        "SETTINGS_PROMPTS": {
            "select_language": "Select language",
            "select_theme": "Select theme",
        },
        "SETTINGS_ACTIONS": {
            "apply_changes": "Apply changes",
        },
        "HOME_TITLE": "ADSdiagnosis",
        "HOME_MENU": "Select page",
        "HOME_DESCRIPTION": "Tool for professionals in the diagnosis and monitoring of Autism Spectrum Disorder (ASD) in children.",
        "MENU_ITEMS": {
            "display_home_page": "Home",
            "display_data_management": "Data Management",
            "display_new_diagnosis": "New Diagnosis",
            "display_diagnosis_history": "Diagnosis History",
            "display_resources_tools": "Resources & Tools",
            "display_settings": "Settings",
        },
        "SIDEBAR_LINKS": {            "research": "ASD Research",
            "communities": "Communities & Organizations",
            "tools_apps": "Tools & Apps",
        },
        "USAGE_INSTRUCTIONS": """
Navigate the menu on the left to access the different sections and features of the application. Use the main action buttons to add new children or perform diagnoses.
""",
        "AUTHORS_LICENSE": {
            "authors": "Authors & Developers: [Names of authors and developers]",
            "email": "Email: [Email addresses]",
            "profiles": "Profiles on social networks or websites: [Links to profiles or websites]",
            "license": "License: [License information and credits]",
        },
        "DATA_MANAGEMENT_VARIABLES": {
            "child_name": "Child's Name",
            "child_surname": "Child's Surname",
            "date_of_birth": "Date of Birth",
            "gender": "Gender",
            "family_history": "Family History",
            "previous_diagnosis": "Previous Diagnosis",
            "observations": "Observations",
            "color": "Color",
            "child_data_updated_success": "Child Data Updated Success",
            "update_child_data": "Update Child Data"
        },
    },
}



def get_text(key, language):  
    return TEXTS[language][key]

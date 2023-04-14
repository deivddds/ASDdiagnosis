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
        "HOME_TITLE": "Seleccione una opción",
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
    },
    "en": {
        "HOME_TITLE": "Select page",
        "HOME_DESCRIPTION": "Tool for professionals in the diagnosis and monitoring of Autism Spectrum Disorder (ASD) in children.",
        "MENU_ITEMS": {
            "display_home_page": "Home",
            "display_data_management": "Data Management",
            "display_new_diagnosis": "New Diagnosis",
            "display_diagnosis_history": "Diagnosis History",
            "display_resources_tools": "Resources & Tools",
            "display_settings": "Settings",
        },
        "SIDEBAR_LINKS": {
            "research": "ASD Research",
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
    },
}

def get_text(key, language):  
    return TEXTS[language][key]

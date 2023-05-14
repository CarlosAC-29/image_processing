import streamlit as st
from process import process
from standarization import estandarization
from denoise import denoise_image
from borders import borders_image

PAGES = {
    "Process": {
        "Segmentation": process,
        "Borders": borders_image
    },
    "Pre process":{
        "Estandarization": estandarization,
        "Denoise": denoise_image
    }
}

# Mostrar selectbox para seleccionar la página
page = st.sidebar.selectbox("Seleccionar página", options=list(PAGES.keys()))

# Verificar qué página se ha seleccionado
if page in PAGES:
    subpage = st.sidebar.selectbox("Seleccionar subpágina", options=list(PAGES[page].keys()))
    PAGES[page][subpage]()

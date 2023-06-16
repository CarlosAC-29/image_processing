import streamlit as st
from process import process
from standarization import estandarization
from denoise import denoise_image
from borders import borders_image
from register import register
from visualizar import visualizar_page
from preprocess import estandarizar
from segmentar import segmentar_process
from registro import registro_process

# Definir las páginas y subpáginas
PAGES = {
    "Estandarizar": estandarizar,
    "Segmentar": segmentar_process,
    "Registro": registro_process
}

# Mostrar selectbox para seleccionar la página
page = st.sidebar.selectbox("Seleccionar página", options=list(PAGES.keys()))

# Verificar qué página se ha seleccionado
if page in PAGES:
    PAGES[page]()
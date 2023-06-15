import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os


def visualizar_page():
    archivos = os.listdir("temp")
    rutas_archivos = [os.path.join("temp", archivo) for archivo in archivos]
    input_file = st.selectbox("Seleccionar archivo", rutas_archivos)

    if input_file is not None:
        eje = st.selectbox("EJE", ["Selecciona", "x", "y", "z"])
        eje_image = 1



        image_data = nib.load(input_file)
        image = image_data.get_fdata()
        if eje == 'x':
            eje_image = st.slider("X", 0, np.shape(image)[0]-1)

        if eje == 'y':
            eje_image = st.slider("Y", 0, np.shape(image)[1]-1)

        if eje == 'z':
            eje_image = st.slider("Z", 0, np.shape(image)[2]-1)
        fig_img, ax_img = plt.subplots()
        if eje_image is not None and eje == 'x':
            ax_img.imshow(image[eje_image, :, :])
        if eje_image is not None and eje == 'y':
            ax_img.imshow(image[:, eje_image, :])
        if eje_image is not None and eje == 'z':
            ax_img.imshow(image[:, :, eje_image])

        st.pyplot(fig_img)
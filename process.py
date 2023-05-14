import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os
from segmentations.thresholding import threshold
from segmentations.kmeans import kmeans_segmentation

def process ():
    st.title("Segmentation")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    with st.container():

        option = st.radio("Seleccionar opción", ("Usar imagen del sistema", "Subir nueva imagen"))

        if option == 'Subir nueva imagen':
            input_file = st.file_uploader('Seleccionar archivo')
        else:
            archivos = os.listdir("temp")
            rutas_archivos = [os.path.join("temp", archivo) for archivo in archivos]
            input_file = st.selectbox("Seleccionar archivo", rutas_archivos)

        col1, col2 = st.columns(2)
        if input_file is not None:
            if option == 'Subir nueva imagen':
                with open(os.path.join("uploads", input_file.name), "wb") as f:
                    f.write(input_file.read())
                input_file_path = os.path.join("uploads", input_file.name)
            else:
                input_file_path = input_file

            eje = col2.selectbox("EJE", ["Selecciona", "x", "y", "z"])
            eje_image = 1



            image_data = nib.load(input_file_path)
            image = image_data.get_fdata()
            if eje == 'x':
                eje_image = col2.slider("X", 0, np.shape(image)[0]-1)

            if eje == 'y':
                eje_image = col2.slider("Y", 0, np.shape(image)[1]-1)

            if eje == 'z':
                eje_image = col2.slider("Z", 0, np.shape(image)[2]-1)
            fig_img, ax_img = plt.subplots()
            if eje_image is not None and eje == 'x':
                ax_img.imshow(image[eje_image, :, :])
            if eje_image is not None and eje == 'y':
                ax_img.imshow(image[:, eje_image, :])
            if eje_image is not None and eje == 'z':
                ax_img.imshow(image[:, :, eje_image])

            col1.pyplot(fig_img)


        tipo_segmentacion = st.selectbox("Tipo de segmentacion", ["Selecciona una opción","Umbralización", "kmeans", "Region Growing"])
        if( tipo_segmentacion ==  'Umbralización'):
            tau = st.text_input("TAU:")
            tolerancia = st.text_input("Tolerancia:")
            buttons_Umbralización = st.button("segmentate")
            if buttons_Umbralización:
                if image is not None:
                    segmentation = threshold(image, float(tau), float(tolerancia))
                    fig_proc, ax_proc = plt.subplots()
                    ax_proc.imshow(segmentation[:,:,20])
                    st.pyplot(fig_proc)
                else:
                    st.warning("Primero cargue una imagen antes de realizar la segmentación")


        if( tipo_segmentacion ==  'kmeans'):
            tolerancia = st.text_input("Tolerancia:")
            number_of_k = st.text_input("K #:")
            iterations = st.text_input("Iterations:")
            buttons_kmeans = st.button("segmentate")
            if buttons_kmeans:
                segmentation = kmeans_segmentation(image, int(number_of_k), int(tolerancia), int(iterations))
                fig_procs, ax_procs = plt.subplots()
                ax_procs.imshow(segmentation[:,:,eje_image])
                st.pyplot(fig_procs)
            else:
                st.warning("Primero cargue una imagen antes de realizar la segmentación")


        if( tipo_segmentacion ==  'Region Growing'):
            tolerancia = st.text_input("Tolerancia:")
            tau = st.text_input("TAU:")
            seed_x = st.slider("Seed initial position X", 0, 100)
            seed_y = st.slider("Seed initial position Y", 0, 100)
            seed_z = st.slider("Seed initial position Z", 0, 100)
            buttons_Region_Growing = st.button("segmentate")
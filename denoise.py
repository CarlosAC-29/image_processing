import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
from denoising.mean_filter import mean_filter_image
from denoising.median_filter import median_filter

def denoise_image():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")


    with st.container():
        st.title("Denoise")

        option = st.radio("Seleccionar opción", ("Usar imagen del sistema", "Subir nueva imagen"))

        if option == 'Subir nueva imagen':
            input_file = st.file_uploader('Seleccionar archivo')
        else:
            archivos = os.listdir("temp")
            rutas_archivos = [os.path.join("temp", archivo) for archivo in archivos]
            input_file = st.selectbox("Seleccionar archivo", rutas_archivos)

        if input_file is not None:
            if option == 'Subir nueva imagen':
                with open(os.path.join("uploads", input_file.name), "wb") as f:
                    f.write(input_file.read())
                input_file_path = os.path.join("uploads", input_file.name)
            else:
                input_file_path = input_file

            image_data = nib.load(input_file_path)
            image_array = image_data.get_fdata()
            nombre_archivo = st.text_input("Nombre del archivo con remoción de ruido","Denoised")
            metodo = st.radio(
            "Metodo de remoción de ruido",
            ('mean filter', 'median filter'))
            standardize = st.button("Denoise")

            

            if standardize and metodo == 'mean filter':


                filtered_image = mean_filter_image(image_array)

                # Obtener la información de afine de la imagen original
                affine = image_data.affine

                # Reconstruir la imagen estandarizada con la información de afine
                reconstructed_image = nib.Nifti1Image(filtered_image, affine)
                output_path = os.path.join("temp", nombre_archivo+".nii.gz")
                nib.save(reconstructed_image, output_path)

                st.success("Imagen estandarizada guardada correctamente.")
            elif standardize and metodo == 'median filter':

                filtered_image = median_filter(image_array)

                # Obtener la información de afine de la imagen original
                affine = image_data.affine

                # Reconstruir la imagen estandarizada con la información de afine
                reconstructed_image = nib.Nifti1Image(filtered_image, affine)
                output_path = os.path.join("temp", nombre_archivo+".nii.gz")
                nib.save(reconstructed_image, output_path)
                
                fig, ax1 = plt.subplots(1, figsize=(10, 5))

                ax1.imshow(filtered_image[:, :, 24])
                ax1.set_title('Imagen')
            

                st.pyplot(fig)

                st.success("Imagen estandarizada guardada correctamente.")

            if os.path.exists("temp"+"/"+ nombre_archivo+".nii.gz"):

                image_data_view = nib.load("temp"+"/"+ nombre_archivo+".nii.gz")
                image_array_view = image_data_view.get_fdata()
                eje = st.slider('#',0,np.shape(image_array_view)[2]-1)
                fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10, 5))
                ax1.imshow(image_array_view[:, :, eje])
                ax1.set_title('Remocion de ruido')
                ax2.imshow(image_array[:,:,eje])
                ax2.set_title('Original')
                st.pyplot(fig)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
from image_borders.df import central_dif

def borders_image():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")


    with st.container():
        st.title("Borders")

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
            nombre_archivo = st.text_input("Nombre del archivo con borders","Bordered")

            process = st.button("Process")
            
            if process :
                borderd_image = central_dif(image_array)

                # Obtener la información de afine de la imagen original
                affine = image_data.affine

                # Reconstruir la imagen estandarizada con la información de afine
                reconstructed_image = nib.Nifti1Image(borderd_image, affine)
                output_path = os.path.join("temp", nombre_archivo+".nii.gz")
                nib.save(reconstructed_image, output_path)
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

                ax1.imshow(borderd_image[:, :, 24])
                ax1.set_title('Imagen')
                
                ax2.hist(borderd_image[borderd_image>0.01].flatten(), 100, alpha=0.5)
                ax2.set_title('Histograma')

                st.pyplot(fig)

                st.success("Imagen estandarizada guardada correctamente.")
            
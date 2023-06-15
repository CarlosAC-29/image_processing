import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
from standardization.rescale import rescale_image
from standardization.zscore import zscore_image
from standardization.whiteStripe import whitestripe_image
from standardization.histogram_matching import histogram_matching

def estandarization():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    with st.container():
        st.title("Standardization")

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

            fig_original, ax_fig_original = plt.subplots()
            ax_fig_original.hist(image_array[image_array>0.01].flatten(), 100, alpha=0.5)
            ax_fig_original.set_title('Histograma')
            st.pyplot(fig_original)

            nombre_archivo = st.text_input("Nombre del archivo estandarizado", "estandarizada")
            metodo = st.radio("Método de estandarización", ('rescale', 'z-score', 'white stripe', 'histogram matching'))
            if metodo == 'histogram matching':
                target = st.file_uploader('Seleccionar archivo', key='target')
                number_of_k = st.text_input("K #:")
                standardize = st.button("Estandarizar histogram")
                if target is not None:
                    with open(os.path.join("histogram", target.name), "wb") as f:
                        f.write(target.read())
                        target_file_path = os.path.join("histogram", target.name)
                        image_data_target = nib.load(target_file_path)
                if standardize :
                    estandarized_image_hist = histogram_matching(image_data_target, image_data, int(number_of_k))
                    affine = image_data.affine

                    # Reconstruir la imagen estandarizada con la información de afine
                    reconstructed_image = nib.Nifti1Image(estandarized_image_hist, affine)
                    output_path = os.path.join("temp", nombre_archivo + ".nii.gz")
                    nib.save(reconstructed_image, output_path)
                    st.success("Imagen estandarizada guardada correctamente.")
            else:
                standardize = st.button("Estandarizar")
                if standardize:
                    if metodo == 'rescale':
                        estandarized_image = rescale_image(image_array)
                    elif metodo == 'z-score':
                        estandarized_image = zscore_image(image_array)
                    elif metodo == 'white stripe':
                        estandarized_image = whitestripe_image(image_array)

                    affine = image_data.affine

                    # Reconstruir la imagen estandarizada con la información de afine
                    reconstructed_image = nib.Nifti1Image(estandarized_image, affine)
                    output_path = os.path.join("temp", nombre_archivo + ".nii.gz")
                    nib.save(reconstructed_image, output_path)
                    st.success("Imagen estandarizada guardada correctamente.")
    
            if os.path.exists("temp"+"/"+nombre_archivo+".nii.gz"):

                image_data_view = nib.load("temp"+"/"+ nombre_archivo+".nii.gz")
                st.write(nombre_archivo)
                image_array_view = image_data_view.get_fdata()
                fig, (ax1) = plt.subplots(1, figsize=(10, 5))
                ax1.hist(image_array_view[image_array_view>0.01].flatten(), 100)
                ax1.set_title('Histograma')
                st.pyplot(fig)

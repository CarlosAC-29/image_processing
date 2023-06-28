import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os
from standardization.zscore import zscore_image
from standardization.rescale import rescale_image
from standardization.whiteStripe import whitestripe_image
from standardization.histogram_matching import histogram_matching
from denoising.mean_filter import mean_filter_image
from denoising.mean_filter import mean_filter_with_edges
from denoising.median_filter import medianFilterBorders
from denoising.median_filter import median_filter

def estandarizar ():
    st.title("Preprocesar")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    with st.container():

        T1_image = None
        FLAIR_image = None
        IR_image = None

        input_files = st.file_uploader('Ingresa las imágenes del paciente', accept_multiple_files=True)

        # Procesar cada archivo subido
        file_paths = []
        if input_files:
            for file in input_files:
                file_name = file.name
                file_path = os.path.join('uploads', file_name)
                with open(file_path, 'wb') as f:
                    f.write(file.getbuffer())
                file_paths.append(file_path)

        # Mostrar los paths de los archivos subidos
        for path in file_paths:
            if "T1" in path :
                T1_image = path
            if "FLAIR" in path :
                FLAIR_image = path
            if "IR" in path :
                IR_image = path
        
        if T1_image and IR_image != None: 
            st.title("Prerprocesar")
            image_T1 = nib.load(T1_image)
            image_T1_data = image_T1.get_fdata()
            image_IR = nib.load(IR_image)
            image_IR_data = image_IR.get_fdata()

            Finish_t1 = None
            Finish_ir = None

            opcion_estandarize = st.radio("Selecciona una opción", (None, "z-score", "rescaling", "whitestripe", "histogram matching"))

            if opcion_estandarize is not None :
                if opcion_estandarize == "z-score" :
                
                    ### ESTANDARIZAR IMAGEN
                    Estandarize_t1 = zscore_image(image_T1_data)
                    Estandarize_ir = zscore_image(image_IR_data)
                    Finish_t1 = "Success"
                    Finish_ir = "Success"
                    
                
                if opcion_estandarize == "rescaling":

                    ## ESTANDARIZAR IMAGEN
                    Estandarize_t1 = rescale_image(image_T1_data)
                    Estandarize_ir = rescale_image(image_IR_data)
                    Finish_t1 = "Success"
                    Finish_ir = "Success"

                if opcion_estandarize == "whitestripe":
                    ## ESTANDARIZAR IMAGEN
                    Estandarize_t1 = whitestripe_image(image_T1_data)
                    Estandarize_ir = whitestripe_image(image_IR_data)
                    Finish_t1 = "Success"
                    Finish_ir = "Success"
                
                if opcion_estandarize == "histogram matching":
                    ## ESTANDARIZAR IMAGEN
                    target_t1 = st.file_uploader('Ingresa imagen de referencia para la imagen t1')
                    target_ir = st.file_uploader('Ingresa imagen de referencia para la imagen ir')
                    if target_t1 and target_ir is not None:
                        target_file_path_t1 = os.path.join("uploads", target_t1.name)
                        with open(target_file_path_t1, "wb") as f:
                            f.write(target_t1.getbuffer())
                        image_target_t1 = nib.load(target_file_path_t1)
                        image_target_data_t1 = image_target_t1.get_fdata()

                        target_file_path_ir = os.path.join("uploads", target_ir.name)
                        with open(target_file_path_ir, "wb") as f:
                            f.write(target_ir.getbuffer())
                        image_target_ir = nib.load(target_file_path_ir)
                        image_target_data_ir = image_target_ir.get_fdata()

                        
                        number_of_k_t1 = st.text_input("K # (T1):", key="k_t1_estan")    
                        number_of_k_ir = st.text_input("K # (IR):", key="k_ir_estan")

                        standarize = st.button("Start")
                        if standarize :
                            Estandarize_t1 = histogram_matching(image_T1_data, image_target_data_t1, int(number_of_k_t1))
                            Estandarize_ir = histogram_matching(image_IR_data, image_target_data_ir, int(number_of_k_ir))
                            Finish_t1 = "Success"
                            Finish_ir = "Success"
            
            ### REMCION DE RUIDO IMAGEN

            if Finish_t1 and Finish_ir is not None: 
                opcion_denoised= st.radio("Selecciona una opción", (None, "mean filter", "median filter", "mean filter with edges", "median filter with edges"))
                if opcion_denoised is not None :
                    if opcion_denoised == "mean filter" :

                        Denoised_t1 = mean_filter_image(Estandarize_t1)
                        Denoised_ir = mean_filter_image(Estandarize_ir)
                    
                    if opcion_denoised == "median filter" :

                        Denoised_t1 = median_filter(Estandarize_t1)
                        Denoised_ir = median_filter(Estandarize_ir)
                    
                    if opcion_denoised == "mean filter with edges" :
                        Denoised_t1 = mean_filter_with_edges(Estandarize_t1)
                        Denoised_ir = mean_filter_with_edges(Estandarize_ir)

                    if opcion_denoised == "median filter with edges" :
                        Denoised_t1 = medianFilterBorders(Estandarize_t1)
                        Denoised_ir = medianFilterBorders(Estandarize_ir)



                    # Crear un contenedor vacío para la imagen
                    container = st.empty()

                    # Mostrar la imagen actualizada en el contenedor vacío
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                    ax1.imshow(Denoised_t1[:, :, 25])
                    ax1.set_title('T1')
                    ax2.imshow(Denoised_ir[:, :, 25])
                    ax2.set_title('IR')
                    container.pyplot(fig)

                    # Obtener la información de afine de la imagen original
                    affine_t1 = image_T1.affine
                    affine_ir = image_IR.affine
                    
                    # Reconstruir la imagen estandarizada con la información de afine
                    reconstructed_image_t1 = nib.Nifti1Image(Denoised_t1.astype(np.float32), affine_t1)
                    reconstructed_image_ir = nib.Nifti1Image(Denoised_ir.astype(np.float32), affine_ir)
                    
                    # Guardar la imagen estandarizada en formato NIfTI
                    output_path_t1 = os.path.join("temp", "Preprocess_t1.nii.gz")
                    output_path_ir = os.path.join("temp", "Preprocess_ir.nii.gz")
                    nib.save(reconstructed_image_t1, output_path_t1)
                    nib.save(reconstructed_image_ir, output_path_ir)
                    
                    # Agregar un enlace para descargar el archivo NIfTI generado
                    st.success("Imagen estandarizada guardada correctamente.")
                    # Agregar el botón de descarga
                    if os.path.exists(output_path_t1):
                        with open(output_path_t1, "rb") as file:
                            st.download_button("Descargar archivo", data=file, file_name="Preprocess_t1.nii.gz")

                    if os.path.exists(output_path_ir):
                        with open(output_path_ir, "rb") as file:
                            st.download_button("Descargar archivo", data=file, file_name="Preprocess_ir.nii.gz")
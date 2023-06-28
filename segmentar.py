import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os
from segmentations.kmeans import kmeans_segmentation
from segmentations.regionGrowing import region_growing_image
from segmentations.thresholding import threshold


def segmentar_process ():
    st.title("Segmentate")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    with st.container():

        T1_image = './temp/Preprocess_t1.nii.gz'
        IR_image = './temp/Preprocess_ir.nii.gz'

        # input_files = st.file_uploader('Ingresa las imágenes del paciente', accept_multiple_files=True)

        
        if os.path.exists(T1_image) and os.path.exists(IR_image):
    
            image_T1 = nib.load(T1_image)
            image_T1_data = image_T1.get_fdata()
            image_IR = nib.load(IR_image)
            image_IR_data = image_IR.get_fdata()

            Finish_t1 = None
            Finish_ir = None


            opcion_segmentar = st.radio("Selecciona una opción", (None, "kmeans", "isodata", "region growing",))
            
            if opcion_segmentar == "kmeans" :
                ### SEGMENTAR IMAGEN
                st.title("T1")
                number_of_k_t1 = st.text_input("K # (T1):", key="k_t1")
                iterations_t1 = st.text_input("Iterations (T1):", key="iter_t1")

                st.title("IR")
                number_of_k_ir = st.text_input("K # (IR):", key="k_ir")
                iterations_ir = st.text_input("Iterations (IR):", key="iter_ir")

                buttons_kmeans= st.button("Segmentate")

                if buttons_kmeans:
                    # Realizar la segmentación utilizando K-means
                    segmentation_t1 = kmeans_segmentation(image_T1_data,int(iterations_t1), int(number_of_k_t1))
                    segmentation_ir = kmeans_segmentation(image_IR_data,int(iterations_ir), int(number_of_k_ir))
                    Finish_t1 = "Success"
                    Finish_ir = "Success"
            
            if opcion_segmentar == "isodata" :
                ### SEGMENTAR IMAGEN
                st.title("T1")
                number_TAU_t1 = st.text_input("TAU # (T1):", key="TAU_t1")
                t1_TOL = st.text_input("TOL (T1):", key="TOL_t1")

                st.title("IR")
                # number_TAU_t1 = st.text_input("TAU # (IR):", key="TAU_ir")
                # ir_TOL = st.text_input("TOL (IR):", key="TOL_ir")
                number_of_k_ir = st.text_input("K # (IR):", key="k_ir")
                iterations_ir = st.text_input("Iterations (IR):", key="iter_ir")

                buttons_isodata= st.button("Segmentate")

                if buttons_isodata:
                    # Realizar la segmentación utilizando K-means
                    segmentation_t1 = threshold(image_T1_data,int(number_TAU_t1), int(t1_TOL))
                    segmentation_ir = kmeans_segmentation(image_IR_data,int(iterations_ir), int(number_of_k_ir))
                    Finish_t1 = "Success"
                    Finish_ir = "Success"
            
            if opcion_segmentar == "region growing" :
                ### SEGMENTAR IMAGEN
                st.title("T1")
                tolerancia_t1 = st.text_input("Tolerancia:", key="tol_t1_region")
                seed_x_t1 = st.slider("Seed initial position X", 0, np.shape(image_T1_data)[0]-1)
                seed_y_t1 = st.slider("Seed initial position Y", 0, np.shape(image_T1_data)[1]-1)
                seed_z_t1 = st.slider("Seed initial position Z", 0, np.shape(image_T1_data)[2]-1)

                st.title("IR")
                # tolerancia_ir = st.text_input("Tolerancia:")
                # seed_x_ir = st.slider("Seed initial position X", 0, np.shape(image_IR_data)[0]-1)
                # seed_y_ir = st.slider("Seed initial position Y", 0, np.shape(image_IR_data)[1]-1)
                # seed_z_ir = st.slider("Seed initial position Z", 0, np.shape(image_IR_data)[2]-1)
                number_of_k_ir = st.text_input("K # (IR):", key="k_ir")
                iterations_ir = st.text_input("Iterations (IR):", key="iter_ir")

                buttons_isodata= st.button("Segmentate", key="tol_ir_region")

                if buttons_isodata:
                    # Realizar la segmentación utilizando K-means
                    segmentation_t1 = region_growing_image(image_T1_data,int(seed_x_t1),int(seed_y_t1), int(seed_z_t1),int(tolerancia_t1))
                    segmentation_ir = kmeans_segmentation(image_IR_data,int(iterations_ir), int(number_of_k_ir))
                    Finish_t1 = "Success"
                    Finish_ir = "Success"

            if Finish_t1 and Finish_ir is not None :
                # Mostrar la imagen segmentada
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                ax1.imshow(segmentation_t1[:,:,25])
                ax1.set_title('T1')
                ax2.imshow(segmentation_ir[:,:,25])
                ax2.set_title('IR')
                st.pyplot(fig)
                
                # Obtener la información de afine de la imagen original
                affine_t1 = image_T1.affine
                affine_ir = image_IR.affine
                
                # Reconstruir la imagen estandarizada con la información de afine
                reconstructed_image_t1 = nib.Nifti1Image(segmentation_t1.astype(np.float32), affine_t1)
                reconstructed_image_ir = nib.Nifti1Image(segmentation_ir.astype(np.float32), affine_ir)
                
                # Guardar la imagen estandarizada en formato NIfTI
                output_path_t1 = os.path.join("temp", "Segmentation_t1.nii.gz")
                output_path_ir = os.path.join("temp", "Segmentation_ir.nii.gz")
                nib.save(reconstructed_image_t1, output_path_t1)
                nib.save(reconstructed_image_ir, output_path_ir)
                
                # Agregar un enlace para descargar el archivo NIfTI generado
                st.success("Imagen estandarizada guardada correctamente.")

                # Agregar el botón de descarga
                if os.path.exists(output_path_t1):
                    with open(output_path_t1, "rb") as file:
                        st.download_button("Descargar archivo t1", data=file, file_name="Segmentation_t1.nii.gz")

                if os.path.exists(output_path_ir):
                    with open(output_path_ir, "rb") as file:
                        st.download_button("Descargar archivo ir", data=file, file_name="Segmentation_ir.nii.gz")
        else:
            st.success("No se preprocesaron la imagenes")
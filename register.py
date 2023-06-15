import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import os
from segmentations.thresholding import threshold
from segmentations.kmeans import kmeans_segmentation
from segmentations.regionGrowing import region_growing_image
from image_registration.rigid_registration import registro_rigido

def register():
    st.title("Registro")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    with st.container():
    

        input_file_movil = st.file_uploader('Seleccionar imagen móvil')
        input_file_fixed = st.file_uploader('Seleccionar imagen de referencia')
        Nombre_archivo = st.text_input("Como quiere guardar el archivo")

        if input_file_movil is not None:
            with open(os.path.join("uploads", input_file_movil.name), "wb") as f:
                f.write(input_file_movil.read())

        if input_file_fixed is not None:
            with open(os.path.join("uploads", input_file_fixed.name), "wb") as f:
                f.write(input_file_fixed.read())

        col1, col2 = st.columns(2)
        registrar = st.button("Registar")

        if registrar :
            if input_file_movil and input_file_fixed and Nombre_archivo is not None:

                input_file_path_movil = os.path.join("uploads", input_file_movil.name)
                input_file_path_fixed = os.path.join("uploads", input_file_fixed.name)

                if os.path.exists(input_file_path_movil) and os.path.exists(input_file_path_fixed):
                    registro_rigido_final = registro_rigido(input_file_path_movil, input_file_path_fixed)
                    # eje = st.slider('#', 0, np.shape(registro_rigido_final)[2] - 1)
                    fig, (ax1) = plt.subplots(1, figsize=(10, 5))
                    ax1.imshow(registro_rigido_final[:, :, 25])
                    ax1.set_title('Registro')
                    st.pyplot(fig)

                    # Botón para descargar el archivo NIfTI
                    output_path = os.path.join("temp", Nombre_archivo+".nii.gz")
                    image_segmented = nib.Nifti1Image(registro_rigido_final, affine=np.eye(4))
                    nib.save(image_segmented, output_path)
                    if st.button('Descargar imagen registrada'):
                        st.download_button(label='Descargar', data=output_path, file_name='registration.nii.gz', mime='application/octet-stream')
                else:
                    st.warning("Los archivos de imagen no existen en las rutas especificadas.")
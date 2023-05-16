import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def histogram_matching(data_orig, data_target):


    # Redimensionar los datos en un solo arreglo 1D
    flat_orig = data_orig.flatten()
    flat_target = data_target.flatten()

    # Calcular los histogramas acumulativos
    hist_orig, bins = np.histogram(flat_orig, bins=256, range=(0, 255), density=True)
    hist_orig_cumulative = hist_orig.cumsum()
    hist_target, _ = np.histogram(flat_target, bins=256, range=(0, 255), density=True)
    hist_target_cumulative = hist_target.cumsum()

    # Ajustar los valores extremos
    min_value = min(flat_orig.min(), flat_target.min())
    max_value = max(flat_orig.max(), flat_target.max())

    # Mapear los valores de la imagen de origen a los valores de la imagen objetivo
    lut = np.interp(hist_orig_cumulative, hist_target_cumulative, bins[:-1])

    # Aplicar el mapeo a los datos de la imagen de origen
    data_matched = np.interp(data_orig, bins[:-1], lut)

    # Ajustar los valores extremos nuevamente
    data_matched = np.clip(data_matched, min_value, max_value)

    return data_matched
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def mean_filter_image(image_data):
    filtered_image = np.zeros_like(image_data)
    for x in range (0, image_data.shape[0]-2):
        for y in range(0, image_data.shape[1]-2):
            for z in range(0, image_data.shape[2]-2):
                # voxel_int = image_data[x,y,z]

                avg = 0

                for dx in range(-1,1) :
                    for dy in range(-1,1) :
                        for dz in range(-1,1) :
                            avg = avg + image_data[x+dx, y+dy, z+dz]

                filtered_image[x,y,z] = avg / 3 ** 3
    return  filtered_image
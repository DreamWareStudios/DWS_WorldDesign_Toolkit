############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script pre-process the necessary dataset for AI predictions related to the land cover masks
A new AI-ready image will be generated using:
    - 20cm resolution orthograhpy image (RVB)
    - 20cm resolution near-infrared imgage (grayscale)
    - 1m resolution surface numerical model (grayscale)
"""

# Import necessary modules
import os
import numpy as np
from osgeo import gdal

# Set the directory paths for each folder
ortho_folder = r'F:\QGIS\Data\Source Files\20cm Orthography\Tiles'
infrared_folder = r'F:\QGIS\Data\Source Files\20cm Infrared\Tiles'
height_folder = r'F:\QGIS\Data\Source Files\20cm Height\Tiles'
output_folder = r'F:\QGIS\Data\Source Files\AI_IMG'

# Get a list of all the tiled images in the ortho folder
ortho_images = [f for f in os.listdir(ortho_folder) if f.endswith('.tif')]

# Loop through each image and extract the ortho bands
for i, image in enumerate(ortho_images):
    if i == 10:  # Stop after processing the first 10 images
        break

    # Get the row and column indices from the image name
    image_parts = os.path.splitext(image)[0].split('_')
    row = int(image_parts[1])
    col = int(image_parts[2])
    
    # Load the ortho image
    ortho_path = os.path.join(ortho_folder, image)
    ortho_ds = gdal.Open(ortho_path)
    
    # Extract the RGB bands
    blue = ortho_ds.GetRasterBand(1).ReadAsArray()
    green = ortho_ds.GetRasterBand(2).ReadAsArray()
    red = ortho_ds.GetRasterBand(3).ReadAsArray()
    
    # Load the infrared image
    infrared_path = os.path.join(infrared_folder, f'infra_{row}_{col}.tif')
    infrared_ds = gdal.Open(infrared_path)
    
    # Extract the infrared band
    nir = infrared_ds.GetRasterBand(1).ReadAsArray()
    
    # Load the height image
    height_path = os.path.join(height_folder, f'mns_{row}_{col}.tif')
    height_ds = gdal.Open(height_path)
    
    # Extract the height band and multiply by 5
    height = height_ds.GetRasterBand(1).ReadAsArray() * 5
    
    # Create the output image with 5 channels
    driver = gdal.GetDriverByName('GTiff')
    output_path = os.path.join(output_folder, f'output_{row}_{col}.tif')
    output_ds = driver.Create(output_path, blue.shape[1], blue.shape[0], 5, gdal.GDT_Byte)
    
    # Write the bands to the output image
    output_ds.GetRasterBand(1).WriteArray(blue)
    output_ds.GetRasterBand(2).WriteArray(green)
    output_ds.GetRasterBand(3).WriteArray(red)
    output_ds.GetRasterBand(4).WriteArray(nir)
    output_ds.GetRasterBand(5).WriteArray(height)
    
    # Set the output image metadata
    output_ds.SetGeoTransform(ortho_ds.GetGeoTransform())
    output_ds.SetProjection(ortho_ds.GetProjection())
    
    # Close the output image
    output_ds = None
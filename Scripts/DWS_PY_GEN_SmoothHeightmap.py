import numpy as np
from scipy import ndimage
from PIL import Image
Image.MAX_IMAGE_PIXELS = None



# Load the heightmap
heightmap = Image.open('F:\\QGIS\\Data\\Source Files\\Cartographie 2022\\a_0_0.tif')
heightmap_array = np.array(heightmap)

# Apply the median filter
ksize = 15  # Adjust the kernel size as needed
smoothed_heightmap_array = ndimage.median_filter(heightmap_array, size=ksize)

# Convert back to an image and save
smoothed_heightmap = Image.fromarray(smoothed_heightmap_array)
smoothed_heightmap.save('F:\\QGIS\\Data\\Source Files\\Cartographie 2022\\smooth.tif')
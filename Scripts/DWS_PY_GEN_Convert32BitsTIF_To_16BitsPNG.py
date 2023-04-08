############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script simply convert 32 bits TIF (.tif or .tiffs) files into 16 bits PNG (Unreal Engine 5 heightmap format)
"""

# Import necessary modules
from PIL import Image
import os

# Increase the maximum image size
Image.MAX_IMAGE_PIXELS = None

# Set the input and output directories
input_dir = 'F:\\QGIS\\Data\\Source Files\\100cm MNT\\'
output_dir = 'F:\\QGIS\\Data\\Source Files\\100cm MNT\\'

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    
    print(f'Processing {filepath}')
    
    # Check if the file is a 32-bit grayscale TIFF image
    if filename.endswith('.tiff') or filename.endswith('.tif'):
        
        print(f'Fetched: {filepath} as a 32-bit TIF image')
        
        # Oen the TIFF image, convert to PNG, and save to output directory
        with Image.open(filepath) as img:
            img.save(os.path.join(output_dir, os.path.splitext(filename)[0] + '.png'))
            
        print(f'Converted {filename} to 16-bit PNG')

print('Conversion complete!')
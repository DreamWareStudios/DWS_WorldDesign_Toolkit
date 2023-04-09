############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script is used to rotate PNG images by 180 degrees and save the rotated images with a new file name in the same directory where the original images are located.

This is usefull for heightmap processing before importing them in Unreal Engine, as we need to flip the Y tiles in TerreSculptor before export, this mean that the tiles are effectively reversed, this script compensate for that.

Only rotated tiles should be imported into Unreal Engine using World Partition system if possible.
"""

# Import necessary modules
from PIL import Image
import os
Image.MAX_IMAGE_PIXELS = None

# Directory containing PNG images
dir_path = 'F:\\QGIS\\Data\\Source Files\\100cm MNT\\Tiles\\'

# Loop through all files in directory
for file_name in os.listdir(dir_path):
    if file_name.endswith('.png'):
        # Open the image
        img = Image.open(os.path.join(dir_path, file_name))

        # Rotate the image 90 degrees
        img = img.transpose(Image.ROTATE_90)

        # Save the rotated image
        new_file_name = os.path.splitext(file_name)[0] + '_rotated.png'
        img.save(os.path.join(dir_path, new_file_name))
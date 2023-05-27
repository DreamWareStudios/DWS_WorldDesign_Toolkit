############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script takes a given folder as input, fetches all .asc files within it and merge the files into a single GeoTIF (.tif) file
This is script might be used when working with 32-bit ASC files (ex: MNT/MNS/MNH from IGN) to avoid the possible
quality loss of tools like QGIS when importing & exporting theses files, it's also make it more streamlined, faster and easier
"""

import os
from osgeo import gdal
from tqdm import tqdm

# Directory path where ASC files are located
asc_dir = r'C:\Users\sebas\Downloads\RGEALTI_2-0_1M_ASC_LAMB93-IGN69_D035_2022-12-16\RGEALTI\1_DONNEES_LIVRAISON_2023-01-00125\RGEALTI_MNT_1M_ASC_LAMB93_IGN69_D035_20230113'

# Output GeoTIFF file path
output_tiff = r'C:\Users\sebas\Downloads\output.tif'

# Get a list of ASC files in the directory
asc_files = [filename for filename in os.listdir(asc_dir) if filename.endswith('.asc')]

# Open the first ASC file to get the required information
first_asc = os.path.join(asc_dir, asc_files[0])
dataset = gdal.Open(first_asc, gdal.GA_ReadOnly)

# Get the projection information from the first ASC file
projection = dataset.GetProjection()

# Get the resolution from the first ASC file
geotransform = dataset.GetGeoTransform()
pixel_width = geotransform[1]
pixel_height = -geotransform[5]

# Calculate the size of the output GeoTIFF based on the tiles
min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
for asc_file in asc_files:
    asc_path = os.path.join(asc_dir, asc_file)
    asc_dataset = gdal.Open(asc_path, gdal.GA_ReadOnly)
    tile_geotransform = asc_dataset.GetGeoTransform()
    tile_min_x = tile_geotransform[0]
    tile_max_y = tile_geotransform[3]
    tile_max_x = tile_min_x + (asc_dataset.RasterXSize * tile_geotransform[1])
    tile_min_y = tile_max_y + (asc_dataset.RasterYSize * tile_geotransform[5])
    min_x = min(min_x, tile_min_x)
    max_x = max(max_x, tile_max_x)
    min_y = min(min_y, tile_min_y)
    max_y = max(max_y, tile_max_y)
    asc_dataset = None

# Calculate the size and number of pixels for the output GeoTIFF
output_cols = int((max_x - min_x) / pixel_width)
output_rows = int((max_y - min_y) / abs(pixel_height))

# Create an empty GeoTIFF file with the specified options
driver = gdal.GetDriverByName('GTiff')
output_dataset = driver.Create(output_tiff, output_cols, output_rows, 1, gdal.GDT_Float32,
                               options=['COMPRESS=NONE', 'BIGTIFF=YES'])
output_dataset.SetGeoTransform((min_x, pixel_width, 0, max_y, 0, pixel_height))
output_dataset.SetProjection(projection)

# Loop through each ASC file and write its data to the corresponding location in the GeoTIFF
with tqdm(total=len(asc_files), desc="Processing") as pbar:
    for asc_file in asc_files:
        asc_path = os.path.join(asc_dir, asc_file)
        asc_dataset = gdal.Open(asc_path, gdal.GA_ReadOnly)
        tile_data = asc_dataset.GetRasterBand(1).ReadAsArray()
        tile_geotransform = asc_dataset.GetGeoTransform()
        tile_min_x = tile_geotransform[0]
        tile_max_y = tile_geotransform[3]
        tile_offset_x = int((tile_min_x - min_x) / pixel_width)
        tile_offset_y = int((max_y - tile_max_y) / abs(pixel_height))
        output_dataset.GetRasterBand(1).WriteArray(tile_data, tile_offset_x, tile_offset_y)
        asc_dataset = None
        pbar.update(1)

# Set the color interpretation to greyscale
output_dataset.GetRasterBand(1).SetColorInterpretation(gdal.GCI_GrayIndex)

# Save and close the output GeoTIFF file
output_dataset.FlushCache()
output_dataset = None

print("Conversion completed successfully.")
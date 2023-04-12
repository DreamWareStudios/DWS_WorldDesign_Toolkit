############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script extracts extents from a given GeoTIF file
This is usefull for DTM/DSM data as exporting them from QGIS generate a "terraced" effect (32bit float not supported)
Just specify the extent and the files variables and you are good to go, extents are:
    - West
    - South
    - East
    - North

You can also change the CRS if needed
"""

# Import necessary modules
import rasterio
from rasterio.windows import from_bounds

# Define the input file path
input_file = r'F:\QGIS\Data\IGN Processed Data\MNT\MNT_Orne_Merged.tif'

# Define the output file path
output_file = r'F:\QGIS\Data\IGN Processed Data\MNT\MNT_Orne_Merged_trimmed.tif'

# Define the CRS extent
xmin, ymin, xmax, ymax = 482923, 6855753, 497204, 6870034
crs_extent = (xmin, ymin, xmax, ymax)

# Define the CRS
crs = 'EPSG:2151'

# Open the input file
with rasterio.open(input_file) as src:

    # Get the window corresponding to the CRS extent
    window = from_bounds(*crs_extent, transform=src.transform)

    # Read the data within the window
    data = src.read(1, window=window)

    # Get the metadata of the output file
    metadata = src.meta.copy()
    metadata.update({
        'height': window.height,
        'width': window.width,
        'transform': rasterio.windows.transform(window, src.transform),
        'crs': crs
    })

    # Write the output file
    with rasterio.open(output_file, 'w', **metadata) as dst:
        dst.write(data, 1)
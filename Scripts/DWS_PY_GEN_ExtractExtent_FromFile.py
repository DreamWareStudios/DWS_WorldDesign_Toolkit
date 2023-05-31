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
from rasterio.crs import CRS

# Define the input file path
input_file = r'C:\Users\sebas\Downloads\D061_Orne.tif'

# Define the output file path
output_file = r'C:\Users\sebas\Downloads\orne_small.tif'

# Define the CRS extent (West, South, East, North)
xmin, ymin, xmax, ymax = 488779.0290, 6859900.1558, 490795.5290, 6861916.6558
crs_extent = (xmin, ymin, xmax, ymax)

# EPSG code for CRS 2154 (RGF93 / Lambert-93)
crs_code = 'EPSG:2154'

try:
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
            'crs': crs_code
        })

        # Write the output file
        with rasterio.open(output_file, 'w', **metadata) as dst:
            dst.write(data, 1)

        print("Script executed successfully!")

except Exception as e:
    print("An error occurred:")
    print(str(e))
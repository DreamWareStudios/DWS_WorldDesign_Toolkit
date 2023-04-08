############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################

"""
This script is used to export a map as a series of tiles from a QGIS project.
The tiles are created by dividing the original map into smaller tiles based on a given number of tiles, and then rendering each tile using QGIS. 

A virtual layer need to be created to create the area of selection before exporting!
"""

# Note: This script is designed to run in QGIS only!
# Import necessary modules
import os
import math
from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob

# Define function to calculate the size of the exported image
def exported_image_size(area, dpi, scale):
    # Calculate the side length of the map in meters based on the given area
    side_length_meters = math.sqrt(area)
    # Calculate the side length of the map in map units based on the given scale
    side_length_map_units = side_length_meters / scale
    # Calculate the side length of the map in inches based on the given DPI
    side_length_inches = side_length_map_units * (1 / dpi)
    # Calculate the side length of the map in pixels
    side_length_pixels = side_length_inches * dpi
    # Return the side length of the map in pixels as an integer
    return int(side_length_pixels)

# Set output directory
output_dir = 'F:\\QGIS\\Data\\Source Files\\Cartographie 2022'

# Set output format (TIFF or JPG)
is_tiff = 1

# Set original map size, scale, and DPI
original_map_size = 55081
original_scale = 1/234.695
original_dpi = 96

# Calculate the size of the exported map based on the original map size, scale, and DPI
computed_map_size = exported_image_size(original_map_size, original_dpi, original_scale)

# Set the number of tiles to create
num_tiles = 5

# Calculate the size of each tile
tile_size = computed_map_size / num_tiles

# Print some information about the exported map and tiles
print("Total size: " + str(computed_map_size) + " px")
print("Tile size: " + str(tile_size) + "px for " + str(num_tiles * num_tiles) + " tiles" )

# Get the QGIS project instance
project = QgsProject.instance()

# Get the layer tree root and find all visible layers
layer_tree_root = project.layerTreeRoot()
visible_layers = [node.layer() for node in layer_tree_root.findLayers() if node.isVisible()]

# Find a vector layer to use as a buffer layer for the map extent
buffer_layer = None
for layer in project.mapLayers().values():
    if isinstance(layer, QgsVectorLayer) and layer.featureCount() > 0:
        buffer_layer = layer
        break

# Raise an error if a buffer layer is not found
if not buffer_layer:
    raise ValueError("Buffer layer not found.")

# Set the extent of the map to be exported based on the buffer layer extent and the number of tiles
extent = buffer_layer.extent()

# Set the map settings
map_settings = QgsMapSettings()
map_settings.setDestinationCrs(buffer_layer.crs())
map_settings.setLayers(visible_layers)
map_settings.setOutputSize(QSize(tile_size, tile_size))

# Calculate the x and y steps for each tile
x_step = (extent.xMaximum() - extent.xMinimum()) / num_tiles
y_step = (extent.yMaximum() - extent.yMinimum()) / num_tiles

# Loop through each tile and render it
for i in range(num_tiles):
    for j in range(num_tiles):
        # Create a QgsRectangle object based on the extent of the tile
        tile_extent = QgsRectangle(
            extent.xMinimum() + i * x_step,
            extent.yMinimum() + j * y_step,
            extent.xMinimum() + (i + 1) * x_step,
            extent.yMinimum() + (j + 1) * y_step
        )

        # Print the extent of the current tile
        print(f'Tile ({i}, {j}) extent: {tile_extent.toString()}')
        
        # Set the map extent to be rendered to the extent of the current tile and the output's DIP
        map_settings.setExtent(tile_extent)
        map_settings.setOutputDpi(original_dpi)
        
        # Create a QgsMapRendererParallelJob object with the map settings and start the render job
        render_job = QgsMapRendererParallelJob(map_settings)
        render_job.start()
        render_job.waitForFinished()
        
        # Print any errors that occurred during rendering and break out of the loop if there were any errors
        if render_job.errors():
            print(f"Errors in rendering job for tile ({i}, {j}): {render_job.errors()}")
            break

        # Save the rendered tile to a file in the output directory
        output_path = os.path.join(output_dir, f'ortho_{i}_{j}' + is_tiff ? 'tiff' : 'jpg')
        if is_tiff == 1:
            img = render_job.renderedImage().convertToFormat(QImage.Format_ARGB32)
            img.save(output_path, "TIFF", QImage.Format_ARGB32)
        else:
            img = render_job.renderedImage()
            img.save(output_path)

        # Print the path of the saved file
        print(f'Saved file: {output_path}')
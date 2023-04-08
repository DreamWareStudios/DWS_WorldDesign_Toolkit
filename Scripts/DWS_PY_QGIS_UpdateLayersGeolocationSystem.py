############################
#   Dreamware Studios SAS  #
# ------------------------ #
#   World Design Toolkit   #
#     Sébastien DESCY      #
############################


"""
This script is used inside a QGIS project to update all the project's layers into a given coordinate system (CRS), by default the Lambert-93 (EPSG:2154) CRS is used
"""

# Note: This script is designed to run in QGIS only!
# Import necessary modules
from qgis.core import *
from qgis.gui import *

# Set the destination CRS to Lambert-93 (EPSG:2154) (IGN standard specification)
crs_dest = QgsCoordinateReferenceSystem('EPSG:2154')

# Get all layers in the current project
layers = QgsProject.instance().mapLayers().values()

# Loop through all layers and set their CRS to the destination CRS
for layer in layers:
    layer.setCrs(crs_dest)

# Refresh the map canvas to update the layer display
iface.mapCanvas().refreshAllLayers()

# Let the user know that the layer geolocation specifications were correctly updated
print("Geolocation successfully updated for all " + str(len(layers)) + " layers")
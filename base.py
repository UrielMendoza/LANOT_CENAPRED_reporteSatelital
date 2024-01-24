# General definitions and configuration
# Set the Copernicus access credentials here

# ------------------------------------------------------------------------------

# Copernicus API access credentials
# Insert your api credencials
Copernicus_username = "lanot_2020"
Copernicus_password = "lanot_2020"
# From DataSpace
Dataspace_username = 'lanot@geografia.unam.mx'
Dataspace_password = 'Lanot_sargazo_#2023'

# ------------------------------------------------------------------------------

# Some tiles of interest in UTM/MGRS format

# SENTINEL-2A and SENTINEL-2B occupy the same orbit, but separated by 180 degrees. The mean orbital altitude is 786 km. The orbit inclination is 98.62 and the Mean Local Solar Time (MLST) at the descending node is 10:30.

tiles = {}

# Volcanes CENAPRED
tiles["volcanes"] = ["14QNG","13QFB","15QVV","15PWS"]

# ------------------------------------------------------------------------------

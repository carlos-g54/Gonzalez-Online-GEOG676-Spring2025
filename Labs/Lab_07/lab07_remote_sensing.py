import arcpy

# band assignment
# spatial analysis ".sa" is used
# https://pro.arcgis.com/en/pro-app/latest/arcpy/spatial-analyst/what-is-the-spatial-analyst-module.htm
source = r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_07\Data\USGS_Imagery"
band1 = arcpy.sa.Raster(r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_07\Data\USGS_Imagery\band1.TIF") #blue
band2 = arcpy.sa.Raster(r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_07\Data\USGS_Imagery\band2.TIF") #green
band3 = arcpy.sa.Raster(r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_07\Data\USGS_Imagery\band3.TIF") #red
band4 = arcpy.sa.Raster(r"C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_07\Data\USGS_Imagery\band4.TIF") #NIR
# Compositebands_management creates one raster from the composites.
combined = arcpy.CompositeBands_management([band1,band2,band3,band4], source + r"\output_combined.tif")

#Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
#ddd calls the 3d analyst module
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/3d-analyst/an-overview-of-the-3d-analyst-toolbox.htm
arcpy.ddd.HillShade(source + r"\DEM.tif", source + r"\output_Hillshade.tif", azimuth, altitude, shadows, z_factor)

#Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\DEM.tif", source + r"\output_slope.tif", output_measurement, z_factor)

print("success!!!")
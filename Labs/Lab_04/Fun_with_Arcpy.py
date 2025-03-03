import arcpy 

arcpy.env.workspace = r'C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_04\lab_4_data\Python_file'
folder_path = r'C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_04'
gdb_name = 'Test.gdb'
gdb_path = folder_path +'\\'+ gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r'C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_04\lab_4_data\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\'+ garage_layer_name

#Open & Copy building features to our geodatabase
campus = r'C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_04\lab_4_data\Campus.gdb'
buildings_campus = campus + '\Structures'
buildings = gdb_path +'\\'+ 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)


#reprojection- make sure the two layers share the same spatial reference
spatial_ref = arcpy.Describe(buildings).spatial.Reference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffering
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path +'\Garage_Points_buffered', 150)

arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TabletoTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf','C:\DevSource\Gonzalez-Online-GEOG676-Spring2025\Labs\Lab_04', 'nearbyBuildings.csv')
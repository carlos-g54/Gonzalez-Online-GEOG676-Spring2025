# -*- coding: utf-8 -*-

import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a Targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
        displayName="GDB Name",
        name="GDBName",
        datatype="GPString",
        parameterType= "Required",
        direction="Input"
        )
        param2 = arcpy.Parameter(
        displayName="Garage CSV File",
        name="GarageCSVFile",
        datatype="DEFile",
        parameterType="Required",
        direction="Input"
        )
        param3 = arcpy.Parameter(
        displayName="Garage Layer Name",
        name="GarageLayerName",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
        )
        param4 = arcpy.Parameter(
        displayName="Campus GDB",
        name="Campus GDB",
        datatype="DEType",
        parameterType="Required",
        direction="Input"
        )
        param5 = arcpy.Parameter(
        displayName="Buffer Distance",
        name="Buffer Distance",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input"
        )

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        folder_path = parameters[0].valueasText
        gdb_name = parameters[1].valueAsText
        gdb_path = folder_path +'\\'+ gdb_name
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        csv_path = parameters[2].valueAsText
        garage_layer_name = 'Garage_Points'
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\'+ garage_layer_name

#Open & Copy building features to our geodatabase
        campus = parameters[4].valueAsText
        buildings_campus = campus  +'\Structures'
        buildings = gdb_path +'\\'+ 'Buildings'

        arcpy.Copy_management(buildings_campus, buildings)


#reprojection- make sure the two layers share the same spatial reference
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffering
        buffer_distance = int(parameters[5].value)
        garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path +'\Garage_Points_buffered', buffer_distance)

        arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

        arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf',folder_path, 'nearbyBuildings.csv')



        return None
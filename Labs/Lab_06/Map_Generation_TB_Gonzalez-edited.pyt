# -*- coding: utf-8 -*-
import time
import arcpy

#https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/parameter.htm

#do not change toolbox name!!!
class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]

#Define the tool
class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        #self.label is what will be displayed in ArcGIS Pro
        self.label = "Graduatedcolor"
        self.description = "Create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        #if more than one tool are in the toolbox, category can help organize. In this case there is only one tool = 1 category
        self.category = "Maptools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        #https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm
        #original project name
        #params = None
        param0 = arcpy.Parameter(
            #shows up in arcgis as a brief description
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputname",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        #which layer you want to clasify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype= "GPLayer",
            parameterType="Required",
            direction="Input"
        )

        #output folder location. 
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input"
        )

        #output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #Define Progressor Variables
        readTime = 3 #the time for users to read the progress
        start = 0 #beginning position of the progressor "0%"
        max = 100 #end position "100%"
        step = 33 #the progress interval to move the progressor along

        #Setup Progressor
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/setprogressor.htm
        # time.sleep is a python method that pauses executio of code for a set moment of time
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) #pause the execution for 3 seconds
        #Add messaage to the Results Pane
        arcpy.AddMessage("Validating Project File...")

        #Project File ".mp" is a sub module
        # https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/introduction-to-arcpy-mp.htm
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText) #param0 is the input file. helps access input project file "param0"


        # A project can have multiple maps (see map tabs)
        # Index "0" grabs the first map and gives us access to it.
        campus = project.listMaps('Map')[0] 

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step)#now is 33% completed
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #Loop through the layers of the map from line 110. a map can have many layers
        for layer in campus.listLayers():
            # Check if the layer is a Feature Layer
            if layer.isFeatureLayer:
                # Copy the layer's symbology
                symbology = layer.symbology
                #Make sure the symbology has rederer attribute
                # https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/symbology-class.htm
                if hasattr(symbology, 'renderer'):
                    # Check Layer Name
                    if layer.name == parameters[1].valueAsText: # check if the layer name match the input layer

                        # Increment Progressor
                        arcpy.SetProgressorPosition(start + step*2) #now 66% completed
                        arcpy.SetProgressorLabel("Calculating & classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating & classifying")

                        #Update the Copy's Renderer to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #Tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField = "Shape_Area"

                        #Set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5

                        #Set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        # Set the Layer's Actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("No Feature layers found")
        
        # Increment Progressor
        arcpy.SetProgressorPosition(start + step*3) #now 99% is complete
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        # https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/arcgisproject-class.htm
        # saveACopy is a method used to write to a new file path or name
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText+ ".aprx")
        #Param 2 is the folder location and param 3 is the name of the new project

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

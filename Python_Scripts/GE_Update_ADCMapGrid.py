##
##Brian Kingery
##5/6/2015
##
##Script designed to export all ADCMapGrid via the the service grid and then to be converted
##to KMZs. All of those KMZs are intended to be referenced and added to Google Earth.
##
##

import arcpy, os, time
from arcpy import env

print "Script Initiated...  ", time.ctime()
start_project = time.clock()

env.overwriteOutput = True

# Set workspace
env.workspace = "C:/Users/bkingery/Desktop/GE/DataPrep.gdb"

##################################################################################
##################################################################################

#Step 1
print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nStep 1 starting..."
print "This step spatially joins the weekly updated ADCMapGrid layer to the service area\ngrid that was manually prepared.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step1 = time.clock()

target_features = "C:/GIS/OperationalSystems/Locations/Waterworks BaseMap/Data/Databases/sdeVectorInfrequent.mdb/Reference/ADCVirginiaPeninsulaGridArea"
join_features = "WW_ServiceArea_40x40"
out_feature_class = "Spatial_Joins/SpatialJoin_ADCMapGrid_to_ServiceArea" 
#could be "CONTAINS"
arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class, "", "", "", "HAVE_THEIR_CENTER_IN")
print "Spatial join of ADCMapGrid with Service Area PageNumber IDs complete."
print time.ctime()

end_step1 = time.clock()

print "\nStep 1 Complete"
seconds = int(end_step1 - start_step1)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))


##################################################################################
##################################################################################

#Step 2
print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nStep 2 starting..."
print "This step selects by analysis by PageNumber and creates a new file that will\nbe used as the final ADCMapGrid layer for each individual page number.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step2 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    # Set local variables
    in_features = "Spatial_Joins/SpatialJoin_ADCMapGrid_to_ServiceArea"
    out_ADCMapGrid = "ADCMapGrid_Grids/ADCMapGrid_Grid_" + str(x)
    where_clause = '"PageNumber" = ' + str(x)
    # Select_analysis
    arcpy.Select_analysis(in_features, out_ADCMapGrid, where_clause)
    print "ADCMapGrid Section Selected:      ", str(x), "  ", time.ctime()
    x+=1
    if x%50 == 0:
        print "Sleeping for 5 seconds to let the cpu/ram calm"
        time.sleep(5)
del x    

end_step2 = time.clock()

print "\nStep 2 Complete"
seconds = int(end_step2 - start_step2)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))

##################################################################################
##################################################################################

#Step 3
print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nStep 3 starting..."
print "This step cycles through the files created above that contain ADCMapGrid\nwhile deleting all empty feature classes.\nA layer is made from the populated feature classes.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step3 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    original_ADCMapGrid = "ADCMapGrid_Grids/ADCMapGrid_Grid_" + str(x)
    ADCMapGrid_count = arcpy.GetCount_management(original_ADCMapGrid)
    count = int(ADCMapGrid_count.getOutput(0))
    if count == 0:
        # Deletes the empty feature class
        arcpy.Delete_management(original_ADCMapGrid)
        print "Empty feature class deleted:           ", "ADCMapGrid_" + str(x)
        
    else:
        # Execute Create a Layer from the copied feature class
        ADCMapGrid_fc = original_ADCMapGrid
        ADCMapGrid_lyr = "ADCMapGrid_Grid_Layer_" + str(x)
        arcpy.MakeFeatureLayer_management(ADCMapGrid_fc, ADCMapGrid_lyr)
        print "Feature class converted to layer:      ", ADCMapGrid_lyr
    x+=1
    if x%50 == 0:
        print "Sleeping for 5 seconds to let the cpu/ram calm"
        time.sleep(5)
del x

end_step3 = time.clock()

print "\nStep 3 Complete"
seconds = int(end_step3 - start_step3)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))

##################################################################################
##################################################################################

#Step 4
print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nStep 4 starting..."
print "This step adds all of the layers to the group layer ('ADCMapGrid_GroupLayer')\nof the selected mxd ('GE_GridIndex_ADCMapGrid.mxd').\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step4 = time.clock()

mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_ADCMapGrid.mxd")

df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
targetGroupLayer = arcpy.mapping.ListLayers(mxd, "ADCMapGrid_GroupLayer", df)[0]

# Remove all layers from the group layer "ADCMapGrid_GroupLayer"

for df in arcpy.mapping.ListDataFrames(mxd):
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "ADCMapGrid_GroupLayer", df)[0]
    for lyr in targetGroupLayer:
        arcpy.mapping.RemoveLayer(df, lyr)
print "All layers removed from ADCMapGrid group layer, 'ADCMapGrid_GroupLayer'."

print "\n          -----------------------------------------\n"
print "Adding layers to the group layer 'ADCMapGrid_GroupLayer'\n"

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    layer_ADCMapGrid = "ADCMapGrid_Grid_Layer_" + str(x)
    if arcpy.Exists(layer_ADCMapGrid):
        addLayer = arcpy.mapping.Layer(layer_ADCMapGrid)
        arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, addLayer, "BOTTOM")
        print "Layer added to 'ADCMapGrid_GroupLayer'     ", layer_ADCMapGrid
    else:
        pass
    x+=1

print "\n          -----------------------------------------\n"
print "Updating the symbology of all ADCMapGrid layers.\n"

for dataframe in arcpy.mapping.ListDataFrames(mxd):
    ADCMapGrid_grouplayer = arcpy.mapping.ListLayers(mxd, "ADCMapGrid_GroupLayer", dataframe)[0]
    for layer in ADCMapGrid_grouplayer:
        sourceLayer = arcpy.mapping.ListLayers(mxd, "ADCMapGrid", dataframe)[0]
        updateLayer = arcpy.mapping.ListLayers(mxd, "ADCMapGrid_GroupLayer", dataframe)[0]
        arcpy.mapping.UpdateLayer(dataframe, layer, sourceLayer, True)

print "\nAll layer symbology has been updated.", "  ", time.ctime()


mxd.save()
print "\nMXD saved!  ", time.ctime(),"  --- GE_GridIndex_ADCMapGrid.mxd ---"

del x, mxd, env.workspace, addLayer, sourceLayer

end_step4 = time.clock()

print "\nStep 4 Complete"
seconds = int(end_step4 - start_step4)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))

##################################################################################
##################################################################################

time.sleep(5) # Let the cpu/ram calm before proceeding!

#Step 5
print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nStep 5 starting..."
print "This step goes through the 'GE_GridIndex_ADCMapGrid.mxd' and converts all of\nthe ADCMapGrid layers to KMLs.\n"
#
start_step5 = time.clock()

# Set workspace
env.workspace = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth"

# Local Variables
mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_ADCMapGrid.mxd")
lyrlist = arcpy.mapping.ListLayers(mxd)
main_outfolder = "GoogleEarthData/ADCMapGrid_Section_KMZs/"

for lyr in lyrlist:
    if lyr.isFeatureLayer:
        outfile = main_outfolder + lyr.name + (".kmz")
        arcpy.LayerToKML_conversion(lyr, outfile)
        print "Successful conversion of ", lyr.name, "  ", time.ctime()

# Delete the empty ADCMapGrid KMZ that was used to set the symbology
ADCMapGridKML = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/ADCMapGrid_Section_KMZs/ADCMapGrid.kmz"
os.remove(ADCMapGridKML)
grid = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/ADCMapGrid_Section_KMZs/WW_ServiceArea_40x40.kmz"
os.remove(grid)

print "\nAll ADCMapGrid sections converted to KMZs and unwanted files deleted.\n"

del env.workspace, mxd, lyrlist, main_outfolder

end_step5 = time.clock()

print "\nStep 5 Complete"
seconds = int(end_step5 - start_step5)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))

##################################################################################
##################################################################################

print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "\nScript Complete!  ", time.ctime(), "\n"

end_project = time.clock()

seconds = int(end_project - start_project)
Minutes = seconds / 60
Hours = Minutes / 60
Days = Hours / 24
if int(Days) == 0:
    if int(Hours) == 0:
        if int(Minutes) == 0:
            print "Runtime: %ssec" % (int(seconds - (Minutes*60)))
        else:
            print "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
    else:
        print "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
else:
    print "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))


##################################################################################
##################################################################################
##################################################################################
##################################################################################





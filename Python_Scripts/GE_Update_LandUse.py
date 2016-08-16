##
##Brian Kingery
##4/27/2015
##
##Script designed to export all LandUse via the the service grid and then to be converted
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
print "This step spatially joins the weekly updated LandUse layer to the service area\ngrid that was manually prepared.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step1 = time.clock()

target_features = "C:/GIS/OperationalSystems/Locations/Waterworks BaseMap/Data/Databases/sdeVectorInfrequent.mdb/SurfaceOverlay/CulturalArea"
join_features = "WW_ServiceArea_40x40"
out_feature_class = "Spatial_Joins/SpatialJoin_LandUse_to_ServiceArea" 
#could be "CONTAINS"
arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class, "", "", "", "HAVE_THEIR_CENTER_IN")
print "Spatial join of LandUse with Service Area PageNumber IDs complete."
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
print "This step selects by analysis by PageNumber and creates a new file that will\nbe used as the final LandUse layer for each individual page number.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step2 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    # Set local variables
    in_features = "Spatial_Joins/SpatialJoin_LandUse_to_ServiceArea"
    out_LandUse = "LandUse_Grids/LandUse_Grid_" + str(x)
    where_clause = '"PageNumber" = ' + str(x)
    # Select_analysis
    arcpy.Select_analysis(in_features, out_LandUse, where_clause)
    print "Land Use Section Selected:      ", str(x), "  ", time.ctime()
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
print "This step cycles through the files created above that contain LandUse\nwhile deleting all empty feature classes.\nA layer is made from the populated feature classes.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step3 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    original_LandUse = "LandUse_Grids/LandUse_Grid_" + str(x)
    LandUse_count = arcpy.GetCount_management(original_LandUse)
    count = int(LandUse_count.getOutput(0))
    if count == 0:
        # Deletes the empty feature class
        arcpy.Delete_management(original_LandUse)
        print "Empty feature class deleted:           ", "LandUse_" + str(x)
        
    else:
        # Execute Create a Layer from the copied feature class
        LandUse_fc = original_LandUse
        LandUse_lyr = "LandUse_Grid_Layer_" + str(x)
        arcpy.MakeFeatureLayer_management(LandUse_fc, LandUse_lyr)
        print "Feature class converted to layer:      ", LandUse_lyr
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
print "This step adds all of the layers to the group layer ('LandUse_GroupLayer')\nof the selected mxd ('GE_GridIndex_LandUse.mxd').\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step4 = time.clock()

mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_LandUse.mxd")

df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
targetGroupLayer = arcpy.mapping.ListLayers(mxd, "LandUse_GroupLayer", df)[0]

# Remove all layers from the group layer "LandUse_GroupLayer"

for df in arcpy.mapping.ListDataFrames(mxd):
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "LandUse_GroupLayer", df)[0]
    for lyr in targetGroupLayer:
        arcpy.mapping.RemoveLayer(df, lyr)
print "All layers removed from LandUse group layer, 'LandUse_GroupLayer'."

print "\n          -----------------------------------------\n"
print "Adding layers to the group layer 'LandUse_GroupLayer'\n"

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    layer_LandUse = "LandUse_Grid_Layer_" + str(x)
    if arcpy.Exists(layer_LandUse):
        addLayer = arcpy.mapping.Layer(layer_LandUse)
        arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, addLayer, "BOTTOM")
        print "Layer added to 'LandUse_GroupLayer'     ", layer_LandUse
    else:
        pass
    if x%50 == 0:
        print "Sleeping for 5 seconds to let the cpu/ram calm"
        time.sleep(5)
    x+=1

print "\n          -----------------------------------------\n"
print "Updating the symbology of all LandUse layers.\n"

for dataframe in arcpy.mapping.ListDataFrames(mxd):
    LandUse_grouplayer = arcpy.mapping.ListLayers(mxd, "LandUse_GroupLayer", dataframe)[0]
    for layer in LandUse_grouplayer:
        sourceLayer = arcpy.mapping.ListLayers(mxd, "LandUse", dataframe)[0]
        updateLayer = arcpy.mapping.ListLayers(mxd, "LandUse_GroupLayer", dataframe)[0]
        arcpy.mapping.UpdateLayer(dataframe, layer, sourceLayer, True)

print "\nAll layer symbology has been updated.", "  ", time.ctime()


mxd.save()
print "\nMXD saved!  ", time.ctime(),"  --- GE_GridIndex_LandUse.mxd ---"

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
print "This step goes through the 'GE_GridIndex_LandUse.mxd' and converts all of\nthe LandUse layers to KMLs.\n"
#
start_step5 = time.clock()

# Set workspace
env.workspace = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth"

# Local Variables
mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_LandUse.mxd")
lyrlist = arcpy.mapping.ListLayers(mxd)
main_outfolder = "GoogleEarthData/LandUse_Section_KMZs/"

for lyr in lyrlist:
    if lyr.isFeatureLayer:
        outfile = main_outfolder + lyr.name + (".kmz")
        arcpy.LayerToKML_conversion(lyr, outfile)
        print "Successful conversion of ", lyr.name, "  ", time.ctime()

# Delete the empty LandUse KMZ that was used to set the symbology
LandUseKML = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/LandUse_Section_KMZs/LandUse.kmz"
os.remove(LandUseKML)
grid = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/LandUse_Section_KMZs/WW_ServiceArea_40x40.kmz"
os.remove(grid)

print "\nAll LandUse sections converted to KMZs and unwanted files deleted.\n"

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





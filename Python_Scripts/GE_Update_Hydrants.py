##
## Brian Kingery
## 4/23/2015
##
## Script designed to export all hydrants via the the service grid and then to be converted
## to KMZs. All of those KMZs are intended to be referenced and added to Google Earth.
##
## Estimated run time is:
## 
## Runtime: 14-15 hours

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
print "This step spatially joins the weekly updated hydrant layer to the service area\ngrid that was manually prepared.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step1 = time.clock()

target_features = "C:/GIS/OperationalSystems/Locations/Waterworks BaseMap/Data/Databases/sdeVectorFrequent.mdb/WaterUtility/v_Hydrant_EAM"
join_features = "WW_ServiceArea_40x40"
out_feature_class = "Spatial_Joins/SpatialJoin_Hydrants_to_ServiceArea" 

arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class)
print "Spatial join of hydrants with Service Area PageNumber IDs complete."
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
print "This step selects by analysis by PageNumber and creates a new file that will\nbe used as the final hydrant layer for each individual page number.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step2 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    # Set local variables
    in_features = "Spatial_Joins/SpatialJoin_Hydrants_to_ServiceArea"
    out_hydrants = "Hydrant_Grids/Hydrant_Grid_" + str(x)
    where_clause = '"PageNumber" = ' + str(x)
    # Select_analysis
    arcpy.Select_analysis(in_features, out_hydrants, where_clause)
    print "Hydrant Section Selected:      ", str(x), "  ", time.ctime()
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
print "This step cycles through the files created above and copies all of the files\nthat contain hydrants while skipping all empty feature classes.\nThen a layer is made from the copied feature class.\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step3 = time.clock()

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    original_hydrant = "Hydrant_Grids/Hydrant_Grid_" + str(x)
    hydrant_count = arcpy.GetCount_management(original_hydrant)
    count = int(hydrant_count.getOutput(0))
    if count == 0:
        # Deletes the empty feature class
        arcpy.Delete_management(original_hydrant)
        print "Empty feature class deleted:           ", "Hydrant_Grid_" + str(x)
        
    else:
        # Execute Create a Layer from the populated feature class
        hydrant_fc = original_hydrant
        hydrant_lyr = "Hydrant_Grid_Layer_" + str(x)
        arcpy.MakeFeatureLayer_management(hydrant_fc, hydrant_lyr)
        print "Feature class converted to layer:      ", hydrant_lyr
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
print "This step adds all of the layers to the group layer ('Hydrants_GroupLayer')\nof the selected mxd ('GE_GridIndex_Hydrants.mxd').\n"

time.sleep(5) # Let the cpu/ram calm before proceeding!
start_step4 = time.clock()

mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_Hydrants.mxd")

df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
targetGroupLayer = arcpy.mapping.ListLayers(mxd, "Hydrants_GroupLayer", df)[0]

# Remove all layers from the group layer "Hydrants_GroupLayer"

for df in arcpy.mapping.ListDataFrames(mxd):
    targetGroupLayer = arcpy.mapping.ListLayers(mxd, "Hydrants_GroupLayer", df)[0]
    for lyr in targetGroupLayer:
        arcpy.mapping.RemoveLayer(df, lyr)
print "All layers removed from hydrant group layer, 'Hydrants_GroupLayer'."

print "\n          -----------------------------------------\n"
print "Adding layers to the group layer 'hydrant_GroupLayer'\n"

x = 1
while x < 1601: #running a test on sample 576-580 before running on all 1600 ##############################################################################################################################################################
    layer_hydrants = "Hydrant_Grid_Layer_" + str(x)
    if arcpy.Exists(layer_hydrants):
        addLayer = arcpy.mapping.Layer(layer_hydrants)
        arcpy.mapping.AddLayerToGroup(df, targetGroupLayer, addLayer, "BOTTOM")
        print "Layer added to 'Hydrants_GroupLayer'     ", layer_hydrants
    else:
        print "Layer does not exist.                  ", str(x)
    x+=1
    if x%50 == 0:
        print "Sleeping for 5 seconds to let the cpu/ram calm"
        time.sleep(5)
        
print "\n          -----------------------------------------\n"
print "Updating the symbology of all hydrant layers.\n"

for dataframe in arcpy.mapping.ListDataFrames(mxd):
    hydrants_grouplayer = arcpy.mapping.ListLayers(mxd, "Hydrants_GroupLayer", dataframe)[0]
    for layer in hydrants_grouplayer:
        sourceLayer = arcpy.mapping.ListLayers(mxd, "Hydrant", dataframe)[0]
        updateLayer = arcpy.mapping.ListLayers(mxd, "Hydrants_GroupLayer", dataframe)[0]
        arcpy.mapping.UpdateLayer(dataframe, layer, sourceLayer, True)

print "\nAll layer symbology has been updated.", "  ", time.ctime()


mxd.save()
print "\nMXD saved!  ", time.ctime(),"  --- GE_GridIndex_Hydrants.mxd ---"

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
print "This step goes through the 'GE_GridIndex_Hydrants.mxd' and converts all of\nthe hydrant layers to KMLs.\n"
#
start_step5 = time.clock()

# Set workspace
env.workspace = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth"

# Local Variables
mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_GridIndex_Hydrants.mxd")
lyrlist = arcpy.mapping.ListLayers(mxd)
main_outfolder = "GoogleEarthData/Hydrant_Section_KMZs/"

for lyr in lyrlist:
    if lyr.isFeatureLayer:
        outfile = main_outfolder + lyr.name + (".kmz")
        arcpy.LayerToKML_conversion(lyr, outfile)
        print "Successful conversion of               ", lyr.name, "  ", time.ctime()

# Delete the empty Hydrant KMZ that was used to set the symbology
hydrantKML = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/Hydrant_Section_KMZs/Hydrant.kmz"
os.remove(hydrantKML)
grid = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/GoogleEarthData/Hydrant_Section_KMZs/WW_ServiceArea_40x40.kmz"
os.remove(grid)

print "\nAll hydrant sections converted to KMZs and unwanted files deleted.\n"

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





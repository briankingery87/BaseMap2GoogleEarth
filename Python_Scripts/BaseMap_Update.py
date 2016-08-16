##
##Brian Kingery
##5/14/2015
##
##Script designed to export all feature layers from the modified basemap to KMZs in a seperate
##folder. All of those KMZs are intended to be referenced and added to Google Earth.
##
##

import arcpy, os, time
from arcpy import env

print "Script Initiated...\n", time.ctime()
start_project = time.clock() # START

env.overwriteOutput = True

# Set workspace
env.workspace = "R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth"

##################################################################################
##################################################################################

print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"

time.sleep(5) # Let the cpu/ram calm before proceeding!

# Local Variables
mxd = arcpy.mapping.MapDocument("R:/Divisions/InfoTech/Private/GIS_Private/Kingery/IssueTrak_Projects/GoogleEarth/MapDocs/GE_BaseMap.mxd")
lyrlist = arcpy.mapping.ListLayers(mxd)
main_outfolder = "GoogleEarthData/"
shared_outfolder = "R:/Divisions/InfoTech/Shared/Projects/GoogleEarth/GoogleEarthData/"

for lyr in lyrlist:
    if lyr.isFeatureLayer:
        outfile = main_outfolder + lyr.name + (".kmz")
        shared_outfile = shared_outfolder + lyr.name + (".kmz")
        
        start_conversion = time.clock() # START

        arcpy.LayerToKML_conversion(lyr, outfile) # FUNCTION to updated my Private folder files
        arcpy.LayerToKML_conversion(lyr, shared_outfile) # FUNCTION to update the files in the Shared folder

        end_conversion = time.clock() # END
        
        seconds = int(end_conversion - start_conversion)
        Minutes = seconds / 60
        Hours = Minutes / 60
        Days = Hours / 24
        if int(Days) == 0:
            if int(Hours) == 0:
                if int(Minutes) == 0:
                    x = "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
                else:
                    x = "Runtime: %smin %ssec" % (int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
            else:
                x = "Runtime: %shrs %smin %ssec" % (int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))
        else:
            x = "Runtime: %s Days %shrs %smin %ssec" % (int(Days), int(Hours - (Days*24)), int(Minutes - (Hours*60)), int(seconds - (Minutes*60)))

        print x, " --> ", lyr.name
                
del env.workspace, mxd, lyrlist, main_outfolder

##################################################################################
##################################################################################

print "\n-----------------------------------------------------------------------"
print "-----------------------------------------------------------------------"
print "Script Complete!\n", time.ctime(), "\n"

end_project = time.clock() # END

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





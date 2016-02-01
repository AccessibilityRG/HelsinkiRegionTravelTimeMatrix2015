# -*- coding: iso-8859-1 -*-
import subprocess, os, time, sys


# -------------------------------
# Metodit
# -------------------------------
def Aloitus():
        aika = time.asctime()
        teksti = "Aloitus: " + aika
        print(teksti)

def Valmis():
        aika = time.asctime()
        teksti = "Valmis: " + aika
        print(teksti)

# -----------------------------------

# ---------------------------------------------------------
# File indices that will be run - CHANGE TO EACH INSTANCE!
# ---------------------------------------------------------
fileNumber = [x for x in range(1,16)]

# Permanent Filepaths
Destinations = r"/home/MY_USERNAME/TTM/OD/Car_Matrix2015_Dest_KKJ2.shp"

for fileindex in fileNumber:
    # File path to origin Shapefile
    Origins = r"/home/MY_USERNAME/TTM/OD/Subsets/%s_Car_Matrix2015_Origs_KKJ2.shp" % fileindex
    OutLines = r"/mnt/TTM_Results/CarTT_Ruuhka_%s_Car_Matrix2015.shp" % fileindex

    # Run ArcGIS specific stuff and get filepaths to OutLines, Origins and Destinations
    print("Processing file in ArcGIS: ", Origins)
    Aloitus()

    arcGIS_cmd = "/home/MY_USERNAME/arcgis/server/tools/python /home/MY_USERNAME/Codes/TTM15_run_ArcGIS.py %s %s" % (Origins, fileindex)
    processPaths=subprocess.check_output(arcGIS_cmd, shell=True)

    # Run Geopandas specific stuff
    print("Processing file in Geopandas: ", os.path.basename(OutLines))
    gpd_cmd = "python /home/MY_USERNAME/Codes/TTM15_run_Geopandas.py %s %s %s" % (OutLines, Origins, Destinations)
    final_result_path = subprocess.check_output(gpd_cmd, shell=True)
    print(final_result_path)
    Valmis()

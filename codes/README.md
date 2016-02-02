# Codes

Producing the Helsinki Region Travel CO2 Matrix 2015 included several __analysis / processing steps__ that are represented here. 

In these calculations CSC Taito and cPouta computing clusters were used to make the computing intensive work (steps 1-3). 
Documentation **how to set up the Taito and Pouta environments** and **instructions how to run the calculations** can be read from here:

   - __Taito__ - [configurations & instructions for MetropAccess-Reititin](Taito/)
   - __Pouta__ - [configurations & instructions for MetropAccess-Digiroad tool](Pouta/)
   
Steps 4-5 were done on a local computer with 16GB of RAM, using Python and PostgSQL 9.4 / PostGIS 2.1. 

## 1. Calculations by Walking

 1. Travel time / distance calculations by __Walking__ using [MetropAccess-Reititin](MetropAccess-Reititin/README.md)
     1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_kavely_allDay.json)
     2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_allday_kavely.lsf)
 
## 2. Calculations by Public Tranportation 

 2. Travel time / distance calculations by __Public Transportation__ using [MetropAccess-Reititin](MetropAccess-Reititin/README.md)
     1. __Rush hour__ (08:00-09:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_rushhour.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_rushhour_joukkoliikenne.lsf)
     1. __Midday__ (12:00-13:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_midday.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_midday_joukkoliikenne.lsf)
 
## 3. Calculations by Private Car


 3. Travel time / distance calculations by __Private Car__ using [MetropAccess-Digiroad tool](MetropAccess-Digiroad/README.md) that was slightly modified for CSC cPouta environment.
   Car calculations were done using ArcGIS for Server 10.2 and specific Python modules (i.e. [geopandas](http://geopandas.org/)). 
   Read more detailed instructions how to run the car calculations in Pouta from **[here](Pouta/README.md#pouta-calculations)**  
   
     1. __Rush hour__ (07:00-09:00 & 15:00-17:00)
         1. [ArcGIS calculation script](Pouta/Python-Codes/TTM15_run_ArcGIS_rushhour.py)
         2. [Geopandas calculation script](Pouta/Python-Codes/TTM15_run_Geopandas.py)
         3. [Control file](Pouta/Python-Codes/TTM15_runModular.py)
         
     1. __Midday__ (09:00-15:00)
         1. [ArcGIS calculation script](Pouta/Python-Codes/TTM15_run_ArcGIS_midday.py)
         2. [Geopandas calculation script](Pouta/Python-Codes/TTM15_run_Geopandas.py)
         3. [Control file](Pouta/Python-Codes/TTM15_runModular.py)
          
  
The analyses and processing phases support multiprocessing using Python [multiprocessing](https://docs.python.org/3.4/library/multiprocessing.html) module 
that makes possible to do processing in parallel utilizing multiple processors on a given machine. ==> Makes possible to do things faster. 
 
## 4. Combining Private Car and PT results + creating PostGIS matrix 

Steps 1-3 produces 5 separate datasets (1 by walking, 2 by PT and 2 by car) with common data structure, i.e. all the result files are based on the same set of origin 
location subsets (293 files) and same destination locations (a single file). 

Next, the result files are combined together and the first version of the matrix is generated into a PostGIS table. PostGIS is used because it is fast / can be used in web development, and 
it is the fastest way to produce the final text file matrix (where data is organized and distributed based on individual 'to_id' locations). 

Required steps:

  1. [Create a PostGIS table for Helsinki Region Travel Time Matrix](Python-PostGIS/Matriisi2015_PostGIS_CreateTable.py)
  2. [Parse results - combine different travel modes / times and push them into PostGIS table](Python-PostGIS/Matriisi2015_Compiler_accessibility_PostGIS.py) 
  
## 5. Create Helsinki Region Travel Time Matrix 2015 (text file version)

The final step is to create the travel time matrix 2015 fetching the data from PostGIS and saving the results into text files. 

Required steps:

  1. [Create database indices for faster look ups](Python-PostGIS/Matriisi2015_PostGIS_CreatePrimaryKey_and_Indices.py)
  2. [Create the final Helsinki Region Travel Time Matrix 2015 (text file version)](Python-PostGIS/Matrix2015_Parse_TextMatrix_from_PostGIS.py)
 


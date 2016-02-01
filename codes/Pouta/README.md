#Pouta Configurations

Here you can find the documentation regarding cPouta Linux Server configurations for ArcGIS Server. Documentation about [how to use/get started with Pouta in CSC can be found here](https://research.csc.fi/pouta-user-guide). 

**NOTICE:** In the following documentation it is assumed that you have ArcGIS installation package extracted to folder:
   - **/home/MY_USERNAME/ArcGIS/ArcGISServer/**
   
After ArcGIS installation is done, it is assumed that arcgis has been installed to folder:
   - **/home/MY_USERNAME/arcgis**
   
If you are following these instructions change the paths accordingly to your own filepaths. 
    
##Contents:

 - [Install ArcGIS 10.3.1 for Server Linux + dependencies](#arcgis-install)
     - [Dependencies](#dependencies)
     - [Configure file handle limits](#handle-limits)
     - [Install ArcGIS](#install-software)
     - [Authenticate](#authenticate)
     - [Change the IP-address in hosts](#change-IP)
     - [Start the ArcGIS Server](#start-server)
     - [Run ArcGIS!](#run-arcgis)
 - [Install Python stuff using Anaconda2 (64 bit)](#python-install)
 - [How Pouta was used to calculate private car travel times/distances?](#pouta-calculations) 

##<a name='arcgis-install'></a>Install ArcGIS Server for Linux

ArcGIS for Server 10.3.1 was installed for cPouta CentOS (6.7) Linux server. We got the installation package from CSC. 

**<a name='dependencies'></a> Install dependencies** ([more info here](http://server.arcgis.com/en/server/latest/install/linux/arcgis-for-server-system-requirements.htm):

  - fontconfig ==> sudo yum install fontconfig
  - freetype ==> sudo yum install freetype
  - gettext ==> sudo yum install gettext
  - libXfont ==> sudo yum install libXfont
  - libXtst / libXi ==> sudo yum install libXtst
  - libXrender ==> sudo yum install libXrender 
  - mesa-libGL ==> sudo yum install mesa-libGL
  - mesa-libGLU ==> sudo yum install mesa-libGLU 
  - Xvfb ==> sudo yum install Xvfb
  
**Other useful libraries:**

  - nano ==> sudo yum install nano
  
**<a name='handle-limits'></a> Configure file handle limits:**

  - sudo nano /etc/security/limits.conf:
  
     - add following lines to the end of the file:
             
             root soft nofile 65535
             root hard nofile 65535
             root soft nproc 25059
             root hard nproc 25059
   
   - log out and log in for changes to take effect and verify (values should be now 65535 and 25059) by running following lines one by one:
   
            sudo su
            ulimit -Hn -Hu
            ulimit -Sn -Su

###<a name='install-software'></a>ArcGIS installation process 

Installation process is straightforward (read the manual).
   
   - **Install the software** by running in /home/MY_USERNAME/ArcGIS/ArcGISServer/ (or in a location where you have extracted your ArcGIS 10.3.1 for Server Linux installation package):
      
            sudo ./Setup
   
   - **<a name='authenticate'></a> Authenticate the ArcGIS installation** with prvc-file (\*.prvc) by running *authorizeSoftware* tool and passing the prvc file into it:
       - run in ___/home/*MY_USERNAME*/arcgis/tools/authorizeSoftware___ (example, not real auth_key):
       
            ./authorizeSoftware -f \_Server\_123456789.prvc  
   
   - **<a name='change-IP'></a> Change the IP-address** in /etc/hosts from 127.0.0.1 to local IP address of the Pouta Instance:
   
     - You can check the local ip of the machine with following code:
     
            ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | cut -d ' ' -f1
     
     - For convenience the following script can be used to automize this modification of the /etc/hosts file
        - [2.updateHosts.sh](2.updateHosts.sh)
        
   - **<a name='start-server'></a> Start the ArcGIS server** by running:
       - run in /arcgis/server/ :
        
            startserver.sh
        
       - For convenience following script does this
           - [3.startArcGISserver.sh](3.startArcGISserver.sh)
        
        
   - **<a name='run-arcgis'></a> Start using ArcGIS**
       - After these procedures ArcGIS python shell is ready to use and you can run for example a python script called _[hello_world.py](hello_world.py)_ in ArcGIS with command:
               
               /home/MY_USERNAME/arcgis/server/tools/python /home/MY_USERNAME/MyScripts/hello_world.py
      
 
## <a name='python-install'></a>Install Python stuff using Anaconda2 

Some parts of the Travel Time/CO2 Matrix calculations were done using Geopandas module instead of arcpy since table processing/management is MUCH faster in pure Python than using ArcGIS.
Because of this Anaconda2 was installed using conda/pip to the server (64 bit), plus following Python modules:
   
   - GDAL (1.11.2)
   - pyproj (1.9.4) 
   - Shapely (1.5.13) 
   - fiona (1.5.1)
   - descartes (1.0.1)
   - geopandas (0.1.1)
  
##<a name='pouta-calculations'></a>How Pouta was used to calculate private car travel times/distances?

Running the ArcGIS calculations in [CSC cPouta](https://pouta.csc.fi/) computing cluster were done using 22 Linux CentOS instances (flavor = small) 
where each instance had 4 VCPUs and 15 360 MB of RAM. First, an image with all the necessary installations (ArcGIS & Python stuff) and data was created. 
That image was then cloned to 22 instances that were used to do the calculations. Running all calculations took approximately 1 day with those 22 instances.

Our calculations was divided on 293 individual subtasks where each task included MetropAccess-Digiroad calculations from 50 origin locations that are within a single *origin-file.shp* Shapefile
to 14 645 destination locations that are within *destinationFile.shp*.
All the private car origin and destination files that were used in calculations are [here](../../data/Car/). 
     
**Required (5) steps for doing the calculations in Pouta (repeated in every instance)**:
   
   1. [Create an output folder to separate disk (/mnt) and set the permits](1.setPermits.sh)
   2. [Update the hosts to /etc/hosts](2.updateHosts.sh)
   3. [Start ArcGIS Server](3.startArcGISserver.sh)
   4. [Update the Python code - set the job range](4.updateCode.sh) (i.e. origin file numbers that will be run)
   5. [Run ArcGIS and do the calculations](5.runArc.sh)
   
**The actual Python codes**:

   - [Control file of the calculations](Python-Codes/TTM15_runModular.py)
   - [ArcGIS related calculations](Python-Codes/TTM15_run_ArcGIS.py) ==> Change the impedance according to time (Ruuhka_aa / Keskpva_aa = Rush-hour / Midday)
   - [Geopandas related calculations](Python-Codes/TTM15_run_Geopandas.py)
   
The result Shapefiles will be located in /mnt/TTM_Results.  
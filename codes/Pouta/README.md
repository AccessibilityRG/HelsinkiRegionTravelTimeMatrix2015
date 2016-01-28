# Pouta Configurations

Documentation regarding cPouta Linux Server configurations for ArcGIS Server.
 
__Contents:__

 - [Install ArcGIS 10.3.1 for Server Linux](#arcgis-install)
 - [Install Python stuff using Anaconda2 (64 bit)](#python-install)
 - [How to run ArcGIS (arcpy) and Python (geopandas) in the same process chain?](#how-to-run)
 
## <a name='arcgis-install'></a> Install ArcGIS Server for Linux

ArcGIS for Server 10.3.1 was installed for cPouta CentOS (6.7) Linux server. We got the installation package from CSC. 

Install dependencies ([more info here](http://server.arcgis.com/en/server/latest/install/linux/arcgis-for-server-system-requirements.htm):

  - fontconfig ==> sudo yum install fontconfig
  - freetype ==> sudo yum install freetype
  - gettext ==> sudo yum install gettext
  - libXfont ==> sudo yum install libXfont
  - libXtst / libXi ==> sudo yum install libXtst
  - libXrender ==> sudo yum install libXrender 
  - mesa-libGL ==> sudo yum install mesa-libGL
  - mesa-libGLU ==> sudo yum install mesa-libGLU 
  - Xvfb ==> sudo yum install Xvfb
  
Other useful libraries:

  - nano: sudo yum install nano
  
**Configure file handle limits:**

  - sudo nano /etc/security/limits.conf:
  
     - add following lines to the end of the file:
   
         root soft nofile 65535
         root hard nofile 65535
         root soft nproc 25059
         root hard nproc 25059
   
   - log out and log in for changes to take effect and verify (values should be now 65535 and 25059) by running:
   
      - sudo su
      - ulimit -Hn -Hu
      - ulimit -Sn -Su

ArcGIS installation process is straightforward (read the manual):
   
   - Install the software by running in /home/username/ArcGIS/ArcGISServer/ (or in a location where you have extracted your ArcGIS 10.3.1 for Server Linux installation package):
      - sudo ./Setup
   
   - Authenticate the ArcGIS installation with prvc-file (\*.prvc) by running *authorizeSoftware* tool and passing the prvc file into it:
       - *tool location:* /home/*username*/arcgis/tools/authorizeSoftware
       - *command example*: ./authorizeSoftware -f \_Server\_123456789.prvc  
   
   - Change the IP-address in /etc/hosts from 127.0.0.1 to local IP address of the Pouta Instance:
   
     - You can check the local ip of the machine with following code:
     
        ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | cut -d ' ' -f1
     
     - For convenience the following script can be used to automize this modification of the /etc/hosts file
        - [2.updateHosts.sh](2.updateHosts.sh)
        
 
## <a name='python-install'></a> Install Python stuff using Anaconda2 (64 bit)

## <a name='how-to-run'></a> How to run ArcGIS (arcpy) and Python (geopandas) in the same process chain?
 
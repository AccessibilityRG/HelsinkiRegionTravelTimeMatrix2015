# Taito Configurations

Here you can find the documentation regarding configurations and installations in Taito so that it is possible to run MetropAccess-Reititin in Taito. 
Our calculation problem is of type ['embarassingly parallel'](https://en.wikipedia.org/wiki/Embarrassingly_parallel), i.e. it is possible to distribute the calculations to as many
computing cores as possible. We use [Taito Array Jobs](https://research.csc.fi/taito-array-jobs) for this purpose. 

## Contents
 - [Installing MetropAccess-Reititin + dependencies to Taito](#reititin-dep)
    - [Nodejs](#nodejs)
    - [MetropAccess-Reititin](#reititin)
    
 - [Creating an array job for Taito using Reititin](#)

##<a name='reititin-dep'></a>Installing MetropAccess-Reititin + dependencies to Taito

MetropAccess-Reititin is written in Javascript and running it locally requires node.js to be installed.  

<a name='nodejs'></a> **Install *node.js* to Taito**:

   - Create folders for mcl and nodejs to appl_taito:
   
         mkdir -p $USERAPPL/{mcl,nodejs}
         
   - Download mcl and extract it ( **might not be needed** ):
          
          cd $USERAPPL/mcl
          wget http://www.micans.org/mcl/src/mcl-latest.tar.gz
          tar xf mcl-latest.tar.gz
   
   - Download the latest version of node.js (source files), extract it to 4.1.2 (here to *4.1.2* ==> Change accordingly to what is the version you use):
          
          cd $USERAPPL/nodejs
          wget https://nodejs.org/download/release/v4.1.2/node-v4.1.2.tar.gz
          tar xf node-v4.1.2.tar.gz
                      
   - Install node.js:
   
      - Swap from Intel to GCC compiler ( *this step has to be done every time you start using MetropAccess-Reititin in Taito* ):
            
            module swap intel gcc
            
      - Configure and install nodejs (we use version 4.1.2 here --> there have been some building problems with certain nodejs versions)
      
           cd $USERAPPL/nodejs/node-v4.1.2
           ./configure --prefix=$USERAPPL/nodejs/node-v4.1.2
           make
           make install
           
   - Export node path to system path ( *this step has to be done every time you start using MetropAccess-Reititin in Taito* )
   
          export PATH=${PATH}:${USERAPPL}/nodejs/node-v4.1.2/bin
          
   - Check that node works (should open a node shell ==> exit by pressing **CNTRL + C** two times)
     
          node
       
<a name='reititin'></a> **Install MetropAccess-Reititin**:

  - Make directory for MetropAccess-Reititin:
        
          mkdir $USERAPPL/reititin
       
  - Download the Linux version of the MetropAccess-Reititin:
  
         cd $USERAPPL/reititin
         wget http://www.helsinki.fi/science/accessibility/tools/MetropAccess-Reititin/reititin-linux.tar.gz
         
  - Extract the contents
         
         tar xf reititin-linux.tar.gz
         
  - Check that reititin works in Taito (should start making a test routing) Todo: PÄIVITÄ REITITIN-LINUX PAKETTIIN ROUTE.SH TIEDOSTO OIKEAKSI!!!
  
         cd $USERAPPL/reititin/reititin/build
         ./route.sh
      

## Creating an array job for Taito using Reititin

Running MetropAccess-Reititin in parallel in Taito can be done easily using [Taito Array Jobs](https://research.csc.fi/taito-array-jobs).
Using array jobs it is possible to divide the calculations to multiple separate jobs running on a different CPU.  

Our calculations was divided on 293 individual jobs where each job included MetropAccess-Reititin route optimizations from 50 origin locations
([an example of a single origin file](../../data/PT/Subsets/1_Walk_Matrix2015_Origs_WGS84.txt)) to 14 645 destination locations ([see the destination file](../../data/PT/destPoints.txt)).
All of the public transportation origin and destination files that were used in calculations are [here](../../data/PT/)


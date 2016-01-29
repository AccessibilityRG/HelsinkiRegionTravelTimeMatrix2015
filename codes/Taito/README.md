# Taito Configurations

Here you can find the documentation regarding configurations and installations in Taito so that it is possible to run MetropAccess-Reititin in Taito. 
Our calculation problem is of type ['embarassingly parallel'](https://en.wikipedia.org/wiki/Embarrassingly_parallel), i.e. it is possible to distribute the calculations to as many
computing cores as possible. We used [Taito Array Jobs](https://research.csc.fi/taito-array-jobs) for this purpose. 

## Contents
 - Installing MetropAccess-Reititin + dependencies to Taito

## Installing MetropAccess-Reititin + dependencies to Taito

MetropAccess-Reititin is written in Javascript and running it locally requires node.js to be installed.  

Thus first thing to do is to install **mcl** and **node.js** to Taito:

   - Create folders for mcl and nodejs to appl_taito:
   
         mkdir -p $HOME/appl_taito/{mcl,nodejs}
         
   - Download mcl and extract it:
          
          cd $HOME/appl_taito/mcl
          wget http://www.micans.org/mcl/src/mcl-latest.tar.gz
          tar xf mcl-latest.tar.gz
   
   - Download node.js, extract it and rename the folder to more reasonable one (to *4.2.6*):
          
          cd $HOME/appl_taito/nodejs
          wget https://nodejs.org/dist/v4.2.6/node-v4.2.6-linux-x64.tar.xz
          tar xf node-v4.2.6-linux-x64.tar.xz
          mv node-v4.2.6-linux-x64 4.2.6
            
   - Install node.js: 
   
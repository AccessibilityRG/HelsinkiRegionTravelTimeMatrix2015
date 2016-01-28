# Taito Configurations

Here you can find the documentation regarding configurations and installations in Taito so that it is possible to run MetropAccess-Reititin in Taito. 
Our calculation problem is of type ['embarassingly parallel'](https://en.wikipedia.org/wiki/Embarrassingly_parallel), i.e. it is possible to distribute the calculations to as many
computing cores as possible. We used [Taito Array Jobs](https://research.csc.fi/taito-array-jobs) for this purpose. 

## Contents
 - Installing MetropAccess-Reititin + dependencies to Taito

## Installing MetropAccess-Reititin + dependencies to Taito

MetropAccess-Reititin is written in Javascript and running it locally requires node.js to be installed.  

Thus first thing to do is to install node.js to Taito:

   - Download node.js:
   
          sudo wget  
            
   - Install node: 
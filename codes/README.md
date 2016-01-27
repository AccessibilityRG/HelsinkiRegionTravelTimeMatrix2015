# Codes

Producing the Helsinki Region Travel CO2 Matrix 2015 included following __analysis / processing steps__:
 
 1. Travel time / distance calculations by __Walking__ using [MetropAccess-Reititin](reititin/README.md)
     1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_kavely_allDay.json)
     2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_allday_kavely.lsf)
 
 2. Travel time / distance calculations by __Public Transportation__ using [MetropAccess-Reititin](reititin/README.md)
     1. __Rush hour__ (08:00-09:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_rushhour.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_rushhour_joukkoliikenne.lsf)
     1. __Midday__ (12:00-13:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_midday.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_midday_joukkoliikenne.lsf)
 
 3. Travel time / distance calculations by __Private Car__ using [MetropAccess-Digiroad tool](reititin/README.md)
     1. __Rush hour__ (08:00-09:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_rushhour.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_rushhour_joukkoliikenne.lsf)
     1. __Midday__ (12:00-13:00)
         1. [Configuration/setup file that was used in calculations](Conf/confMassaAjo2015_pt_midday.json)
         2. [Taito array job file that was used to run MetropAccess-Reititin in parallel](Taito/reititin_massaAjo_2015_midday_joukkoliikenne.lsf)
 
 
The analyses and processing phases support multiprocessing using Python [multiprocessing](https://docs.python.org/3.4/library/multiprocessing.html) module 
that makes possible to do processing in parallel utilizing multiple processors on a given machine. ==> Makes possible to do things faster. 
 
## Structure of the code


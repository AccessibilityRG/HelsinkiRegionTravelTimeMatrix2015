# Helsinki Region Travel Time Matrix 2015
This repository demonstrates / documents how __[Helsinki Region Travel Time Matrix 2015](http://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2015/)__ is calculated. 
Dataset was produced by [Accessibility Research Group](http://www.helsinki.fi/science/accessibility), University of Helsinki.

__Contents:__

- [What is Helsinki Region Travel Time Matrix 2015?](#what-is)
- [Attributes of Helsinki Region Travel Time Matrix 2015](#attributes)
- [How calculations were done?](#calculations)
- [Licence](#license)
- [How to cite this work?](#how-to-cite)
- [Codes](#codes)
- [Contribution / Contact](#contact)

## <a name="what-is"></a>What is Helsinki Region Travel Time Matrix 2015?
 
[__Helsinki Region Travel Time Matrix 2015__](http://www.helsinki.fi/science/accessibility/data) is a dataset that contains travel time and distance information of the routes
that have been calculated from all 250 m x 250 m grid cell centroids (n = 13231) in the Capital Region of Helsinki 
([see this map](http://www.helsinki.fi/science/accessibility/tools/YKR/YKR_Identifier.html)) by walking, public transportation (PT) and private car. 
Calculations were done separately for two different time of the day using rush hour (08:00-09:00) and midday (12:00-13:00) schedules/traffic conditions. 
The grid cells are compatible with the statistical grid cells in the YKR (yhdyskuntarakenteen seurantajärjestelmä) data set produced by the Finnish Environment Institute (SYKE). 
   
Dataset is openly available for everyone for free and it can be downloaded from the [Accessibility Research Group website](http://www.helsinki.fi/science/accessibility/data) (under a Creative Commons 4.0 Licence, see [licence text](#license)).

Helsinki Region Travel Time Matrix 2015 is closely related to __[Helsinki Region Travel CO2 Matrix 2015](http://www.helsinki.fi/science/accessibility/data/)__ 
that is also produced by Accessibility Research Group. 
More information on how the Helsinki Region Travel CO2 Matrix 2015 was calculated can be found [from here](https://github.com/AccessibilityRG/HelsinkiRegionTravelCO2Matrix2015). 
 
__Scientific examples__ of the approach used here can be read from the following articles:

- Lahtinen, J., Salonen, M. & Toivonen, T. (2013). [Facility allocation strategies and the sustainability of service delivery: 
Modelling library patronage patterns and their related CO2-emissions](http://www.sciencedirect.com/science/article/pii/S014362281300163X). Applied Geography 44, 43-52.

- Salonen, M. & Toivonen, T. (2013). [Modelling travel time in urban networks: comparable measures for private car and public transport.](http://www.sciencedirect.com/science/article/pii/S096669231300121X) Journal of Transport Geography 31, 143–153.

## <a name="attributes"></a>Attributes of Helsinki Region Travel Time Matrix 2015

| Attribute | Definition |
| --------- | ---------- | 
| __from_id__   | ID number of the origin grid cell |
| __to_id__     | ID number of the destination grid cell |
| __walk_t__    | Travel time from origin to destination by walking | 
| __walk_d__    | Distance (meters) of the walking route | 
| __pt_r_tt__   | Travel time from origin to destination by public transportation in rush hour traffic; whole travel chain has been taken into acount including the waiting time at home | 
| __pt_r_t__    | Travel time from origin to destination by public transportation in rush hour traffic; whole travel chain has been taken into account excluding the waiting time at home | 
| __pt_r_d__    | Distance (meters) of the public transportation route in rush hour traffic |
| __pt_m_tt__   | Travel time from origin to destination by public transportation in midday traffic; whole travel chain has been taken into acount including the waiting time at home |
| __pt_m_t__    | Travel time from origin to destination by public transportation in midday traffic; whole travel chain has been taken into account excluding the waiting time at home | 
| __pt_m_d__    | Distance (meters) of the public transportation route in midday traffic |
| __car_r_t__   | Travel time from origin to destination by private car in rush hour traffic; the whole travel chain has been taken into account |
| __car_r_d__   | Distance (meters) of the private car route in rush hour traffic |
| __car_m_t__   | Travel time from origin to destination by private car in midday traffic; the whole travel chain has been taken into account |
| __car_m_d__   | Distance (meters) of the private car route in midday traffic |

 
## <a name="calculations"></a>How calculations were done?

Add documentation here.    

## <a name="license"></a>Licence

Helsinki Region Travel Time Matrix 2015 by Accessibility Research Group (University of Helsinki) is licensed under a Creative Commons Attribution 4.0 International License. 
More information about license: http://creativecommons.org/licenses/by/4.0/

If the datasets are being used extensively in scientific research, we welcome the opportunity for co-authorship of papers. Please contact project leader to discuss about the matter.

## <a name="how-to-cite"></a>Citation practices

If you use Helsinki Region-Travel Time Matrix 2015 dataset or related tools in your work, we encourage you to cite properly to our work.

You can cite to our work as follows:

Data/Tools description:
__Toivonen, T., M. Salonen, H. Tenkanen, P. Saarsalmi, T. Jaakkola & J. Järvi (2014). 
Joukkoliikenteellä, autolla ja kävellen: Avoin saavutettavuusaineisto pääkaupunkiseudulla. Terra 126: 3, 127-136.__ 

DOI name for the dataset:
__Toivonen, T., H. Tenkanen, V. Heikinheimo, T. Jaakkola, J. Järvi & M. Salonen (2015). Helsinki Region-Travel Time Matrix 2015. DOI: 10.13140/RG.2.1.1901.3201__

## <a name="codes"></a>Codes

All the codes and analysis steps that have been used to produce the Helsinki Region Travel Time Matrix 2015 are documented separately in [here](codes/README.md). 

## <a name="contact"></a>Contribution / Contact
Helsinki Region Travel Time Matrix 2015 was created by the [Accessibility Research Group](http://www.helsinki.fi/science/accessibility) 
at the Department of Geosciences and Geography, University of Helsinki, Finland.
 
Following people have contributed / are responsible for creating this dataset:

 - [Henrikki Tenkanen](http://blogs.helsinki.fi/accessibility/people_and_contact/) (PhD candidate, contact person regarding the dataset, in charge of the analyses / calculations)
 - Vuokko Heikinheimo (PhD candidate, accessibility calculations, documentation)
 - Tuuli Toivonen (PI, leader of the research group)
 
In addition, we thank [CSC - IT Center for Science](https://www.csc.fi/) for computational resources and help. 
CSC Taito and cPouta computing clusters were used as our workhorses to calculate the travel times/distances (approx. 1 billion routes were calculated) 
using MetropAccess-Digiroad- and MetropAccess-Reititin Tools.   
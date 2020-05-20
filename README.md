# precip-interpolator

#### Data workflow for interpolation of precipitation data from a network of rain gauges on the Central Plains Experimental Range (referred to as hydromet network by our local scientists)

This repository is for development of code to interpolate and map precipitation across the Central Plains Experimental Range (CPER), a 15,500 acre Agricultural Research Service, USDA site in Nunn, CO. In the spring and summer monthes rangelands in the central plains receive precipitation at variable rates; rainfall differs in location, timing and intensity across relative small areas.  This is the time of year moisture is received through isolated convective storms, and is also when cattle are grazed on the landscape for beef production.  Many experimental rangeland sites, such as the CPER, are being instrumented with networks of environmental sensors.   These sensor can tell us precisely when, where and how much rain fell.  But getting the data to scientists and stakeholders in a timely manner to be used to enable precision rangeland management decisions is a challenge.  Maps and plots of data must be presented throughout the season in easy-to-use visualizations, when decisions are being made.

***
<img src="https://mountainscholar.org/bitstream/handle/10217/84527/NRELSGSL_Storm_CSH.jpg?sequence=1&isAllowed=y" alt="Rainstorm" title="Rainstorm" width="300" height="150" /> 

***Localized nature of rainfall on semi-arid rangelands, by Sean Hauser***
***

Interpolation of the CPER hydromet network precipitation data with various statistical methods will result in a script that our scientists will be able to use as a programming module to help answer reseach questions in other locations, in addition to making more precise rangeland management decision on the CPER.  

In addition, we know soil moisture is a master variable that drives plant production and other ecological processes that influence plant communities in semi-arid rangelands.  We also know that interpolation of soil moisture data is more complicated, because of the complexities of landscape position and soil type, so within this repository we will also develop scripts to produce a series of graphics for visualizing soil moisture.  These will be presented to scientists and stakeholders workng on the CPER for feedback.

#### The scripts in this repository will produce tools that can be used in making management of rangelands more precise, and will serve to produce a visualization of evidence to support science-based decisions to help achieve objectives for agricultural production and conservation in rangelands with highly variable precipitation regimes.  

### Python Packages Required for the Workflow:

 * glob 
 * os
 * NumPy
 * Pandas
 * Geopandas
 * Matplotlib
 * Rasterio
 * SciPy
 * Datetime
 
 ### Required conda environment installations:
 
 * See yml file, which I will upload
 
 ### Jupyter Notebooks in the src folder:
 
 1. CARM_FinalProject_NicKaplan_1.ipynb contains code to georefernce precipitaton gauges installed as a network at CPER and interpolate precipitation amounts every two weeks across the CPER site.  This specifically used 2019 data as a proof of concept.
 
 
 ### Data Sources:

Data from the USDA ARS CARM PROJECT (http://www.ars.usda.gov/Research/docs.htm?docid=25733) are available by contacting the CPER; please contact <a href="mailto:Nicole.Kaplan@usda.gov">Nicole.Kaplan@usda.gov</a>
 
 ### Run workflow:
 
1. Clone this repository (https://github.com/nickaplan/precip-interpolator.git)

2. Create working directory for input data and output files for plots and maps of interpolated precipitation data and soil moisture graphics

3. For now, CPER must run R script locally for QC of all sensor data to generate input csv files (available upon request, for now) for interpolation scripts

4. Run script to georeference and interpolate precipitation data, and create graphics of soil moisture


 
 

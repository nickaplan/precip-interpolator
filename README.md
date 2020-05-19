# precip-interpolator

## Data workflow for interpolation of precipitation data from a network of raingauges on the Central Plains Experimental Range (referred to as hydromet network bu our local scientists)

### This repository is for development of code to interpolate and map precipitation across the Central Plains Experimental Range (CPER), a 15,500 acre Agricultural Research Service, USDA site in Nunn, CO.  In the spring and summer months rnagelands in the central plains receive precipitation at variable rates, both in location and intensity.  This is the time of year moisture is received through isolated convective storms.  This is also the time of year when cattle are grazed on the landscape.  Many research sites across experimental rangeland sites are being instrumented with networks of environmental sensors which can tell us, when, where and how much rain fell.  But getting the data to scientists and stakeholders in a timely manner to be used to make precise decisions for field experiments in rangelands is a challenge.  Maps and plots of data must be presented throughout the season in easy-to-use visualizations, when rangeland managers are making management decisions. 


### Interpolation of the CPER hydromet network precipitation data with various statistical methods will result in a script that our scientists will be able to use as a module for reseach questions in other locations, in addition to making management decisions on experiments at the CPER.  

### In addition, we know soil moisture is a master variable that drive plant production and other processed in semi-arid rangelands.  We also know that interpolation of soil moisture data is more complicated, because of the complexities of landscape position and soil type, but we will also develop scripts to produce a series of graphics for visualizing those data.  These will be presented to scientists and stakeholders worlng on the CPER for feedback.

### The scripts in this repository will produce tools that can be used in making management of rangelands more precise, and will serve to produce a visualization of evidence to support science-based decisions to help achieve objectives for agricultural production and conservation in rangelands with highly variable precipitation regimes.  

## Python Packages Required for the Workflow:

 * glob 
 * os
 * NumPy
 * Pandas
 * Geopandas
 * Matplotlib
 * Rasterio
 * SciPy
 * Datetime
 
 ## Requireed installations:
 
 * See yml file, which I will upload
 
 ## Data Sources:
 
 ### Provisional data are available by contacting the CPER; please contact <a href="mailto:Nicole.Kaplan@usda.gov">Nicole.Kaplan@usda.gov</a>
 
 ## Run workflow:
 
1. Clone or fork repository

1.1 Create output file for plots and maps of interpolated precipitation data and soil moisture graphics

2. Run R script for QC of all sensor data 

3. Run script for export of precipitation and soil moisture content data

4. Run script to georeference and interpolate precipitation data, and create graphics of soil moisture

 
 
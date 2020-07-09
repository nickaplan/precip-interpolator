# precip-interpolator

#### Data workflow for interpolation of precipitation data from a network of rain gauges on the Central Plains Experimental Range (referred to as hydromet network by our local scientists)

This repository is for development of code to interpolate and map precipitation across the Central Plains Experimental Range (CPER), a 15,500 acre Agricultural Research Service, USDA site in Nunn, CO. In the spring and summer monthes rangelands in the central plains receive precipitation at variable rates; rainfall differs in location, timing and intensity across relative small areas.  This is the time of year moisture is received through isolated convective storms, and is also when cattle are grazed on the landscape for beef production.  Many experimental rangeland sites, such as the CPER, are being instrumented with networks of environmental sensors.   These sensors can tell us precisely when, where and how much rain fell.  But getting the data to scientists and stakeholders in a timely manner to be used to enable precision rangeland management decisions is a challenge.  Maps and plots of data must be presented throughout the season in easy-to-use visualizations, when decisions are being made.

***
<img src="https://mountainscholar.org/bitstream/handle/10217/84527/NRELSGSL_Storm_CSH.jpg?sequence=1&isAllowed=y" alt="Rainstorm" title="Rainstorm" width="300" height="150" /> 

***Localized nature of rainfall on semi-arid rangelands, by Sean Hauser***
***
The interpolate.py script and GNU Make Makefile are part of an automated workflow of precipitation data from field to stakeholder.  Data from the sensors are delivered to a USDA server via telecom, which runs with a task scheduler on the server.  The script in this repository is a tool that can be used in making management of rangelands more precise, and will serve to produce a visualization of evidence to support science-based decisions to help achieve objectives for agricultural production and conservation in rangelands with highly variable precipitation regimes.  

### Specific Python Packages Required for the Workflow are listed and included in the Earth Analytics Python Environment (https://github.com/earthlab/earth-analytics-python-env)

Specifically, I used this list of packages:
import os
import sys
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib import colors
from scipy.spatial import cKDTree
from datetime import datetime
import earthpy as et
import earthpy.plot as ep
 
 
 ### Sample Jupyter Notebooks in the src folder:
 
 1. precip-interpolator-example.ipynb contains sample code blocks and a table of contents to give the user more control over the initial workflow upon which the interpolate.py python script was compiled to run automatically with the Gnu Make utility using the Makefile_3.txt. 
 
 
 ### Data Sources:

Data for this repository is generated from the USDA ARS CARM PROJECT (http://www.ars.usda.gov/Research/docs.htm?docid=25733). Sample input data are provided in the input folder to run the notebook.  Information is available from the CPER; please contact <a href="mailto:Nicole.Kaplan@usda.gov">Nicole.Kaplan@usda.gov</a>

Data required to run the example notebook includes:

1. CPERBody: A shape file of the CPER Boundary (used in mapping function)
2. cper_pastures_2017_clip: A shape file of the Pastures (used in mapping function)
3. ppt_locations: A csv file of the UTM locations of the precipitation gauges on the CPER (used as input array in interpolating precipitation across the CPER)
4. flagged_ppt_sample: A csv file with sample precipitation data (June 2020) collected everything 15 minutes from the 24 rain gauges (used as input array in interpolating precipitation across the CPER)


 
 ### Run workflow with interpolate.py:
 
1. Clone this repository: https://github.com/nickaplan/precip-interpolator.git

2. The python script is comppiled by the GNU Make Utility (https://swcarpentry.github.io/make-novice/).  GNU MAke requires a Makefile_3.txt which contains the data (and the paths to the data) used to run the script.  IMPORTANT NOTE: The interpolate.py script specifies the working directory to the data.  The Makefile should be placed at the root of the repository, and the script and data may be subdirectories. At the command prompt, navigate to the git repository and type: *python -f Makefile_3.txt*

3. Open jpeg file of interpolated precipitation map.

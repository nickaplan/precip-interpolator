#!/usr/bin/env python

######### WORKFLOW DOCUMENTATION of FUNCTIONS #############################################
# First *InputArrays* to output 2 arrays (ppt value and xy values)
# Second *Run_IDW* for interpolation of the ppt-values, note has daughter classes
# Third *classify* classification of precipitation 
# Fourth *interpolate_map* create of array for plotting, plot and export jpg 

# Import functions
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

############### Function 1 Create Arrays from HydroMet Network Data #######################
def InputArrays(ppt_locations, flagged_ppt):
    """ Takes measured values, calculates cumulative sum, joins them to 
        a list of sample locations, and produces a arrays for interpolation.
        
        Parameters
        ------------
        values:  string
        name of csv file as time-series of values measured at each location 
        used to derive cumulative sum
        
        locations: string
        names of csv file as list of point name, x and y coordinate as UTM
        
        Returns
        ------------
        ar_ppt_wks: np array
        array of 3-week cumulative precipitation in inches
        
        ppt_xy_list: np array
        as list of x y coordinates for each derived sum
        
        date1: date 
        at beginning of range of sum
        
        date2: date 
        at end of range of sum
        
     """
     
    ppt_xy = pd.read_csv(ppt_locations)
    ppt_xy_sort = ppt_xy.sort_values(by=['pasture'], ascending=True) 

    df_ppt = pd.read_csv(flagged_ppt, parse_dates=['date'], delimiter = ",", 
                         usecols = (5,6,8,10,11,12))
    df_ppt.rename(columns={'raw.value': 'raw_value', 'raw.measurement' : 
                           'raw_measurement'}, inplace=True)
    df_ppt['date'] = pd.to_datetime( df_ppt['date'], format='%Y-%m-%d')

    # get last date in the dataset
    date2 = (df_ppt['date'].max()) 
    date1 = date2 - pd.offsets.Day(7)

    # filter ppt data for range and resample
    df_ppt_range = df_ppt.loc[(
        df_ppt['date'] > date1) & (df_ppt['date'] < date2)]
    df_ppt_range = df_ppt.sort_values(by=['site'], ascending=True)

    #merge dataframe and cumulative sum for each site in inches
    df_merged = pd.merge(df_ppt_range, ppt_xy[["pasture", "Easting_UTM", "Northing_UTM"]], 
                         left_on="site", right_on="pasture", how="left")
    df_ppt_wks = (df_merged.groupby(["site"])['raw_value'].sum()) / 25.4

    # Get coordinates for sample location
    df_xy_first = df_merged.groupby(["site"]).first()
    df_xy = df_xy_first[["Easting_UTM", "Northing_UTM"]]
    plot_df = gpd.GeoDataFrame(df_xy_first, geometry=gpd.points_from_xy(
    df_xy_first.Easting_UTM,  df_xy_first.Northing_UTM), crs="epsg:32613")

    # Convert data to numpy array for return
    ar_ppt_wks = df_ppt_wks.to_numpy()
    ppt_xy_list = df_xy.to_numpy()
    
    return(ar_ppt_wks, ppt_xy_list, date1, date2, plot_df)

######################### Function 2 IDW #############################################
# Create Class containing functions for inverse distance weighing

    """
        Inverse distance weighting (IDW)
        --------------------------------

        Compute the score of query points based on the scores of their k-nearest neighbours,
        weighted by the inverse of their distances.

        @reference:
        https://en.wikipedia.org/wiki/Inverse_distance_weighting

        Parameters:
        ----------
            X: (N, d) ndarray
                Coordinates of N sample points in a d-dimensional space.
            z: (N,) ndarray
                Corresponding scores.
            leafsize: int (default 10)
                Leafsize of KD-tree data structure;
                should be less than 20.

        Returns:
        --------
            tree instance: object

        Notes:
        --------
        Wrapper around ___intit____().

       """

class tree(object):  # use tree as the name of the function
    def __init__(self, X=None, z=None, leafsize=20):
        if not X is None:
            self.tree = cKDTree(X, leafsize=leafsize)
        if not z is None:
            self.z = np.array(z)

    def fit(self, X=None, z=None, leafsize=20):

        return self.__init__(X, z, leafsize)

    def __call__(self, X, k=4, eps=1e-6, p=1, regularize_by=1e-9):

        self.distances, self.idx = self.tree.query(X, k, eps=eps, p=p)
        self.distances += regularize_by
        weights = self.z[self.idx.ravel()].reshape(self.idx.shape)
        mw = np.sum(weights/self.distances, axis=1) / \
            np.sum(1./self.distances, axis=1)

        return mw

    def transform(self, X, k=4, p=1, eps=1e-6, regularize_by=1e-9):
        return self.__call__(X, k, eps, p, regularize_by)

    """
        Run_IDW
        ---------

        Create grid from CPER boundary and run interpolation

        Parameters:
        ---------------
            ar_ppt_wks: array
            derived sum of precipitation 

            ppt_xy_list: array
            list of sample locations

         Returns:
         ---------------
             results: array
             interpolated data across the grid of CPER

    """    

def Run_IDW(ar_ppt_wks, ppt_xy_list):

    # Create grid from CPER boundary
    spacing_x = np.linspace(517624.84375, 527273.75, 400)
    spacing_y = np.linspace(4514740.5, 4524361.0, 400)
    X2 = np.meshgrid(spacing_x, spacing_y)
    X2 = np.reshape(X2, (2, -1)).T

    # Assign data to be interpolated for one date
    X = np.reshape(ppt_xy_list, (2, -1)).T  # site points as array

    # Run function and return list of interpolated precipitation values
    z = ar_ppt_wks 
    model = tree(X, z)
    model.fit()
    results = model.transform(X2)

    return results, X2
        
########### Function 3 to Classify precipitation ##################################
def classify(to_class_arr, X2):

    """
    Function classifies numpy arrays using classes defined and
    return stack numpy array along grid

    Parameters
    ----------
    to_class_arr : numpy arr
        arrays that need to be classified

    X2: 2-D numpy arr
        grid for mapping interpolated values

    Returns
    ------
    idw : numpy arr
        arrays with classified values

    """
    # Classify precipitation amount stack in grid
    class_list  = [-np.inf, .75, 1.5, 2.2, 2.3, 2.4, 2.5, np.inf] 
    classified_arr = np.digitize(to_class_arr, class_list)
    idw = np.column_stack((to_class_arr, X2, classified_arr))

    return idw

######### Function 4 to plot numpy array and vector data ##########################################
def interpolate_map(CPERBody, df_xy, cper_pastures_2017_clip, idw, date1, date2):

    """
    Function gets shapes files, maps interpolated array,
    and exports as jpeg

    Parameters:
    -----------------    
    idw: 2-D numpy array
    interpolated and classifed

    boundary: shape file ## OR STRING AS PARAMETER TO USE IN ReADING SHAPE FILE???####
    boundary of CPER

    pasture: shape file
    pasture of CPER in CARM treatment

    Returns:
    ------------------
    jpeg: 
    image file to be included in CARM report, etc

    """      
    extent = (517624.84375, 527273.75, 4514740.5, 4524361.0)

     # Get shape files for site
    cper_bndy = gpd.read_file(CPERBody)
    cper_bounds = cper_bndy.bounds

    # Get shape files and pasture boundaries
    pasture_org = gpd.read_file(cper_pastures_2017_clip)
    AGM_trt = pasture_org[pasture_org['Treatment'].isin(["AGM"])]

    # Reshape array for plotting 
    values_ppt = [1,2,3,4,5,6,7] 
    values_arr = idw[:, 3]
    arr = values_arr.reshape(int(math.sqrt(values_arr.shape[0])), int(math.sqrt(values_arr.shape[0])))
    arr_plt = np.flipud(arr)

    # Create labels and colors for map
    ppt_cat_names = ["0-.75", ".75-1.5", "1.5-2.2", "2.2-2.3", "2.3-2.4", "2.4-2.5", ">2.5"]
    ppt_colors = ["white", "lightcyan", "paleturquoise", "skyblue", 
                  "lightsteelblue", "mediumslateblue", "mediumorchid"]
    ppt_cmap = ListedColormap(ppt_colors)

    # Plot the data with a custom legend
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(arr_plt,
                   cmap=ppt_cmap,
                   vmin=1,
                   vmax=7,
                   extent=extent)

    ep.draw_legend(im,
                   classes=values_ppt,
                   titles=ppt_cat_names)

    cper_bndy.plot(alpha=1, ax=ax, color="none", edgecolor="black", linewidth=1)
    plot_df.plot(alpha=1, ax=ax, color="black", marker="P", markersize=10)
    ax2 = AGM_trt.plot(alpha=1, ax=ax, color="none", edgecolor="black", linewidth=1)
    AGM_trt.apply(lambda x: ax2.annotate(s=x.CARM_Name, xy=x.geometry.centroid.coords[0], 
                                         ha='center', fontsize=8, color="black", fontweight='bold'),axis=1)

    ax.set_title("Inches of Rain Received on CPER From \n" +str(date1)+ " to " +str(date2), fontsize=12)
    ax.text(0, -.05, 'Data Source: USDA ARS', transform=ax.transAxes, fontsize=8)
    ax.set_axis_off()

    filepath = os.path.join(output_path, "ppt21days.jpg")
    plt.savefig(filepath, dpi=300)

    return(print("jpeg saved"))

############# Below is not executed if this file is imported as module ##############################
# Anything created under the if can be passed to functions 
if __name__ == '__main__': # main is defined as the objects and functions listed below 
    
    # Create output folder
    output_path = os.path.join(et.io.HOME, 'ea_python_spatial', 'Final_Project', 'precip-interpolator', "data", "output_maps")

    if not os.path.exists(output_path):
        os.mkdir(output_path) 

    ppt_locations = sys.argv[1] 
    flagged_ppt = sys.argv[2] 
    CPERBody = sys.argv[3] 
    cper_pastures_2017_clip = sys.argv[4] 
   
    ### Hold on here we go.....
    
    #F1
    ar_ppt_wks, ppt_xy_list, date1, date2, plot_df = InputArrays(ppt_locations, flagged_ppt)
    
    #F2
    results, X2 = Run_IDW(ar_ppt_wks, ppt_xy_list)
    
    #F3
    idw = classify(results, X2)
    
    #F4 saves a jpegs to an output folder
    interpolate_map(CPERBody,  plot_df, cper_pastures_2017_clip, idw, date1, date2)
    
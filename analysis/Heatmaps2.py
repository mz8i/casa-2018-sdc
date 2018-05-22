# -*- coding: utf-8 -*-
"""
Created on Tue May 22 10:50:56 2018

@author: josen
"""

import geopandas as gpd
import numpy as np
from scipy import ndimage
import pandas as pd
import os
import statistics
import datetime as dt
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from shapely.geometry import Point
import copy
pylab.rcParams['figure.figsize'] = 8, 6



#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

# IMPORT NECESSARY PACKAGES##############################################
## IMPORT DATA
###Crime
crimes = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv"))  
#Drop rows without location information
crimes=crimes.dropna(subset=['Latitude', 'Longitude'])
crimes = crimes[(crimes[['X Coordinate','Y Coordinate']] != 0).all(axis=1)]
#Change Lat, Lon name
crimes=crimes.rename(columns={'Latitude':'Lat','Longitude':'Lon'})

#Project CRS WGS84 EPSG:4326
crs = {'init': 'epsg:4326'}
#Dataframes dicionaries
dict_of_df = {}
dict_of_geom={}
dict_of_gdf={}

#Build the GeoDataframe for all crimes for each year
for year in np.sort(crimes['Year'].unique()):
    #Names for each dataframe
    key = "crimes_" + str(year)
    key_geom = "g_crimes_"+str(year)
    key_gdf="gdf_crimes_"+str(year)
    #Build of each dataframe
    dict_of_df[key] = crimes[crimes.Year == year]
    dict_of_geom[key_geom]=[Point(xy) for xy in zip(dict_of_df[key].Lon, dict_of_df[key].Lat)]
    dict_of_gdf[key_gdf] = GeoDataFrame(dict_of_df[key], crs=crs, geometry=dict_of_geom[key_geom])

#Plott all years of data using a heatmap for each year
i=0
j=0
fig, axes = plt.subplots(nrows=3, ncols=6, figsize=(21,9), sharex=True, sharey=True)
for year in np.sort(crimes['Year'].unique()):
    #Access to the dataframe dictionaries
    key = "crimes_" + str(year)
    key_geom = "g_crimes_"+str(year)
    key_gdf="gdf_crimes_"+str(year)    
    #Method to get x and y coordinates from points
    def getx(pt):
        return pt.coords[0][0]

    def gety(pt):
        return pt.coords[0][1]

    #List all of the points for each of the dataframes calculated
    x = list(dict_of_gdf[key_gdf].geometry.apply(getx))
    y = list(dict_of_gdf[key_gdf].geometry.apply(gety))
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=150)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    
    #Calculate heatmap values using a gaussian aprox
    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, 1, mode='nearest')
    
    #Build the plot
    axes[i,j].imshow(logheatmap, cmap='jet', extent=extent)
    #plt.colorbar()
    axes[i,j].set_title(str(year), fontsize=15, color='grey', style='italic')
    plt.gca().invert_yaxis()
    #plt.show()
    j+=1
    if j>5:
        i+=1
        j=0
plt.savefig('Years', dpi=300, alpha=True)
dict_of_df.keys()
dict_of_geom.keys()
dict_of_gdf.keys()

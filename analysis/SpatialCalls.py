# -*- coding: utf-8 -*-
"""
Created on Fri May 18 21:18:02 2018

@author: josen
"""

import pandas as pd
import os
import numpy as np
import statistics
import datetime as dt
from matplotlib import pyplot as plt
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from sqlalchemy import create_engine


#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

# IMPORT NECESSARY PACKAGES##############################################
## IMPORT DATA
###Crime
alley_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Alley_Lights_Out.csv")) 
all_lights_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Street_Lights_-_All_Out.csv")) 
one_light_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Street_Lights_-_One_Out.csv")) 

#Remove Duplicates
alley_311 = alley_311[alley_311.Status.str[-5:] != "- Dup"]
all_lights_311 = all_lights_311[all_lights_311.Status.str[-5:] != "- Dup"]
one_light_311 = one_light_311[one_light_311.Status.str[-5:] != "- Dup"]

#Import Police Beats
ch_pbeats = gpd.read_file(os.path.join(data_dir, 'BeatsPolice.shp'))

#Project CRS WGS84 EPSG:4326
crs = {'init': 'epsg:4326'}
#Change Latitude and Longitude names
alley_311=alley_311.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
all_lights_311=all_lights_311.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
one_light_311=one_light_311.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
#Create a Point data with Lon and Lat
g_alley = [Point(xy) for xy in zip(alley_311.Lon, alley_311.Lat)]
g_all_light = [Point(xy) for xy in zip(all_lights_311.Lon, all_lights_311.Lat)]
g_one_light = [Point(xy) for xy in zip(one_light_311.Lon, one_light_311.Lat)]
#Delete Long and Lat columns from dataframes
#alley_311 =alley_311.drop(['Lon', 'Lat'], axis=1)
#all_lights_311 =all_lights_311.drop(['Lon', 'Lat'], axis=1)
#one_light_311 =one_light_311.drop(['Lon', 'Lat'], axis=1)
#Create GeoDataFrame from point dataframe
gdf_alleys = GeoDataFrame(alley_311, crs=crs, geometry=g_alley)
gdf_all_lights = GeoDataFrame(all_lights_311, crs=crs, geometry=g_all_light)
gdf_one_light = GeoDataFrame(one_light_311, crs=crs, geometry=g_one_light)

#Spatial Join between Police Beats and Call Centroids
beat_calls = gpd.sjoin(ch_pbeats, gdf_alleys, how="inner", op='intersects')
beat_calls = gpd.sjoin(ch_pbeats, gdf_all_lights, how="inner", op='intersects')
beat_calls = gpd.sjoin(ch_pbeats, gdf_one_light, how="inner", op='intersects')

# Make a copy because I'm going to drop points as I
# assign them to polys, to speed up subsequent search.
pts = gdf_alleys.copy() 

# We're going to keep a list of how many points we find.
pts_in_polys = []

# Loop over polygons with index i.
for i, poly in ch_pbeats.iterrows():

    # Keep a list of points in this poly
    pts_in_this_poly = []

    # Now loop over all points with index j.
    for j, pt in pts.iterrows():
        if poly.geometry.contains(pt.geometry):
            # Then it's a hit! Add it to the list,
            # and drop it so we have less hunting.
            pts_in_this_poly.append(pt.geometry)
            pts = pts.drop([j])

    # We could do all sorts, like grab a property of the
    # points, but let's just append the number of them.
    pts_in_polys.append(len(pts_in_this_poly))

# Add the number of points for each poly to the dataframe.
ch_pbeats['number of points'] = gpd.GeoSeries(pts_in_polys)


fig, ax = plt.subplots(1)
base = ch_pbeats.plot(ax=ax, color='gray')
gdf_alleys.plot(ax=base, marker="o",markersize=20, alpha=0.5)
_ = ax.axis('off')
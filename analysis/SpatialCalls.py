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
###311 Calls
alley_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Alley_Lights_Out.csv")) 
all_lights_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Street_Lights_-_All_Out.csv")) 
one_light_311 = pd.read_csv(os.path.join(data_dir, "311_Service_Requests_-_Street_Lights_-_One_Out.csv")) 

one_light_311['Type of Service Request'] = one_light_311['Type of Service Request'].replace({"Street Light - 1/Out": "Street Light Out"})

#Join All dataframes for cleaning
Dataframes = [alley_311, all_lights_311, one_light_311]
calls311 = pd.concat(Dataframes)

#Remove Duplicates
calls311 = calls311[calls311.Status.str[-5:] != "- Dup"]

#Transform dates to correct type
calls311['RealCreationDate'] =  pd.to_datetime(calls311['Creation Date'], format="%m/%d/%Y")
calls311['RealCompletionDate'] =  pd.to_datetime(calls311['Completion Date'], format="%m/%d/%Y")

#Calculate Answer time for the calls
calls311_Completed = calls311[calls311.Status == "Completed"]
calls311_Completed['RespTime']= calls311_Completed['RealCompletionDate']-calls311_Completed['RealCreationDate']
calls311_Completed['RespTime']= (calls311_Completed['RespTime'] / np.timedelta64(1, 'D')).astype(int)

#Filtering for 2017
calls311_Completed['Year']=calls311_Completed['RealCreationDate'].dt.year
calls311_2017=calls311_Completed[calls311_Completed.Year == 2017]

####Spatial Analysis
#Import Police Beats
ch_pbeats = gpd.read_file(os.path.join(data_dir, 'BeatsPolice.shp'))
#Project CRS WGS84 EPSG:4326
crs = {'init': 'epsg:4326'}
#Change Latitude and Longitude names
calls311_2017=calls311_2017.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
#Create a Point data with Lon and Lat
g_calls311_2017 = [Point(xy) for xy in zip(calls311_2017.Lon, calls311_2017.Lat)]
#Create the GeoDataframe
gdf_calls311_2017 = GeoDataFrame(calls311_2017, crs=crs, geometry=g_calls311_2017)
#Assign each call its correspondent Beat
id_calls311_2017 = gpd.sjoin(ch_pbeats, gdf_calls311_2017, how="inner", op='intersects')

#Filter Dataframes per type of call
alley_2017=id_calls311_2017[id_calls311_2017['Type of Service Request'] == 'Alley Light Out']
all_lights_2017=id_calls311_2017[id_calls311_2017['Type of Service Request'] == 'Street Lights - All/Out']
one_light_2017=id_calls311_2017[id_calls311_2017['Type of Service Request'] == 'Street Light Out']

#Count number of calls per beat and calculate the mean answer time for the calls
beat_alley = alley_2017.Status.groupby(alley_2017['beat_num']).count().to_frame(name='Calls_Alley')
beat_all_out = all_lights_2017.Status.groupby(all_lights_2017['beat_num']).count().to_frame(name='Calls_All_Out')
beat_one_out = one_light_2017.Status.groupby(one_light_2017['beat_num']).count().to_frame(name='Calls_One_Out')

beat_alley['Time_Alleys'] = alley_2017['RespTime'].groupby(alley_2017['beat_num']).mean()
beat_all_out['Time_All_Out'] = all_lights_2017['RespTime'].groupby(all_lights_2017['beat_num']).mean()
beat_one_out['Time_One_Out'] = one_light_2017['RespTime'].groupby(one_light_2017['beat_num']).mean()

#Combine everithing into a DataFrame
beat_calls = pd.concat([beat_alley, beat_all_out,beat_one_out], axis=1)
beat_calls.to_csv('beat_calls.csv')



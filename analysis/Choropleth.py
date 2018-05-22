# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:52:02 2018

@author: josen
"""

import geopandas as gpd
import pandas as pd
import os
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from geopandas import GeoDataFrame
from shapely.geometry import Point
import seaborn as sns
pylab.rcParams['figure.figsize'] = 8, 6



#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

# IMPORT NECESSARY PACKAGES##############################################
## IMPORT DATA
###Crime
crimes = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv"))  
crimes=crimes.dropna(subset=['Latitude', 'Longitude'])
crimes=crimes.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
crimes = crimes[(crimes[['X Coordinate','Y Coordinate']] != 0).all(axis=1)]
#Filtering for 2017
crimes_2017=crimes[crimes.Year == 2017]

#Project CRS WGS84 EPSG:4326
crs = {'init': 'epsg:4326'}

#####Beats Shapefile
ch_pbeats = gpd.read_file(os.path.join(data_dir, 'BeatsPolice.shp'))
beats = ch_pbeats[['geometry','beat_num']]

#### CSV Data
pop = pd.read_csv(os.path.join(data_dir, "beat_pop.csv"))
calls = pd.read_csv(os.path.join(data_dir, "beat_calls.csv"))
trans = pd.read_csv(os.path.join(data_dir, "beat_transport.csv"))
affinity  = pd.read_csv(os.path.join(data_dir, "data_clusters.csv"))
hierarch = pd.read_csv(os.path.join(data_dir, "beats_clusters_hierarch.csv"))

#Drop first row of every dataet
pop=pop.drop(pop.index[0])
calls=calls.drop(calls.index[0])
trans=trans.drop(trans.index[0])
affinity=affinity.drop(affinity.index[0])
hierarch=hierarch.drop(hierarch.index[0])
#countries = countries.rename(columns={'name':'country'})

popbeat= pop['beat_num']
callsbeat=calls['beat_num']
trasnbeat = trans['beat_num']
affinitybeat =affinity['beat_num']
hierarchbeat=hierarch['beat_num']

#Reorganize the dataframes
pop=pop.drop(['beat_num','geometry'], axis =1)
calls=calls.drop('beat_num', axis = 1)
trans=trans.drop('beat_num', axis =1)
affinity=affinity.drop('beat_num', axis =1)
hierarch=hierarch.drop('beat_num', axis =1)

pop['beat_num']=popbeat
calls['beat_num']=callsbeat
trans['beat_num']=trasnbeat
affinity['beat_num']=affinitybeat
hierarch['beat_num']=hierarchbeat

#Merge Beats and numerical data
beats = beats.merge(pop, on='beat_num')
beats = beats.merge(calls, on='beat_num')
beats = beats.merge(trans, on='beat_num')
beats = beats.merge(affinity, on='beat_num')
beats = beats.merge(hierarch, on='beat_num')

#Plot and save maps for clustering results
ch_pbeats=ch_pbeats.set_geometry('geometry')
beats.plot(column='cluster', cmap='tab20c',markersize=30, categorical=True, legend=True)
plt.savefig('Hierarch', dpi=300, alpha=True)

fig, ax = plt.subplots(1)
beats.plot(column='Affinity', cmap='Set2',markersize=30, categorical=True, legend=True)
plt.savefig('Affinity', dpi=300, alpha=True)

fig, ax = plt.subplots(1)
beats.plot(column='Agglomerative', cmap='Set3',markersize=30, categorical=True, legend=True)
plt.savefig('Agglomerative', dpi=300, alpha=True)

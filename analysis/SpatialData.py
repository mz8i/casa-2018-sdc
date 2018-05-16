# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:43:14 2018

@author: josen
"""

import shapefile as shp
import os
import geopandas as gpd
from osgeo import ogr
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point

#Read shapefiles
ch_blocks = gpd.read_file('C:/Users/josen/Documents/2nd Term UCL/Spatial Data Capture/Final Project/Blocks.shp')
ch_pbeats = gpd.read_file('C:/Users/josen/Documents/2nd Term UCL/Spatial Data Capture/Final Project/BeatsPolice.shp')
#Read CSV files
ch_pop = pd.read_csv('C:/Users/josen/Documents/2nd Term UCL/Spatial Data Capture/Final Project/Population_by_2010_Census_Block1.csv')
ch_pop=ch_pop.drop(0)
ch_crime = pd.read_csv('C:/Users/josen/Documents/2nd Term UCL/Spatial Data Capture/Final Project/export_2017.csv')

#Sort DataFrames/GeoDataFrames for processing
ch_blocks = ch_blocks.rename(columns={'tract_bloc': 'CENSUS BLOCK'})
ch_crime=ch_crime.rename(columns={'Latitude':'Lat','Longitude':'Lon'})
ch_blocks = ch_blocks[['geometry','CENSUS BLOCK']]
ch_pop=ch_pop[['TOTAL POPULATION','CENSUS BLOCK']]

############## Population Spatial projection

#Population merge with Census Blocks
ch_blocks = ch_blocks.merge(ch_pop, on='CENSUS BLOCK')

#Transform Census Blocks into Centroids
ch_blocks['centroid_column'] = ch_blocks.centroid
ch_blocks = ch_blocks.set_geometry('centroid_column')

#Spatial Join between Police Beats and Block Centroids
block_with_beat = gpd.sjoin(ch_blocks, ch_pbeats, how="inner", op='intersects')
block_with_beat = block_with_beat.set_geometry('geometry')

#Aggregate population per Beat
beat_pop = block_with_beat.dissolve(by='beat_num', aggfunc='sum')

#Produce Crime GeoDataFrame
geometry = [Point(xy) for xy in zip(ch_crime.Lon, ch_crime.Lat)]
ch_crime = ch_crime.drop(['Lon', 'Lat'], axis=1)
crs = {'init': 'epsg:4326'}
crimes_gdf = GeoDataFrame(ch_crime, crs=crs, geometry=geometry)


beat_pop = beat_pop.rename(columns={'index_right': 'index'})

beat_crime = gpd.sjoin(beat_pop, crimes_gdf, how="inner", op='intersects')



# We're going to keep a list of how many points we find.
crime_in_beats = []
crime_copy=crimes_gdf.copy()

# Loop over polygons with index i.
for i, poly in beat_pop.iterrows():

    # Keep a list of points in this poly
    crimes_in_this_beat = []

    # Now loop over all points with index j.
    for j, pt in crime_copy.iterrows():
        if poly.geometry.contains(pt.geometry):
            # Then it's a hit! Add it to the list,
            # and drop it so we have less hunting.
            crimes_in_this_beat.append(pt.geometry)
            crime_copy = crime_copy.drop([j])

    # We could do all sorts, like grab a property of the
    # points, but let's just append the number of them.
    crime_in_beats.append(len(crimes_in_this_beat))

# Add the number of points for each poly to the dataframe.
polygons['number of points'] = gpd.GeoSeries(pts_in_polys)







beat_pop_32616 = beat_pop.to_crs('+init=epsg:32616')

beat_pop.plot(column = 'TOTAL POPULATION', cmap='OrRd')

beat_pop.crs



# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:43:14 2018

@author: josen
"""
import os
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from sqlalchemy import create_engine

#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

#Read shapefiles
ch_blocks = gpd.read_file(os.path.join(data_dir, 'Blocks.shp'))
ch_pbeats = gpd.read_file(os.path.join(data_dir, 'BeatsPolice.shp'))
#Read CSV files
ch_pop = pd.read_csv(os.path.join(data_dir, "Population_by_2010_Census_Block1.csv"))
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
beat_pop['beat_num'] = beat_pop.index

#################Convert file and upload it to MySQL
# create the connection string to the MySQL database


################## THIS PART IS ONLY FOR THE CONNECTION TO WORK THROUGH SSH ###########################
from sshtunnel import SSHTunnelForwarder
server =  SSHTunnelForwarder(
     ('dev.spatialdatacapture.org', 22),
     ssh_password=os.environ.get('DB_PASSWORD'),
     ssh_username=os.environ.get('DB_USER'),
     remote_bind_address=('127.0.0.1', 3306))
server.start()

print(server.local_bind_port)
engine = create_engine('mysql+pymysql://ucfnmbz:sadohazije@127.0.0.1:%s/ucfnmbz' % server.local_bind_port)
############################################################################################################
#engine = create_engine('mysql+pymysql://ucfnmbz:sadohazije@dev.spatialdatacapture.org:3306/ucfnmbz')

# Create SQL connection engine
conn = engine.raw_connection()

# Function to generate WKB hex
def wkb_hexer(line):
    return line.wkt

#Convert geometry column in GeoDataFrame to hex
#Then the GeoDataFrames are just regular DataFrames
beat_pop['geometry'] = beat_pop['geometry'].apply(lambda x: x.wkt)

# Connect to database and export data
with engine.connect() as conn, conn.begin():
    beat_pop.to_sql('beat_population', con=conn, 
               if_exists='append', index=False)









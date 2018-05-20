# -*- coding: utf-8 -*-
"""
Created on Sat May 19 16:50:56 2018

@author: josen
"""

import pandas as pd
import os
import numpy as np
import geopandas as gpd
from sqlalchemy import create_engine



#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

####Spatial Analysis
#Import Police Beats
rail = gpd.read_file(os.path.join(data_dir, 'CTA_RailStations.shp'))
bus = gpd.read_file(os.path.join(data_dir, 'CTA_BusStops.shp'))
ch_pbeats = gpd.read_file(os.path.join(data_dir, 'BeatsPolice.shp'))
#Drop 'Nones' in Bus routes
bus = bus.dropna(subset=['ROUTESSTPG'])

#Re project the transport data
crs = {'init': 'epsg:4326'}
rail = rail.to_crs(crs)
bus = bus.to_crs(crs)

#Divide the columns where lines information is registered to count the numberof services at each station
divide = lambda x: pd.Series([i for i in reversed(x.split(','))])
rail_lines = rail['LINES'].apply(divide)
bus_lines = bus['ROUTESSTPG'].apply(divide)

#Count the number of services at each station
rail_lines['Total'] = (rail_lines[list(rail_lines.columns.values)] > pd.notna).sum(1)
bus_lines['Total'] = (bus_lines[list(bus_lines.columns.values)] > pd.notna).sum(1)

#Join Geodataframe and the count of services per station
rail = pd.concat([rail, rail_lines['Total']], axis=1)
bus = pd.concat([bus, bus_lines['Total']], axis=1)
#Rename total column
rail = rail.rename(columns={'Total': 'T_Services'})
bus = bus.rename(columns={'Total': 'T_Services'})
#Spatial join to identify which point belongs to each Beat
id_rail = gpd.sjoin(ch_pbeats, rail, how="inner", op='intersects')
id_bus = gpd.sjoin(ch_pbeats, bus, how="inner", op='intersects')

#Group by beat number to get the amount of stations per beat
beat_rail = id_rail.STATION_ID.groupby(id_rail['beat_num']).count().to_frame(name='Rail_Stations')
beat_bus = id_bus.WARD.groupby(id_bus['beat_num']).count().to_frame(name='bus_Stations')
#Calculate the average number of services that works on each beat
beat_rail['Routes_Rail'] = id_rail['T_Services'].groupby(id_rail['beat_num']).mean()
beat_bus['Routes_Bus'] = id_bus['T_Services'].groupby(id_bus['beat_num']).mean()
#Join everithing in one dataframe
beat_transport = pd.concat([beat_bus, beat_rail], axis=1)
beat_transport.to_csv('beat_transport.csv')

#Import file to match the correspondent station Codes for Rail system with the data from GTFS
rail_codes = pd.read_csv(os.path.join(data_dir, "CTA_-_System_Information_-_List_of__L__Stops_-_Map.csv")) 
rail_codes['STATION_CODE'] = rail_codes.MAP_ID.astype(str).str[-4:].astype(np.int64)
rail_codes_join = pd.merge(rail_codes, id_rail, left_on='STATION_CODE',right_on= 'STATION_ID')
rail_codes_join = rail_codes_join.drop(['ADA_x','RED','BLUE','G','BRN','P','Pexp','Y', 'Pnk','O','district', 'sector','geometry','index_right','ADA_y','PKNRD'], 1)

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

#Drop geometry column to turn the file into a regular Geodataframe
point_bus=id_bus.drop(['geometry'],1) 
  
# Connect to database and export data
with engine.connect() as conn, conn.begin():
    rail_codes_join.to_sql('rail_beat', con=conn, 
               if_exists='append', index=False)
    point_bus.to_sql('bus_beat', con=conn, 
               if_exists='append', index=False)


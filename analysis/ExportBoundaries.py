# -*- coding: utf-8 -*-
"""
Created on Sat May 19 00:38:52 2018

@author: josen
"""

import os
import geopandas as gpd
from sqlalchemy import create_engine

#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

#Read shapefiles
ch_boundaries = gpd.read_file(os.path.join(data_dir, 'ChicagoBoundaries.shp'))
ch_community = gpd.read_file(os.path.join(data_dir, 'ChicagoCommunityAreas.shp'))


#################Convert file and upload it to MySQL
# create the connection string to the MySQL database


################## THIS PART IS ONLY FOR THE CONNECTION TO WORK WITH NICO(C) PC ###########################
from sshtunnel import SSHTunnelForwarder
server =  SSHTunnelForwarder(
     ('dev.spatialdatacapture.org', 22),
     ssh_password="Br1ck.ManiAc",
     ssh_username="ucfnjnb",
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

# Convert `'geom'` column in GeoDataFrame `gdf` to hex
    # Note that following this step, the GeoDataFrame is just a regular DataFrame
    # because it does not have a geometry column anymore. Also note that
    # it is assumed the `'geom'` column is correctly datatyped.
ch_boundaries['geometry'] = ch_boundaries['geometry'].apply(lambda x: x.wkt)
ch_community['geometry'] = ch_community['geometry'].apply(lambda x: x.wkt)

# Connect to database using a context manager
with engine.connect() as conn, conn.begin():
    # Note use of regular Pandas `to_sql()` method.
    ch_boundaries.to_sql('ch_boundaries', con=conn, 
               if_exists='append', index=False)
    ch_community.to_sql('ch_community', con=conn, 
               if_exists='append', index=False)
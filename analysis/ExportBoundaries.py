# -*- coding: utf-8 -*-
"""
Created on Sat May 19 00:38:52 2018

@author: josen
"""

import os
import geopandas as gpd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT

#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

#Read shapefiles
ch_boundaries = gpd.read_file(os.path.join(data_dir, 'ChicagoBoundaries.shp'))
ch_community = gpd.read_file(os.path.join(data_dir, 'ChicagoCommunityAreas.shp'))

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

# Function to generate WKT file
def wkb_hexer(line):
    return line.wkt

#Convert geometry column in GeoDataFrame to hex
#Then the GeoDataFrames are just regular DataFrames 
ch_boundaries['geometry'] = ch_boundaries['geometry'].apply(lambda x: x.wkt)
ch_community['geometry'] = ch_community['geometry'].apply(lambda x: x.wkt)

# Connect to database and export data
with engine.connect() as conn, conn.begin():
    ch_boundaries.to_sql('ch_boundaries', con=conn, 
               if_exists='append', index=False, dtype={'shape_len':sqlalchemy.types.INTEGER(),
                                                       'shape_area':sqlalchemy.types.Float(),
                                                       'objectid':sqlalchemy.types.INTEGER(),
                                                       'name':sqlalchemy.types.NVARCHAR(length=255),
                                                       'geometry':LONGTEXT()})
    ch_community.to_sql('ch_community', con=conn, 
               if_exists='append', index=False, dtype={'perimeter':sqlalchemy.types.INTEGER(),
                                                       'community':sqlalchemy.types.NVARCHAR(length=255),
                                                       'shape_len':sqlalchemy.types.Float(),
                                                       'shape_area':sqlalchemy.types.Float(),
                                                       'area':sqlalchemy.types.INTEGER(),
                                                       'comarea':sqlalchemy.types.INTEGER(),
                                                       'area_numbe':sqlalchemy.types.INTEGER(),
                                                       'area_num_1':sqlalchemy.types.INTEGER(),
                                                       'comarea_id':sqlalchemy.types.INTEGER(),
                                                       'geometry':LONGTEXT()})
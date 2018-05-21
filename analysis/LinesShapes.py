# -*- coding: utf-8 -*-
"""
Created on Mon May 21 00:43:37 2018

@author: josen
"""

import pandas as pd
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import os
import geopandas as gpd
from sqlalchemy import create_engine


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
 
route_shapes=pd.read_sql_table('shapes', engine)


# Zip the coordinates into a point object and convert to a GeoDataFrame
geometry = [Point(xy) for xy in zip(route_shapes.shape_pt_lon, route_shapes.shape_pt_lat)]
r_shape_geo = GeoDataFrame(route_shapes, geometry=geometry)


# Aggregate these points with the GroupBy
r_shape_geo = r_shape_geo.groupby(['shape_id'])['geometry'].apply(lambda x: LineString(x.tolist()))
r_shape_geo = GeoDataFrame(r_shape_geo, geometry='geometry')
r_shape_geo['shape_id']=r_shape_geo.index
r_shape_geo.plot()


# Function to generate WKB hex
def wkb_hexer(line):
    return line.wkt

#Convert geometry column in GeoDataFrame to hex
#Then the GeoDataFrames are just regular DataFrames
r_shape_geo['geometry'] = r_shape_geo['geometry'].apply(lambda x: x.wkt)
r_shape_geo.rename(index=str, columns={"geometry": "geom", "C": "c"})

# Connect to database and export data
with engine.connect() as conn, conn.begin():
    r_shape_geo.to_sql('route_shapes', con=conn, 
               if_exists='append', index=False)







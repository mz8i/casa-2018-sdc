# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:03:17 2018

@author: Nico
"""

import pandas as pd
import os
import numpy as np
import statistics
import datetime as dt
from matplotlib import pyplot as plt

#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

# IMPORT NECESSARY PACKAGES##############################################
## IMPORT DATA
###Crime
data = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv")) 
sliced=data.iloc[:, :]
#Change to datetime format and get minute, hour, day, month, year
sliced['RealDate'] =  pd.to_datetime(sliced['Date'], format="%m/%d/%Y  %I:%M:%S %p")
sliced['Minute']=sliced['RealDate'].dt.minute
sliced['Hour'] = sliced['RealDate'].dt.hour
sliced['Day'] = sliced['RealDate'].dt.day
sliced['Month'] = sliced['RealDate'].dt.month
sliced['Year']=sliced['RealDate'].dt.year
#Calculate time in real number
sliced['timeReal']=sliced['Hour']+sliced['Minute']/60

#Working only with 2017 data
sliced_2017=sliced[sliced.Year == 2017]

#Creating table per hour
#Column Counts per hour
counts_perhour=sliced_2017.RealDate.groupby(sliced_2017.Hour).count().to_frame(name='Counts')
#Column Percentages per hour
counts_perhour['Percentages']=(counts_perhour.Counts)/sum(counts_perhour.Counts.values)
#Column cumulative percentages per hour
counts_perhour['CumPercent']=counts_perhour.Percentages.cumsum()
#Plotting Percentages
plt.plot(counts_perhour.index,counts_perhour.Percentages)
#Plotting Cumulative Percentages
plt.plot(counts_perhour.index,counts_perhour.CumPercent)

#Changing order of the rows, to get the cumulative percentage from 5AM instead of 00HRS
rows=counts_perhour.index.tolist()
rows=rows[5:]+rows[:5]
counts_2=counts_perhour.loc[rows,:]
counts_2['CumPercent']=counts_2.Percentages.cumsum()
counts_2.index=counts_2.index.map(str)
#Plotting Percentages (it didn't #$$!! worked)
plt.plot(counts_2.index,counts_2.Percentages)

#As far as I understand, we don't need the table, so let's try to get the quantiles only
#I'm missing grouping the data by hour in the codes below!!!!
#Try sth like: 
quant=sliced.RealDate.groupby(sliced.Year).quantile([.25,.5,.75])

#Median
med_2017=statistics.median(sliced_2017.RealDate)

#Isolate the Time from timestamp column
sliced_2017['time'] = [d.time() for d in sliced_2017['RealDate']]
sliced['time']=[d.time() for d in sliced['RealDate']]

#1st, 2nd(median) and 3rd quartiles
quantiles_2017=sliced.Hour.astype('int64').quantile([.25,.5,.75]).astype('datetime64[ns]')

#Trying to gte the values in 5AM base instead of 00HRS
#First we substract 5 hours (using timedelta function)
quantiles_2017_5AM=(sliced.Hour-dt.timedelta(hours=5)).astype('int64').quantile([.25,.5,.75]).astype('datetime64[ns]')


###################################### Statistics every half hour ###########################################

#Create count, percentages and cumulative percentages tables
counts_halfhour=sliced.timeReal.groupby(pd.cut(sliced["timeReal"], np.arange(0., 24.5, 0.5),include_lowest = True)).count().to_frame(name='Counts')
counts_halfhour_2017=sliced_2017.timeReal.groupby(pd.cut(sliced_2017["timeReal"], np.arange(0., 24.5, 0.5),include_lowest = True)).count().to_frame(name='Counts')
#Column Percentages per hour
counts_halfhour['Percentages']=(counts_halfhour.Counts)/sum(counts_halfhour.Counts.values)
counts_halfhour_2017['Percentages']=(counts_halfhour_2017.Counts)/sum(counts_halfhour_2017.Counts.values)
#Column cumulative percentages per hour
counts_halfhour['CumPercent']=counts_halfhour.Percentages.cumsum()
counts_halfhour_2017['CumPercent']=counts_halfhour_2017.Percentages.cumsum()
#Change index column
counts_halfhour=counts_halfhour.set_index(np.arange(0.5,24.5,0.5))
counts_halfhour_2017=counts_halfhour.set_index(np.arange(0.5,24.5,0.5))
#Statistics
quantiles_halfhour=sliced.timeReal.astype('int64').quantile([.25,.5,.75]).astype(float)
quantiles_halfhour_2017=sliced_2017.timeReal.astype('int64').quantile([.25,.5,.75]).astype(float)

#Changing order of the rows, to get the cumulative percentage from 5AM instead of 00HRS
rows=counts_halfhour.index.tolist()
rows=rows[10:]+rows[:10]
c_halfhour_5am=counts_halfhour.loc[rows,:]
c_halfhour_5am['CumPercent']=c_halfhour_5am.Percentages.cumsum()

quantiles_halfhour = pd.DataFrame(index={2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017},columns={'1stQuart','Median','3rdQuart','Timespan','FiveFive'})
quantiles_halfhour = pd.DataFrame(index=range(2001,2018),columns={'1stQuart','Median','3rdQuart','Timespan','FiveFive'})

quantiles_halfhour['1stQuart'] = counts_halfhour.index[counts_halfhour['CumPercent']>0.25][0]
counts_halfhour.index[counts_halfhour['CumPercent']>0.5][0]
counts_halfhour.index[counts_halfhour['CumPercent']>0.75][0]
counts_halfhour.index[counts_halfhour.index >0.5][0]


for year in sliced['Year'].unique():
    df1 = sliced[sliced['Year'] == year]
    df2=df1.timeReal.groupby(pd.cut(df1["timeReal"], np.arange(0., 24.5, 0.5),include_lowest = True)).count().to_frame(name='Counts_'+str(year))
    df2['Percentages_'+str(year)]=(df2['Counts_'+str(year)])/sum(df2['Counts_'+str(year)].values)
    df2['CumPercent_'+str(year)]=df2['Percentages_'+str(year)].cumsum()
    df3=df1.timeReal.astype('int64').quantile([.25,.5,.75]).astype(float)   
    
    counts_halfhour = pd.concat([counts_halfhour, df2], axis=1, join_axes=[counts_halfhour.index])
    quantiles_halfhour['timeReal_'+str(year)] = df3


















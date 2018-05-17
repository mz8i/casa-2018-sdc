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

#Working only with 2017 data
sliced_2017=sliced[sliced.Year == 2017]

#Creating table per hour
#Column Counts per hour
counts_perhour=sliced.RealDate.groupby(sliced_2017.Hour).count().to_frame(name='Counts')
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
plt.bar(counts_2.index,counts_2.Percentages)

#As far as I understand, we don't need the table, so let's try to get the quantiles only
#I'm missing grouping the data by hour in the codes below!!!!
#Try sth like: 
#quant=sliced.RealDate.groupby(sliced_2017.Hour).astype('int64').quantile([.25,.5,.75]).astype('datetime64[ns]')

#Median
med_2017=statistics.median(sliced_2017.RealDate)
#1st, 2nd(median) and 3rd quartiles
quantiles_2017=sliced.RealDate.astype('int64').quantile([.25,.5,.75]).astype('datetime64[ns]')

#Trying to gte the values in 5AM base instead of 00HRS
#First we substract 5 hours (using timedelta function)
quantiles_2017_5AM=(sliced.RealDate-dt.timedelta(hours=5)).astype('int64').quantile([.25,.5,.75]).astype('datetime64[ns]')



#type(sliced_2017.RealDate)
#type(counts_perhour.Counts.values)
#type(counts_2.index)

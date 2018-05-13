# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:33:18 2018

@author: julian
"""
# hola
# library
import seaborn as sns
import pandas as pd
import numpy as np
import pylab

import os


analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

# IMPORT NECESSARY PACKAGES##############################################
## IMPORT DATA
###Crime
data = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv")) 
###Light
datasun = pd.read_csv(os.path.join(data_dir, "Night_Day_time1.csv"))
data.head

#CLEANING################################################################
########################RENAMING and grouping

# iloc[row slicing, column slicing]
sliced=data.iloc[:, :]
from matplotlib import pyplot as plt

sliced["Primary Type"].value_counts()
sliced.loc[sliced["Primary Type"] == "NON - CRIMINAL","Primary Type"]="NON-CRIMINAL"
sliced.loc[sliced["Primary Type"] == "NON-CRIMINAL (SUBJECT SPECIFIED)","Primary Type"]="NON-CRIMINAL"

sliced.loc[sliced["Primary Type"] == "OTHER NARCOTIC VIOLATION","Primary Type"]="NARCOTICS"
sliced["Primary Type"].value_counts()


#DAY LIGHT
pd.to_datetime(datasun['Astr Start'], format="%H:%M")

#Read as date data
date_test = "03/18/2015 07:44:00 PM"
sliced['RealDate'] =  pd.to_datetime(sliced['Date'], format="%m/%d/%Y  %I:%M:%S %p")

sliced['Day'] = sliced['RealDate'].dt.day

sliced['Month'] = sliced['RealDate'].dt.month

sliced['Hour'] = sliced['RealDate'].dt.hour

sliced['Year']=sliced['RealDate'].dt.year

sliced['Crime1'] = 1

#Histogram
plt.hist(sliced['Hour'])

#only month and day
sliced['tesdate'] = sliced['Month'].apply(str).str.zfill(2) +"."+ sliced['Day'].apply(str).str.zfill(2)

#only month, month and year
sliced['testdateyear'] = sliced['Month'].apply(str).str.zfill(2) +"."+ sliced['Day'].apply(str).str.zfill(2)+"."+sliced['Year'].apply(str).str.zfill(2)
#transform into datetime
sliced['MD'] =  pd.to_datetime(sliced['testdateyear'], format="%m.%d.%Y")

#Subsetting for Each year
sliced_2001=sliced[sliced.Year == 2001]
sliced_2002=sliced[sliced.Year == 2002]
sliced_2003=sliced[sliced.Year == 2003]
sliced_2004=sliced[sliced.Year == 2004]
sliced_2005=sliced[sliced.Year == 2005]
sliced_2006=sliced[sliced.Year == 2006]
sliced_2007=sliced[sliced.Year == 2007]
sliced_2008=sliced[sliced.Year == 2008]
sliced_2009=sliced[sliced.Year == 2009]
sliced_2010=sliced[sliced.Year == 2010]
sliced_2011=sliced[sliced.Year == 2011]
sliced_2012=sliced[sliced.Year == 2012]
sliced_2013=sliced[sliced.Year == 2013]
sliced_2014=sliced[sliced.Year == 2014]
sliced_2015=sliced[sliced.Year == 2015]
sliced_2016=sliced[sliced.Year == 2016]
sliced_2017=sliced[sliced.Year == 2017]

#THEFT SUBSET ###########################################################
sliced_Theft2017=sliced_2017[sliced_2017["Primary Type"] == "THEFT"]
#Export csv
spatial_Theft2017=sliced_Theft2017[sliced_Theft2017.Latitude.notnull()]
spatial_Theft2017.to_csv(os.path.join(data_dir, "export_spatial_theft_2017.csv"))
##########################################################################

#Remove data between 00:00 and 01:00
sliced_23=sliced[sliced.Hour != 0]
#and now Remove data from first day of months
sliced_0223=sliced_23[sliced_23.Day != 1]
#and now Remove data from 02.29
sliced_29=sliced_0223[sliced_0223.tesdate != "02.29"]


#PIE PLOT###############################################################"
sliced["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")
sliced_2015["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")
sliced_2016["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")
sliced_2017["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")

#Exported CSV per year
export_2016=sliced[sliced.Year == 2016]
export_2017=sliced[sliced.Year == 2017]

#export_2016.to_csv("D:/Dropbox/Cloud - Master's - Docs/Spatial Data Capture, Storage and Analysis/Data Project/City-Crime/export_2016.csv")

#export_2017.to_csv("D:/Dropbox/Cloud - Master's - Docs/Spatial Data Capture, Storage and Analysis/Data Project/City-Crime/export_2017.csv")

#Category distribution pet year
sliced["Primary Type"].value_counts()
sliced_2017["Primary Type"].value_counts()
sliced_2016["Primary Type"].value_counts()
sliced_2015["Primary Type"].value_counts()
sliced_2014["Primary Type"].value_counts()
sliced_2013["Primary Type"].value_counts()
sliced_2012["Primary Type"].value_counts()
sliced_2011["Primary Type"].value_counts()
sliced_2010["Primary Type"].value_counts()



#######PLOT TIME SERIES #################################################

 #Getting unique values after grouping by hour and DAY FOR 2016
sliced_newTime = sliced[sliced["Month"] >= 1].groupby(["Crime1", "MD"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newTime = sliced_newTime.reset_index(name="Count")
plt.plot(sliced_newTime["MD"], sliced_newTime['Count'])

#TOP10 Crimes :P
sliced["Top10"]= sliced["Primary Type"]

sliced.loc[sliced["Primary Type"] == "DOMESTIC VIOLENCE","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "RITUALISM","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "HUMAN TRAFFICKING","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "PUBLIC INDECENCY","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "CONCEALED CARRY LICENSE VIOLATION","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "NON-CRIMINAL","Top10"]="Other"
sliced.loc[sliced["Primary Type"] == "OBSCENITY","Top10"]="Other"

sliced["Top10"].value_counts()

sliced["Top10"].value_counts().plot(kind="pie",autopct="%.2f")
#########################################################################

#SPATIAL DATA SUBSET#####################################################
spatial_crime=sliced[sliced.Latitude.notnull()]

# let's put more analysis here

#HEATMAP by CATEGORY ######################################################
# Getting unique values after grouping by hour and CATEGORY
sliced_newC = sliced[sliced["Month"] >= 1].groupby(["Hour", "Top10"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newC = sliced_newC.reset_index(name="Count")
sliced_newC["Sum"]=sliced_newC["Count"]/sliced_newC.groupby("Top10")["Count"].transform(np.sum)
#Plot the Heatmap
heatcat=sns.heatmap(sliced_newC.pivot("Top10","Hour", "Sum"), annot=False, cmap="BuPu")
plt.xticks(rotation=45)
####################################################################




#HEATMAP by Hour and Month ############################################
# Getting unique values after grouping by HOUR and MONTH
sliced_new = sliced[sliced["Month"] >= 1].groupby(["Hour", "Month"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new = sliced_new.reset_index(name="Count")

#Dictionary To get right day numbers (select all lines and run)
days_in_month={
        1:31,
        2:28,
        3:31,
        4:30,
        5:31,
        6:30,
        7:31,
        8:31,
        9:30,
        10:31,
        11:30,
        12:31
}

sliced_new['Month'].map(days_in_month)
sliced_new['CountN']=sliced_new['Count']/sliced_new['Month'].map(days_in_month)

#Plot the Heatmap
sns.heatmap(sliced_new.pivot("Hour", "Month", "CountN"), annot=False, cmap="BuPu")
####################################################################


#HEATMAP by DAY 2016################################################
# Getting unique values after grouping by hour and DAY FOR 2016
sliced_new16 = sliced_2016[sliced_2016["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new16 = sliced_new16.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new16.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
####################################################################

#HEATMAP By MONTH AND YEAR #########################################
# Getting unique values after grouping by MONTH AND YEAR
sliced_newY = sliced[sliced["Month"] >= 1].groupby(["Month", "Year"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newY = sliced_newY.reset_index(name="Count")

sliced_newY['Month'].map(days_in_month)
sliced_newY['CountN']=sliced_newY['Count']/sliced_newY['Month'].map(days_in_month)
#Plot the Heatmap
sns.heatmap(sliced_newY.pivot("Month", "Year", "CountN"), annot=False, cmap="BuPu")
####################################################################

#HEATMAP BY HOUR  AND DAY 2017 ########################################
# Getting unique values after grouping by hour and DAY FOR 2017
sliced_new17 = sliced_2017[sliced_2017["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new17 = sliced_new17.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new17.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
#######################################################################


#NOT WORKING -----------------------#HEATMAP BY HOUR AND DAY###############################################
# Getting unique values after grouping by hour and DAY 
sliced_newM = sliced[sliced["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newM = sliced.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_newM.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################

#HEATMAP BY HOUR AND DAY----NO MIDNIGHT ################################
# Getting unique values after grouping by hour and DAY no hour 0
sliced_new0223 = sliced_0223[sliced_0223["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new0223 = sliced_new0223.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new0223.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################


#HEATMAP by HOUR AND DAY ---    NO FEB29 ###############################
# Getting unique values after grouping by hour and DAY no hour 0 no feb29
sliced_new29 = sliced_29[sliced_29["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new29 = sliced_new29.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new29.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################
#sns_plot.savefig("output1.png")


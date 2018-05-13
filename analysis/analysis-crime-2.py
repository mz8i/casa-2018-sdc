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

# IMPORT NECESSARY PACKAGES
# IMPORT DATA
data = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv"))

data.head



# iloc[row slicing, column slicing]
sliced=data.iloc[:, :]

from matplotlib import pyplot as plt


#for time data
import datetime

date_test = "03/18/2015 07:44:00 PM"
#Read as date data
sliced['RealDate'] =  pd.to_datetime(sliced['Date'], format="%m/%d/%Y  %I:%M:%S %p")

sliced['Day'] = sliced['RealDate'].dt.day

sliced['Month'] = sliced['RealDate'].dt.month

sliced['Hour'] = sliced['RealDate'].dt.hour

sliced['Year']=sliced['RealDate'].dt.year

sliced['Crime1'] = 1

#Histogram
plt.hist(sliced['Hour'])

sliced['tesdate'] = sliced['Month'].apply(str).str.zfill(2) +"."+ sliced['Day'].apply(str).str.zfill(2)
#transform into datetime
sliced['MD'] =  pd.to_datetime(sliced['tesdate'], format="%m.%d")

#Subsetting for Each year
sliced_2015=sliced[sliced.Year == 2015]
sliced_2016=sliced[sliced.Year == 2016]
sliced_2017=sliced[sliced.Year == 2017]

#THEFT####################################################################
sliced_Theft2017=sliced_2017[sliced_2017["Primary Type"] == "THEFT"]
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
sliced_2015["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")
sliced_2016["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")
sliced_2017["Primary Type"].value_counts().plot(kind="pie",autopct="%.2f")

#Exported CSV per year
export_2016=sliced[sliced.Year == 2016]
export_2017=sliced[sliced.Year == 2017]

#export_2016.to_csv("D:/Dropbox/Cloud - Master's - Docs/Spatial Data Capture, Storage and Analysis/Data Project/City-Crime/export_2016.csv")

#export_2017.to_csv("D:/Dropbox/Cloud - Master's - Docs/Spatial Data Capture, Storage and Analysis/Data Project/City-Crime/export_2017.csv")



#CLEANING################################################################ ;
#RENAMING and grouping

sliced["Primary Type"].value_counts()
sliced.loc[sliced["Primary Type"] == "NON - CRIMINAL","Primary Type"]="NON-CRIMINAL"
sliced.loc[sliced["Primary Type"] == "NON-CRIMINAL (SUBJECT SPECIFIED)","Primary Type"]="NON-CRIMINAL"

sliced.loc[sliced["Primary Type"] == "OTHER NARCOTIC VIOLATION","Primary Type"]="NARCOTICS"


#########################################################################

#SPATIAL DATA SUBSET#####################################################
spatial_crime=sliced[sliced.Latitude.notnull()]

# let's put more analysis here

#HEATMAP##################################################################
# Getting unique values after grouping by HOUR and MONTH
sliced_new = sliced[sliced["Month"] >= 1].groupby(["Hour", "Month"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new = sliced_new.reset_index(name="Count")

#Dictionary To get right day numbers
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



#HEATMAP################################################################
# Getting unique values after grouping by hour and DAY FOR 2016
sliced_new16 = sliced_2016[sliced_2016["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new16 = sliced_new16.reset_index(name="Count")

#Plot the Heatmap
sns.heatmap(sliced_new16.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
####################################################################

###################################################################
# Getting unique values after grouping by MONTH AND YEAR
sliced_newY = sliced[sliced["Month"] >= 1].groupby(["Month", "Year"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newY = sliced_newY.reset_index(name="Count")

sliced_newY['Month'].map(days_in_month)
sliced_newY['CountN']=sliced_newY['Count']/sliced_newY['Month'].map(days_in_month)
#Plot the Heatmap
sns.heatmap(sliced_newY.pivot("Month", "Year", "CountN"), annot=False, cmap="BuPu")
####################################################################





#HEATMAP###############################################################
# Getting unique values after grouping by hour and DAY FOR 2017
sliced_new17 = sliced_2017[sliced_2017["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new17 = sliced_new17.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new17.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
#######################################################################


#HEATMAP################################################################
# Getting unique values after grouping by hour and DAY 
sliced_newM = sliced[sliced["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_newM = sliced.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_newM.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################

#HEATMAP################################################################
# Getting unique values after grouping by hour and DAY no hour 0
sliced_new0223 = sliced_0223[sliced_0223["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new0223 = sliced_new0223.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new0223.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################


#HEATMAP################################################################
# Getting unique values after grouping by hour and DAY no hour 0 no feb29
sliced_new29 = sliced_29[sliced_29["Month"] >= 1].groupby(["Hour", "tesdate"])["Crime1"].size()
# Pivot the dataframe to create a [hour x date] matrix containing counts
sliced_new29 = sliced_new29.reset_index(name="Count")
#Plot the Heatmap
sns.heatmap(sliced_new29.pivot("Hour", "tesdate", "Count"), annot=False, cmap="BuPu")
########################################################################
#sns_plot.savefig("output1.png")

list(sliced)
sliced['FBI Code'].value_counts()

#Dictionary for FBI codes
dictionary_FBI={
    '01A':'01A Homicide 1st & 2nd Degree',
    '02':'02 Criminal Sexual Assault',
    '03':'03 Robbery',
    '04A':'04A Aggravated Assault',
    '04B':'04B Aggravated Battery',
    '05':'05 Burglary',
    '06':'06 Larceny',
    '07':'07 Motor Vehicle Theft',
    '09':'09 Arson',
    '01B':'01B Involuntary Manslaughter',
    '08A':'08A Simple Assault',
    '08B':'08B Simple Battery',
    '10':'10 Forgery & Counterfeiting',
    '11':'11 Fraud',
    '12':'12 Embezzlement',
    '13':'13 Stolen Property',
    '14':'14 Vandalism',
    '15':'15 Weapons Violation',
    '16':'16 Prostitution ',
    '17':'17 Criminal Sexual Abuse',
    '18':'18 Drug Abuse',
    '19':'19 Gambling',
    '20':'20 Offenses Against Family',
    '22':'22 Liquor License',
    '24':'24 Disorderly Conduct',
    '26':'26 Misc Non-Index Offense'
}

#Dictionary for whom the crime was against
dictionary_against={
    '01A':'Persons',
    '02':'Persons',
    '03':'Property',
    '04A':'Persons',
    '04B':'Persons',
    '05':'Property',
    '06':'Property',
    '07':'Property',
    '09':'Property',
    '01B':'Persons',
    '08A':'Persons',
    '08B':'Persons',
    '10':'Property',
    '11':'Property',
    '12':'Property',
    '13':'Property',
    '14':'Property',
    '15':'Society',
    '16':'Society',
    '17':'Persons',
    '18':'Society',
    '19':'Society',
    '20':'Persons',
    '22':'Society',
    '24':'Society',
    '26':'Society'
}

#Dcitionary severity according to FBI code
dictionary_severity={
'01A':'More serious',
'02':'More serious',
'03':'More serious',
'04A':'More serious',
'04B':'More serious',
'05':'More serious',
'06':'More serious',
'07':'More serious',
'09':'More serious',
'01B':'Less Serious',
'08A':'Less Serious',
'08B':'Less Serious',
'10':'Less Serious',
'11':'Less Serious',
'12':'Less Serious',
'13':'Less Serious',
'14':'Less Serious',
'15':'Less Serious',
'16':'Less Serious',
'17':'Less Serious',
'18':'Less Serious',
'19':'Less Serious',
'20':'Less Serious',
'22':'Less Serious',
'24':'Less Serious',
'26':'Less Serious'
}
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 18:35:50 2018

@author: Nico
"""
import pandas as pd
import os
import numpy as np
#import statistics
#import datetime as dt
#from matplotlib import pyplot as plt

############DATA CLEANING######################################################

#First you need to change your current directory to the analysis directory in your computer
#os.chdir("C:/.../casa-2018-sdc/analysis")
analysis_dir = os.getcwd()
data_dir = os.path.join(analysis_dir, 'data')

## IMPORT DATA
###Crime
data = pd.read_csv(os.path.join(data_dir, "Crimes_-_2001_to_present.csv")) 
sliced=data.iloc[:, :]
##Beat population 2017
beat_pop=pd.read_csv(os.path.join(data_dir, "beat_pop.csv"))
beat_pop.index=beat_pop.beat_num
beat_pop=beat_pop['TOTAL POPULATION'].to_frame(name='Population')

#Crimes percentages for various features
beat_percentages=pd.read_csv(os.path.join(data_dir, "beatStat_2017.csv"))
beat_percentages.index=beat_percentages.Beat
beat_percentages=beat_percentages.iloc[:,2:]


#Change to datetime format and get minute, hour, day, month, year
sliced['RealDate'] =  pd.to_datetime(sliced['Date'], format="%m/%d/%Y  %I:%M:%S %p")
sliced['Minute']=sliced['RealDate'].dt.minute
sliced['Hour'] = sliced['RealDate'].dt.hour
sliced['Day'] = sliced['RealDate'].dt.day
sliced['Month'] = sliced['RealDate'].dt.month
sliced['Year']=sliced['RealDate'].dt.year

#Working only with 2017 data
sliced_2017=sliced[sliced.Year == 2017]

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
    '16':'16 Prostitution ',
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

sliced_2017['FBI Type']=sliced_2017['FBI Code'].map(dictionary_FBI)
sliced_2017.loc[:,'FBI Against']=sliced_2017.loc[:,'FBI Code'].map(dictionary_against)
sliced_2017['FBI Severity']=sliced_2017['FBI Code'].map(dictionary_severity)


#Creating Counts per beat dataset
data_beat=sliced_2017.groupby(sliced_2017.Beat)['ID'].count().to_frame(name='Counts')

#Merging Counts and population
data_beat=pd.merge(data_beat,beat_pop,how='left',left_index=True,right_index=True)

#Adding Total crimes per 1000 people living in each beat
data_beat['Total_per1000']=data_beat.Counts/data_beat.Population*1000
#There was a beat with population=0, so I change inf to nan in that beat
data_beat=data_beat.replace(np.inf,np.nan)

#Merging with other percentages (crimes during night, serious, spring, summer, autumn, winter)
data_beat=pd.merge(data_beat,beat_percentages,how='left',left_index=True,right_index=True)

#Adding Domestic crimes
data_beat['Pct_Domestic']=sliced_2017.groupby(sliced_2017.Beat)['Domestic'].sum().to_frame(name='Counts')
data_beat['Pct_Domestic']=data_beat['Pct_Domestic']/data_beat.Counts

#Adding Arrested crimes
data_beat['Pct_Arrest']=sliced_2017.groupby(sliced_2017.Beat)['Arrest'].sum().to_frame(name='Counts')
data_beat['Pct_Arrest']=data_beat['Pct_Arrest']/data_beat.Counts

#Adding types of crimes
#First we separate them in dummies
dummies_FBI_code=pd.get_dummies(sliced_2017['FBI Code'])
#Add 'Beat' column to group the values by beat
dummies_FBI_code['Beat']=sliced_2017.Beat
dummies_FBI_beat=dummies_FBI_code.groupby(sliced_2017.Beat).sum()
#Remove 'Beat' column
dummies_FBI_beat=dummies_FBI_beat.iloc[:,:-1]
#Divide by Count of crimes per beat, to get percentages
dummies_FBI_beat=dummies_FBI_beat.div(data_beat.Counts,axis=0)
#Merging with data_beat
data_beat=pd.merge(data_beat,dummies_FBI_beat,how='left',left_index=True,right_index=True)

#Dictionary for reducing Locations to 17 categories (only for 2107)
dictionary_Locations={
'VACANT LOT/LAND':'L_const',
'CONSTRUCTION SITE':'L_const',
'ABANDONED BUILDING':'L_const',
'AIRPORT TERMINAL UPPER LEVEL - SECURE AREA':'L_airp',
'AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA':'L_airp',
'AIRPORT VENDING ESTABLISHMENT':'L_airp',
'AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA':'L_airp',
'AIRPORT EXTERIOR - NON-SECURE AREA':'L_airp',
'AIRPORT PARKING LOT':'L_airp',
'AIRPORT BUILDING NON-TERMINAL - SECURE AREA':'L_airp',
'AIRPORT TERMINAL UPPER LEVEL - NON-SECURE AREA':'L_airp',
'AIRCRAFT':'L_airp',
'AIRPORT/AIRCRAFT':'L_airp',
'AIRPORT TERMINAL LOWER LEVEL - SECURE AREA':'L_airp',
'AIRPORT EXTERIOR - SECURE AREA':'L_airp',
'AIRPORT TERMINAL MEZZANINE - NON-SECURE AREA':'L_airp',
'AIRPORT TRANSPORTATION SYSTEM (ATS)':'L_airp',
'APARTMENT':'L_apart',
'CHA APARTMENT':'L_apart',
'CHA HALLWAY/STAIRWELL/ELEVATOR':'L_apart',
'BANK':'L_bank',
'ATM (AUTOMATIC TELLER MACHINE)':'L_bank',
'CURRENCY EXCHANGE':'L_bank',
'CREDIT UNION':'L_bank',
'SAVINGS AND LOAN':'L_bank',
'TAVERN':'L_lesr',
'BAR OR TAVERN':'L_lesr',
'CLUB':'L_lesr',
'TAVERN/LIQUOR STORE':'L_lesr',
'COMMERCIAL / BUSINESS OFFICE':'L_offic',
'GAS STATION DRIVE/PROP.':'L_gas',
'GAS STATION':'L_gas',
'NURSING HOME/RETIREMENT HOME':'L_HEP',
'MEDICAL/DENTAL OFFICE':'L_HEP',
'SCHOOL, PUBLIC, BUILDING':'L_HEP',
'HOSPITAL BUILDING/GROUNDS':'L_HEP',
'SCHOOL, PUBLIC, GROUNDS':'L_HEP',
'GOVERNMENT BUILDING/PROPERTY':'L_HEP',
'ATHLETIC CLUB':'L_HEP',
'SCHOOL, PRIVATE, BUILDING':'L_HEP',
'LIBRARY':'L_HEP',
'SPORTS ARENA/STADIUM':'L_HEP',
'SCHOOL, PRIVATE, GROUNDS':'L_HEP',
'DAY CARE CENTER':'L_HEP',
'COLLEGE/UNIVERSITY GROUNDS':'L_HEP',
'POOL ROOM':'L_HEP',
'ANIMAL HOSPITAL':'L_HEP',
'COLLEGE/UNIVERSITY RESIDENCE HALL':'L_HEP',
'FIRE STATION':'L_HEP',
'FEDERAL BUILDING':'L_HEP',
'CEMETARY':'L_HEP',
'CHURCH':'L_HEP',
'SCHOOL YARD':'L_HEP',
'NURSING HOME':'L_HEP',
'CHURCH/SYNAGOGUE/PLACE OF WORSHIP':'L_HEP',
'HOTEL/MOTEL':'L_hotel',
'CTA STATION':'L_mob',
'CTA BUS':'L_mob',
'CTA PLATFORM':'L_mob',
'CTA BUS STOP':'L_mob',
'TAXICAB':'L_mob',
'VEHICLE-COMMERCIAL':'L_mob',
'CTA GARAGE / OTHER PROPERTY':'L_mob',
'OTHER RAILROAD PROP / TRAIN DEPOT':'L_mob',
'VEHICLE - OTHER RIDE SERVICE':'L_mob',
'OTHER COMMERCIAL TRANSPORTATION':'L_mob',
'CAR WASH':'L_mob',
'AUTO':'L_mob',
'BOAT/WATERCRAFT':'L_mob',
'CTA TRACKS - RIGHT OF WAY':'L_mob',
'VEHICLE - DELIVERY TRUCK':'L_mob',
'AUTO / BOAT / RV DEALERSHIP':'L_mob',
'VEHICLE - OTHER RIDE SHARE SERVICE (E.G., UBER, LYFT)':'L_mob',
'CTA PROPERTY':'L_mob',
'CTA "L" PLATFORM':'L_mob',
'VEHICLE NON-COMMERCIAL':'L_mob',
'CTA TRAIN':'L_mob',
'COIN OPERATED MACHINE':'L_other',
'OTHER':'L_other',
'STAIRWELL':'L_other',
'ROOMING HOUSE':'L_other',
'VESTIBULE':'L_other',
'CHA HALLWAY':'L_other',
'LAKEFRONT/WATERFRONT/RIVERBANK':'L_green',
'FOREST PRESERVE':'L_green',
'RIVER BANK':'L_green',
'PARK PROPERTY':'L_green',
'PARKING LOT/GARAGE(NON.RESID.)':'L_park',
'CHA PARKING LOT/GROUNDS':'L_park',
'PARKING LOT':'L_park',
'CHA PARKING LOT':'L_park',
'VACANT LOT':'L_park',
'POLICE FACILITY/VEH PARKING LOT':'L_polic',
'JAIL / LOCK-UP FACILITY':'L_polic',
'RESIDENCE':'L_res',
'RESIDENTIAL YARD (FRONT/BACK)':'L_res',
'RESIDENCE PORCH/HALLWAY':'L_res',
'RESIDENCE-GARAGE':'L_res',
'DRIVEWAY - RESIDENTIAL':'L_res',
'PORCH':'L_res',
'HOUSE':'L_res',
'YARD':'L_res',
'GARAGE':'L_res',
'BASEMENT':'L_res',
'MOVIE HOUSE/THEATER':'L_lesr',
'BOWLING ALLEY':'L_lesr',
'RESTAURANT':'L_lesr',
'SMALL RETAIL STORE':'L_store',
'DEPARTMENT STORE':'L_store',
'GROCERY FOOD STORE':'L_store',
'CONVENIENCE STORE':'L_store',
'DRUG STORE':'L_store',
'WAREHOUSE':'L_const',
'APPLIANCE STORE':'L_store',
'CLEANING STORE':'L_store',
'PAWN SHOP':'L_store',
'NEWSSTAND':'L_store',
'RETAIL STORE':'L_store',
'BARBERSHOP':'L_store',
'SIDEWALK':'L_strt',
'DRIVEWAY':'L_strt',
'STREET':'L_strt',
'ALLEY':'L_strt',
'HIGHWAY/EXPRESSWAY':'L_strt',
'BRIDGE':'L_strt',
'HALLWAY':'L_strt',
'GANGWAY':'L_strt',
'FACTORY/MANUFACTURING BUILDING':'L_const'      
}

#Mapping Locations in crime dataset
sliced_2017['Locations_17']=sliced_2017['Location Description'].map(dictionary_Locations)

#Adding Crimes Locations
#First we separate them in dummies
dummies_Locations=pd.get_dummies(sliced_2017['Locations_17'])
#Add 'Beat' column to group the values by beat
dummies_Locations['Beat']=sliced_2017.Beat
dummies_Locations=dummies_Locations.groupby(sliced_2017.Beat).sum()
#Remove 'Beat' column
dummies_Locations=dummies_Locations.iloc[:,:-1]
#Divide by Count of crimes per beat, to get percentages
dummies_Locations=dummies_Locations.div(data_beat.Counts,axis=0)
#Merging with data_beat
data_beat=pd.merge(data_beat,dummies_Locations,how='left',left_index=True,right_index=True)
#Data_beat without columns: 'crimes count'
data_beat_X=data_beat.iloc[:,1:]

#Save data in csv (for not running the whole data cleaning)
data_beat_X.to_csv(os.path.join(data_dir, "Data_beats.csv"))

#PCA Analysis


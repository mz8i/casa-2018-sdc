# -*- coding: utf-8 -*-
"""
Created on Thu May 17 18:35:50 2018

@author: Nico
"""
##################INCLUDES:####################################################
#0.-Importing Packages
#1.-DATA CLEANING
#2.-Scatter Matrix
#3.-Scaling dataset
#4.-Performing PCA
##4.1.-Biplot (can be used with without coloring points by clusters)
##4.2.-PCA without Serious Crimes
#5.-ClUSTERING ANALYSIS
##5.1.-DBSCAN
##5.2.-Running Agglomerative (Hierarchical) Clustering with Silhouette analysis
##5.3.-Silhouette Analysis can be used with KMeans as well by uncommenting + Plot
##5.3.-Affinity propagation clustering + Plot
###############################################################################


################ 0.- Importing Packages #######################################
from __future__ import print_function#Used in Silhoutte analysis chunk

import pandas as pd
import os
import numpy as np
#import statistics
#import datetime as dt
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

#Silhoutte analysis chunk
#from sklearn.datasets import make_blobs
#from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering as agglom
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
from itertools import cycle


############### 1.- DATA CLEANING #############################################

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


#Beats with calls data
data_calls= pd.read_csv(os.path.join(data_dir, "beat_calls.csv"),index_col=0)
data_calls.rename(columns={"Calls_Alley":"C_Alley","Time_Alleys":"TC_Alley","Calls_All_Out":"C_Two","Time_All_Out":"TC_Two","Calls_One_Out":"C_One","Time_One_Out":"TC_One"},inplace=True)
#Merging with data_beat
data_beat_X=pd.merge(data_beat_X,data_calls,how='left',left_index=True,right_index=True)
#Changing Counts of calls for calls per 1000 inhabitants
data_beat_X.C_Alley=data_beat_X.C_Alley/data_beat_X.Population*1000
data_beat_X.C_Two=data_beat_X.C_Two/data_beat_X.Population*1000
data_beat_X.C_One=data_beat_X.C_One/data_beat_X.Population*1000

#Beats with transport data
data_transport= pd.read_csv(os.path.join(data_dir, "beat_transport.csv"),index_col=0)
data_transport.rename(columns={"bus_Stations":"T_BusS","Routes_Bus":"T_BusR","Rail_Stations":"T_RailS","Routes_Rail":"T_RailR"},inplace=True)
#Merging with data_beat
data_beat_X=pd.merge(data_beat_X,data_transport,how='left',left_index=True,right_index=True)
data_beat_X.T_BusS=data_beat_X.T_BusS/data_beat_X.Population*1000
data_beat_X.T_RailS=data_beat_X.T_RailS/data_beat_X.Population*1000
#Replacing nan with zeros
data_beat_X.T_BusS.fillna(0,inplace=True)
data_beat_X.T_BusR.fillna(0,inplace=True)
data_beat_X.T_RailS.fillna(0,inplace=True)
data_beat_X.T_RailR.fillna(0,inplace=True)


#Save data in csv (for not running the whole data cleaning)
#data_beat_X.to_csv(os.path.join(data_dir, "Data_beats.csv"))

#####Calls data
#Importing data (not neccesary if you are running all of the above code)
#beats with 59 variables
data_beat_X = pd.read_csv(os.path.join(data_dir, "Data_beats.csv"),index_col=0) 

#Replacing na and inf values for 0
data_beat_X=data_beat_X.replace(np.inf,0)
data_beat_X.fillna(0,inplace=True)

#Data without Pct_Serious
data_wout_Serious=data_beat_X.drop(labels='Pct_Serious',axis=1)

################## 2.- Scatter Matrix##########################################
def scatter_features(data): 
    axs=pd.plotting.scatter_matrix(data, alpha=0.2, figsize=(12, 12), diagonal='kde')
    n = len(data.columns)
    for x in range(n):
        for y in range(n):
            # to get the axis of subplots
            ax = axs[x, y]
            # to make x axis name vertical  
            ax.xaxis.label.set_rotation(90)
            # to make y axis name horizontal 
            ax.yaxis.label.set_rotation(0)
            # to make sure y axis names are outside the plot area
            ax.yaxis.labelpad = 50 

#Scatter for first 10 columns
scatter_features(data_beat_X.iloc[:,0:10])
#Saving figure
plt.savefig(os.path.join(data_dir,"Scatter.png"),bbox_inches='tight')

#Scatter for types of crimes
scatter_features(data_beat_X.iloc[:,10:36])

#Scatter for locations of crimes
scatter_features(data_beat_X.iloc[:,36:53])

#Scatter for Transport and calls
scatter_features(data_beat_X.iloc[:,53:])

################### 3.- Scaling dataset########################################
import sklearn.preprocessing as preprocessing

data_scaled=pd.DataFrame(preprocessing.scale(data_beat_X),index=data_beat_X.index,columns=list(data_beat_X))
#Other way to scale data
data_std = preprocessing.StandardScaler().fit_transform(data_beat_X)

#Scale dataset without Serious crimes
data_std_woutS = preprocessing.StandardScaler().fit_transform(data_wout_Serious)

################## 4.- Perform PCA#############################################
from sklearn.decomposition import PCA as sklearnPCA
#sklearn_pca = sklearnPCA(n_components=4)
sklearn_pca = sklearnPCA()
#Saving observations projected into PC1,PC2,PC3 (scores)
Y_sklearn = sklearn_pca.fit_transform(data_std)
Y_sklearn=pd.DataFrame(Y_sklearn,index=data_beat_X.index,columns=['PC' + str(number) for number in list(range(1,Y_sklearn.shape[1]+1))])

#Getting loadings for the first 3 components
loadings=pd.DataFrame(sklearn_pca.components_,index=['PC' + str(number) for number in list(range(1,Y_sklearn.shape[1]+1))],columns=list(data_beat_X))
loadings=loadings.T

#Plotting first two scores
plt.scatter(Y_sklearn.iloc[:,0],Y_sklearn.iloc[:,1])
#Saving scores
Y_sklearn.iloc[:,0:3].to_csv(os.path.join(data_dir, "Y_sklearn.csv"))


######### 4.1.- Biplot #############
def biplot(score,coeff,pcax,pcay,labels=None,color_clusters=None):
    pca1=pcax-1
    pca2=pcay-1
    xs = score[:,pca1]
    ys = score[:,pca2]
    n=score.shape[1]
    scalex = 1.0/(xs.max()- xs.min())
    scaley = 1.0/(ys.max()- ys.min())
    
    if color_clusters is None:
        plt.scatter(xs*scalex,ys*scaley)
    else:
        plt.scatter(xs*scalex,ys*scaley,c=color_clusters,cmap='Dark2', 
                    alpha=0.9)
        #plt.scatter(xs*scalex,ys*scaley,c=color_clusters,cmap='Dark2', marker='.', 
        #            s=30, lw=0, alpha=0.7, edgecolor='k')
    #Adding color
    #plt.scatter(xs*scalex,ys*scaley,c=clusters)
    for i in range(n):
        plt.arrow(0, 0, coeff[i,pca1], coeff[i,pca2],color='r',alpha=0.5) 
        if labels is None:
            plt.text(coeff[i,pca1]* 1.15, coeff[i,pca2] * 1.15, "Var"+str(i+1), color='g', ha='center', va='center')
        else:
            plt.text(coeff[i,pca1]* 1.15, coeff[i,pca2] * 1.15, labels[i], color='g', ha='center', va='center')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("PC{}".format(pcax))
    plt.ylabel("PC{}".format(pcay))
    plt.grid()
    

#We can plot 2d biplots for the 3 pairs of PC
#PC1 vs PC2
biplot(sklearn_pca.fit_transform(data_std),np.transpose(sklearn_pca.components_),1,2,labels=list(data_beat_X))
#PC1 vs PC3
biplot(sklearn_pca.fit_transform(data_std),np.transpose(sklearn_pca.components_),1,3,labels=list(data_beat_X))
#PC2 vs PC3
biplot(sklearn_pca.fit_transform(data_std),np.transpose(sklearn_pca.components_),2,3,labels=list(data_beat_X))

########### 4.2.- PCA without Serious Crimes ###########
pca_woutS = sklearnPCA()
#Saving observations projected into PC1,PC2,PC3 (scores)
Y_sklearn_woutS_numpy = pca_woutS.fit_transform(data_std_woutS)
Y_sklearn_woutS=pd.DataFrame(Y_sklearn_woutS_numpy,index=data_wout_Serious.index,columns=['PC' + str(number) for number in list(range(1,Y_sklearn_woutS_numpy.shape[1]+1))])

#Percentage of Variance explained by PComponents
variance_woutS=pca_woutS.explained_variance_ratio_ 
variance_woutS[0:3]
sum(variance_woutS[0:3])

#Getting loadings for the first 3 components
loadings_woutS=pd.DataFrame(pca_woutS.components_,index=['PC' + str(number) for number in list(range(1,Y_sklearn_woutS.shape[1]+1))],columns=list(data_wout_Serious))
loadings_woutS=loadings_woutS.T

#Saving scores
Y_sklearn_woutS.iloc[:,0:3].to_csv(os.path.join(data_dir, "Y_sklearn_woutS.csv"))


##################### 5.- CLUSTERING ANALYSIS##################################

###### 5.1.- Running DBSCAN #######
#Choosing eps parameter
#from sklearn.neighbors import NearestNeighbors
nbrs = NearestNeighbors(n_neighbors=4).fit(Y_sklearn_woutS.iloc[:,0:3])
distances, indices = nbrs.kneighbors(Y_sklearn_woutS.iloc[:,0:3])
#print(distances.shape)
#print(type(distances[:,3]))
distances_ordered=np.sort(distances[:,3])#sorting in ascending order
#distances_ordered=-np.sort(-distances[:,4])#sorting in descending order
#Plotting distances of the 4th nearest neighbours to choose eps (look for a knee)
plt.plot(distances_ordered)
plt.axhline(y=1.3, color='r', linestyle='--')

#from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=4) # create DBSCAN cluster object
dbscan.fit(Y_sklearn_woutS.iloc[:,0:3]) # run the .fit() function on the scaled dataset
dbscan_labels = dbscan.labels_


#### 5.2.- Running Agglomerative (Hierarchical) Clustering #####
########## with Silhouette analysis #########################

#from __future__ import print_function

#from sklearn.datasets import make_blobs
#from sklearn.cluster import KMeans
#from sklearn.metrics import silhouette_samples, silhouette_score

#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import numpy as np

X=Y_sklearn_woutS_numpy[:,0:3]

range_n_clusters = list(range(7,8))#range(2,11) or [2, 3, 4, 5, 6, 7, 8, 9, 10]

for n_clusters in range_n_clusters:
    # Create a subplot with 1 row and 2 columns
    fig, ((ax1,ax5,ax6), (ax2,ax3,ax4)) = plt.subplots(2, 3)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    #clusterer = KMeans(n_clusters=n_clusters, random_state=10) #using KMeans
    clusterer = agglom(n_clusters=n_clusters) #using agglomerative
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    y_lower = 10
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    #for i in range(n_clusters):
    for i, color in zip(range(n_clusters), colors):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        #color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')
    ###Only with KMeans##################################
    ## Labeling the clusters
    #centers = clusterer.cluster_centers_
    ## Draw white circles at cluster centers
    #ax2.scatter(centers[:, 0], centers[:, 1], marker='o',
    #            c="white", alpha=1, s=200, edgecolor='k')
    #
    #for i, c in enumerate(centers):
    #    ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
    #                s=50, edgecolor='k')
    ###End of the only KMeans part#######################

    ax2.set_title("The visualization of the clustered data.")
    ax2.set_xlabel("Feature space for the 1st feature")
    ax2.set_ylabel("Feature space for the 2nd feature")
    
    # 3rd Plot showing the actual clusters formed
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax3.scatter(X[:, 0], X[:, 2], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')
    ax3.set_title("The visualization of the clustered data.")
    ax3.set_xlabel("Feature space for the 1st feature")
    ax3.set_ylabel("Feature space for the 3rd feature")

    # 4th Plot showing the actual clusters formed
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax4.scatter(X[:, 1], X[:, 2], marker='.', s=30, lw=0, alpha=0.7,
                c=colors, edgecolor='k')
    ax4.set_title("The visualization of the clustered data.")
    ax4.set_xlabel("Feature space for the 2nd feature")
    ax4.set_ylabel("Feature space for the 3rd feature")

    plt.suptitle(("Silhouette analysis for Agglomerative clustering on sample data "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')
    
#Saving results for k=7
agglomerative=agglom(n_clusters=7)
agglomerative.fit(X)
agglomerative_labels = agglomerative.labels_

#a=len(np.unique(agglomerative_labels))
#b=len(np.unique(affinity_labels))

########## 5.3.- Affinity propagation clustering#######
########## (8 clusters)################################

from sklearn.cluster import AffinityPropagation
#affinity=AffinityPropagation(preference=-50)
affinity=AffinityPropagation(damping=0.7,preference=-200)
affinity.fit(X) # run the .fit() function on the scaled dataset
affinity_labels = affinity.labels_
cluster_centers_indices = affinity.cluster_centers_indices_
n_clusters_ = len(cluster_centers_indices)
print(n_clusters_)
unique, counts = np.unique(affinity_labels, return_counts=True)
print (np.asarray((unique, counts)).T)

# Plot result
#from itertools import cycle
#plt.close('all')
plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
#color_list = plt.cm.Dark2(np.linspace(0, 1, 8))
#color_list=color_list[:,:3]
for k, col in zip(range(n_clusters_), colors):
    class_members = affinity_labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + '.')#Change between 0,1,2
    #plt.scatter(X[class_members, 0], X[class_members, 1], tuple(color_list[k]))#Change between 0,1,2
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,#Change between 0,1,2
    #plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=tuple(color_list[k]),#Change between 0,1,2
             markeredgecolor='k', markersize=10)
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)#Change between 0,1,2
plt.title('Estimated number of clusters: %d' % n_clusters_)

#Scatterplots
#plt.figure(2)
#plt.scatter(X[:, 0], X[:, 2],c=affinity_labels) #Change between 0,1,2
#plt.scatter(X[:, 0], X[:, 1],c=affinity_labels,cmap='winter')      

#We can plot 2d biplots for the 3 pairs od PC with colors
#PC1 vs PC2
plt.figure(13)
biplot(Y_sklearn_woutS_numpy,np.transpose(pca_woutS.components_),1,2,labels=list(data_wout_Serious),color_clusters=affinity_labels)
#PC1 vs PC3
plt.figure(14)
biplot(Y_sklearn_woutS_numpy,np.transpose(pca_woutS.components_),1,3,labels=list(data_wout_Serious),color_clusters=affinity_labels)
#PC2 vs PC3
plt.figure(15)
biplot(Y_sklearn_woutS_numpy,np.transpose(pca_woutS.components_),2,3,labels=list(data_wout_Serious),color_clusters=affinity_labels)

#######Saving beats clustered by Agglomerative/Hierarchical Method and Affinity Propagation
data_clusters=data_wout_Serious
data_clusters['Agglomerative']=agglomerative_labels
data_clusters['Affinity']=affinity_labels
data_clusters=data_clusters.iloc[:,-2:]
data_clusters.to_csv(os.path.join(data_dir,'data_clusters.csv'))
data_clusters.Affinity.value_counts()
data_clusters.Agglomerative.value_counts()

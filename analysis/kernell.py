# -*- coding: utf-8 -*-
"""
Created on Mon May 14 20:11:33 2018

@author: josen
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_species_distributions
from sklearn.datasets.species_distributions import construct_grids
from sklearn.neighbors import KernelDensity
import pandas as pd

# if basemap is available, we'll use it.
# otherwise, we'll improvise later...
try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False

# Get matrices/arrays of species IDs and locations
data = fetch_species_distributions()
species_names = ['Bradypus Variegatus', 'Microryzomys Minutus']

Xtrain = np.vstack([data['train']['dd lat'],
                    data['train']['dd long']]).T
ytrain = np.array([d.decode('ascii').startswith('micro')
                  for d in data['train']['species']], dtype='int')
Xtrain *= np.pi / 180.  # Convert lat/long to radians


crimes = pd.read_csv('C:/Users/josen/Documents/2nd Term UCL/Spatial Data Capture/Final Project/export_spatial_theft_2017.csv')
crimes_day=crimes[crimes.tesdate == 9.06]
XTrain= crimes[['Longitude','Latitude']]
XTrain=XTrain.values
XTrain*=np.pi/180

# Set up the data grid for the contour plot
x = np.linspace(-88., -87.)
y = np.linspace(41.5, 42.5)
X, Y = np.meshgrid(x, y)

xy = np.vstack([Y.ravel(), X.ravel()]).T

# Plot map of South America with distributions of each species
fig = plt.figure()
fig.subplots_adjust(left=0.05, right=0.95, wspace=0.05)

for i in range(1):
    plt.subplot(1, 2, i + 1)

    # construct a kernel density estimate of the distribution
    print(" - computing KDE in spherical coordinates")
    kde = KernelDensity(bandwidth=0.1, metric='haversine',
                        kernel='gaussian', algorithm='ball_tree')
    kde.fit(Xtrain)

    # evaluate only on the land: -9999 indicates ocean

    Z = np.exp(kde.score_samples(xy))
    Z = Z.reshape(X.shape)

    # plot contours of the density
    levels = np.linspace(0, Z.max(), 25)
    plt.contourf(X, Y, Z, levels=levels, cmap=plt.cm.Reds)

    if basemap:
        print(" - plot coastlines using basemap")
        m = Basemap(projection='cyl', llcrnrlat=Y.min(),
                    urcrnrlat=Y.max(), llcrnrlon=X.min(),
                    urcrnrlon=X.max(), resolution='c')
        m.drawcoastlines()
        m.drawcountries()
    else:
        print(" - plot coastlines from coverage")
        plt.contour(X, Y,
                    levels=[-9999], colors="k",
                    linestyles="solid")
        plt.xticks([X])
        plt.yticks([Y])

    plt.title(species_names[i])


plt.show()
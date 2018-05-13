# -*- coding: utf-8 -*-
"""
Created on Sun May 13 20:56:30 2018

@author: julian
"""

##API for SUNLIGHT in CHICAGO

import requests
import pandas as pd

from datetime import date

#Most requests are made up of three parts - the requested endpoint, the required (and optional, if using) parameters, and authentication details. We're going to use the Requests library to sort this out. Let's break this down.

#First, we define the endpoint, this is a simple web address, with parameters beginning from a question mark...

def get_sunlight_for_date(d):
        endpoint = 'https://api.sunrise-sunset.org/json'
        params = {
                'lat': 41.8781, 
                'lng': -87.6298,
                'date': d.isoformat(),
                'formatted': 0
        }

        r = requests.get(endpoint, params=params)

        if r.status_code == 200:
                return r.json()['results']
        raise ValueError('The API request was not successful')

start_date = date(2017, 12, 25)
end_date = date(2017,12,31)

api_results = []
date_range = pd.date_range(start_date, end_date)
date_range_n = len(date_range)
    
for ind, d in enumerate(date_range):
    print("Running request {} of {}...".format(ind+1, date_range_n))
    api_results.append(get_sunlight_for_date(d))
    
sunlight_df = pd.DataFrame(api_results)
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 20:56:30 2018

@author: julian
"""

##API for SUNLIGHT in CHICAGO

import requests
import pandas as pd

#Most requests are made up of three parts - the requested endpoint, the required (and optional, if using) parameters, and authentication details. We're going to use the Requests library to sort this out. Let's break this down.

#First, we define the endpoint, this is a simple web address, with parameters beginning from a question mark...

endpoint = 'https://api.sunrise-sunset.org/json'

#Next, we set up some parameters, which are sent as Python dictionary. Certain parameters are required for each API, and it's your job to figure out what is required. This time I've written this one out for you. In this case, we're going to extract the keywords within a website.

params = {
        'lat': 41.8781, 
        'lng': -87.6298,
        'date': '2017-02-08',
        'formatted': 0
        }

r = requests.get(endpoint, params=params)

#Now check out the response below. Here, the code will tell you different things. Success = 200, Failure = 400+. Good old Wikipedia has a breakdown of the codes here, which can help you identify any problems with your request. You can also add .json() to the request to get the full response.

r.status_code

#The response allows us to assess whether we should continue with the processing of the data. So providing you received a response 200 you can continue with checking out the json data returned. The command below extracts the json element of the response.

r.json()

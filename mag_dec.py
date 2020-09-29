#-------------------------------------------------------------------------------
# Name:        mag_dec.py
# Purpose:      return magnetic deviation and change
#
# Author:      kimo
#
# Created:     20/05/2020
# Copyright:   (c) kimo 2020
# Licence:     Creative Commons 4.0 New Zealand
#-------------------------------------------------------------------------------


from __future__ import print_function
import sys
import os
import requests
import json
import math
# import arcpy

def get_declination(longitude,latitude, date):
    """ call british geological survey API"""
    url2 = "http://geomag.bgs.ac.uk/web_service/GMModels/wmm/2020/?latitude={}&longitude={}&date={}&format=json".format(
        latitude, longitude,  date)
    result = json.loads(requests.get(url2).content)
    # print(result)
    dec = result['geomagnetic-field-model-result']['field-value']['declination']
    change = result['geomagnetic-field-model-result']['secular-variation']['declination']
    return dec, change
try:
    longitude = float(sys.argv[1])
    latitude = float(sys.argv[2])
except:
    longitude = 174.5
    latitude = -36.5
date = '2020-05-25'
result = get_declination(longitude, latitude, date)
print(longitude, latitude, date, result[0]['value'],result[0]['units'], result[1]['value'], result[1]['units'])

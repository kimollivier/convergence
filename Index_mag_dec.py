# -------------------------------------------------------------------------------
# Name:        mag_dec.py
# Purpose:      return magnetic deviation and change
#               great idea but a very limited service
#               have to restart if too fast, so need to
#               store successful values to avoid repeating
# Author:      kimo
#
# Created:     20/05/2020
# Copyright:   (c) kimo 2020
# Licence:     Creative Commons 4.0 New Zealand
# -------------------------------------------------------------------------------
from __future__ import print_function
import sys
import os
import requests
import json
import time
import arcpy
import sqlite3


def get_declination(longitude, latitude, date):
    """ call british geological survey API very slowly"""
    url2 = "http://geomag.bgs.ac.uk/web_service/GMModels/wmm/2020/?latitude={}&longitude={}&date={}&format=json".format(
        latitude, longitude,  date)
    result = json.loads(requests.get(url2).content)
    # print(result)
    dec = result['geomagnetic-field-model-result']['field-value']['declination']
    change = result['geomagnetic-field-model-result']['secular-variation']['declination']
    return dec, change


def test():
    """ test for Auckland
    174.5 -36.5 2020-09-25 19.681 deg (east) 5.3 arcmin/y (east)
    """
    longitude = 174.5
    latitude = -36.5
    date = '2020-09-25'
    result = get_declination(longitude, latitude, date)
    print(longitude, latitude, date,
          result[0]['value'], result[0]['units'], result[1]['value'], result[1]['units'])


if __name__ == "__main__":
    drive = sys.argv[0][0]
    ws = '{}:/teararoa/nz/current.gdb'.format(drive)
    home = os.path.dirname(ws)
    if not arcpy.Exists(ws):
        raise IOError
    arcpy.env.workspace = ws
    wgs84 = arcpy.SpatialReference(4326)
    date = '2020-09-16'
    index = 'squareindex'

    # get a dict of centroid long/lat values
    dCentroid = {row[0]: row[1] for row in arcpy.da.SearchCursor(
        index, ['PageName', 'SHAPE@XY'], spatial_reference=wgs84)}
    # put into a database to keep records
    # then restart rest API to fill in the values
    conn = sqlite3.connect("{}/mag.sqlite".format(home))
    conn.execute("""CREATE TABLE IF NOT EXISTS magnetic (
        map text(16),
        magdate text(20),
        longitude double,
        latitude double,
        declination double,
        decunits text(20),
        variation double,
        rate_units text(20)
        ) """)

    for map in dCentroid.keys():
        map_found = conn.execute(
            """SELECT map from magnetic WHERE map = '{}' """.format(map)).fetchone()
        if not map_found:
            # print(map, dCentroid[map][0], dCentroid[map][1], date)
            result = get_declination(
                dCentroid[map][0], dCentroid[map][1], date)
            sql = """INSERT INTO magnetic VALUES ('{}',{},{},{},{},'{}',{},'{}')""".format(
                map,
                date,
                dCentroid[map][0],
                dCentroid[map][1],
                result[0]['value'],
                result[0]['units'],
                result[1]['value'],
                result[1]['units'])
            ok = conn.execute(sql)
            conn.commit()
            time.sleep(2)  # needed for rate limiting on website
            line = "{},{},{},{},{},{},{},{}".format(
                map, date, dCentroid[map][0], dCentroid[map][1], result[0]['value'], result[0]['units'], result[1]['value'], result[1]['units'])
            print(line)
        else:
            print(map, "done already")
    conn.close()
    print("finished download? If not re-run until all are done")
    # update squareindex from local sqlite database
    conn = sqlite3.connect("{}/mag.sqlite".format(home))
    result = conn.execute(
        """SELECT map,declination from magnetic""").fetchall()
    dDec = {r[0]: r[1] for r in result}
    with arcpy.da.UpdateCursor(index, ['PageName', 'magnetic']) as cur:
        for row in cur:
            row[1] = dDec[row[0]]
            cur.updateRow(row)
    print("Done")

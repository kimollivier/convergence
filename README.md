# Meridian Convergence

It is quite hard to find a way of calculating convergence, the difference in bearing between True North and Grid North on a map.

A common diagram on the side of published maps is a compass rose with an indicator of True North and Magnetic Deviation.
Both values are needed to find the Deviation from Grid North. True North is sadly missing from the NZ Topo 50 map legend.
These tools enable you to provide the value of the difference between Grid North and True North and hence Magnetic to Grid difference.
The topo maps add the True to Grid offset to just provide a Grid to Magnetic deviation.

* Use pyproj/PROJ to get meridian_convergence.

This works for any projection but is a sledgehammer solution for Transverse Mercator or UTM

* Use the published equations from the UK Ordnance Survey 1983.

The equations are daunting but they have an example written in an early BASIC.
I have translated this to Python, only the standard math module is required.
This only supports Transverse Mercator projections, but that is a very common case.


The two methods agree closely on test coordinates. See the Wiki for more information and installation.

[Deeper explanation](http://www.threelittlemaids.co.uk/magdec/explain.html) for the UK National Grid and UTM.

## Direct Calculation method
Use my example script **transverse.py** for Transverse Mercator.

## PYPROJ method
The python module pyproj which interfaces to the PROJ tool has had a new function [get_factors()](https://pyproj4.github.io/pyproj/latest/api/proj.html#pyproj-proj-factors) added in Feb 2020.
https://github.com/pyproj4/pyproj/issues/503

This is a tiny sample script to use this new function. Small scale global maps will have convergence varying all over the map, but large scale maps (< 1:50,000) the convergence can be taken as a constant over the extent of the map unless you need survey precision where it may become a factor when using GPS technology.

```
## Example
```python
import pyproj
from pyproj import CRS

crs_nztm = CRS.from_user_input(2193)
p = pyproj.Proj(crs_nztm)
lon, lat = 178.0, -40.0
facts = p.get_factors(lon, lat)
print(p(lon, lat), facts.meridian_convergence, crs_nztm.name)
```
```
PS D:\project\geodesy> conda activate proj
PS D:\project\geodesy> & c:/ProgramData/Anaconda3/envs/proj/python.exe d:/project/geodesy/convergence.py
(2026893.3022699037, 5560253.082980049) -3.2187882335062867 NZGD2000 / New Zealand Transverse Mercator 2000
PS D:\project\geodesy> 
```

## Magnetic Deviation
The next item to obtain is the magnetic deviation. This is conveniently supplied by the BGS site with a little REST interface. The site is very rate-limited so you have to pace your requests. Even that was not enough and I get thrown out easily. In the end I built a little database in sqlite to store the results. You can just keep re-running the script until all points are retrieved. There is a sample mag_dec.py script that works for a one off and another that uses arcpy to extract some centroids of map sheets in lat/long and then save the results in an sqlite file. I have added a delay but even that is not enough for a lot of sheets.
A new script just added index_mag_dev.py works for an Esri featureclass called "SquareIndex". It stores the results in a sqlite database that can be used to calculate the deviation from Grid North. Esri tools include a convergence function.

## QGIS Plugins
There are some excellent plugins **Magnetic Declination**  and **Azimuth and Distance Calculator** that manage to extract the magnetic deviation (because the model is built-in) and convergence without a rest web service. They are not combined so you would have to separately extract the valued and add them. They also are not easy to incorporate into a script that iterates over a whole layer of index sheets. TODO: combine the two plugins and automate for a whole atlas.
Note that the WMM parameters change each year and have a 5 year prediction. The plugin I downloaded has the latest parameter file built in but the unittest has not been updated for the new values.

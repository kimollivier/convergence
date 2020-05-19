# Meridian Convergence

It is quite hard to find a way of calculating convergence, the difference in bearing between True North and Grid North on a map.

* Use pyproj/PROJ to get meridian_convergence.

This works for any projection but is a sledgehammer solution for Transverse Mercator or UTM
just use my example script transverse.py

* Use the published equations from the UK Ordnance Survey 1983.

The equations are daunting but they have an example written in and early BASIC.
I have translated this to Python. only the standard math module is required.
This only supports Transverse Mercator projections, but that is a very common case.

The two methods agree closely on test coordinates. See the Wiki for more information and installation

A common diagram on the side of published maps is a compass rose with an indicator of True North and Magnetic Deviation.
Both values are needed to find the Deviation from Grid North.

This tool enables you to provide the value of the difference between Grid North and True North.
[Deeper explanation](http://www.threelittlemaids.co.uk/magdec/explain.html) for the UK, but sadly missing from the NZ Topo 50 map legend. The convergence in NZTM varies from zero in the central meridian (173 E) and is at a maximum to the East and West of 3 degrees.

## PYPROJ method
The python module pyproj which interfaces to the PROJ tool has had a new function [get_factors()](https://pyproj4.github.io/pyproj/latest/api/proj.html#pyproj-proj-factors) added in Feb 2020.
https://github.com/pyproj4/pyproj/issues/503

This is a tiny sample script to use this new function. Small scale global maps will have convergence varying all over the map, but large scale maps (< 1:50,000) the convergence can be taken as a constant over the extent of the map unless you need survey precision where it may become a factor when using GPS technology.

I have tested it against the ArcGIS Tool [CalculateGridConvergenceAngle](https://pro.arcgis.com/en/pro-app/tool-reference/cartography/calculate-grid-convergence-angle.htm) for some sample points.
Unfortunately there is a difference in definition of convergence (from True North or to True North) so the two results have an opposite sign.

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

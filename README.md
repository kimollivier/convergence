# Meridian Convergence

Using pyproj/PROJ to get meridian_convergence

A common diagram on the side of published maps is a compass rose with an indicator of True North and Magnetic Deviation.

This tool enables you to provide the value of the difference between Grid North and True North.
[Deeper explanation](http://www.threelittlemaids.co.uk/magdec/explain.html) for the UK, but sadly missing from the NZ Topo 50 map legend. The convergence in NZTM varies from zero in the central meridian (173 E) and is at a maximum to the East and West of 3 degrees.

The python module pyproj which interfaces to the PROJ tool has had a new function get_factors() added in Feb 2020.
https://github.com/pyproj4/pyproj/issues/503

This is a tiny sample script to use this new function.

I have tested it against the ArcGIS Tool [CalculateGridConvergenceAngle](https://pro.arcgis.com/en/pro-app/tool-reference/cartography/calculate-grid-convergence-angle.htm) for some sample points.
Unfortunately there is a difference in definition of convergence so the two results have an opposite sign.

## Prerequisites:
+ PROJ 6.2+ is required
+ pyproj 2.6.1.post1 is required
+ Python 3.4+ is require

It is challenging to install PROJ on Windows 10. It requires a Wheel which must be compiled and it is a 9.4 GB download
So that requires a compiler not installed in Windows by default, just like Python.

## Install a C++ compiler
Microsoft Visual C++ 14.0 is required. 
Get it with ["Build Tools for Visual Studio":] (https://visualstudio.microsoft.com/downloads/)

I recommend that you install Microsoft VC++  compiler now that it is free and is the compiler used to build cPython.
It is required for Cython if you are going to use that later, not minwing
It is also a good idea to use a virtual environment to avoid module version incompatibility.

## Install Python and an IDE
You need python 3.x and an IDE that can handle virtual environments.
I have switched to Microsoft VSCode because of the excellent support and integration with VC++, GitHub, Python.
It does take a bit of learning, but there are good tutorials and YouTube videos available.

## Installing PROJ and pyproj
```
conda create -n proj -c conda-forge proj cython
conda activate proj
pip install pyproj==2.6.1.post1
```

<<<<<<< HEAD
# Convergence using pyproj 2.6.1.post1
# which requires PROJ6.2+
# which requires python 3.6+
# and also requires VC++ to compile PROJ
# downloaded using conda and set up a venv called proj
# 16 May 2020
# copyright Kim Ollivier Creative Commons 4.0 New Zealand
import pyproj
from pyproj import CRS

crs_nztm = CRS.from_user_input(2193)
p = pyproj.Proj(crs_nztm)
lon, lat = 178.0, -40.0 # Far East of NZ
facts = p.get_factors(lon, lat)
print(p(lon, lat), facts.meridian_convergence, crs_nztm.name)
# result
"""(2026893.3022699037, 5560253.082980049) -3.2187882335062867 NZGD2000 / New Zealand Transverse Mercator 2000"""
=======
# Convergence using pyproj 2.6.1.post1
# which requires PROJ6.2+
# which requires python 3.6+
# and also requires VC++ to compile PROJ
# downloaded using conda and set up a venv called proj
# 16 May 2020
# copyright Kim Ollivier Creative Commons 4.0 New Zealand
import pyproj
from pyproj import CRS

crs_nztm = CRS.from_user_input(2193)
p = pyproj.Proj(crs_nztm)
lon, lat = 178.0, -40.0 # Far East of NZ
facts = p.get_factors(lon, lat)
print(p(lon, lat), facts.meridian_convergence, crs_nztm.name)
# result
"""(2026893.3022699037, 5560253.082980049) -3.2187882335062867 NZGD2000 / New Zealand Transverse Mercator 2000"""
>>>>>>> d431142ba184e277a99f25ef06be83a9ad6c883b
# Note that the central meridian is 141.0 E for NZTM
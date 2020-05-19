# Transverse Mercator
# ref Ordnance Survey Information Pamphlet
# Transverse Mercator Projection Constants, Formulae and Methods March 1983
# http://www.threelittlemaids.co.uk/magdec/transverse_mercator_projection.pdf
# Appendix A subroutines in BASIC translated to Python, commented numbers are original BASIC line numbers
# Modifications
#     remove line numbers but keep as a comment for reference
#     replace GOTO with a while loop
#     BASIC syntax to python syntax eg for power ^ to **
#     make all constant variables global for functions
#     add a driver to input coordinates and call functions
#     BASIC subroutines renamed as functions
#       GOSUB260 : ArcofMeridian
#       GOSUB350 : ComputePhi
#       GOSUB460 : ComputeV
# Variables
# Where possible a variable used in the following
# routines is either the same as that used in the
# formulae or can be deduced from the suffix.
#
# No suffix= Upper Case Letter
# Suffix 1 = Lower Case Letter
# Suffix 2 = Lower Case Letter Squared
# Suffix 0 =Subscript 0 e.g. E0 =Grid Eastings of True 0rigin.
#
# J3-J9 are used for intermediate values.
#
# The variables not covered by the above rules are listed below:
# K = Phi (Latitude) or Phi'
# L = Lambda (Longitude)
# R = Rho (Radius of Curvature in Meridian)
# V = Nu (Radius of Curvature in Prime Vertical)
# H2 = Eta Squared (Nu/Rho - 1)
# K3 = Phi2 - Phi1 (Difference Latitude)
# K4 = Phi2 + Phi1 (Sum Latitudes)
# Ga, Gb = (t - T) at line terminals A and B
# All angular arguments are in Radians
#
# Kim Ollivier 17 May 2020
import sys
import math
from math import sin, cos, tan, sqrt
import re

# define global constants to mimic BASIC, set later depending on projection
A1, B1, F0, E0, N0, L0, K0, N1, E1, E2 = (None,)*10


def ArcofMeridian(K3, K4):
    """ GOSUB260 
    Arc of Meridian 
    """
    J3 = (1+N1+5/4*N1**2+5/4*N1**3)*K3  # 260
    J4 = (3*N1+3*N1**2+21/8*N1**3)*sin(K3)*cos(K4)  # 270
    J5 = (15/8*N1**2+15/8*N1**3)*sin(2*K3)*cos(2*K4)  # 280
    J6 = 35/24*N1**3*sin(3*K3)*cos(3*K4)  # 290
    M = B1*(J3-J4+J5-J6)  # 300
    return M


def ComputePhi(N):
    """ GOSUB350
    Compute Phi' (K) Latitude """
    K = K0 + (N - N0)/A1  # 350
    K3 = K - K0  # 360
    K4 = K + K0  # 370
    M = ArcofMeridian(K3, K4)  # 380
    while abs(N-N0-M) > 0.001:
        K = K + (N-N0-M)/A1  # 400
        K3 = K - K0  # 360
        K4 = K + K0  # 370
        M = ArcofMeridian(K3, K4)  # 380
    return K


def ComputeV(K):
    """ GOSUB460 
    Compute V, R & H2 """
    V = A1/sqrt(1-E2*sin(K)**2)  # 460
    R = V*(1-E2)/(1-E2*sin(K)**2)  # 470
    H2 = V/R-1  # 480
    return V, R, H2


def ComputeE_NfromLatLon(K, L):
    """ E & N from Latitude (K) & Longitude (L) """
    K3 = K-K0  # 530
    K4 = K+K0  # 540
    M = ArcofMeridian(K3, K4)  # 550
    V, R, H2 = ComputeV(K)  # 560
    P = L-L0  # 570
    J3 = M+N0  # 580
    J4 = V/2*sin(K)*cos(K)  # 590
    J5 = V/24*sin(K)*cos(K)**3*(5-tan(K)**2+9*H2)  # 600
    J6 = V/720*sin(K)*cos(K)**5*(61-58*tan(K)**2+tan(K)**4)  # 610
    N = J3+P**2*J4+P**4*J5+P**6*J6  # 620
    #
    J7 = V*cos(K)  # 630 IV
    J8 = V/6*cos(K)**3*(V/R-tan(K)**2)  # 640 IV
    J9 = V/120*cos(K)**5  # 650
    J9 = J9*(5-18*tan(K)**2+tan(K)**4+14*H2-58*tan(K)**2*H2)  # VI ## 660
    E = E0+P*J7+P**3*J8+P**5*J9  # 670
    return E, N


def ComputeLatLongfromE_N(E, N):
    """Latitude & Longitude from E & N"""
    K = ComputePhi(N)  # 720
    V, R, H2 = ComputeV(K)  # 730
    Y1 = E-E0  # 740
    J3 = tan(K)/(2*R*V)  # 750
    J4 = tan(K)/(24*R*V**3)*(5+3*tan(K)**2+H2-9*tan(K)**2*H2)  # 760
    J5 = tan(K)/(720*R*V**5)*(61+90*tan(K)**2+45*tan(K)**4)  # 770
    K9 = K-Y1**2*J3+Y1**4*J4-Y1**6*J5  # 780
    J6 = 1/(cos(K)*V)  # 790
    J7 = 1/(cos(K)*6*V**3)*(V/R+2*tan(K)**2)  # 800
    J8 = 1/(cos(K)*120*V**5)*(5+28*tan(K)**2+24*tan(K)**4)  # 810
    J9 = 1/(cos(K)*5040*V**7)  # 820
    J9 = J9*(61+662*tan(K)**2+1320*tan(K)**4+720*tan(K)**6)  # 830
    L = L0+Y1*J6-Y1**3*J7+Y1**5*J8-Y1**7*J9  # 840
    K = K9  # 850
    return K, L


def ComputeConvergencefromLL(K, L):
    """ Convergence from Latitude & Longitude"""
    V, R, H2 = ComputeV(K)  # GOSUB460 ## 900
    P = L-L0  # 910
    J3 = sin(K)  # 920
    J4 = sin(K)*cos(K)**2/3*(1+3*H2+2*H2**2)  # 930
    J5 = sin(K)*cos(K)**4/15*(2-tan(K)**2)  # 940
    C = P*J3+P**3*J4+P**5*J5  # 950
    return math.degrees(C)


def ComputeConvergencefromE_N(E, N):
    """Convergence from E & N"""
    K = ComputePhi(N)  # GOSUB350 ## 1000
    V, R, H2 = ComputeV(K)  # GOSUB460 ## 1010
    Y1 = E-E0  # 1020
    J3 = tan(K)/V  # 1030
    J4 = tan(K)/(3*V**3)*(1+tan(K)**2-H2-2*H2**2)  # 1040
    J5 = tan(K)/(15*V**5)*(2+5*tan(K)**2+3*tan(K)**4)  # 1050
    C = Y1*J3-Y1**3*J4+Y1**5*J5  # 1060
    return math.degrees(C)


def ComputeFactorfromLL(K, L):
    """F scale factor at a point from Latitude & Longitude"""
    V, R, H2 = ComputeV(K)  # GOSUB460 ## 1110
    P = L-L0  # 1120
    J3 = cos(K)**2/2*(1+H2)  # XIX ## 1130
    J4 = cos(K)**4/24*(5-4*tan(K)**2+14*H2-28*tan(K)**2*H2)  # XX ## 1140
    F = F0*(1+P**2*J3+P**4*J4)  # 1150
    return F  # 1160


def ComputeFactorfromE_N(E, N):
    """F (scale factor) from E & N"""
    K = ComputePhi(N)  # GOSUB350 ## 1200
    V, R, H2 = ComputeV(N)  # GOSUB460 ## 1210
    Y1 = E-E0  # 1220
    J3 = 1/(2*R*V)  # 1230
    J4 = (1+4*H2)/(24*R**2*V**2)  # 1240
    F = F0*(1+Y1**2*J3+Y1**4*J4)  # 1250
    return F


def ComputeTfromE_N(Na, Nb, Y1a, Y1b):
    """(t - T) from E, N"""
    N = (Na+Nb)/2  # 1300
    K = ComputePhi(N)  # GOSUB350 ## 1310
    V, R, H2 = ComputeV(K)  # GOSUB460 ## 1320
    J3 = 1/(6*R*V)  # 1330
    Ga = (2*Y1a+Y1b)*(Na-Nb)*J3  # 1340
    Gb = (2*Y1b+Y1a)*(Nb-Na)*J3  # 1350
    return math.degrees(Ga), math.degrees(Gb)


def SetConstants(name):
    """ 
    set global projection and datum parameter
    constants for the projection to mimic BASIC
    these are used in the other internal utility functions
    """
    global A1, B1, F0, E0, N0, L0, K0, N1, E1, E2
    # f = (a-b)/a so b = a-a*f
    if name == 'NZT':
        # Global constants for NZTM which is a UTM with custom Central Meridian and False Origin
        # GRS80: a = 6378137.0, 1/f = 298.257222101 used for NZGD2000
        A1 = 6378137.000  # Major semi-axis GRS80
        inv_f = 1.0/298.257222101
        # B1 = 6356752.31414036 # Minor semi-axis GRS80
        F0 = 0.9996  # scale factor at 173.0,0.0 NZTM
        E0 = 1600000.0  # false NZTM E origin (m)
        N0 = 10000000.0  # false NZTM N origin (m)
        L0 = math.radians(173.0)  # Lamda Longitude NZTM of true origin
        K0 = math.radians(0.0)  # Phi Latitude NZTM equator true origin
    elif name == "BNP":
        # Global constants for British National Projection which is a TM with Airy GRS
        # GRS Airy: a = 6377563.396, 1/f = 299.32498
        A1 = 6377563.396  # Major semi-axis
        inv_f = 1.0/298.257222101
        # B1 = 6356256.910 # Minor semi-axis BNP
        F0 = 0.9996012717  # scale factor at 173.0,0.0 NZTM
        E0 = 400000.0  # false NZTM E origin (m)
        N0 = -100000.0  # false NZTM N origin (m)
        L0 = math.radians(-2.0)  # Lamda Longitude NZTM of true origin
        K0 = math.radians(49.0)  # Phi Latitude NZTM equator true origin
    elif name[0:3] == 'UTM':
        # eg name = UTM30N
        # (WGS84 a = 6378137.0 1/f = 298.257223563)
        zone = int(name[3:-1])  # 1 - 60
        hemi = name[-1]
        if int(zone) not in range(1, 60):
            err = "zone must be in range 1 - 60"
            print(err)
            raise IOError
        if hemi == 'N':
            N0 = 0.0
        elif hemi == 'S':
            N0 = 10000000.0
        else:
            err = "hemisphere must be N or S"
            print(err)
            raise IOError
        L0 = math.radians(6*int(zone) - 183.0)  # mid meridian every 6 degrees
        K0 = math.radians(0.0)
        A1 = 6378137.0
        inv_f = 1.0/298.257223563
        F0 = 0.9996
        E0 = 500000.0
    else:
        print("unrecognised projection name:", name)
        raise IOError
    # derived parameter constants common to all TM projections
    B1 = A1 - A1*inv_f
    N1 = (A1 - B1)/(A1 + B1)
    E2 = (A1**2 - B1**2) / A1**2
    E1 = sqrt(E2)
    return


# ============================= main ===============================
if __name__ == '__main__':
    print("Transverse Mercator v 3.1")
    DEBUG = False
    try:
        l = float(sys.argv[1])
        k = float(sys.argv[2])
        if sys.argv.count() == 4:
            name = sys.argv[3].upper()[0:3]
        else:
            name = 'NZT'
    except:
        k = -38.0
        l = 178.0
        name = 'NZT'  # default or BNP or UTM<zone><hemisphere> eg UTM30N
        print(
            "Usage: transverse.py lon(dd) lat(dd) {name NZT|BNP|UTM<zone><N|S>}")
    print("defaults", l, k, name)
    # validate bounds
    if not re.match("NZT|BNP|WGS[1-6][0-9](N|S)", name):
        print("Unknown projection: ", name)
        print(
            "Usage: transverse.py lon(dd) lat(dd) {name NZTM|BNP|UTM<zone><N|S>}")
        raise IOError
    minlon, maxlon, minlat, maxlat = (None,)*4
    if name[0:3] == 'UTM':
        zone = int(name[3:-1])
        mid = 6*int(zone) - 183.0
        minlon = mid-3
        maxlon = mid + 3
        hemi = name[-1]
        if hemi == 'N':
            minlat = 5.0
            maxlat = 90.0
        else:
            minlat = -85.0
            maxlat = 0.0
    bounds = {'NZT': (166, -60, 180, -30), 'BNP': (-10, 50, 10, 30),
              'UTM': (minlon, minlat, maxlon, maxlat)}
    if not bounds[name][1] <= k <= bounds[name][3]:
        print(k, 'latitude not in range', bounds[name][1], bounds[name][3])
        raise IOError
    if not bounds[name][0] <= l <= bounds[name][2]:
        print(l, 'longitude not in range', bounds(name)[0], bounds[name][2])
        raise IOError
    # Initialise
    K = math.radians(k)
    L = math.radians(l)
    SetConstants(name)
    if DEBUG:
        for gvar in ['A1', 'B1', 'F0', 'E0', 'N0', 'L0', 'K0', 'N1', 'E1', 'E2']:
            print(gvar, eval(gvar))

    print("\nLong Lat:    {} {}".format(l, k),
          "\nE, N:  {:12.3f} {:12.3f} {}".format(
        *ComputeE_NfromLatLon(K, L), name),
        "\nConvergence:{:8.3f} ".format(ComputeConvergencefromLL(K, L)),
        "\nScale:        {:5.4f}".format(ComputeFactorfromLL(K, L)))
    # test bulk process
    """import csv
    with open("D:/project/geodesy/sample.txt", "r") as f1:
        csvreader = csv.reader(f1)
        next(csvreader)
        for row in csvreader:
            K = math.radians(float(row[2]))
            L = math.radians(float(row[1]))
            print(int(row[0]), ",",
            # ComputeE_NfromLatLon(K, L), 
            ComputeConvergencefromLL(K, L),
            )
    """

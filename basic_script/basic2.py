# Basic Transverse Mercator
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
# ref Ordnance Survey Information Pamphlet
# Transverse Mercator Projection Constants, Formulae and Methods March 1983
# Appendix A subroutines in BASIC translated to Python, commented numbers are original BASIC line numbers
# Mods
#     remove line numbers
#     replace subroutines with functions
#     basic syntax to python syntax ^ to **
#     make all variables local to functions
#     
# Kim Ollivier 17 May 2020
import math
from math import sin, cos, tan, sqrt

# subroutines renamed as functions
# GOSUB260 = ArcofMeridian
# GOSUB350 = ComputePhi
# GOSUB460 = ComputeV

# variables are set for NZTM which is a UTM with custom Central Meridian and False Origin
# GRS80 a = 6378137.0, 1/f = 298.257222101 used for NZGD2000
# (WGS84 a = 6378137.0 1/f = 298.257223563)
# f = (a - b) /a
A1 = 6378137.000 # Major semi-axis GRS80
B1 = 6356752.31414036 # Minor semi-axis GRS80
F0 = 0.9996 # scale factor at 173.0,0.0 NZTM
E0 = 1600000.0 # false NZTM E origin (m)
N0 = 10000000.0  # false NZTM N origin (m)
L0 = math.radians(173.0) # Lamda Longitude NZTM of true origin
K0 = math.radians(0.0) # Phi Latitude NZTM equator true origin
# derived parameter constants
N1 = (A1 - B1)/(A1+B1)
E2 = (A1**2 - B1**2) / A1**2
E1 = sqrt(E2)

def ArcofMeridian(N1,B1,K3,K4):
    """ GOSUB260 
    """
    J3 = (1+N1+5/4*N1**2+5/4*N1**3)*K3 ## 260
    J4 = (3*N1+3*N1**2+21/8*N1**3)*sin(K3)*cos(K4) ## 270
    J5 = (15/8*N1**2+15/8*N1**3)*sin(2*K3)*cos(2*K4) ## 280
    J6 = 35/24*N1**3*sin(3*K3)*cos(3*K4) ## 290
    M = B1*(J3-J4+J5-J6) ## 300
    return M 


def ComputePhi(N, N0, A1, K0):
    """ GOSUB350
    Compute Phi' (K) Latitude ## 340
    """
    K = K0 + (N - N0)/A1 ## 350 
    K3 = K - K0 ## 360
    K4 = K + K0 ## 370
    M =  ArcofMeridian(N1,B1,K3,K4) ## 380
    while abs(N-N0-M) > 0.001:
        K = K + (N-N0-M)/A1 ## 400
        K3 = K - K0 ## 360
        K4 = K + K0 ## 370
        M =  ArcofMeridian(N1,B1,K3,K4) ## 380
    return K 

def ComputeV(A1, E2, K):
    """ GOSUB460 
    Compute V, R & H2 ## 450
    """
    V=A1/sqrt(1-E2*sin(K)**2) ## 460
    R = V*(1-E2)/(1-E2*sin(K)**2) ## 470
    H2=V/R-1 ## 480
    return V, R, H2  

def ComputeE_NfromLatLon(K,L,L0=L0,E0=E0,N0=N0,K0=K0,A1=A1):
    """ 
    E & N from Latitude (K) & Longitude (L) 
    """
    K3=K-K0 ## 530
    K4=K+K0 ## 540
    M = ArcofMeridian(N1,B1,K3,K4) ## 550 
    V, R, H2 = ComputeV(A1, E2, K) ## 560
    P=L-L0 ## 570
    J3=M+N0 ## 580
    J4=V/2*sin(K)*cos(K) ## 590
    J5=V/24*sin(K)*cos(K)**3*(5-tan(K)**2+9*H2) ## 600
    J6=V/720*sin(K)*cos(K)**5*(61-58*tan(K)**2+tan(K)**4) ## 610
    N=J3+P**2*J4+P**4*J5+P**6*J6 ## 620

    J7=V*cos(K) ## 630 IV
    J8=V/6*cos(K)**3*(V/R-tan(K)**2)  ## 640 IV
    J9=V/120*cos(K)**5 ## 650
    J9=J9*(5-18*tan(K)**2+tan(K)**4+14*H2-58*tan(K)**2*H2)#VI ## 660
    E=E0+P*J7+P**3*J8+P**5*J9 ## 670
    return E, N  


def ComputeLatLongfromE_N(E,N,N0=N0,E2=E2):
    """Latitude & Longitude from E & N"""
    K = ComputePhi(N,N0,A1,K0) ## 720
    V, R, H2 = ComputeV(A1, E2, K) ## 730
    Y1=E-E0 ## 740
    J3=tan(K)/(2*R*V) ## 750
    J4=tan(K)/(24*R*V**3)*(5+3*tan(K)**2+H2-9*tan(K)**2*H2) ## 760
    J5=tan(K)/(720*R*V**5)*(61+90*tan(K)**2+45*tan(K)**4) ## 770
    K9=K-Y1**2*J3+Y1**4*J4-Y1**6*J5 ## 780
    J6=1/(cos(K)*V) ## 790
    J7=1/(cos(K)*6*V**3)*(V/R+2*tan(K)**2) ## 800
    J8=1/(cos(K)*120*V**5)*(5+28*tan(K)**2+24*tan(K)**4) ## 810
    J9=1/(cos(K)*5040*V**7) ## 820
    J9=J9*(61+662*tan(K)**2+1320*tan(K)**4+720*tan(K)**6) ## 830
    L=L0+Y1*J6-Y1**3*J7+Y1**5*J8-Y1**7*J9 ## 840
    K=K9 ## 850
    return K,L

def ComputeConvergencefromLL(K, L, E2=E2):
    """ Convergence from Latitude & Longitude"""
    V, R, H2 = ComputeV(A1, E2, K)# GOSUB460 ## 900
    P=L-L0 ## 910
    J3=sin(K) ## 920
    J4=sin(K)*cos(K)**2/3*(1+3*H2+2*H2**2) ## 930
    J5=sin(K)*cos(K)**4/15*(2-tan(K)**2) ## 940
    C=P*J3+P**3*J4+P**5*J5 ## 950
    return math.degrees(C) 


def ComputeConvergencefromE_N(E, N, N0=N0,A1=A1,K0=K0):
    """Convergence from E & N"""
    K = ComputePhi(N, N0, A1, K0) #GOSUB350 ## 1000
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1010
    Y1 = E - E0 ## 1020
    J3 = tan(K)/V ## 1030
    J4 = tan(K)/(3*V**3)*(1 + tan(K)**2 - H2 - 2*H2**2) ## 1040
    J5 = tan(K)/(15*V**5)*(2 + 5*tan(K)**2 + 3*tan(K)**4) ## 1050
    C = Y1*J3 - Y1**3*J4 + Y1**5*J5 ## 1060
    return math.degrees(C)

def ComputeFfromLL(K,L,N=N1,N0=N0,A1=A1,K0=K0):
    """F scale factor at a point from Latitude & Longitude"""
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1110
    P = L - L0 ## 1120
    J3=cos(K)**2/2*(1 +H2) # XIX ## 1130
    J4=cos(K)**4/24*(5-4*tan(K)**2+14*H2-28*tan(K)**2*H2) # XX ## 1140
    F= F0*(1 + P**2*J3+ P**4*J4) ## 1150
    return F ## 1160

def ComputeFfromE_N(E,N,N0=N0,A1=A1,K0=K0):
    """F (scale factor) from E & N"""
    K = ComputePhi(N, N0, A1, K0) #GOSUB350 ## 1200
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1210
    Y1 = E - E0 ## 1220
    J3 = 1 /(2*R*V) ## 1230
    J4 = (1 + 4*H2)/(24*R**2*V**2) ## 1240
    F=F0*(1 +Y1**2*J3+Y1**4*J4) ## 1250
    return F 


def ComputeTfromE_N(Na, Nb, Y1a, Y1b, N, N0, A1, K0):
    """(t - T) from E, N"""
    N=(Na+ Nb)/2 ## 1300
    K = ComputePhi(N, N0, A1, K0) # GOSUB350 ## 1310
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1320
    J3=1/(6*R*V) ## 1330
    Ga=(2*Y1a+Y1b)*(Na-Nb)*J3 ## 1340
    Gb=(2*Y1b+Y1a)*(Nb-Na)*J3 ## 1350
    return math.degrees(Ga), math.degrees(Gb)

    # ================= main ======================
print("Transverse Mercator")
k = -37.0
l = 174.0
K = math.radians(k)
L = math.radians(l)
print("Lat Long:",(k, l), 
    "E,N:",ComputeE_NfromLatLon(K, L), 
    "Convergence:", ComputeConvergencefromLL(K, L),
    "Scale:",ComputeFfromLL(K, L))

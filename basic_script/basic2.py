# Variables ## 10
# Where possible a variable used in the following ## 20
# routines is either the same as that used in the ## 30
# formulae or can be deduced from the suffix. ## 40
# ## 50
# No suffix= Upper Case Letter ## 60
# Suffix 1 = Lower Case Letter ## 70
# Suffix 2 = Lower Case Letter Squared ## 80
# Suffix 0 =Subscript 0 e.g. E0 =Grid Eastings of True 0rigin. ## 90
# ## 100
# J3-J9 are used for intermediate values. ## 110
# ## 120
# The variables not covered by the above rules are listed below: ## 130
# K = Phi (Latitude) or Phi' ## 140
# L = Lambda (Longitude) ## 150
# R = Rho (Radius of Curvature in Meridian) ## 160
# V = Nu (Radius of Curvature in Prime Vertical) ## 170
# H2 = Eta Squared (Nu/Rho - 1) ## 180
# K3 = Phi2 - Phi1 (Difference Latitude) ## 190
# K4 = Phi2 + Phi1 (Sum Latitudes) ## 200
# Ga, Gb = (t - T) at line terminals A and B ## 210
# All angular arguments are in Radians ## 220
import math
from math import sin, cos, tan, sqrt

# called functions
# GOSUB260 = ArcofMeridian
# GOSUB350 = ComputePhi
# GOSUB460 = ComputeV

# variables
# GRS80 a = 6378137.0 1/f = 298.257222101 used for NZGD2000
# WGS84 a = 6378137.0 1/f = 298.257223563
# f = (a - b) /a
A1 = 6378137.000 # Major
B1 = 6356752.31414036 # Minor
F0 = 0.9996 # at 173.0,0.0
E0 = 500000.0 # false E origin (m)
N0 = 10000000.0      # false N origin (m)
L0 = math.radians(173.0) # Lamda Longitude NZTM of true origin
K0 = math.radians(0.0) # Phi Latitude NZTM equator true origin
N1 = (A1 - B1)/(A1+B1)
E2 = (A1**2 - B1**2) / A1**2
E1 = sqrt(E2)

# Arc of Meridian ## 250
def ArcofMeridian(N1,B1,K3,K4):
    """ GOSUB260 
    N1, B1 constants"""
    J3 = (1+N1+5/4*N1**2+5/4*N1**3)*K3 ## 260
    J4 = (3*N1+3*N1**2+21/8*N1**3)*sin(K3)*cos(K4) ## 270
    J5 = (15/8*N1**2+15/8*N1**3)*sin(2*K3)*cos(2*K4) ## 280
    J6 = 35/24*N1**3*sin(3*K3)*cos(3*K4) ## 290
    M = B1*(J3-J4+J5-J6) ## 300
    return M ## 310

# Compute Phi' (K) Latitude ## 340
def ComputePhi(N, N0, A1, K0):
    """ sub 350"""
    K = K0 + (N - N0)/A1 ## 350 
    K3 = K - K0 ## 360
    K4 = K + K0 ## 370
    M =  ArcofMeridian(N1,B1,K3,K4) ## 380
    while math.abs(N-N0-M) > 0.001:
        K = K + (N-N0-M)/A1 ## 400
        K3 = K - K0 ## 360
        K4 = K + K0 ## 370
        M =  ArcofMeridian(N1,B1,K3,K4) ## 380
    return K ## 420

# Compute V, R & H2 ## 450
def ComputeV(A1, E2, K):
    """ sub 460 """
    V=A1/sqrt(1-E2*sin(K)**2) ## 460
    R = V*(1-E2)/(1-E2*sin(K)**2) ## 470
    H2=V/R-1 ## 480
    return V, R, H2  ## 490

# E & N from Latitude (K) & Longitude (L) ## 520
def ComputeE_NfromLatLon(K,L,L0=L0,E0=E0,N0=N0,K0=K0,A1=A1):
    """ sub 530 """
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
    return E,N   ## 680

# Latitude & Longitude from E & N  ## 710
def ComputeLatLongfromE_N(N,N0,E2,E):
    """ sub 720 """
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
    return L, K ## 860

# Convergence from Latitude & Longitude ## 890
def ComputeConvergencefromLL(L, E2, K):
    """ sub 900"""
    V, R, H2 = ComputeV(A1, E2, K)# GOSUB460 ## 900
    P=L-L0 ## 910
    J3=sin(K) ## 920
    J4=sin(K)*cos(K)**2/3*(1+3*H2+2*H2**2) ## 930
    J5=sin(K)*cos(K)**4/15*(2-tan(K)**2) ## 940
    C=P*J3+P**3*J4+P**5*J5 ## 950
    return math.degrees(C) ## 960

# Convergence from E & N  ## 990
def ComputeConvergencefromE_N(E, N):
    """ sub 1000"""
    K = ComputePhi(N, N0, A1, K0) #GOSUB350 ## 1000
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1010
    Y1 = E - E0 ## 1020
    J3 = tan(K)/V ## 1030
    J4 = tan(K)/(3*V**3)*(1 + tan(K)**2 - H2 - 2*H2**2) ## 1040
    J5 = tan(K)/(15*V**5)*(2 + 5*tan(K)**2 + 3*tan(K)**4) ## 1050
    C = Y1*J3 - Y1**3*J4 + Y1**5*J5 ## 1060
    return math.degrees(C) ## 1070

# F scale factor at a point from Latitude & Longitude ## 1100
def ComputeFfromLL(L,K):
    """ sub 1110 """
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1110
    P = L - L0 ## 1120
    J3=cos(K)**2/2*(1 +H2) # XIX ## 1130
    J4=cos(K)**4/24*(5-4*tan(K)**2+14*H2-28*tan(K)**2*H2) # XX ## 1140
    F= F0*(1 + P**2*J3+ P**4*J4) ## 1150
    return F ## 1160

# F (scale factor) from E & N ## 1190
def ComputeFfromE_N():
    """ sub 1200"""
    K = ComputePhi(N, N0, A1, K0) #GOSUB350 ## 1200
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1210
    Y1 = E - E0 ## 1220
    J3 = 1 /(2*R*V) ## 1230
    J4 = (1 + 4*H2)/(24*R**2*V**2) ## 1240
    F=F0*(1 +Y1**2*J3+Y1**4*J4) ## 1250
    return F ## 1260

# (t - T) from E, N ## 1290
def ComputeTfromE_N(Na, Nb, Y1a, Y1b, N, N0, A1, K0):
    """ sub 1300"""
    N=(Na+ Nb)/2 ## 1300
    K = ComputePhi(N, N0, A1, K0) # GOSUB350 ## 1310
    V, R, H2 = ComputePhi(N, N0, A1, K0) # GOSUB460 ## 1320
    J3=1/(6*R*V) ## 1330
    Ga=(2*Y1a+Y1b)*(Na-Nb)*J3 ## 1340
    Gb=(2*Y1b+Y1a)*(Nb-Na)*J3 ## 1350
    return math.degrees(Ga), match.degrees(Gb) ## 1360

    # ================= main ======================
    print("Transverse Mercator")
    k = -37.0
    l = 174.0
    K = math.radians(k)
    L = math.radians(l)
    print(k, l, ComputeE_NfromLatLon(K,L))

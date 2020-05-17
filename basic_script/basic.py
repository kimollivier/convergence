# Variables ## 10
# Where possible a variable used in the following ## 20
# routines is either the same as that used in the ## 30
# formulae or can be deduced from the suffix. ## 40
# ## 50
# No suffix= Upper Case Letter ## 60
# Suffix 1 = Lower Case Letter ## 70
# Suffix 2 = Lower Case Letter Squared ## 80
I Suffix 0 =Subscript 0 e.g. EO =Grid Eastings of True Origin. ## 90
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


# Arc of Meridian ## 250
def ArcofMeridian():
    """ sub 260 """
J3 = (1+N1+5/4*N1^2+5/4*N1^3)*K3 ## 260
J4 = (3*N1+3*N1^2+21/8*N1^3)*SIN(K3)*COS(K4) ## 270
J5 = (15/8*N1^2+15/8*N1^3)*SIN(2*K3)*COS(2*K4) ## 280
J6 = 35/24*N1^3*SIN(3*K3)*COS(3*K4) ## 290
M=B1*(J3-J4+J5-J6) ## 300
RETURN ## 310

# Compute Phi' (K) ## 340
K = (N - NO)/A1+KO ## 350
K3 = K - KO ## 360
K4 = K +KO ## 370
GOSUB 260 ## 380
IF ABS(N-NO-M) < .001 THEN 420 ## 390
K = K + (N-NO-M)/A1 ## 400
GOTO 360 ## 410
RETURN ## 420

# Compute V, R&H2 ## 450
V=A1/SQR(1-E2*SIN(K)A2) ## 460
R = V*(1-E2)/(1-E2*SIN(K)^2) ## 470
H2=V/R-1 ## 480
RETURN ## 490

# E & N from Latitude (K) & Longitude (L) ## 520
K3=K-KO ## 530
K4=K+KO ## 540
GOSUB 260 ## 550
GOSUB 460 ## 560
P=L-LO ## 570
J3=M+NO ## 580
J4=V/2*SIN(K)*COS(K) ## 590
J5=V/24*SIN(K)*COS(K)^3*(5-TAN(K)^2+9*H2) ## 600
J6=V/720*SIN(K)*COS(K)^5*(61-58*TAN(K)^2+TAN(K)^4) ## 610
N=J3+P^2*J4+P^4*J5+P^6*J6 ## 620
J7=V*COS(K) ## 630 IV
J8=V/6*COS(K)^3*(V/R-TAN(K)^2)  ## 640 IV
J9=V/120*COS(K)^5 ## 650
J9=J9*(5-18*TAN(K)A2+TAN(K)A4+14*H2-58*TAN(K)A2*H2)#VI ## 660
E=EO+P*J7+P^3*J8+PA5d9 ## 670
RETURN ## 680

# Latitude & Longitude from E & N  ## 710
GOSUB 350 ## 720
GOSUB 460 ## 730
Y1=E-EO ## 740
J3=TAN(K)/(2*R*V) ## 750
J4=TAN(K)/(24*R*V^3)*(5+3*TAN(K)^2+H2-9*TAN(K)^2*H2) ## 760
J5=TAN(K)/(720*R*V^5)*(61+90*TAN(K)^2+45*TAN(K)^4) ## 770
K9=K-Y1A2*J3+Y1A4*J4-Y1A6*J5 ## 780
J6=1/(COS(K)*V) ## 790
J7=1/(COS(K)*6*V^3)*(V/R+2*TAN(K)A2)J8=1 ## 800
J8=1/(COS(K)*120*V^5)*(5+28*TAN(K)^2+24*TAN(K)^4) ## 810
J9=1/(COS(K)*5040*V^7) ## 820
J9=J9*(61+662*TAN(K)^2+1320*TAN(K)^4+720*TAN(K)^6) ## 830
L=LO+Y1*J6-Y1^3d*J7+Y1^5*J8-Y1^7*J9 ## 840
K=K9 ## 850
RETURN ## 860

# C from Latitude & Longitude ## 890
GOSUB 460 ## 900
P=L-LO ## 910
J3=SIN(K) ## 920
J4=SIN(K)*COS(K)^2/3*(1+3*H2+2*H2^2) ## 930
J5=SIN(K)*COS(K)^4/15*(2-TAN(K)^2) ## 940
C=P*J3+P^3*J4+P^5*J5 ## 950
RETURN ## 960

# C from E & N  ## 990
GOSUB 350 ## 1000
GOSUB 460 ## 1010
Y1 = E - EO ## 1020
J3 = TAN(K)/V ## 1030
J4 = TAN(K)/(3*V^3)*(1 + TAN(K)^2 - H2- 2*H2^2) ## 1040
J5 = TAN(K)/(15*V^5)*(2 + 5*TAN(K) ^2 + 3*TAN(K) ^4) ## 1050
C = Y1*J3 - Y1^3*J4 + Y1^5*J5 ## 1060
RETURN ## 1070

# F from Latitude & Longitude ## 1100
GOSUB 460 ## 1110
P = L - LO ## 1120
J3=COS(K)^2/2*(1 +H2) # XIX ## 1130
J4=COS(K)^4/24*(5-4*TAN(K)^2+14*H2-28*TAN(K)^2*H2) # XX ## 1140
F= F0*(1 + P^2*J3+ P^4*J4) ## 1150
RETURN ## 1160

# F from E & N ## 1190
GOSUB 350 ## 1200
GOSUB 460 ## 1210
Y1 = E - EO ## 1220
J3 = 1 /(2*R*V) ## 1230
J4 = (1 + 4*H2)/(24*R^2*V^2) ## 1240
F=F0*(1 +Y1^2*J3+Y1^4*J4) ## 1250
RETURN ## 1260

# (t - T) from E, N ## 1290
N=(Na+ Nb)/2 ## 1300
GOSUB350 ## 1310
GOSUB 460 ## 1320
J3=1/(6*R*V) ## 1330
Ga=(2*Y1a+Y1b)*(Na-Nb)*J3 ## 1340
Gb=(2*Y1b+Y1a)*(Nb-Na)*J3 ## 1350
RETURN ## 1360
 

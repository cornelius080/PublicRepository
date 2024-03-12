# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 12:34:11 2022
@author: gscalera
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from WitMotionRead import WitMotionRead
import Utilities
Utilities.ClearAll();


def AllanVarianceAnalysis(signal, dt):
    signalInt = np.cumsum(signal)*dt

    L = len(signal)
    maxNumM = 100
    maxM = 2**np.floor(math.log2(L/2))
    m = np.logspace(np.log10(1), np.log10(maxM), maxNumM)
    m = np.ceil(m).astype(int)
    m = np.unique(m)
    tau = m*dt

    avar = np.zeros((len(m), 1))
    for i in np.linspace(1,len(m),len(m)).astype(int):
        mi = m[i-1]
        avar[i-1] = sum((signalInt[2*mi:L] -2*signalInt[mi:L-mi] + signalInt[0:L-2*mi])**2)
        
    c1 = tau**2
    c2 = L-2*m
    normCoeff = 2*c1*c2
    avar = np.squeeze(avar)
    avar = avar / normCoeff
    adev = avar**0.5
    return adev, tau


def CalculateAngleRandomWalk(tau, adev):
    slope = -0.5
    logtau = np.log10(tau)
    logadev = np.log10(adev)
    dlogadev = np.diff(logadev) / np.diff(logtau)
    index = np.argmin(abs(dlogadev - slope))
    # Find the y-intercept of the line.
    b = logadev[index] - slope*logtau[index]
    # Determine the angle random walk coefficient from the line.
    logN = slope*math.log(1) + b
    N = 10**logN

    tauN = 1
    lineN = N / np.sqrt(tau)
    return N, tauN, lineN


def CalculateRateRandomWalk(tau, adev):
    slope = 0.5
    logtau = np.log10(tau)
    logadev = np.log10(adev)
    dlogadev = np.diff(logadev) / np.diff(logtau)
    index = np.argmin(abs(dlogadev - slope))

    # Find the y-intercept of the line.
    b = logadev[index] - slope*logtau[index]
    # Determine the rate random walk coefficient from the line.
    logK = slope*np.log10(3) + b
    K = 10**logK

    tauK = 3;
    lineK = K * np.sqrt(tau/3)
    return K, tauK, lineK


def CalculateBiasInstability(tau, adev):
    #Find the index where the slope of the log-scaled Allan deviation is equal to the slope     specified.
    slope = 0
    logtau = np.log10(tau)
    logadev = np.log10(adev)
    dlogadev = np.diff(logadev) / np.diff(logtau)
    index = np.argmin(abs(dlogadev - slope))

    # Find the y-intercept of the line.
    b = logadev[index] - slope*logtau[index]
    # Determine the bias instability coefficient from the line.
    scfB = np.sqrt(2*math.log(2)/math.pi)
    logB = b - np.log10(scfB)
    B = 10**logB

    tauB = tau[index]
    lineB = B * scfB * np.ones(tau.shape)
    return B, tauB, lineB, scfB

    



# %% DATA LOADING
fileName = '220308174439_1hour.txt'
dataRead = WitMotionRead(fileName)
acc  = dataRead["acc"]
gyro = dataRead["gyro"]
time = dataRead["time"]

# USEFUL DATA 
sf = (time[1] - time[0]) ** -1
accMod  = ( acc[:,0]**2 +  acc[:,1]**2 +  acc[:,2]**2)**0.5
gyroMod = (gyro[:,0]**2 + gyro[:,1]**2 + gyro[:,2]**2)**0.5


# %% GYRO ALLAN VARIANCE
f1 = plt.figure(1)
plt.subplot(2, 1, 1)
plt.plot(time, gyro[:,0], color = 'r')
plt.plot(time, gyro[:,1], color = 'g')
plt.plot(time, gyro[:,2], color = 'b')
plt.legend(['X', 'Y', 'Z']); plt.ylabel("ANG VEL (°/s)")
fontTitle = {'color':'black','size':20}; plt.title("GYROSCOPE", fontdict=fontTitle)
plt.subplot(2, 1, 2)
plt.plot(time, gyroMod, color = 'm')
plt.legend(['MOD']); plt.xlabel("TIME (s)"); plt.ylabel("ANG VEL (°/s)")
plt.show()

adev_GyroX, tau_GyroX = AllanVarianceAnalysis(gyro[:,0], time[1]-time[0])
adev_GyroY, tau_GyroY = AllanVarianceAnalysis(gyro[:,1], time[1]-time[0])
adev_GyroZ, tau_GyroZ = AllanVarianceAnalysis(gyro[:,2], time[1]-time[0])

f2 = plt.figure(2)
plt.plot(tau_GyroX, adev_GyroX, color = 'r')
plt.plot(tau_GyroY, adev_GyroY, color = 'g')
plt.plot(tau_GyroZ, adev_GyroZ, color = 'b')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO X', 'GYRO Y', 'GYRO Z'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('GYROSCOPE - ALLAN DEVIATION')
plt.show()


# %% GYRO ANGLE RANDOM WALK N
N_GyroX, tauN_GyroX, lineN_GyroX = CalculateAngleRandomWalk(tau_GyroX, adev_GyroX)
N_GyroY, tauN_GyroY, lineN_GyroY = CalculateAngleRandomWalk(tau_GyroY, adev_GyroY)
N_GyroZ, tauN_GyroZ, lineN_GyroZ = CalculateAngleRandomWalk(tau_GyroZ, adev_GyroZ)

f3 = plt.figure(3)
plt.subplot(3,1,1)
plt.plot(tau_GyroX, adev_GyroX, color = 'r')
plt.plot(tau_GyroX, lineN_GyroX, '--', color='k')
plt.plot(tauN_GyroX, N_GyroX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO X', 'ARW = ' + str(N_GyroX) + '((rad/s)/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('GYROSCOPE - ANGLE RANDOM WALK NOISE')
plt.subplot(3,1,2)
plt.plot(tau_GyroY, adev_GyroY, color = 'g')
plt.plot(tau_GyroY, lineN_GyroY, '--', color='k')
plt.plot(tauN_GyroY, N_GyroY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Y', 'ARW = ' + str(N_GyroY) + '((rad/s)/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_GyroZ, adev_GyroZ, color = 'b')
plt.plot(tau_GyroZ, lineN_GyroZ, '--', color='k')
plt.plot(tauN_GyroZ, N_GyroZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Z', 'ARW = ' + str(N_GyroZ) + '((rad/s)/(Hz^0.5))'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()


# %% GYRO RATE RANDOM WALK K
K_GyroX, tauK_GyroX, lineK_GyroX = CalculateRateRandomWalk(tau_GyroX, adev_GyroX)
K_GyroY, tauK_GyroY, lineK_GyroY = CalculateRateRandomWalk(tau_GyroY, adev_GyroY)
K_GyroZ, tauK_GyroZ, lineK_GyroZ = CalculateRateRandomWalk(tau_GyroZ, adev_GyroZ)

f4 = plt.figure(4)
plt.subplot(3,1,1)
plt.plot(tau_GyroX, adev_GyroX, color = 'r')
plt.plot(tau_GyroX, lineK_GyroX, '--', color='k')
plt.plot(tauK_GyroX, K_GyroX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO X', 'RRW = ' + str(K_GyroX) + '((rad/s)/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('GYROSCOPE - RATE RANDOM WALK NOISE')
plt.subplot(3,1,2)
plt.plot(tau_GyroY, adev_GyroY, color = 'g')
plt.plot(tau_GyroY, lineK_GyroY, '--', color='k')
plt.plot(tauK_GyroY, K_GyroY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Y', 'RRW = ' + str(K_GyroY) + '((rad/s)/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_GyroZ, adev_GyroZ, color = 'b')
plt.plot(tau_GyroZ, lineK_GyroZ, '--', color='k')
plt.plot(tauK_GyroZ, K_GyroZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Z', 'RRW = ' + str(K_GyroZ) + '((rad/s)/(Hz^0.5))'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()


# %% GYRO BIAS INSTABILITY B
B_GyroX, tauB_GyroX, lineB_GyroX, scfB_GyroX = CalculateBiasInstability(tau_GyroX, adev_GyroX)
B_GyroY, tauB_GyroY, lineB_GyroY, scfB_GyroY = CalculateBiasInstability(tau_GyroY, adev_GyroY)
B_GyroZ, tauB_GyroZ, lineB_GyroZ, scfB_GyroZ = CalculateBiasInstability(tau_GyroZ, adev_GyroZ)

f5 = plt.figure(5)
plt.subplot(3,1,1)
plt.plot(tau_GyroX, adev_GyroX, color = 'r')
plt.plot(tau_GyroX, lineB_GyroX, '--', color='k')
plt.plot(tauB_GyroX, scfB_GyroX*B_GyroX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO X', 'BI = ' + str(B_GyroX) + '(rad/s)'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('GYROSCOPE - BIAS INSTABILITY NOISE')
plt.subplot(3,1,2)
plt.plot(tau_GyroY, adev_GyroY, color = 'g')
plt.plot(tau_GyroY, lineB_GyroY, '--', color='k')
plt.plot(tauB_GyroY, scfB_GyroX*B_GyroY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Y', 'BI = ' + str(B_GyroY) + '(rad/s)'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_GyroZ, adev_GyroZ, color = 'b')
plt.plot(tau_GyroZ, lineB_GyroZ, '--', color='k')
plt.plot(tauB_GyroZ, scfB_GyroX*B_GyroZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['GYRO Z', 'BI = ' + str(B_GyroZ) + '(rad/s)'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()


# %% ACC ALLAN VARIANCE
f6 = plt.figure(6)
plt.subplot(2, 1, 1)
plt.plot(time, acc[:,0], color = 'r')
plt.plot(time, acc[:,1], color = 'g')
plt.plot(time, acc[:,2], color = 'b')
plt.legend(['X', 'Y', 'Z']); plt.ylabel("ACC (g)"); 
fontTitle = {'color':'black','size':20}; plt.title("ACCELEROMETER", fontdict=fontTitle)
plt.subplot(2, 1, 2)
plt.plot(time, accMod, color = 'm')
plt.legend(['MOD']); plt.xlabel("TIME (s)"); plt.ylabel("ACC (g)"); 
plt.show()

adev_AccX, tau_AccX = AllanVarianceAnalysis(acc[:,0], time[1]-time[0])
adev_AccY, tau_AccY = AllanVarianceAnalysis(acc[:,1], time[1]-time[0])
adev_AccZ, tau_AccZ = AllanVarianceAnalysis(acc[:,2], time[1]-time[0])

f7 = plt.figure(7)
plt.plot(tau_AccX, adev_AccX, color = 'r')
plt.plot(tau_AccY, adev_AccY, color = 'g')
plt.plot(tau_AccZ, adev_AccZ, color = 'b')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC X', 'ACC Y', 'ACC Z'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('ACCELEROMETER - ALLAN DEVIATION')
plt.show()


# %% ACC VELOCITY RANDOM WALK N
N_AccX, tauN_AccX, lineN_AccX = CalculateAngleRandomWalk(tau_AccX, adev_AccX)
N_AccY, tauN_AccY, lineN_AccY = CalculateAngleRandomWalk(tau_AccY, adev_AccY)
N_AccZ, tauN_AccZ, lineN_AccZ = CalculateAngleRandomWalk(tau_AccZ, adev_AccZ)

f8 = plt.figure(8)
plt.subplot(3,1,1)
plt.plot(tau_AccX, adev_AccX, color = 'r')
plt.plot(tau_AccX, lineN_AccX, '--', color='k')
plt.plot(tauN_AccX, N_AccX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC X', 'VRW = ' + str(N_AccX) + '(g/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('ACCELEROMETER - VELOCITY RANDOM WALK NOISE')
plt.subplot(3,1,2)
plt.plot(tau_AccY, adev_AccY, color = 'g')
plt.plot(tau_AccY, lineN_AccY, '--', color='k')
plt.plot(tauN_AccY, N_AccY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC Y', 'VRW = ' + str(N_AccY) + '(g/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_AccZ, adev_AccZ, color = 'b')
plt.plot(tau_AccZ, lineN_AccZ, '--', color='k')
plt.plot(tauN_AccZ, N_AccZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC Z', 'VRW = ' + str(N_AccZ) + '(g/(Hz^0.5))'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()


# %% ACC RATE RANDOM WALK K
K_AccX, tauK_AccX, lineK_AccX = CalculateRateRandomWalk(tau_AccX, adev_AccX)
K_AccY, tauK_AccY, lineK_AccY = CalculateRateRandomWalk(tau_AccY, adev_AccY)
K_AccZ, tauK_AccZ, lineK_AccZ = CalculateRateRandomWalk(tau_AccZ, adev_AccZ)

f9 = plt.figure(9)
plt.subplot(3,1,1)
plt.plot(tau_AccX, adev_AccX, color = 'r')
plt.plot(tau_AccX, lineK_AccX, '--', color='k')
plt.plot(tauK_AccX, K_AccX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC X', 'RRW = ' + str(K_AccX) + '(g/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('ACCELEROMETER - RATE RANDOM WALK NOISE')
plt.subplot(3,1,2)
plt.plot(tau_AccY, adev_AccY, color = 'g')
plt.plot(tau_AccY, lineK_AccY, '--', color='k')
plt.plot(tauK_AccY, K_AccY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC Y', 'RRW = ' + str(K_AccY) + '(g/(Hz^0.5))'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_AccZ, adev_AccZ, color = 'b')
plt.plot(tau_AccZ, lineK_AccZ, '--', color='k')
plt.plot(tauK_AccZ, K_AccZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['ACC Z', 'RRW = ' + str(K_AccZ) + '(g/(Hz^0.5))'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()


# %% ACC BIAS INSTABILITY B
B_AccX, tauB_AccX, lineB_AccX, scfB_AccX = CalculateBiasInstability(tau_AccX, adev_AccX)
B_AccY, tauB_AccY, lineB_AccY, scfB_AccY = CalculateBiasInstability(tau_AccY, adev_AccY)
B_AccZ, tauB_AccZ, lineB_AccZ, scfB_AccZ = CalculateBiasInstability(tau_AccZ, adev_AccZ)

f10 = plt.figure(10)
plt.subplot(3,1,1)
plt.plot(tau_AccX, adev_AccX, color = 'r')
plt.plot(tau_AccX, lineB_AccX, '--', color='k')
plt.plot(tauB_AccX, scfB_AccX*B_AccX, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['Acc X', 'BI = ' + str(B_AccX) + '(g)'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.title('ACCELEROMETER - BIAS INSTABILITY NOISE')
plt.subplot(3,1,2)
plt.plot(tau_AccY, adev_AccY, color = 'g')
plt.plot(tau_AccY, lineB_AccY, '--', color='k')
plt.plot(tauB_AccY, scfB_AccX*B_AccY, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['Acc Y', 'BI = ' + str(B_AccY) + '(g)'])
plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.subplot(3,1,3)
plt.plot(tau_AccZ, adev_AccZ, color = 'b')
plt.plot(tau_AccZ, lineB_AccZ, '--', color='k')
plt.plot(tauB_AccZ, scfB_AccX*B_AccZ, 'o', color = 'k', markersize=30, markerfacecolor='none')
plt.xscale("log"); plt.yscale("log");
plt.legend(['Acc Z', 'BI = ' + str(B_AccZ) + '(g)'])
plt.xlabel("TIME CLUSTER (s)"); plt.ylabel("ALLAN DEVIATION")
plt.grid(True, which="both", ls="-")
plt.show()

























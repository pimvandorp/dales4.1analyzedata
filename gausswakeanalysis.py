#!/usr/bin/bash

import numpy as np
import matplotlib.pyplot as plt
import readnamoptions as rno
from scipy.optimize import curve_fit

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
def dgaus(x,a,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+a*np.exp(-(x-x1)**2/(2*sigma**2))
def dgaus2(x,a,b,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+b*np.exp(-(x-x1)**2/(2*sigma**2))

exptitle = 'Single_turbine_Aitken_stable'
expnr = '101'
ext = '_4_6'

namopt = rno.readnamoptions(exptitle,expnr,'pim', parallel = False)
dy = namopt['dy']
dx = namopt['dx']
dz = namopt['dz']
xsize = namopt['xsize']
ysize = namopt['ysize']
zsize = namopt['zsize']
turhx = namopt['turhx']
turhy = namopt['turhy']
turhz = namopt['turhz']
turD = 2*namopt['turr']

xt = dx + dx*np.arange(0,xsize/dx)
yt = dy + dy*np.arange(0,ysize/dy)
zt = dz + dz*np.arange(0,zsize/dz)
dataxy = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + expnr + '/' + exptitle + '_' + expnr + '_vhoravg_xy' + ext + '.npy')/1000.
dataxz = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + expnr + '/' + exptitle + '_' + expnr + '_vhoravg_xz' + ext + '.npy')/1000.

Vfs_xy = np.mean(dataxy[:10,:],axis=0)
Vfs_xz = np.mean(dataxz[:,:10],axis=1)

VD_xy = (Vfs_xy-dataxy)/Vfs_xy
VD_xz = dataxz
for i, u in enumerate(zt):
    VD_xz[i,:] = (Vfs_xz[i]-dataxz[i,:])/Vfs_xz[i]

s = np.arange(0,10*turD,turD*.1)

VD_xy_max = np.zeros((len(s)))
VD_xz_max = np.zeros((len(s)))

sym = True
diag = True
if diag:
    s = [7*turD]
for i, u in enumerate(s):
    s_in = (turhx+u)/dx

    if u <= 7*turD:
        if sym:
            popt,pcov = curve_fit(dgaus,yt,VD_xy[:len(yt),s_in],p0=[0.5,350,450,30])
            fit_xy = dgaus(yt,popt[0],popt[1],popt[2],popt[3])
            #VD_xy_max[i] = popt[0]
            VD_xy_max[i] = np.amax(fit_xy)

            popt,pcov = curve_fit(dgaus,zt,VD_xz[:,s_in],p0=[0.5,50,90,30])
            fit_xz = dgaus(zt,popt[0],popt[1],popt[2],popt[3])
            #VD_xz_max[i] = popt[0]
            VD_xz_max[i]=np.amax(fit_xz)
        else:
            popt,pcov = curve_fit(dgaus2,yt,VD_xy[:len(yt),s_in],p0=[0.5,0.5,350,450,30])
            fit_xy = dgaus2(yt,popt[0],popt[1],popt[2],popt[3],popt[4])
            VD_xy_max[i] = np.amax(fit_xy)

            popt,pcov = curve_fit(dgaus2,zt,VD_xz[:,s_in],p0=[0.5,0.5,50,90,30])
            fit_xz = dgaus2(zt,popt[0],popt[1],popt[2],popt[3],popt[4])
            VD_xz_max[i]=np.amax(fit_xz)
    else:
        popt,pcov = curve_fit(gaus,yt,VD_xy[:len(yt),s_in],p0=[0.5,400,50])
        fit_xy = gaus(yt,popt[0],popt[1],popt[2])
        VD_xy_max[i] = popt[0]

        popt,pcov = curve_fit(gaus,zt,VD_xz[:,s_in],p0=[0.5,70,30])
        fit_xz = gaus(zt,popt[0],popt[1],popt[2])
        VD_xz_max[i] = popt[0]

    if diag:
        plt.figure(1)
        plt.plot(VD_xz[:,s_in],zt)
        plt.plot(fit_xz,zt)
        plt.figure(2)
        plt.plot(VD_xy[:len(yt),s_in],yt)
        plt.plot(fit_xy,yt)

if not diag:
    aitken_mean = np.loadtxt('wakemeasurements/aitken_stable.txt',skiprows=1)
    aitken_lower = np.loadtxt('wakemeasurements/aitken_stable_lower.txt')
    aitken_upper = np.loadtxt('wakemeasurements/aitken_stable_upper.txt')
    plt.plot(s/turD,VD_xy_max*100)
    plt.plot(s/turD,VD_xz_max*100)
    plt.plot(aitken_mean[:,0],aitken_mean[:,1],'bd')
    plt.plot(aitken_lower[:,0],aitken_lower[:,1], 'b')
    plt.plot(aitken_upper[:,0],aitken_upper[:,1], 'b')
    plt.xlim(1.2,6.6)
    plt.ylim(0,100)
plt.show()



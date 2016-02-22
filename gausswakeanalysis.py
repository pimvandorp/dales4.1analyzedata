#!/usr/bin/bash

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import readnamoptions as rno
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import os.path
import datetime as dt

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
def dgaus(x,a,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+a*np.exp(-(x-x1)**2/(2*sigma**2))
def dgaus2(x,a,b,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+b*np.exp(-(x-x1)**2/(2*sigma**2))


color = ['#000000','#939393','#00A6D6']

presentation = True
save = True
diag = False
mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']   

nsubfigures = 2
a4height = 11.7
a4width = 8.27
margin = .7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth
if presentation:
    def cm2inch(value):
        return value/2.54
#12.8cm x 9.6cm
    figwidth = cm2inch(9)
    figheight = cm2inch(6)

print 'figheight, figwidth = ', figheight, figwidth
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
fig1.set_size_inches(figwidth,figheight)
if diag:
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    fig2.set_size_inches(figwidth,figheight)

aitken = False
mirocha = True
kasler = False
if aitken:
    exptitle = 'Single_turbine_Aitken_stable'
    expnr = '101'
    ext = '_4_6'
elif mirocha:
    exptitle = 'Single_turbine_Mirocha_wcbl'
    expnr = '210'
    ext = '_14_179'
elif kasler:
    exptitle = 'Single_turbine_GABLS'
    expnr = '140'
    ext = '_9_179'

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

xt = 0.5*dx + dx*np.arange(0,xsize/dx)
yt = 0.5*dy + dy*np.arange(0,ysize/dy)
#zt = 0.5*dz + dz*np.arange(0,zsize/dz)
dataxy = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + expnr + '/' + exptitle + '_' + expnr + '_vhoravg_xy' + ext + '.npy')/1000.
dataxz = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + expnr + '/' + exptitle + '_' + expnr + '_vhoravg_xz' + ext + '.npy')/1000.
zt = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + expnr + '/' + exptitle + '_' + expnr + '_zt' + ext + '.npy')

Vfs_xy = np.mean(dataxy[:10,:],axis=0)
Vfs_xz = np.mean(dataxz[:,:10],axis=1)

VD_xy = (Vfs_xy-dataxy)/Vfs_xy
VD_xz = dataxz
for i, u in enumerate(zt):
    VD_xz[i,:] = (Vfs_xz[i]-dataxz[i,:])/Vfs_xz[i]

s = np.arange(0,10.1*turD,turD*.1)

VD_xy_max = np.zeros((len(s)))
VD_xz_max = np.zeros((len(s)))

if kasler:
    vertical = False
    spanwise = True
    sym = False
    dmax = 10
elif mirocha:
    vertical = True
    spanwise = False
    sym = False
    dmax = -1
elif aitken:
    vertical = True
    spanwise = False
    sym = False
    dmax = 10

if diag:
    s = [3*turD]

for i, u in enumerate(s):
    s_in = (turhx+u)/dx

    if u <= dmax*turD:
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
        ax1.plot(VD_xz[:,s_in],zt)
        ax1.plot(fit_xz,zt)
        ax2.plot(VD_xy[:len(yt),s_in],yt)
        ax2.plot(fit_xy,yt)


if not diag:
    if spanwise:
        ax1.plot(s/turD,VD_xy_max*100,'k',zorder=10,label='DALES')
    if vertical:
        ax1.plot(s/turD,VD_xz_max*100,'k',zorder=10,label='DALES')

    if aitken:
        aitken_mean = np.loadtxt('wakemeasurements/aitken_stable.txt')
        aitken_lower = np.loadtxt('wakemeasurements/aitken_stable_lower.txt')
        aitken_upper = np.loadtxt('wakemeasurements/aitken_stable_upper.txt')
        flower = interp1d(aitken_lower[:,0],aitken_lower[:,1])
        fupper = interp1d(aitken_upper[:,0],aitken_upper[:,1])
        xspread = np.linspace(1.21,6.58,100)
        ax1.plot(aitken_mean[:,0],aitken_mean[:,1],'-',color=color[2],zorder = 2, label = 'Measured')
        ax1.fill_between(xspread,flower(xspread),fupper(xspread),color=color[2],alpha=0.2,zorder = 1)
        ax1.set_xlim(1.2,6.6)
    elif mirocha:
        mirocha_mean = np.loadtxt('wakemeasurements/mirocha_wcbl.txt')
        mirocha_lower = np.loadtxt('wakemeasurements/mirocha_wcbl_lower.txt')
        mirocha_upper = np.loadtxt('wakemeasurements/mirocha_wcbl_upper.txt')
        flower = interp1d(mirocha_lower[:,0],mirocha_lower[:,1])
        fupper = interp1d(mirocha_upper[:,0],mirocha_upper[:,1])
        xspread = np.linspace(0.2,5.5,100)
        ax1.plot(mirocha_mean[:,0],mirocha_mean[:,1],'-',color=color[2],zorder = 2, label = 'Measured')
        ax1.fill_between(xspread,flower(xspread),fupper(xspread),color=color[2],alpha=0.2,zorder = 1)
        ax1.set_xlim(0.2,5.5)
    elif kasler:
        kasler_mean = np.loadtxt('wakemeasurements/kasler_stable.txt')
        ax1.plot(kasler_mean[:,0],kasler_mean[:,1],'.',color=color[2],zorder = 2, label = 'Measured')
        ax1.set_xlim(0,10)

    ax1.set_ylim(0,100)

plt.xlabel('Distance from wind turbine $[D]$')
plt.ylabel('Velocity deficit $[\%]$')
if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax1.set_xticklabels(ax1.get_xticks(), fontProperties)
    ax1.set_yticklabels(ax1.get_yticks(), fontProperties)
    ax1.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%0.0f'))
    ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%0.0f'))

ax1.legend(loc = 'best',frameon = False,fontsize = 10)

figuredir = '/home/pim/figures/validation/'
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)
if aitken:
    filename = 'aitken_stable'
elif mirocha:
    filename = 'mirocha_wcbl'
elif kasler:
    filename = 'kasler_stable'
if presentation:
    filename += '_presentation'
tdy = dt.datetime.today()
filename += '_' + tdy.strftime('%d%m_%H%M%S')
figurepath = figuredir + filename + '.pdf'
if save:
    fig1.savefig(figurepath,bbox_inches='tight')
else:
    plt.show()



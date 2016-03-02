#!/usr/bin/bash

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import readnamoptions as rno
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import os.path
import datetime as dt
from scipy import interpolate

def gaus(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
def dgaus(x,a,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+a*np.exp(-(x-x1)**2/(2*sigma**2))
def dgaus2(x,a,b,x0,x1,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+b*np.exp(-(x-x1)**2/(2*sigma**2))

colorexp = ['#00A6D6','#000000','#939393']

presentation = False
save = True
diag = False
interp = False
mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']   

nsubfigures = 2
a4height = 11.7
a4width = 8.27
margin = .7
figwidth = (a4width-2*margin)/float(nsubfigures)+0.1
figheight = 0.6*figwidth
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

exptitle = 'Single_turbine_EUROCS'
expnr = ['450', '461'] 
ext = ['_659_719', '_1379_1439']
markertime = ['-', ':'] 
labelcase = ['Clouds (daytime)', 'Clouds (nighttime)', 'No clouds (daytime)', 'No clouds (nighttime)']

n = 0
for e,ee in enumerate(expnr):
    for j, jj in enumerate(ext):
        namopt = rno.readnamoptions(exptitle,ee,'pim', parallel = False)
        dy = namopt['dy']
        dx = namopt['dx']
        dz = namopt['dz']
        xsize = namopt['xsize']
        ysize = namopt['ysize']
        zsize = namopt['zsize']
        turhx = 393.75#namopt['turhx']
        turhy = 1243.750  #namopt['turhy']
        turhz = 70#namopt['turhz']
        turD = 80#2*namopt['turr']

        xt = 0.5*dx + dx*np.arange(0,xsize/dx)
        yt = 0.5*dy + dy*np.arange(0,ysize/dy)
        #zt = 0.5*dz + dz*np.arange(0,zsize/dz)
        dataxy = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + ee + '/' + exptitle + '_' + ee + '_vhoravg_xy' + jj + '.npy')/1000.
        dataxz = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + ee + '/' + exptitle + '_' + ee + '_vhoravg_xz' + jj + '.npy')/1000.
        zt = np.load('/nfs/livedata/pim/binary_fd_data/wakeanalysis/' + exptitle + '/' + ee + '/' + exptitle + '_' + ee + '_zt' + jj + '.npy')

        Vfs_xy = np.mean(dataxy[:10,:],axis=0)
        Vfs_xz = np.mean(dataxz[:,:10],axis=1)


        VD_xy = (Vfs_xy-dataxy)/Vfs_xy
        VD_xz = dataxz
        for i, u in enumerate(zt):
            VD_xz[i,:] = (Vfs_xz[i]-dataxz[i,:])/Vfs_xz[i]

        s = np.arange(0,10.1*turD,turD*.2)
        sinterp = np.arange(0,10,0.005)

        VD_xy_max = np.zeros((len(s)))
        VD_xz_max = np.zeros((len(s)))

        vertical = False
        spanwise = True
        sym = False
        dmax = -1

        if diag:
            s = [1*turD]

        s_in = np.arange(32,len(s)+32)
        for i, u in enumerate(s_in):

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
                popt,pcov = curve_fit(gaus,yt,VD_xy[:len(yt),u],p0=[0.5,1200,50])
                fit_xy = gaus(yt,popt[0],popt[1],popt[2])
                VD_xy_max[i] = popt[0]

                popt,pcov = curve_fit(gaus,zt,VD_xz[:,u],p0=[0.5,70,30])
                fit_xz = gaus(zt,popt[0],popt[1],popt[2])
                VD_xz_max[i] = popt[0]

            if diag:
                ax1.plot(VD_xz[:,u],zt)
                ax1.plot(fit_xz,zt)
                ax2.plot(VD_xy[:len(yt),u],yt)
                ax2.plot(fit_xy,yt)

        if not diag:
            if spanwise:
                if interp:
                    f = interpolate.interp1d(s/turD,VD_xy_max*100,kind='linear')
                    ax1.plot(sinterp,f(sinterp),markertime[j], color = colorexp[e],zorder=10,label=labelcase[n])
                else:
                    ax1.plot(s/turD,VD_xy_max*100,markertime[j], color = colorexp[e],zorder=10,label=labelcase[n])
            if vertical:
                ax1.plot(s/turD,VD_xz_max*100,'k',zorder=10,label='DALES')
            
        n += 1

ax1.set_ylim(0,100)

plt.xlabel('Distance from wind turbine $[D]$')
plt.ylabel('Velocity deficit $[\%]$')
if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax1.set_xticklabels(ax1.get_xticks(), fontProperties)
    ax1.set_yticklabels(ax1.get_yticks(), fontProperties)
    ax1.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%0.0f'))
    ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%0.0f'))

ax1.legend(loc = 'best',frameon = False,fontsize = 8)

figuredir = '/home/pim/figures/Single_turbine_EUROCS/'
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)
filename = 'EUROCS_wakeanalysis'
if presentation:
    filename += '_presentation'
tdy = dt.datetime.today()
filename += '_' + tdy.strftime('%d%m_%H%M%S')
figurepath = figuredir + filename + '.pdf'
if save:
    fig1.savefig(figurepath,bbox_inches='tight')
else:
    plt.show()



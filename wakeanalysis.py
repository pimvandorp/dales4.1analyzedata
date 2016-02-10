#!/usr/bin/python
# Filename: wakeanalysis.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics
# Description: 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import os.path
import os

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx
#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------
presentation = True

mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']   
    mpl.rcParams['font.sans-serif']='cm'


username = 'pim'

cbl = 'Single_turbine_CBL'
sbl = 'Single_turbine_GABLS'
nbl = 'Single_turbine_NBL'

exptitle = [cbl]
expnr = ['306','257']
labels = ['CBL', 'NBL']
#labels = ['SBL', 'NBL', 'CBL']

marker = ['-', '-', '-']

color = ['#939393','#00A6D6']
#color = ['#000000','#00A6D6','#939393']

xfs = [2500,2000]

xmin = 0
xmax = 2000
zmin = 0
zmax = 300

save = False

verticalanalysis = True
xval = [200,1000]

spanwiseanalysis = False

axisanalysis = False
plotDelV = False
plotV = False
plotdif = False
tophat = False
ntophat = 2
kwake = [0.05, 0.075]

nsubfigures = 1
a4height = 11.7
a4width = 8.27
margin = 1.7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth*0.5

tura = 0.25
gamma = ((1-tura)/(1-2*tura))**0.5
Ct=1-(1-tura)**2

figuredir = '/home/%s/figures/wakeanalysis' % (username)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = 'Wakeanalysis'
for i,v in enumerate(expnr):
    filename += '_%s' % v
    
tdy = dt.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

fig = plt.figure()
ax = plt.subplot(111)
fig.set_size_inches(figwidth,figheight)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

datadir = '/home/%s/dales4.1analyzedata/wakeanalysis/data' % (username)

if verticalanalysis:
    for i,v in enumerate(exptitle):
        for j,w in enumerate(xval):
            filename = '%s_%s_vhoravg_xz.npy' % (v, expnr[i])
            datapath = datadir + '/%s' % (filename)
            vhoravg_xz = np.load(datapath)/1000.

            filename = '%s_%s_zt.npy' % (v, expnr[i])
            datapath = datadir + '/%s' % (filename)
            z = np.load(datapath)
            zmin_in = find_nearest(z,zmin)
            zmax_in = find_nearest(z,zmax)

            filename = '%s_%s_xt.npy' % (v, expnr[i])
            datapath = datadir + '/%s' % (filename)
            x = np.load(datapath)
            xval_in = find_nearest(x,w)
            xfs_in = find_nearest(x,xfs[i])

            filename = '%s_%s_Vw_ax.npy' % (v, expnr[i])
            datapath = datadir + '/%s' % (filename)
            Vwax = np.load(datapath)/1000.
            Vfs = Vwax[xfs_in]
            print 'Vfs based on max = ', Vfs 
            DelV = (Vfs - vhoravg_xz)/Vfs

            plt.plot(DelV[zmin_in:zmax_in,xval_in],z[zmin_in:zmax_in],marker[i],color=color[i], label=labels[i],linewidth=0.8)


if axisanalysis:
    for i,v in enumerate(exptitle):
        Vwax = 0
        Vfs = 0
        filename = '%s_%s_Vw_ax.npy' % (v, expnr[i])
        datapath = datadir + '/%s' % (filename)

        Vwax = np.load(datapath)/1000.

        filename = '%s_%s_xt.npy' % (v, expnr[i])
        datapath = datadir + '/%s' % (filename)

        x = np.load(datapath)
        xmin_in = find_nearest(x,xmin)
        xmax_in = find_nearest(x,xmax)
        xfs_in = find_nearest(x,xfs[i])
        
        x = x/100.

        Vfs = Vwax[xfs_in]
        print 'Vfs based on max = ', Vfs 
        DelVwax = (Vfs - Vwax)/Vfs

        if plotDelV:
            plt.plot(x[xmin_in:xmax_in],DelVwax[xmin_in:xmax_in],marker[i],color=color[i], label=labels[i],linewidth=0.8)
        elif plotV:
            plt.plot(x[xmin_in:xmax_in],Vwax[xmin_in:xmax_in],marker[i],color=color[i], label=labels[i],linewidth=0.8)
        elif plotdif:
            plt.plot(x[xmin_in:xmax_in-1],np.diff(Vwax[xmin_in:xmax_in]),marker[i],color=color[i], label=labels[i],linewidth=0.8)

    if tophat:
        for i in range(0,ntophat):
            xtophat = np.arange(xmin,xmax,1)
            wakeDelVth= (2*tura)/((1+kwake[i]*xtophat/(gamma*50))**2)
            xtophat = xtophat/100.
            ax.plot(xtophat,wakeDelVth,'g',label='Jensen model, $\kappa_{\mathrm{wake}}$ = %s' % kwake[i])

    plt.xlim(2,xmax/100.)
    plt.xlabel('$x/D$')
    plt.ylabel('$\left(\Delta V/V_{\infty}\\right)_{\mathrm{max}}$')

if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax.set_xticklabels(ax.get_xticks(), fontProperties)
    ax.set_yticklabels(ax.get_yticks(), fontProperties)

if save:
    plt.savefig(figurepath,bbox_inches='tight')
else:
    plt.show()

plt.close()





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

username = 'pim'

cbl = 'Single_turbine_CBL'
sbl = 'Single_turbine_GABLS'
nbl = 'Single_turbine_NBL'

exptitle = [sbl,cbl]#, nbl,nbl, cbl, cbl]
expnr = ['103','305']#'203','251', '301', '350']
labels = ['SBL-GABLS1', 'TNBL', 'CNBL-REF', 'CBL-W06', 'CBL-S024']
marker = ['xk', 'xb', ':b', '-r', ':r']

xmin = 200 
xmax = 2000

save = False
show = True

plotDelV = True
plotV = False

tophat = True
ntophat = 1
kwake = [0.075]

nsubfigures = 1
a4height = 11.7
a4width = 8.27
margin = 1.7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth

tura = 0.25
gamma = ((1-tura)/(1-2*tura))**0.5
Ct=1-(1-tura)**2

figuredir = '/home/%s/figures/%s' % (username,exptitle)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = 'Wakeanalysis_'
for i,v in enumerate(expnr):
    filename += '_%s' % v
    
tdy = dt.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

fig = plt.figure()
ax = plt.subplot(111)
fig.set_size_inches(figwidth,figheight)

font = {'family' : 'computer modern',
    'weight' : 'bold',
    'size'   : 10}
mpl.rc('font', **font)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

datadir = '/home/%s/dales4.1analyzedata/wakeanalysis/data' % (username)

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

    #Vwaxdiff = np.diff(Vwax[xmin_in:xmax_in])
    #inds = []
    #for j,w in enumerate(Vwaxdiff):
    #    if w<0.001 and w>0 and j>30:
    #        inds.append(j)
    #print inds
    #print 'Vwax[inds[0]] = ', Vwax[inds[0]]
    #Vfs = np.mean(Vwax[inds[0]:])
    #print 'Vfs based on mean = ', Vfs
    Vfs = np.amax(Vwax[xmin_in:])
    print 'Vfs based on max = ', Vfs 
    DelVwax = (Vfs - Vwax)/Vfs

    if plotDelV:
        plt.plot(x[xmin_in:xmax_in],DelVwax[xmin_in:xmax_in],marker[i], label=labels[i],linewidth=0.8)
    elif plotV:
        plt.plot(x[xmin_in:xmax_in],Vwax[xmin_in:xmax_in],marker[i], label=labels[i],linewidth=0.8)

if tophat:
    xtophat = np.arange(xmin,xmax,1)
    for i in range(0,ntophat):
        wakeDelVth= (2*tura)/((1+kwake[i]*xtophat/(gamma*50))**2)
        ax.plot(xtophat,wakeDelVth,'g',label='Jensen model, $\kappa_{\mathrm{wake}}$ = %s' % kwake[i])
plt.xlim(xmin,xmax)
plt.xlabel('$x$')
plt.ylabel('$\Delta V/V_{\infty}$')
if show:
    plt.show()
if save:
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()





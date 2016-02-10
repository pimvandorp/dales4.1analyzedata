#!/usr/bin/python
# Filename: turbanalysis.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics
# Description: 

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
import datetime as dt
import readnamoptions as rno
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

eurocs = True
gabls = False
cbl = False
nbl = False

expnr = '410'

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if cbl:
    exptitle = 'Single_turbine_CBL'
if nbl:
    exptitle = 'Single_turbine_NBL'

save = False

prop = 'vhor'

subgrid = False
resTKE = False
plotxy = True
plotxz = False

xmin = -100 
if cbl:
    xmax = 2000
else:
    xmax = 2000
ymin = -200
ymax = 200
zmin = 0
zmax = 250

nsubfigures = 1
a4height = 11.7
a4width = 8.27
margin = 1.7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth

figuredir = '/home/%s/figures/turbanalysis' % (username)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

if subgrid:
    prop = 'e12'

if resTKE:
    prop = 'TKE'

if plotxy:
    plane = 'x_y'
else:
    plane = 'x_z'

filename = 'turbanalysis_%s_%s_%s_%s' % (exptitle, expnr, prop, plane)
    
tdy = dt.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

fig = plt.figure(1)
ax1 = fig.add_subplot(1,1,1,aspect='equal')

fig.set_size_inches(figwidth,figheight)

datadir = '/home/%s/dales4.1analyzedata/turbanalysis/data' % (username)

if resTKE:
    filename = '%s_%s_TKE_xz.npy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    TKE_xz = np.load(datapath)/1E6
    print 'shape xz = ', np.shape(TKE_xz)

    filename = '%s_%s_TKE_xy.npy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    TKE_xy = np.load(datapath)/1E6
    print 'shape xy = ', np.shape(TKE_xy)

elif subgrid:
    filename = '%s_%s_e12_xz.npy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    e12_xz = np.load(datapath)/1E3

    filename = '%s_%s_e12_xy.npy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    e12_xy = np.load(datapath)/1E3
else:
    filename = '%s_%s_%swavg_xy.npy' % (exptitle, expnr,prop)
    datapath = datadir + '/%s' % (filename)
    propwavg_xy = np.load(datapath)/1E6

    filename = '%s_%s_%swavg_xz.npy' % (exptitle, expnr,prop)
    datapath = datadir + '/%s' % (filename)
    propwavg_xz = np.load(datapath)/1E6


filename = '%s_%s_xt.npy' % (exptitle, expnr)
datapath = datadir + '/%s' % (filename)
x = np.load(datapath)
xmin_in = find_nearest(x,xmin)
xmax_in = find_nearest(x,xmax)
print 'xmin, xmax', xmin_in , xmax_in
filename = '%s_%s_yt.npy' % (exptitle, expnr)
datapath = datadir + '/%s' % (filename)
y = np.load(datapath)
ymin_in = find_nearest(y,ymin)
ymax_in = find_nearest(y,ymax)
print 'ymin, ymax', ymin_in , ymax_in
filename = '%s_%s_zt.npy' % (exptitle, expnr)
datapath = datadir + '/%s' % (filename)
z = np.load(datapath)
zmin_in = find_nearest(z,zmin)
zmax_in = find_nearest(z,zmax)
print 'zmin, zmax', zmin_in , zmax_in

if plotxy:
    if subgrid:
        CF1 = ax1.contourf(x[xmin_in:xmax_in],y[ymin_in:ymax_in],e12_xy[ymin_in:ymax_in,xmin_in:xmax_in],100,rasterized=True)
    elif resTKE:
        print 'shape x,y = ', np.shape(x[xmin_in:xmax_in]), np.shape(y[ymin_in:ymax_in]), np.shape(TKE_xy[ymin_in:ymax_in,xmin_in:xmax_in])
        CF1 = ax1.contourf(x[xmin_in:xmax_in],y[ymin_in:ymax_in],TKE_xy[ymin_in:ymax_in,xmin_in:xmax_in],100,rasterized=True)
    else:
        CF1 = ax1.contourf(x[xmin_in:xmax_in],y[ymin_in:ymax_in],propwavg_xy[ymin_in:ymax_in,xmin_in:xmax_in],100,rasterized=True)
    ax1.set_yticks([-100,0,100])
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
elif plotxz:
    if subgrid:
        CF1 = ax1.contourf(x[xmin_in:xmax_in],z[zmin_in:zmax_in],e12_xz[zmin_in:zmax_in,xmin_in:xmax_in],100,rasterized=True)
    elif resTKE:
        CF1 = ax1.contourf(x[xmin_in:xmax_in],z[zmin_in:zmax_in],TKE_xz[zmin_in:zmax_in,xmin_in:xmax_in],100,rasterized=True)
    else:
        CF1 = ax1.contourf(x[xmin_in:xmax_in],z[zmin_in:zmax_in],propwavg_xz[zmin_in:zmax_in,xmin_in:xmax_in],100,rasterized=True)
    ax1.set_yticks([0,200])
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$z$')

for c in CF1.collections:
    c.set_edgecolor("face")

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)

cbar1 = plt.colorbar(CF1, cax = cax1,ticks=[-4,0,4])
tick_locator = ticker.MaxNLocator(nbins=7)
cbar1.locator = tick_locator
cbar1.update_ticks()

if save:
    fig.savefig(figurepath,bbox_inches='tight',format='pdf')
else:
    plt.show()



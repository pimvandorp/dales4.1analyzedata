#!/usr/bin/python
#Filename: readprofiles.py
#Description: read profiles.nc file from DALES

import numpy as np
import pupynere as pu
import readnamoptions as rno
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import os.path
import os

hour = 3600

def readprop(exptitle,expnr,prop,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    f = pu.netcdf_file(expdir + '/profiles.%s.nc' % (expnr))

    # columns of data
    zt = f.variables['zt'][:] # full levels
    zm = f.variables['zm'][:] # half levels

    # rows of data
    time = f.variables['time'][:]

    prop = f.variables[prop][:,:] 

    return {'zt' : zt, 'zm' : zm, 'time': time, 'prop':prop} 

def readproptmser(exptitle,expnr,prop,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    f = pu.netcdf_file(expdir + '/tmser.%s.nc' % (expnr))

    time = f.variables['time'][:]

    prop = f.variables[prop][:] 

    return {'time': time, 'prop':prop} 

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

#---------------------
#   General input
#---------------------
username = 'pim'
optpath = 'refcases'

save = False
show = False
if not save:
    show = True

cbl = 'Single_turbine_CBL'
sbl = 'Single_turbine_GABLS'
nbl = 'Single_turbine_NBL'

exptitle = [sbl, nbl,nbl, cbl, cbl]
expnr = ['102','203','251', '301', '350']
labels = ['SBL-GABLS1', 'TNBL', 'CNBL-REF', 'CBL-W06', 'CBL-S024']
marker = ['-k', '-b', ':b', '-r', ':r']

# time settings
t_start = 5*hour
t_end = 6*hour

#---------------------
#     Properties
#---------------------
# wthvt = buoyancy flux; wthlt = total theta_l flux; thv = virtual pot. temp; thl = liq. pot. temp; w2r = vert. velocity variance; uwt/vwt = vertical momentum fluxes
# tmser.nc: lwp_bar, zb, zc_av
# Use wthvt instead of wthlt when no difference to get lowest level right
prop = 'vwt' 

normprop = False

#---------------------
#   profiles.nc
#---------------------
readprof = True

timeseries = False
height_av = False

zser = True
zmin = 0 
zmax = 1500

trans = False

#---------------------
#      tmser.nc
#---------------------
readtmser = False
if not readprof:
    readtmser = True

#---------------------
#    Plot options
#---------------------

nsubfigures = 2
a4height = 11.7
a4width = 8.27
margin = .7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth
print 'figheight, figwidth = ', figheight, figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

# Axes
#ax.set_xlim((-0.1,2))
ax.set_ylim((0,1500))

# Labels
if readprof:
    ax.set_ylabel('$z \ \mathrm{[m]}$')
    if prop == 'w2r':
        ax.set_xlabel('$\mathrm{Vertical \ velocity \ variance} \ \mathrm{[m^2/s^2]}$')
    elif prop == 'wthvt' or prop=='wthlt':
        ax.set_xlabel('$\mathrm{Buoyancy \ flux} \\times 10^4 \  \mathrm{[m^2/s^3]}$')
    elif prop == 'thl':
        ax.set_xlabel('$\\theta(z)-\\theta(0) \ \mathrm{[K]}$')
    elif prop == 'Vwt':
        ax.set_xlabel('$\mathrm{Tot. \ vertical \ momentum \ flux} \ \mathrm{[m^2/s^2]}$')
else:
    ax.set_xlabel('$t \ \mathrm{[h]}$')
    if prop == 'lwp_bar':
        ax.set_xlabel('$\mathrm{LWP} \ \mathrm{[g/m^2]}$')

figuredir = '/home/%s/figures/profilesanalysis/%s' % (username, optpath)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

if readprof:
    filename = 'profile'
else:
    filename = 'tmser'
filename += '_%s'% prop
for i,v in enumerate(expnr):
    filename += '_%s' % v
    
tdy = datetime.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

font = {'family' : 'computer modern',
    'weight' : 'bold',
    'size'   : 10}
mpl.rc('font', **font)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

for i,u in enumerate(exptitle):
    if readprof:
        if prop == 'Vwt':
            data = readprop(u,expnr[i],'uwt')
            datavw = readprop(u,expnr[i],'vwt')
            p = data['prop']+datavw['prop']
        else:
            data = readprop(u,expnr[i],prop)
            p = data['prop']

        if prop == 'wthvt' or prop=='wthlt':
            th0 = readprop(u,expnr[i],'thl')['prop'][0]
            p = (9.81/th0)*p*10000

        time = data['time']
        t_start_in = find_nearest(time,t_start)
        t_end_in = find_nearest(time,t_end)
        time = time/3600.

        zt = data['zt']
        zm = data['zm']
        if v == 'w2r' or v == 'uwt' or v == 'wthvt' or v == 'Vwt' or v == 'vwt':
                z = zm 
            else:
                z = zt

        if timeseries:
            zmin_in = find_nearest(z,zmin)
            if height_av:
                zmax_in = find_nearest(z,zmax)
            else:
                zmax_in = zmin_in+1
                p = np.mean(p[:,zmin_in:zmax_in],axis=1)
                plt.plot(time,p[t_start_in:t_end_in])
        elif zser:
            p = np.mean(p[t_start_in:t_end_in,:],axis=0)
            if normprop:
                p = p/np.amax(p)
            if trans:
                p = p - p[0]
            zmin_in = find_nearest(z,zmin)
            zmax_in = find_nearest(z,zmax)
            plt.plot(p[zmin_in:zmax_in],z[zmin_in:zmax_in],marker[i], label=labels[i],linewidth=0.8)
    elif readtmser:
        data = readproptmser(u,expnr[i],prop)

        time = data['time']
        t_start_in = find_nearest(time,t_start)
        t_end_in = find_nearest(time,t_end)
        time = time/3600.

        p = data['prop']

        if prop=='lwp_bar':
            p = p*1000

        plt.plot(time[t_start_in:t_end_in],p[t_start_in:t_end_in],marker[i], label=labels[i],linewidth=0.8)

if show:
    plt.show()
if save:
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()




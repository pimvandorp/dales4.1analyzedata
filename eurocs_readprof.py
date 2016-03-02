#!/usr/bin/python
#Filename: readprofiles.py
#Description: read profiles.nc file from DALES

import numpy as np
import pupynere as pu
import readnamoptions as rno
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker
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
optpath = 'eurocs'
presentation = False

mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']   

save = True
show = False
if not save:
    show = True

eurocs = 'Single_turbine_EUROCS'

exptitle = [eurocs, eurocs]
#expnr = ['400','402']
expnr = ['450','461']


label = ['Cloudy', 'Clear'] 
marker = ['-', ':']
colorexp = ['#00A6D6','#000000','#939393']

# time settings
t_start = [11*hour, 23*hour] 
t_end = [12*hour, 24*hour]

#---------------------
#     Properties
#---------------------
# wthvt = buoyancy flux; wthlt = total theta_l flux; thv = virtual pot. temp; thl = liq. pot. temp; w2r = vert. velocity variance; uwt/vwt = vertical momentum fluxes
# tmser.nc: lwp_bar, zb, zc_av
# Use wthvt instead of wthlt when no moist to get lowest level right
#prop = ['lwp_bar'] 
prop = ['wthvt']

normprop = False

#---------------------
#   profiles.nc
#---------------------
readprof = True

timeseries = False
height_av = False

zser = True
zmin = 0 
zmax = 700

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
if nsubfigures == 1:
    margin = 2
else:
    margin = 1.5
figwidth = (a4width-2*margin)/float(nsubfigures)
if prop == 'lwp_bar': 
    figheight = figwidth/3.
else:
    figheight = figwidth

if presentation:
    def cm2inch(value):
        return value/2.54
#12.8cm x 9.6cm
    #figwidth = cm2inch(5)
    figwidth = cm2inch(10)
    figheight = cm2inch(5)

print 'figheight, figwidth = ', figheight, figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

# Axes
if prop[0] == 'w2r':
    ax.set_xlim((0,0.3))
    ax.set_ylim((0,zmax))

# Labels
if readprof:
    ax.set_ylabel('Height [m]')
    if prop[0] == 'w2r':
        ax.set_xlabel('$\mathrm{Vertical \ velocity \ variance} \ \mathrm{[m^2/s^2]}$')
    elif prop[0] == 'wthvt':
        ax.set_xlabel('$\mathrm{Buoyancy \ flux} \\times 10^4 \  \mathrm{[m^2/s^3]}$')
    elif prop[0] == 'thl':
        ax.set_xlabel('$\\theta(z)-\\theta(0) \ \mathrm{[K]}$')
    elif prop[0] == 'Vwt':
        ax.set_xlabel('$\mathrm{Tot. \ vertical \ momentum \ flux} \ \mathrm{[m^2/s^2]}$')
else:
    ax.set_xlabel('$t \ \mathrm{[h]}$')
    if prop[0] == 'lwp_bar':
        ax.set_ylabel('$\mathrm{LWP} \ \mathrm{[g/m^2]}$')


figuredir = '/home/%s/figures/profilesanalysis/%s' % (username, optpath)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

if readprof:
    filename = 'profile'
else:
    filename = 'tmser'
for i,u in enumerate(prop):
    filename += '_%s'% u
filename += '_%s_%s' % (int((t_start[0])/3600.), int((t_end[0])/3600.))
for i,u in enumerate(expnr):
    filename += '_%s' % u
    
tdy = datetime.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

for i,u in enumerate(exptitle):
    for j,v in enumerate(prop):
        for t, tt in enumerate(t_start):
            if readprof:
                if v == 'Vwt':
                    data = readprop(u,expnr[i],'uwt')
                    datavw = readprop(u,expnr[i],'vwt')
                    p = data['prop']+datavw['prop']
                else:
                    data = readprop(u,expnr[i],v)
                    p = data['prop']

                if v == 'wthvt' or v=='wthlt':
                    th0 = readprop(u,expnr[i],'thl')['prop'][0]
                    p = (9.81/th0)*p*10000

                time = data['time']
                t_start_in = find_nearest(time,t_start[t])
                t_end_in = find_nearest(time,t_end[t])
                time = time/3600.

                zt = data['zt']
                zm = data['zm']
                if v == 'w2r' or v == 'uwt' or v == 'wthvt':
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
                    plt.plot(p[zmin_in:zmax_in],z[zmin_in:zmax_in],marker[t],color=colorexp[i],label=label[i], linewidth=0.8)
            elif readtmser:
                data = readproptmser(u,expnr[i],v)
                time = data['time']
                t_start_in = find_nearest(time,t_start[t])
                t_end_in = find_nearest(time,t_end[t])
                print t_start_in, t_end_in
                time = time/3600.

                p = data['prop']

                if v=='lwp_bar':
                    p = p*1000

                plt.plot(time[t_start_in:t_end_in],p[t_start_in:t_end_in],marker[t],color=colorexp[i],label=label[i],linewidth=0.8)

if presentation:
    if day:
        plt.title('11.00-12.00')
    elif night:
        plt.title('23.00-24.00')

    if prop[0] == 'w2r':
        ax.set_xticks([0,0.1,0.2,0.3])
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax.set_xticklabels(ax.get_xticks(), fontProperties)
    ax.set_yticklabels(ax.get_yticks(), fontProperties)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
    #ax.legend(fontsize=8,frameon=False)#,loc=2)

if prop[0] == 'w2r':
    ax.set_xticks([0,0.1,0.2,0.3])
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
if prop[0] == 'wthvt':
    ax.set_xticks(np.arange(-6,10,2))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
ax.set_yticks(np.arange(100,800,100))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

if show:
    plt.show()
if save:
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()




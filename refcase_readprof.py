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

    p = f.variables[prop][:,:] 

    return {'zt' : zt, 'zm' : zm, 'time': time, prop:p} 

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

presentation = True

mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']   

save = True
show = False
if not save:
    show = True

cbl = 'Single_turbine_CBL'
sbl = 'Single_turbine_GABLS'
nbl = 'Single_turbine_NBL'

exptitle = [sbl, nbl,cbl]

expnr = ['110','255','301']

labels = ['SBL', 'NBL', 'CBL']

markerexp = ['-', '-', '-', '-r', ':r']
colorexp = ['#000000','#00A6D6','#939393']

# time settings
t_start = 5*hour
t_end = 7*hour

#---------------------
#     Properties
#---------------------
# wthvt = buoyancy flux; wthlt = total theta_l flux; thv = virtual pot. temp; thl = liq. pot. temp; w2r = vert. velocity variance; uwt/vwt = vertical momentum fluxes
# tmser.nc: lwp_bar, zb, zc_av
# Use wthvt instead of wthlt when no difference to get lowest level right
prop = ['vhor'] 

normprop = False

#---------------------
#   profiles.nc
#---------------------
readprof = True

timeseries = False
height_av = False

zser = True
zmin = 0 
zmax = 1200

trans = False
if prop[0] == 'thl':
    trans = True


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
if presentation:
    def cm2inch(value):
        return value/2.54
#12.8cm x 9.6cm
    figwidth = cm2inch(6.5)
    figheight = cm2inch(6.5)

print 'figheight, figwidth = ', figheight, figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

# Axes
ax.set_xlim((1,9))
ax.set_ylim((0,zmax))

# Labels
if readprof:
    ax.set_ylabel('$z \ \mathrm{[m]}$')
    if prop[0] == 'w2r':
        #ax.set_xlabel('$\mathrm{Vertical \ velocity \ variance} \ \mathrm{[m^2/s^2]}$')
        ax.set_xlabel('$\overline{w\'w\'} \ \mathrm{[m^2/s^2]}$')
    elif prop[0] == 'wthvt' or prop[0]=='wthlt':
        ax.set_xlabel('$\mathrm{Buoyancy \ flux} \\times 10^4 \  \mathrm{[m^2/s^3]}$')
    elif prop[0] == 'thl':
        ax.set_xlabel('$\\theta(z)-\\theta(0) \ \mathrm{[K]}$')
    elif prop[0] == 'uwt':
        ax.set_xlabel('$\overline{uw} \ \mathrm{[m^2/s^2]}$')
    elif prop[0] == 'vwt':
        ax.set_xlabel('$\overline{vw} \ \mathrm{[m^2/s^2]}$')
    elif prop[0] == 'vhor':
        #ax.set_xlabel('$\sqrt{u^2+v^2} \ \mathrm{[m/s]}$')
        ax.set_xlabel('$V \ \mathrm{[m/s]}$')
    elif prop[0] == 'Vwt':
        ax.set_xlabel('$\mathrm{Tot. \ vert. \ momentum \ flux} \ \mathrm{[m^2/s^2]}$')
    elif prop[0] == 'tkeres':
        ax.set_xlabel('$\mathrm{TKE} \ \mathrm{[m^2/s^2]}$')
else:
    ax.set_xlabel('$t \ \mathrm{[h]}$')
    if prop[0] == 'lwp_bar':
        ax.set_xlabel('$\mathrm{LWP} \ \mathrm{[g/m^2]}$')

figuredir = '/home/%s/figures/profilesanalysis/%s' % (username, optpath)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

if readprof:
    filename = 'profile'
else:
    filename = 'tmser'
filename += '_%s'% prop[0]
for i,v in enumerate(expnr):
    filename += '_%s' % v
    
tdy = datetime.datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

for i,u in enumerate(exptitle):
    for j,v in enumerate(prop):
        print 'Plotting: ', u
        print 'v =', v

        if readprof:
            if v == 'Vwt':
                data = readprop(u,expnr[i],'uwt')
                datav = readprop(u,expnr[i],'vwt')
                p = data['uwt'] + datav['vwt']
            elif v == 'vhor':
                data = readprop(u,expnr[i],'u')
                datav = readprop(u,expnr[i],'v')
                p = (data['u']**2+datav['v']**2)**0.5
            elif v == 'tkeres':
                data = readprop(u,expnr[i],'u2r')
                datav = readprop(u,expnr[i],'v2r')
                dataw = readprop(u,expnr[i],'w2r')
                p = data['u2r']+datav['v2r']+dataw['w2r']
            else:
                data = readprop(u,expnr[i],v)
                p = data[v]

            if v == 'wthvt' or v =='wthlt':
                th0 = readprop(u,expnr[i],'thl')['thl'][0]
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
                plt.plot(p[zmin_in:zmax_in],z[zmin_in:zmax_in],markerexp[i],color=colorexp[i], label=labels[i],linewidth=0.8)
        elif readtmser:
            data = readproptmser(u,expnr[i],v)

            time = data['time']
            t_start_in = find_nearest(time,t_start)
            t_end_in = find_nearest(time,t_end)
            time = time/3600.

            p = data[v]

            if v=='lwp_bar':
                p = p*1000

            plt.plot(time[t_start_in:t_end_in],p[t_start_in:t_end_in],markerexp[i],color=colorexp[i], label=labels[i],linewidth=0.8)

if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax.set_xticklabels(ax.get_xticks(), fontProperties)
    ax.set_yticklabels(ax.get_yticks(), fontProperties)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

    #ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
    #ax.legend(fontsize=8,frameon=False,loc=2)
    ax.legend(fontsize=8,frameon=False,loc='upper left')
    ax.set_xticks(np.arange(2,10,2))
    #ax.set_xticks(np.arange(.1,.7,.2))
    #ax.set_xticks(np.arange(-1,4))
    #ax.set_yticks(np.arange(0,500,100))

ax.set_xticks(np.arange(2,10,2))
ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))


if show:
    plt.show()
if save:
    print 'Saving figure'
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()




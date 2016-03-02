#!/usr/bin/python
#Filename: animatefielddump.py
#Description: make an animation of snapshot contours

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
import pupynere as pu
import readfielddump as rfd
import readnamoptions as rno
import datetime as dt
import os
import os.path
import subprocess
import matplotlib.cm as cm


presentation = True

mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath']   

username = 'pim'

#exptitle = 'Hornsrev_wakeclouds'
exptitle = 'NorthHoyle_NBL'
expnr = '102'

prop = 'vhoravg' # property to be analysed (u,v,w,etc.)  

trange=[119,179]
t_start_in=0
t_end_in= trange[1] - trange[0] - 1

nFrames = t_end_in-t_start_in
print 'nFrames = ', nFrames

print 'Loading array from disk'
datadir = '/nfs/livedata/pim/fielddumpdata/%s/%s' % (exptitle,expnr)

filename = '%s_%s_%s_%s_%s.nc' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

f = pu.netcdf_file(datapath)

pfull = f.variables[prop][:,:,:]
x = f.variables['xt'][:]/1000.
y = f.variables['yt'][:]/1000.

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(10,8)

tempdir = './animtemp/%s/%s' % (exptitle,expnr)
if not os.path.isdir(tempdir):
    os.makedirs(tempdir)
os.system('rm -r ./%s/*' % (tempdir))

fontProperties = {'family':'sans-serif', 'size' : 10}

ax.set_aspect('equal')
ax.set_xticks(np.arange(1,8,1))
ax.set_yticks(np.arange(1,7,1))
ax.set_xticklabels(ax.get_xticks(), fontProperties)
ax.set_yticklabels(ax.get_yticks(), fontProperties)
ax.set_xlabel('$x$ [km]')
ax.set_ylabel('$y$ [km]')

for i in range(0,nFrames):
    ii = i + t_start_in
    z = pfull[ii,9:-9,9:-9]
    #levmin = np.amin(pfull[:,9:-9,9:-9])#pfull[max(i-16,0):min(i+16,t_end_in),:,:])
    #levmax = np.amax(pfull[:,9:-9,9:-9])#pfull[max(i-16,0):min(i+16,t_end_in),:,:])
    levmin = np.amin(pfull[max(ii-10,0):min(ii+10,t_end_in),9:-9,9:-9])
    levmax = np.amax(pfull[max(ii-10,0):min(ii+10,t_end_in),9:-9,9:-9])
    levels = np.linspace(levmin,levmax,100)
    #cont = ax.contourf(x[9:-9],y[9:-9],z,levels,cmap = cm.Greys_r)
    cont = ax.contourf(x[9:-9],y[9:-9],z,levels)
    print 'saving frame %s' % i
    plt.savefig(tempdir + '/anim-%d.png' % (i+1) ,dpi=200, bbox_inches='tight')

figuredir = '/home/%s/animations/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s_%s_' % (exptitle, expnr, prop,t_start_in,t_end_in)
tdy = dt.datetime.today()
filename += tdy.strftime('%d%m_%H%M%S')
figurepath = figuredir + '/%s.mp4' % (filename)

os.system('ffmpeg -framerate 7 -i \'' + tempdir + '/anim-%d.png\' -f mp4 -vcodec libx264 -pix_fmt yuv420p -vf scale=1920:-2 animtemp/output.mp4') 
os.system('mv animtemp/output.mp4 %s' % (figurepath) )
    

    
    



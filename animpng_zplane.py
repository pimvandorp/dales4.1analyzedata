#!/usr/bin/python
#Filename: animatefielddump.py
#Description: make an animation of snapshot contours

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import pupynere as pu
import readfielddump as rfd
import readnamoptions as rno
import datetime as dt
import os
import os.path
import subprocess


username = 'pim'

exptitle = 'Q7_CBL'
expnr = '003'

dpi = 100
fps = 7
bitrate = -1

prop = 'vhoravg' # property to be analysed (u,v,w,etc.)  

# x-axis 
xa = 'x' 

# y-axis
ya = 'y'

hour = 60

trange=[29,37]
t_start_in=0
t_end_in=trange[1] - trange[0] - 1

nFrames = t_end_in-t_start_in
print 'nFrames = ', nFrames

print 'Loading array from disk'
datadir = '/nfs/livedata/pim/fielddumpdata/%s/%s' % (exptitle,expnr)

filename = '%s_%s_%s_%s_%s.nc' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

f = pu.netcdf_file(datapath)

pfull = f.variables[prop][:,:,:]
x = f.variables['xt'][:]
y = f.variables['yt'][:]

#x = np.arange(0,np.shape(pfull)[2])*dx+0.5*dx #xt
#y = np.arange(0,np.shape(pfull)[1])*dy+0.5*dy #yt

fig = plt.figure(frameon=False, figsize=(7, 5), dpi=200)
canvas_width, canvas_height = fig.canvas.get_width_height()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

#xa_start = int(round(xa_start/dx))
#ya_start = int(round(ya_start/dy))
#xa_end = int(round(xa_end/dx))
#ya_end = int(round(ya_end/dy))

os.system('rm -r ./animtemp/*')

for i in range(0,nFrames):
    z = pfull[i,:,:]
    levmin = np.amin(pfull[max(i-16,0):min(i+16,t_end_in),:,:])
    levmax = np.amax(pfull[max(i-16,0):min(i+16,t_end_in),:,:])
    levels = np.linspace(levmin,levmax,100)
    cont = plt.contourf(x,y,z,levels)
    plt.gca().set_aspect('equal')
    print 'saving frame %s' % i
    plt.savefig('animtemp/%d.png' % (i+1) ,bbox_inches='tight',dpi=200)

figuredir = '/home/%s/animations/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s_%s' % (exptitle, expnr, prop,trange[0],trange[1])
figurepath = figuredir + '/%s.mp4' % (filename)

os.system('ffmpeg -f image2 -r 8 -i \'animtemp/%d.png\' -r 24 -vcodec copy animtemp/out.mp4')

os.system('mv animtemp/out.mp4 %s' % figurepath )
    

    
    



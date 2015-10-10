#!/usr/bin/python
#Filename: animatefielddump.py
#Description: make an animation of snapshot contours

from numpy import *
from matplotlib import pyplot as plt
from matplotlib import animation
import readfielddump as rfd
import readnamoptions as rno
from datetime import *
import os
import os.path

username = 'pim'

exptitle = 'PVD_WINDFARM'
plot_title = 'PVD-WINDFARM' # Required for LATEX handling when e.g. underscores are present in exptitle 
expnr = '103'

# read namoptions
namopt = rno.readnamoptions(exptitle,expnr)
runtime = namopt['runtime']
kmax = namopt['kmax']
itot = namopt['itot'] 
jtot = namopt['jtot']
nprocy = namopt['nprocy']
turhx = namopt['turhx']
turhy = namopt['turhy']
turhz = namopt['turhz']
turr = namopt['turr']
xsize = namopt['xsize']
ysize = namopt['ysize']
zsize = namopt['zsize']
dy = namopt['dy']
Ct = namopt['Ct'] 

prop = 'vhor' # property to be analysed (u,v,w,etc.)  

# x-axis 
xa = 'x' 

xa_start = 0
xa_end = xsize

# y-axis
ya = 'y'
ya_start = 0
ya_end = ysize

# plane at 
plane = turhz

t_start_in = 0 
t_end_in = 228
nFrames = t_end_in-t_start_in

data = rfd.readprop(exptitle,expnr,prop,xa,ya,plane,t_start_in,t_end_in)
x = data['x']
y = data['y']
p = data[prop] 

tdy = datetime.today()

figuredir = '/home/%s/animations/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
figurepath = figuredir + '/%s.mp4' % (filename)

fig = plt.figure()
ax = plt.axes()

xa_start = int(round(xa_start/dy))
ya_start = int(round(ya_start/dy))
xa_end = int(round(xa_end/dy))
ya_end = int(round(ya_end/dy))


def animate(i):
    z = p[i,:,:]
    cont = plt.contourf(x[xa_start:xa_end],y[ya_start:ya_end],z[ya_start:ya_end,xa_start:xa_end])
    plt.gca().set_aspect('equal')
    return cont
anim = animation.FuncAnimation(fig,animate,frames=nFrames,blit=True) #interval is delay between frames
dpi = 250
writer = animation.writers['ffmpeg'](bitrate=15000,fps=10,codec='libx264')
anim.save(figurepath,writer=writer,dpi=dpi)

    
    



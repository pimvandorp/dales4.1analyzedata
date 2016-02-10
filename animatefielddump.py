#!/usr/bin/python
#Filename: animatefielddump.py
#Description: make an animation of snapshot contours

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import readfielddump as rfd
import readnamoptions as rno
import datetime as dt
import os
import os.path

username = 'pim'

eurocs = False
gabls = False
cbl = True

expnr = '320'

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if cbl:
    exptitle = 'Single_turbine_CBL'

dpi = 250
fps = 8
bitrate = -1

# read namoptions
namopt = rno.readnamoptions(exptitle,expnr)
runtime = namopt['runtime']
kmax = namopt['kmax']
itot = namopt['itot'] 
jtot = namopt['jtot']
turhx = namopt['turhx']
turhy = namopt['turhy']
turhz = namopt['turhz']
turr = namopt['turr']
xsize = namopt['xsize']
ysize = namopt['ysize']
zsize = namopt['zsize']
dx = namopt['dx']
dy = namopt['dy']
dz = namopt['dz']
dtav = namopt['dtav'] 

for i in range(0,len(turhz)):
    turhxgr = int(round(turhx[i]/dx)) 
    turhygr = int(round(turhy[i]/dy)) 
    turhzgr = int(round(turhz[i]/dz)) 
    turhx[i] = 0.5*dx + dx*(int(round(turhx[i]/dx))-1) 
    turhy[i] = 0.5*dy + dy*(int(round(turhy[i]/dy))-1) 
    turhz[i] = 0.5*dz + dz*(int(round(turhz[i]/dz))-1) 

prop = 'vhoravg' # property to be analysed (u,v,w,etc.)  

# x-axis 
xa = 'x' 

xa_start = 0
xa_end = xsize

# y-axis
ya = 'y'
ya_start = 0
ya_end = ysize

# plane at 
plane = turhz[0]

hour = 3600.
t_start = 0*hour 
t_end = 5*hour
dtav = 60.

t_start_in = int(t_start/dtav)
t_end_in = int(t_end/dtav-1)

print 't_start, t_end = ', t_start, t_end
print 't_start_in, t_end_in = ', t_start_in, t_end_in
t_start_in=90
t_end_in=539

trange=[0,539]

nFrames = t_end_in-t_start_in

print 'Loading array from disk'
datadir = '/home/%s/fd_data/%s' % (username,exptitle)

filename = '%s_%s_%s_%s_%s.npy' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

pfull = np.load(datapath,mmap_mode='r')
p = pfull[t_start_in:t_end_in,plane/dz,:,:]

x = np.arange(0,np.shape(p)[2])*dx+0.5*dx #xt
y = np.arange(0,np.shape(p)[1])*dy+0.5*dy #yt

tdy = dt.datetime.today()

figuredir = '/home/%s/animations/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
figurepath = figuredir + '/%s.mp4' % (filename)

fig = plt.figure()
ax = plt.axes()

xa_start = int(round(xa_start/dx))
ya_start = int(round(ya_start/dy))
xa_end = int(round(xa_end/dx))
ya_end = int(round(ya_end/dy))

alph = 1/60.
levmin = np.amin(p)
levmax = np.amax(p)
#levmin = alph*np.amin(z)+(1-alph)*levmin 
#levmax = alph*np.amin(z)+(1-alph)*levmax 
levels = np.linspace(levmin,levmax,80)

print 'Building animation'
def animate(i):
    z = p[i,:,:]
    cont = plt.contourf(x[xa_start:xa_end],y[ya_start:ya_end],z[ya_start:ya_end,xa_start:xa_end],levels)
    plt.gca().set_aspect('equal')
    return cont
anim = animation.FuncAnimation(fig,animate,frames=nFrames,blit=True) #interval is delay between frames

writer = animation.writers['ffmpeg'](bitrate=bitrate,fps=fps,codec='libx264')
print 'Saving animation'
anim.save(figurepath,writer=writer,dpi=dpi)

    
    



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

eurocs = True
gabls = False

expnr = '001'

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'

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

t_start = 60 # t_start and t_end are required to be multiples of dtav
t_end = runtime 

t_start = dtav*int(round(t_start/dtav))
t_end = dtav*int(round(t_end/dtav))

tin = rfd.readtime(exptitle,expnr,username=username)
tsteps = tin['tsteps']
t = tin['t']

t = ndarray.tolist(t)

if t_start > t[-1]:
    t_start = t[-1]
elif t_start < t[0]:
    t_start = t[0]
t_start_in = t.index(t_start)

if t_end > t[-1]:
    t_end = t[-1]
t_end_in = t.index(t_end)

print 't_start, t_end = ', t_start, t_end
nFrames = t_end_in-t_start_in

data = rfd.readprop(exptitle,expnr,prop,xa,ya,plane,t_start_in,t_end_in)
x = data['x']
y = data['y']
p = data[prop] 
p = p/float(1E3)

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

levels = linspace(amin(p),amax(p),50)

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

    
    



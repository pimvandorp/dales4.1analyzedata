#!/usr/bin/python
# Filename: fielddumpanalysis.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 14 sept 2015
# Description: Extract, analyze and plot data from DALES' fielddump .nc files 

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------

from numpy import *
import readfielddump as rfd
import readnamoptions as rno
from fieldplot import simplefieldplot
import sys
from datetime import *
import os.path
import os

#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------

username = 'pim'

exptitle = 'PVD_WINDFARM'
plot_title = 'PVD-WINDFARM' # Required for LATEX handling when e.g. underscores are present in exptitle 
expnr = '110'

# read namoptions
namopt = rno.readnamoptions(exptitle,expnr,username=username)
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
dx = namopt['dx']
dz = namopt['dz']
Ct = namopt['Ct'] 

#-----------------------------------------------------------------
#                     1.1 Data/range selection           
#-----------------------------------------------------------------

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

time_av = False # toggle time averaging

t_start = 1200 # t_start and t_end are required to be multiples of dtav
t_end = 3600 


#-----------------------------------------------------------------
#                         1.2 Plot options
#-----------------------------------------------------------------

contour = True # make contour plot
turbine = False # plot line at turbine position

# information to write to companion text file
optinfo = 'Meyers and Meneveau; KULEUVEN method. Ct\' = %s, turbine hub height at %s m, turbine radius of %s m' % (Ct,turhz,turr)




#-----------------------------------------------------------------
#                      2 Read and analyze data
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#                               2.1 Time
#-----------------------------------------------------------------

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

if time_av == False:
    t_end_in = t_start_in + 1

if time_av==True:
    info = '%s #%s \naveraged from %s to %s s\n' % (exptitle,expnr,t_start,t_end) + optinfo
else: 
    info = '%s #%s \nsnapshot at t=%s\n' % (exptitle,expnr,t_start) + optinfo
#-----------------------------------------------------------------
#                      2.1 Position and property
#-----------------------------------------------------------------
cu = namopt['cu'] 
cv = namopt['cv'] 

print 'Reading property array'
data = rfd.readprop(exptitle,expnr,prop,xa,ya,plane,t_start_in,t_end_in,username=username)
p = data[prop] 
if prop == 'u':
    p = (p/1000) + cu
elif prop == 'v': 
    p = (p/1000) + cv
elif prop == 'w':
    p = (p/1000)
elif prop == 'vhor':
    p = (p/1000)
else:
    pass
x = data['x']
y = data['y']
z = data['z']

print 'Calculating time average'
p_tmean = mean(p[:,:,:],axis=0)
print 'shape(p_tmean) = ', shape(p_tmean)


#-----------------------------------------------------------------
#                           3 Turbine
#-----------------------------------------------------------------

if turbine == True:
    print 'Building turbine'
    turrgr = int(round(turr/dy))
    turhxgr = int(round(turhx/dx))
    turhygr = int(round(turhy/dy))
    turhzgr = int(round(turhz/dz))

    turklow = turhzgr - turrgr 
    turkhigh = turhzgr + turrgr +1

    turjlow = turhygr - turrgr 
    turjhigh = turhygr + turrgr +1

    turxlow = x[turhxgr-3]
    turzlow = z[turklow-2]
    turzhigh = z[turkhigh-2]
    width = dy
    height = turzhigh-turzlow
else:
    pass


#-----------------------------------------------------------------
#                           4 Plot data
#-----------------------------------------------------------------

print 'Initializing plot routine'
if contour == True:
    if xa == 'x' and ya == 'z':
        xa_start = int(round(xa_start/dx))
        ya_start = int(round(ya_start/dz))
        xa_end = int(round(xa_end/dx))
        ya_end = int(round(ya_end/dz))
        print 'xa_start, xa_end, ya_start, ya_end = ', xa_start, xa_end, ya_start, ya_end
        if turbine == True:
            simplefieldplot(x[xa_start:xa_end],z[ya_start:ya_end],
                    p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                    xlabel='x',ylabel='z',optitle='at y=%s' % plane,
                    optinfo = info, turbine=turbine, 
                    turxlow=turxlow, turzlow=turzlow, width=width,height=height,
                    plot_title=plot_title,username=username)
        else:
            simplefieldplot(x[xa_start:xa_end],z[ya_start:ya_end],
                    p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                    xlabel='x',ylabel='z',optitle='at y=%s' % plane,
                    optinfo = info, turbine=turbine, plot_title=plot_title,username=username) 


    if xa == 'x' and ya == 'y':
        xa_start = int(round(xa_start/dx))
        ya_start = int(round(ya_start/dy))
        xa_end = int(round(xa_end/dx))
        ya_end = int(round(ya_end/dy))
        simplefieldplot(x[xa_start:xa_end],y[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel='x',ylabel='y',optitle='at z=%s' % plane,
                optinfo = info, plot_title=plot_title,username=username)

    if xa == 'y' and ya == 'z':
        xa_start = int(round(xa_start/dy))
        ya_start = int(round(ya_start/dz))
        xa_end = int(round(xa_end/dy))
        ya_end = int(round(ya_end/dz))
        simplefieldplot(y[xa_start:xa_end],z[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel='y',ylabel='z',optitle='at x=%s' % plane,
                optinfo = info, plot_title=plot_title,username=username)

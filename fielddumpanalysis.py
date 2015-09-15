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
from fieldplot import simplefieldplot, lineplot
import sys

#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------

exptitle = 'JHU-LES'
expnr = '022'

# read namoptions
namopt = rno.readnamoptions(exptitle,expnr)
runtime = namopt['runtime']
kmax = namopt['kmax']
itot = namopt['itot'] 
jtot = namopt['jtot']
turbh = namopt['turbh']
turbr = namopt['turbr']
turbloc = namopt['turbloc']
xsize = namopt['xsize']
ysize = namopt['ysize']
Ct = namopt['Ct']
dy = ysize/jtot
turbhuby = jtot/2

#-----------------------------------------------------------------
#                     1.1 Data/range selection           
#-----------------------------------------------------------------

prop = 'u' # property to be analysed (u,v,w,etc.)  

# x-axis 
xa = 'y' 

xa_start = 0
xa_end = 200

# y-axis
ya = 'z'
ya_start = 0
ya_end = 200

# plane at 
plane = turbloc

time_av = True # toggle time averaging

t_start = 60 # t_start and t_end are required to be multiples of dtav
t_end = 1800 

#-----------------------------------------------------------------
#                         1.2 Plot options
#-----------------------------------------------------------------

contour = True # make contour plot
line = False # make line plot
turbine = True # plot line at turbine position

# information to write to companion text file
optinfo = 'fturx only, Ct = %s, turbine hub height of %s m' % (Ct,turbh)

#-----------------------------------------------------------------
#                     2 Analyze and plot data
#-----------------------------------------------------------------

data = rfd.readfielddump(exptitle,expnr,prop)
t = ndarray.tolist(data['t'])

if t_start > t[-1] or t_start < t[0]:
    t_start = t[0]
t_start_in = t.index(t_start)

if t_end > t[-1]:
    t_end = t[-1]
t_end_in = t.index(t_end)

if time_av == False:
    t_end_in = t_start_in + 1

x = data['x']
y = data['y']
z = data['z']

p = data[prop] 

cu = namopt['cu'] 
cv = namopt['cv'] 

if prop == 'u':
    p = (p/1000) + cu
elif prop == 'v': 
    p = (p/1000) + cv
elif prop == 'w':
    p = (p/1000)
else:
    pass

p_tmean = mean(p[t_start_in:t_end_in,:,:,:],axis=0)

def find_nearest(array,value):
    idx = (abs(array-value)).argmin()
    return array[idx]

info = '%s #%s \naveraged from %s to %s s\n' % (exptitle,expnr,t_start,t_end) + optinfo

if contour == True:
    if xa == 'x' and ya == 'z':
        c = find_nearest(y,plane)
        y = ndarray.tolist(y)
        c = y.index(c)
        simplefieldplot(x[xa_start:xa_end],z[ya_start:ya_end],
                p_tmean[ya_start:ya_end,c,xa_start:xa_end],exptitle,expnr,prop,
                xlabel='x',ylabel='z',optitle='at y=%s' % plane,
                optinfo = info, turbine=turbine)

    if xa == 'x' and ya == 'y':
        c = find_nearest(z,plane)
        z = ndarray.tolist(z)
        c = z.index(c)
        simplefieldplot(x[xa_start:xa_end],y[ya_start:ya_end],
                p_tmean[c,ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel='x',ylabel='y',optitle='at z=%s' % plane,
                optinfo = info)

    if xa == 'y' and ya == 'z':
        ya_end = find_nearest(z,ya_end)
        z = ndarray.tolist(z)
        ya_end = z.index(ya_end)

        c = find_nearest(x,plane)
        x = ndarray.tolist(x)
        c = x.index(c)
        simplefieldplot(y[xa_start:xa_end],z[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end,c],exptitle,expnr,prop,
                xlabel='y',ylabel='z',optitle='at x=%s' % plane,
                optinfo = info)

if line == True:

    zlow = int((turbh-turbr)/dy)
    zhigh = int((turbh+turbr)/dy)
    ylow = int(((jtot/2)*dy-turbr)/dy)
    yhigh = int(((jtot/2)*dy+turbr)/dy)

    p_tymean = mean(p_tmean[:,ylow:yhigh,:],axis=1)

    p_tyzmean = mean(p_tymean[zlow:zhigh,:], axis=0)

    if xa == 'x':
        lineplot(x[xa_start:xa_end],p_tyzmean[xa_start:xa_end],exptitle,expnr,prop,
                xlabel='x',ylabel=prop,optinfo = info)




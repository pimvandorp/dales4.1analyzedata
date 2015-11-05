#!/usr/bin/python
# Filename: fielddumpanalysis.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 14 sept 2015
# Description: Extract, analyze and plot data from DALES' fielddump .nc files 

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------

import numpy as np
import readfielddump as rfd
import readnamoptions as rno
from fieldplot import simplefieldplot
import sys
from datetime import *
import os.path
import os
from scipy import ndimage

#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------

username = 'pim'

eurocs = False
gabls = True

expnr = '100'

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'

namopt = rno.readnamoptions(exptitle,expnr,username=username)
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
dy = namopt['dy']
dx = namopt['dx']
dz = namopt['dz']
tura = namopt['tura'] 
dtav = namopt['dtav'] 
for i in range(0,len(turhz)):
    turhxgr = int(round(turhx[i]/dx)) 
    turhygr = int(round(turhy[i]/dy)) 
    turhzgr = int(round(turhz[i]/dz)) 
    turhx[i] = 0.5*dx + dx*(int(round(turhx[i]/dx))-1) 
    turhy[i] = 0.5*dy + dy*(int(round(turhy[i]/dy))-1) 
    turhz[i] = 0.5*dz + dz*(int(round(turhz[i]/dz))-1) 
#-----------------------------------------------------------------
#                     1.1 Data/range selection           
#-----------------------------------------------------------------

prop = 'vhoravg' 

xa = 'x' 
xa_start = 0
xa_end = xsize

ya = 'y'
ya_start = 0
ya_end = ysize

plane = turhz[0]
print 'Plane at %s' % plane

normaxes = False
normprop = False
rotate = True
reshape = False

smart_timeset = True
time_av = True 
t_start = 300 
t_end = runtime

#-----------------------------------------------------------------
#                         1.2 Plot options
#-----------------------------------------------------------------
usr_size = False

nsubfigures = 3
a4height = 11.7
a4width = 8.27
if nsubfigures == 1:
    margin = 1.7
else:
    margin = 0.3

figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth

if usr_size:
    print 'figwidth, figheight = ', figwidth, figheight

colorbar = False

filetype = 'pdf'

#-----------------------------------------------------------------
#                      2 Read and analyze data
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#                               2.1 Time
#-----------------------------------------------------------------

if smart_timeset:
    tin = rfd.readtime(exptitle,expnr,username=username)
    tsteps = tin['tsteps']
    t = tin['t']

    t = np.ndarray.tolist(t)

    t_start = dtav*int(round(t_start/dtav))
    t_end = dtav*int(round(t_end/dtav))

    if t_start > t[-1]:
        t_start = t[-1]
    elif t_start < t[0]:
        t_start = t[0]
    t_start_in = t.index(t_start)

    if t_end > t[-1]:
        t_end = t[-1]
    t_end_in = t.index(t_end)
else:
    t_start = dtav*int(round(t_start/dtav))
    t_end = dtav*int(round(t_end/dtav))
    t_start_in = t_start/dtav
    t_end_in = t_end/dtav

if time_av == False:
    t_end_in = t_start_in + 1

print 't_start, t_end = ', t_start, t_end

#-----------------------------------------------------------------
#                      2.1 Position and property
#-----------------------------------------------------------------
if not (rotate and xa=='x' and ya=='z'):
    print 'Reading property array'
    data = rfd.readprop(exptitle,expnr,prop,xa,ya,plane,t_start_in,t_end_in,username=username)
    p = data[prop] 
    if prop == 'u' or prop == 'uavg':
        p = (p/float(1E3))
    elif prop == 'v' or prop =='vavg': 
        p = (p/float(1E3))
    elif prop == 'w' or prop == 'wavg':
        p = (p/float(1E3))
    elif prop == 'vhor' or prop == 'vhoravg':
        p = (p/float(1E3))
    else:
        pass

x = np.arange(0,itot)*dx+0.5*dx #xt
y = np.arange(0,jtot)*dy+0.5*dy #yt
z = np.arange(0,kmax)*dz+0.5*dz #zt

if normaxes == True:
    x = x/(2*turr[0])
    y = y/(2*turr[0])
    z = z/(2*turr[0])

if rotate:
    print 'Rotating...'
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    ntur = namopt['ntur']

    winddirdata = np.loadtxt(expdir + '/winddir.%s' % (expnr),skiprows=1)
    m = np.shape(winddirdata)[0]
    n = np.shape(winddirdata)[1]
    winddiravg = np.zeros((ntur,m/ntur))
    winddirinst = np.zeros((ntur,m/ntur))

    for i in range(0,ntur):
        winddirinst[i,:] = winddirdata[i::ntur,2] 
        winddiravg[i,:] = winddirdata[i::ntur,3] 

    if xa == 'x' and ya == 'z':
        datafull = rfd.readfull(exptitle,expnr,prop,t_start_in,t_end_in,username=username) 
        pfull = datafull[prop] 
        pfullmax = np.amax(pfull)
        for i in range(0,np.shape(pfull)[0]):
            for j in range(0,np.shape(pfull)[1]):
                pfull[i,j,:,:] = ndimage.interpolation.rotate(pfull[i,j,:,:],(180/3.14)*winddiravg[0,i],reshape=reshape,cval=pfullmax)

        p_tmean = np.mean(pfull[:,:,plane/dy,:],axis=0)/float(1E3)
    else:
        pmax = np.amax(p)
        for i in range(0,np.shape(p)[0]):
            p[i,:,:] = ndimage.interpolation.rotate(p[i,:,:],(180/3.14)*winddiravg[0,i],reshape=reshape,cval=pmax)

        print 'Calculating time average'
        p_tmean = np.mean(p[:,:,:],axis=0)

else:
    print 'Calculating time average'
    p_tmean = np.mean(p[:,:,:],axis=0)

if normprop == True:
    p_tmean = p_tmean/(np.amax(abs(p_tmean)))

#-----------------------------------------------------------------
#                           4 Plot data
#-----------------------------------------------------------------

print 'Initializing plot routine'
if rotate:
    if xa == 'x' and ya == 'z':
        if normaxes:
            xlabel = '$x/D$'
            ylabel='$z/D$'
        else:
            xlabel = '$x$'
            ylabel='$z$'
        simplefieldplot(x,z,
                p_tmean,exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
    if xa == 'x' and ya == 'y':
        if normaxes:
            xlabel = '$x/D$'
            ylabel='$y/D$'
        else:
            xlabel = '$x$'
            ylabel='$y$'
        simplefieldplot(x,y,
                p_tmean,exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
else:
    if xa == 'x' and ya == 'z':
        xa_start = int(round(xa_start/dx))
        ya_start = int(round(ya_start/dz))
        xa_end = int(round(xa_end/dx))
        ya_end = int(round(ya_end/dz))
        print 'xa_start, xa_end, ya_start, ya_end = ', xa_start, xa_end, ya_start, ya_end
        if normaxes:
            xlabel = '$x/D$'
            ylabel='$z/D$'
        else:
            xlabel = '$x$'
            ylabel='$z$'
        simplefieldplot(x[xa_start:xa_end],z[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 

    if xa == 'x' and ya == 'y':
        xa_start = int(round(xa_start/dx))
        ya_start = int(round(ya_start/dy))
        xa_end = int(round(xa_end/dx))
        ya_end = int(round(ya_end/dy))
        if normaxes:
            xlabel = '$x/D$'
            ylabel='$y/D$'
        else:
            xlabel = '$x$'
            ylabel='$y$'
        simplefieldplot(x[xa_start:xa_end],y[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 

    if xa == 'y' and ya == 'z':
        xa_start = int(round(xa_start/dy))
        ya_start = int(round(ya_start/dz))
        xa_end = int(round(xa_end/dy))
        ya_end = int(round(ya_end/dz))
        simplefieldplot(y[xa_start:xa_end],z[ya_start:ya_end],
                p_tmean[ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 

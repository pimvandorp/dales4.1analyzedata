#!/usr/bin/python2.7
# Filename: fielddumpanalysis_2.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 7 nov 2015
# Description: Extract, analyze and plot data from DALES' fielddump .nc files, in a smart way

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------
import numpy as np
import readfielddump as rfd
from fieldplot import simplefieldplot
import matplotlib.pyplot as plt
import readnamoptions as rno
from scipy import ndimage
#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------
username = 'pim'

eurocs = False
gabls = False
cbl = True
nbl = False

expnr = '355'

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if cbl:
    exptitle = 'Single_turbine_CBL'
if nbl:
    exptitle = 'Single_turbine_NBL'

namopt = rno.readnamoptions(exptitle,expnr,username)
dy = namopt['dy']
dx = namopt['dx']
dz = namopt['dz']
xsize = namopt['xsize']
ysize = namopt['ysize']
zsize = namopt['zsize']
turhx = namopt['turhx']
turhy = namopt['turhy']
turhz = namopt['turhz']
ntur = namopt['ntur']
for i in range(0,ntur):
    turhxgr = int(round(turhx[i]/dx)) 
    turhygr = int(round(turhy[i]/dy)) 
    turhzgr = int(round(turhz[i]/dz)) 
    turhx[i] = 0.5*dx + dx*(turhxgr-1) 
    turhy[i] = 0.5*dy + dy*(turhygr-1) 
    turhz[i] = 0.5*dz + dz*(turhzgr-1)

print 'dx, dy, dz = ', dx, dy, dz


prop = 'vhoravg'

xa = 'x' 
xa_start = 900#turhx[0]-200
xa_end = xsize+1000#turhx[0]+1000

ya = 'z'
ya_start = 0#turhy[0]-200
ya_end = 250#turhy[0]+200

plane = turhy[0]
print 'Plane at %s' % plane

save = True
if save:
    show = False
else:
    show = True

normaxes = False
normprop = True
rotate = True
pad = True
reshape = False
appendxdir = True

hour = 3600.
t_start = 2*hour 
t_end = 3*hour
dtav = 60.
trange_start = 3*hour
trange_end = 6*hour
trange = [int((trange_start)/dtav-1),int((trange_end)/dtav-1)]
print 'trange = ', trange

#-----------------------------------------------------------------
#                         1.2 Plot options
#-----------------------------------------------------------------
usr_size = True

nsubfigures = 1
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
t_start_in = int(t_start/dtav)
t_end_in = int(t_end/dtav-1)

print 't_start, t_end = ', t_start, t_end
print 't_start_in, t_end_in = ', t_start_in, t_end_in

#-----------------------------------------------------------------
#                               2.2 Data
#-----------------------------------------------------------------
print 'Loading array from disk'
datadir = '/home/%s/fd_data/%s' % (username,exptitle)

filename = '%s_%s_%s_%s_%s.npy' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

pfull = np.load(datapath,mmap_mode='r')
print 'Calculating time average'
pfull = np.mean(pfull[t_start_in:t_end_in,:,:,:],axis=0)

if appendxdir:
    pfull = np.append(pfull,pfull[:,:,0:turhxgr],axis=2)

if rotate:
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
        if ntur == 1:
            winddirinst = winddirinst[0,trange[0]:trange[1]]
            winddiravg = winddiravg[0,trange[0]:trange[1]]

    pshp = np.shape(pfull)
    if pad:
        pa = turhxgr
        pb = pshp[2]-turhxgr
        pe = pshp[2]
        pc = turhygr
        pd = pshp[1]-turhygr
        pf = pshp[1]

        print 'Pad: a,b,c,d,e,f = ', pa, pb, pc, pd, pe, pf
        print 'pshp = ', pshp

    print 'Start rotation'
    angle = (180/3.14)*np.mean(winddiravg[t_start_in:t_end_in])
    print 'Angle (deg,rad) = ', angle, np.mean(winddiravg[t_start_in:t_end_in])

    for j in range(0,pshp[0]):
        if pad:
            pfullpad = np.mean(pfull[j,:,:])*np.ones((2*pf,2*pe))
            pfullpad[pd:pd+pf,pb:pb+pe] = pfull[j,:,:]
            pfullpad = ndimage.interpolation.rotate(pfullpad,angle,reshape=reshape,cval=np.mean(pfull[j,:,:]))
            pfull[j,:,:] = pfullpad[pd:pd+pf,pb:pb+pe]
        else:
            pfull[j,:,:] = ndimage.interpolation.rotate(pfull[j,:,:],angle,reshape=reshape,cval=np.mean(pfull[j,:,:]))

x = np.arange(0,np.shape(pfull)[2])*dx+0.5*dx #xt
y = np.arange(0,np.shape(pfull)[1])*dy+0.5*dy #yt
z = np.arange(0,np.shape(pfull)[0])*dz+0.5*dz #zt

x = x - 1000
y = y - 1000
#-----------------------------------------------------------------
#                           4 Plot data
#-----------------------------------------------------------------

if xa == 'x' and ya == 'z':
    xa_start = int(round(xa_start/dx))
    xa_end = int(round(xa_end/dx))
    ya_start = int(round(ya_start/dz))
    ya_end = int(round(ya_end/dz))
    if normprop:
        pfull = pfull/np.amax(pfull[ya_start:ya_end,plane/dy,xa_start:xa_end])

    if normaxes:
        xlabel = '$x/D$'
        ylabel='$z/D$'
    else:
        xlabel = '$x$'
        ylabel='$z$'
    if save:
        simplefieldplot(x[xa_start:xa_end],z[ya_start:ya_end],
                pfull[ya_start:ya_end,plane/dy,xa_start:xa_end],exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
    else:
        plt.contourf(x[xa_start:xa_end],y[ya_start:ya_end],pfull[plane/dz,ya_start:ya_end,xa_start:xa_end],N=200)
        plt.show()
        plt.close()

elif xa == 'x' and ya == 'y':
    xa_start = int(round(xa_start/dx))
    xa_end = int(round(xa_end/dx))
    ya_start = int(round(ya_start/dy))
    ya_end = int(round(ya_end/dy))
    if normprop:
        pfull = pfull/np.amax(pfull[plane/dz,ya_start:ya_end,xa_start:xa_end])

    if normaxes:
        xlabel = '$x/D$'
        ylabel='$y/D$'
    else:
        xlabel = '$x$'
        ylabel='$y$'
    if save:
        simplefieldplot(x[xa_start:xa_end],y[ya_start:ya_end],
                pfull[plane/dz,ya_start:ya_end,xa_start:xa_end],exptitle,expnr,prop,
                xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
    else:
        fig,ax = plt.subplots()

        cax = ax.contourf(x[xa_start:xa_end],y[ya_start:ya_end],pfull[plane/dz,ya_start:ya_end,xa_start:xa_end],N=200)
        cbaxes = fig.add_axes([0.2,1.0,0.6,0.03])
        cbar = fig.colorbar(cax,ticks=[0,1],cax=cbaxes,orientation='horizontal')
        plt.show()
        plt.close()


            

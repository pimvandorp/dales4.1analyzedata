#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import readnamoptions as rno
import pupynere as pu
import os
import os.path
import matplotlib.cm as cm

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

presentation = False
mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath',r'\usepackage{siunitx}',r'\sisetup{detect-all}']           

cp = 1004.703 
g = 9.81
Rd = 287.06  
Rv = 461.5
p0 = 1.e5
Lv = 2.5008e6

username = 'pim'

exptitle = 'Hornsrev_wakeclouds'
expnr = '306'
prop = 'ql'

datadir = '/nfs/livedata/pim/fielddumpdata/%s/%s' % (exptitle,expnr)
trange=[199,299]

readnamopt = True
if readnamopt:
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

if prop == 'RELH': 
    pres = readprop(exptitle,expnr,'presh')['presh'][-1,:]
    exnr = ((pres/p0)**(Rd/cp))

    filename = '%s_%s_thl_%s_%s.nc' % (exptitle, expnr, trange[0],trange[1])
    datapath = datadir + '/%s' % (filename)
    f = pu.netcdf_file(datapath)
    thl = np.mean(f.variables['thl'][:,turhz/dz,:,:]*1e-2+300, axis=0)
    x = f.variables['xt'][:]
    y = f.variables['yt'][:]
    z = f.variables['zt'][:]

    filename = '%s_%s_qt_%s_%s.nc' % (exptitle, expnr, trange[0],trange[1])
    datapath = datadir + '/%s' % (filename)
    f = pu.netcdf_file(datapath)
    qt = np.mean(f.variables['qt'][:,turhz/dz,:,:]*1e-5,axis=0)

    qsat = np.zeros(np.shape(thl))
    for i,u in enumerate(x):
        for j,v in enumerate(y):
            #for k,w in enumerate(z):
            tmp = thl[j,i]*exnr[turhz/dz]
            esat = 610.78 * np.exp ((17.2694*(tmp-273.16))/(tmp-35.86))
            rsat = Rd/Rv * esat/(pres[turhz/dz]-esat)
            qsat[j,i] = rsat/(1+rsat)
            #if qt[j,i]/qsat[j,i] < 0.995:
            #    qt[j,i] = 0

    p = np.divide(qt,qsat)
else:
    filename = '%s_%s_%s_%s_%s.nc' % (exptitle, expnr,prop, trange[0],trange[1])
    datapath = datadir + '/%s' % (filename)
    f = pu.netcdf_file(datapath)
    pfull = f.variables[prop][:,:,:,:]
    x = f.variables['xt'][:]
    y = f.variables['yt'][:]
    #z = f.variables['zt'][:]

    #p = pfull[0,:,:]
    p = np.sum(pfull[0,:,:,:],axis=1)


fig = plt.figure()
ax = fig.add_subplot(1,1,1,aspect='equal')

levmin = np.amin(p)
levmax = np.amax(p)
levels = np.linspace(levmin,levmax,100)
CF = ax.contourf(x,y,p,levels,cmap = cm.Greys_r)
#CF = ax.contourf(x,y,p,levels)

fig.colorbar(CF)
for c in CF.collections:
    c.set_edgecolor("face")

tdy = dt.datetime.today()
    
figuredir = '/home/%s/figures/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
if presentation:
    filename += '_presentation'

figurepath = figuredir + '/%s.png' % (filename)

plt.show()
#fig.savefig(figurepath,bbox_inches='tight',format='png',dpi=400)


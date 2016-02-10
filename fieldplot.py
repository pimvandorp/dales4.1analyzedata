#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import readnamoptions as rno
import pupynere as pu
import os
import os.path

username = 'pim'

exptitle = 'Single_turbine_CBL'
expnr = '390'

presentation = False

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

prop = 'vhoravg'

trange=[0,2]

t_start_in=0
t_end_in=trange[1] - trange[0] - 1

datadir = '/nfs/livedata/pim/fielddumpdata/%s/%s' % (exptitle,expnr)

filename = '%s_%s_%s_%s_%s.nc' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

f = pu.netcdf_file(datapath)

pfull = f.variables[prop][:,:,:,:]
x = f.variables['xt'][:]
y = f.variables['yt'][:]
z = f.variables['zt'][:]

mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath',r'\usepackage{siunitx}',r'\sisetup{detect-all}']           

fig = plt.figure()
ax = fig.add_subplot(1,1,1,aspect='equal')

#p = np.mean(pfull[:,turhz[0]/dz,:,:],axis=0)
p = pfull[-1,turhz[0]/dz,:,:]
#p = pfull[-1,:,50,:]

levmin = np.amin(p)
levmax = np.amax(p)
levels = np.linspace(levmin,levmax,100)
CF = ax.contourf(p,levels)
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


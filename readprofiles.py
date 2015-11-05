#!/usr/bin/python
#Filename: readprofiles.py
#Description: read profiles.nc file from DALES

from numpy import *
import pupynere as pu
import readnamoptions as rno
import matplotlib.pyplot as plt
import matplotlib as mpl

username = 'pim'

eurocs = False
cbl = True
gabls = False

expnr = ['301', '350']

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if cbl:
    exptitle = 'Single_turbine_CBL'

turbine = False

def readprop(exptitle,expnr,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    f = pu.netcdf_file(expdir + '/profiles.%s.nc' % (expnr))

    zt = f.variables['zt'][:]
    zm = f.variables['zm'][:] # = columns of data
    time = f.variables['time'][:] # = rows of data
    tker = f.variables['tker'][:,:] #resolved TKE
    wthvt = f.variables['wthvt'][:,:] #total buoyancy flux
    w2s = f.variables['w2s'][:,:] #SFSTKE
    ql = f.variables['ql'][:,:] #liquid water specific humidity
    thv = f.variables['thv'][:,:] #virtual potential temperature

    return {'zt' : zt, 'zm' : zm, 'time': time, 'tker':tker, 'wthvt': wthvt, 'w2s':w2s, 'ql' : ql, 'thv':thv}  

for i,v in enumerate(expnr):
    data = readprop(exptitle,v)

    time = data['time']
    dt = time[1]-time[0]
    time = time/3600.
    zt = data['zt']
    tker = data['tker']
    w2s = data['w2s']
    wthvt = data['wthvt']
    ql = data['ql']
    thv = data['thv']

    plt.plot(wthvt[len(time)/2.,:],zt,label='%s' % v)
    #plt.plot(tker[-1,:],zt)
#plt.plot(time,w2s[:,turhzgr])
#plt.plot(time,tker[:,turhzgr])

plt.show()




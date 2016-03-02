#!/usr/bin/python

import numpy as np
import pupynere as pu
import os

fddatadir = '/home/pim/fdjiyunting'
expnr = '404'

prop = 'sv001'
itot = 32
jtot = 32
kmax = 100
dx = 100
dy = 100
dz = 20
dtav = 60


print 'Extracting time array'
f = pu.netcdf_file(fddatadir + '/fielddump.000.000.%s.nc' % (expnr))

t = f.variables['time'][:]
tsteps = len(t)

nx = 0
procx = True
while True:
    procx = os.path.exists(fddatadir + '/fielddump.%s.000.%s.nc' % (str(nx).rjust(3,'0'),expnr))
    if procx == False:
        break
    else: 
        nx = nx +1

ny = 0
procy = True
while True:
    procy = os.path.exists(fddatadir + '/fielddump.000.%s.%s.nc' % (str(ny).rjust(3,'0'),expnr))
    if procy == False:
        break
    else: 
        ny = ny +1

imax = itot/nx
jmax = jtot/ny

print 'nprocx = ', nx, ' and nprocy = ', ny

p = np.zeros((tsteps,kmax,jtot,itot))
print 'Start extraction of property array'
for i in range(0,nx):
    ii = str(i).rjust(3,'0')
    for j in range(0,ny):
        jj = str(j).rjust(3,'0')
        
        f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
        print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
        p[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][:,:,:,:]
        print 'Finished writing for myidx, myidy = ', ii, jj

timein = np.arange(dtav,(1+np.shape(p)[0])*dtav,dtav)
xtin = np.arange(0,np.shape(p)[3])*dx+0.5*dx #xt
ytin = np.arange(0,np.shape(p)[2])*dy+0.5*dy #yt
ztin = np.arange(0,np.shape(p)[1])*dz+0.5*dz #zt

filename = 'test'
filename += '.nc'

f = pu.netcdf_file('./' + filename, 'w')

f.createDimension('time', np.shape(p)[0])
time = f.createVariable('time', 'f', ('time',))
time[:] = timein[:]
time.units = 'seconds since 2010-11-9 00:00:00 +0.00' 

f.createDimension('xt', itot)
xt = f.createVariable('xt', 'f', ('xt',))
xt[:] = xtin[:]
xt.units = 'meter' 
f.createDimension('yt', jtot)
yt = f.createVariable('yt', 'f', ('yt',))
yt[:] = ytin[:]
yt.units = 'meter' 
f.createDimension('zt', kmax)
zt = f.createVariable('zt', 'f', ('zt',))
zt[:] = ztin[:]
zt.units = 'meter' 
dataout = f.createVariable(prop, 'f', ('time', 'zt', 'yt', 'xt'))
dataout[:,:,:,:] = p[:,:,:,:]

f.close()



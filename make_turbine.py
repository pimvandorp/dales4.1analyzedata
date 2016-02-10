#!/usr/bin/python

import pupynere as pu
import numpy as np

dtav = 10.
tstart = 0

tsteps = 720

turhx = 297.5
turhy = 197.5
turhz = 67.5
turr = 40

itot = 320
jtot = 80
kmax = 80
dx = 5
dy = 5
dz = 5

turhxgr = int(round(turhx/dx)) 
turhygr = int(round(turhy/dy)) 
turhzgr = int(round(turhz/dz)) 
turrgr = int(round(turr/dy))

timein = np.arange(tstart+dtav,tstart+(tsteps)*dtav,dtav) #time
print timein
xtin = np.arange(0,itot)*dx+0.5*dx #xt
ytin = np.arange(0,jtot)*dy+0.5*dy #yt
ztin = np.arange(0,kmax)*dz+0.5*dz #zt

f = pu.netcdf_file('test_turbine.nc', 'w')

#f.createDimension('time', tsteps-1)    
#time = f.createVariable('time', 'f', ('time',))         
#time[:] = timein[:]          
#time.units = 'seconds since 2010-11-9 00:00:00 +0.00'       

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

#turbine = f.createVariable('turbine','f',('time' , 'zt' , 'yt' , 'xt' ))
turbine = f.createVariable('turbine','f',('zt' , 'yt' , 'xt' ))
turbine[:,:,:] = 0. 
turbine[turhzgr-turrgr:turhzgr+turrgr,turhygr-turrgr:turhygr+turrgr,turhxgr:turhxgr+1] = 1. 
turbine[0:turhzgr,turhygr:turhygr+1,turhxgr+1:turhxgr+2] = 1. 

ground = f.createVariable('ground','f',('zt' , 'yt' , 'xt' ))
ground[:,:,:] = 0.
ground[0,:,:] = 1.

f.close()





#!/usr/bin/python
#Filename: readfielddump.py
#Description: read fielddump nc files from DALES

from numpy import *
import pupynere as pu
import readnamoptions as rno
import os.path
import fieldplot 
import sys

def readfielddump(exptitle, expnr,prop):
    expsdir = '/home/pim/Les/Experiments'
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    namopt = rno.readnamoptions(exptitle,expnr)

###################### extract time array ###################### 
    print 'Extracting time array'
    f = pu.netcdf_file(expdir + '/fielddump.000.000.%s.nc' % (expnr))

    t = f.variables['time'][:]

###################### make position arrays ###################### 
    print 'Extracting position array\'s'
    zt = f.variables['zt'][:]

    jtot = namopt['jtot']
    ysize = namopt['ysize']
    yt = []
    for i in range(jtot):
        yt = append(yt,(i+0.5)*float(ysize)/jtot)

    itot = namopt['itot']
    xsize = namopt['xsize']
    xm = []
    for i in range(itot):
        xm = append(xm,i*float(xsize)/itot)

###################### extract property array ###################### 

    nx = 0
    procx = True
  
    while True:
        procx = os.path.exists(expdir + '/fielddump.%s.000.%s.nc' % (str(nx).rjust(3,'0'),expnr))
        if procx == False:
            break
        else: 
            nx = nx +1

    ny = 0
    procy = True
  
    while True:
        procy = os.path.exists(expdir + '/fielddump.000.%s.%s.nc' % (str(ny).rjust(3,'0'),expnr))
        if procy == False:
            break
        else: 
            ny = ny +1


    print 'nprocx = ', nx, ' and nprocy = ', ny
    
    print 'Start extraction of property array'
    for i in range(0,nx):
        ii = str(i).rjust(3,'0')
        for j in range(0,ny):
            jj = str(j).rjust(3,'0')
            
            f = pu.netcdf_file(expdir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
            
            if j == 0:
                p = f.variables[prop][:,:,:,:]
            else:
                p = append(p,f.variables[prop][:,:,:,:],axis=2)           
        if i == 0:
            pp  = p
        else:
            pp  = append(pp, p, axis=3)
    print 'Finished extraction of property array'
    return {prop: pp, 'x': xm, 'y': yt, 'z': zt, 't': t, 'nprocx': nx, 'nprocy': ny}






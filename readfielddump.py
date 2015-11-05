#!/usr/bin/python
#Filename: readfielddump.py
#Description: read fielddump nc files from DALES

from numpy import *
import pupynere as pu
import readnamoptions as rno
import os.path
import fieldplot 
import sys
import math

def readtime(exptitle,expnr,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    print 'Extracting time array'
    f = pu.netcdf_file(expdir + '/fielddump.000.000.%s.nc' % (expnr))

    t = f.variables['time'][:]
    tsteps = len(t)

    return {'tsteps' : tsteps, 't' : t}  

def readfull(exptitle, expnr,prop,t_start_in,t_end_in,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    namopt = rno.readnamoptions(exptitle,expnr)

    itot = namopt['itot']
    jtot = namopt['jtot']
    kmax = namopt['kmax'] 

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

    imax = itot/nx
    jmax = jtot/ny
    tsteps = t_end_in-t_start_in

    print 'nprocx = ', nx, ' and nprocy = ', ny

    p = zeros((tsteps,kmax,jtot,itot))
    print 'Start extraction of property array'
    for i in range(0,nx):
        ii = str(i).rjust(3,'0')
        for j in range(0,ny):
            jj = str(j).rjust(3,'0')
            
            f = pu.netcdf_file(expdir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
            print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
            p[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,:,:,:]
            print 'Finished writing for myidx, myidy = ', ii, jj

    return {prop: p} 

def readprop(exptitle, expnr,prop,xa,ya,plane,t_start_in,t_end_in,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    namopt = rno.readnamoptions(exptitle,expnr)
    
    itot = namopt['itot']
    jtot = namopt['jtot']
    kmax = namopt['kmax'] 

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
    
    imax = itot/nx
    jmax = jtot/ny
    tsteps = t_end_in-t_start_in
    ysize = namopt['ysize']
    dy = ysize/float(jtot)
    plane_in = int(round(plane/dy))

    if xa == 'x' and ya == 'z':
        j = int(math.floor(plane_in/jmax))
        planeloc = plane_in - j*jmax
        p = zeros((tsteps,kmax,itot))

        print 'Start extraction of property array'
        for i in range(0,nx):
            ii = str(i).rjust(3,'0')
            jj = str(j).rjust(3,'0')
            f = pu.netcdf_file(expdir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
            print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
            p[:,:,(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,:,planeloc,:]
            print 'Finished writing for myidx, myidy = ', ii, jj

    if xa=='x' and ya=='y':
        p = zeros((tsteps,jtot,itot))
        print 'Start extraction of property array'
        for i in range(0,nx):
            ii = str(i).rjust(3,'0')
            for j in range(0,ny):
                jj = str(j).rjust(3,'0')
                
                f = pu.netcdf_file(expdir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
                print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
                p[:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,plane_in,:,:]
                print 'Finished writing for myidx, myidy = ', ii, jj

    if xa == 'y' and ya == 'z':
        i = int(math.floor(plane_in/imax))
        planeloc = plane_in - i*imax
        p = zeros((tsteps,kmax,jtot))

        print 'Start extraction of property array'
        for j in range(0,ny):
            ii = str(i).rjust(3,'0')
            jj = str(j).rjust(3,'0')
            f = pu.netcdf_file(expdir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
            print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
            p[:,:,(j*jmax):((j+1)*jmax)] = f.variables[prop][t_start_in:t_end_in,:,:,planeloc]
            print 'Finished writing for myidx, myidy = ', ii, jj


    print 'Finished extraction of property array'

    return {prop: p, 'nprocx': nx, 'nprocy': ny}


#!/usr/bin/python
#Filename: readfielddump.py
#Description: read fielddump nc files from DALES

import numpy as np
import pupynere as pu
import readnamoptions as rno
import os
import os.path
import sys
import math

def readtime(exptitle,casetitle,expnr,livedata=False,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    fddatadir = expdir

    print 'Extracting time array'
    f = pu.netcdf_file(fddatadir + '/fielddump.000.000.%s.nc' % (expnr))

    t = f.variables['time'][:]
    tsteps = len(t)

    return {'tsteps' : tsteps, 't' : t}  

def readfull(exptitle,casetitle, expnr,prop,t_start_in,t_end_in,livedata=False,username='pim',save=False,timeav=False,fielddumpdir=True, netcdf = False, dtav = 60,zslice=False,zsum = False):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    fddatadir = expdir

    namopt = rno.readnamoptions(exptitle,expnr)

    itot = namopt['itot']
    jtot = namopt['jtot']
    kmax = namopt['kmax'] 
    dx = namopt['dx']
    dy = namopt['dy']
    dz = namopt['dz']
    turhz = namopt['turhz']

    nx = 0
    procx = True
  
    print fddatadir
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
    tsteps = t_end_in-t_start_in

    print 'nprocx = ', nx, ' and nprocy = ', ny

    if prop == 'uw':
        #u_in = np.zeros((tsteps,kmax,jtot,itot))
        #w_in = np.zeros((tsteps,kmax,jtot,itot))
        uw = np.zeros((tsteps,kmax,jtot,itot))
        pmean = np.zeros((kmax,jtot,itot))
        print 'Start extraction of property array'
        for i in range(0,nx):
            ii = str(i).rjust(3,'0')
            for j in range(0,ny):
                jj = str(j).rjust(3,'0')
                
                f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
                print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
                #u_in[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables['ustar0'][t_start_in:t_end_in,:,:,:]
                #w_in[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables['w'][t_start_in:t_end_in,:,:,:]
                u_in = f.variables['ustar0'][t_start_in:t_end_in,:,:,:]
                w_in = f.variables['w'][t_start_in:t_end_in,:,:,:]
                #u_mean = np.mean(u_in,axis=0)
                #w_mean = np.mean(w_in,axis=0)
                for k in range(0,tsteps):
                    #uw[k,:,:,:] = np.multiply(u_in[k,:,:,:]-u_mean[:,:,:],w_in[k,:,:,:]-w_mean[:,:,:])
                    #uw[k,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = np.multiply(u_in[k,:,:,:]-u_mean[:,:,:],w_in[k,:,:,:]-w_mean[:,:,:])
                    uw[k,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = np.multiply(u_in[k,:,:,:],w_in[k,:,:,:])
                print 'Calculating time average'
                pmean[:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = np.mean(uw[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)],axis=0)
                print 'Finished writing for myidx, myidy = ', ii, jj
    else:
        if timeav:
            p = np.zeros((tsteps,kmax,jtot,itot))
            pmean = np.zeros((kmax,jtot,itot))
            print 'Start extraction of property array'
            for i in range(0,nx):
                ii = str(i).rjust(3,'0')
                for j in range(0,ny):
                    jj = str(j).rjust(3,'0')
                    
                    f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
                    print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
                    p[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,:,:,:]
                    print 'Calculating time average'
                    pmean[:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = np.mean(p[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)],axis=0)
                    print 'Finished writing for myidx, myidy = ', ii, jj
        else:
            p = np.zeros((tsteps,kmax,jtot,itot))
            print 'Start extraction of property array'
            for i in range(0,nx):
                ii = str(i).rjust(3,'0')
                for j in range(0,ny):
                    jj = str(j).rjust(3,'0')
                    
                    f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
                    print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
                    p[:,:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,:,:,:]
                    print 'Finished writing for myidx, myidy = ', ii, jj

    if zslice:
        turhzgr = int(round(turhz[0]/dz)) 
        pzhub = p[:,turhzgr,:,:]

    if zsum:
        pzsum = np.sum(p,axis=1)

    if save:
        if not netcdf:
            datadir = '/nfs/livedata/pim/binary_fd_data/%s/%s' % (exptitle,expnr)

            if not os.path.isdir(datadir):
                os.makedirs(datadir)

            filename = '%s_%s_%s_%s_%s' % (exptitle,expnr, prop, t_start_in, t_end_in)

            if timeav:
                filename += '_timeav'
                datapath = datadir + '/%s' % filename
                np.save(datapath,pmean)
            else:
                datapath = datadir + '/%s' % filename
                np.save(datapath,p)
        else:
            print 'max(p) =', np.amax(p)
            fin = pu.netcdf_file(fddatadir + '/fielddump.000.000.%s.nc' % (expnr))

            timein = np.arange(dtav,(1+np.shape(p)[0])*dtav,dtav)
            print 'timein = ', timein
            xtin = np.arange(0,np.shape(p)[3])*dx+0.5*dx #xt
            ytin = np.arange(0,np.shape(p)[2])*dy+0.5*dy #yt
            ztin = np.arange(0,np.shape(p)[1])*dz+0.5*dz #zt

            datadir = '/nfs/livedata/pim/fielddumpdata/%s/%s' % (exptitle,expnr)

            if not os.path.isdir(datadir):
                os.makedirs(datadir)

            filename = '%s_%s_%s_%s_%s' % (exptitle,expnr, prop, t_start_in, t_end_in)

            if timeav:
                filename += '_timeav'
            filename += '.nc'

            datapath = datadir + '/%s' % filename

            f = pu.netcdf_file(datapath, 'w')
            if not timeav:
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

                if zslice:
                    dataout = f.createVariable(prop, 'f', ('time', 'yt', 'xt'))
                    dataout[:,:,:] = pzhub[:,:,:]
                elif zsum:
                    dataout = f.createVariable(prop, 'f', ('time', 'yt', 'xt'))
                    dataout[:,:,:] = pzsum[:,:,:]
                else:
                    f.createDimension('zt', kmax)
                    zt = f.createVariable('zt', 'f', ('zt',))
                    zt[:] = ztin[:]
                    zt.units = 'meter' 
                    dataout = f.createVariable(prop, 'f', ('time', 'zt', 'yt', 'xt'))
                    dataout[:,:,:,:] = p[:,:,:,:]
            f.close()


def readprop(exptitle, expnr,prop,xa,ya,plane,t_start_in,t_end_in,username='pim',livedata=False):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)
    if livedata:
        fddatadir = '/nfs/livedata/%s/fielddumpdata/%s/%s' % (username,exptitle,expnr)
    else:
        fddatadir = expdir

    namopt = rno.readnamoptions(exptitle,expnr)
    
    itot = namopt['itot']
    jtot = namopt['jtot']
    kmax = namopt['kmax'] 

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
        p = np.zeros((tsteps,kmax,itot))

        print 'Start extraction of property array'
        for i in range(0,nx):
            ii = str(i).rjust(3,'0')
            jj = str(j).rjust(3,'0')
            f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
            print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
            p[:,:,(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,:,planeloc,:]
            print 'Finished writing for myidx, myidy = ', ii, jj

    if xa=='x' and ya=='y':
        p = np.zeros((tsteps,jtot,itot))
        print 'Start extraction of property array'
        for i in range(0,nx):
            ii = str(i).rjust(3,'0')
            for j in range(0,ny):
                jj = str(j).rjust(3,'0')
                
                f = pu.netcdf_file(fddatadir + '/fielddump.%s.%s.%s.nc' % (ii,jj,expnr)) 
                print 'Finished reading from fielddump.%s.%s.%s.nc' % (ii,jj,expnr)
                p[:,(j*jmax):((j+1)*jmax),(i*imax):((i+1)*imax)] = f.variables[prop][t_start_in:t_end_in,plane_in,:,:]
                print 'Finished writing for myidx, myidy = ', ii, jj

    if xa == 'y' and ya == 'z':
        i = int(math.floor(plane_in/imax))
        planeloc = plane_in - i*imax
        p = np.zeros((tsteps,kmax,jtot))

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


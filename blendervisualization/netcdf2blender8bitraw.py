#!/usr/bin/python

import numpy as np
from scipy.io import netcdf
import os.path
import os

datapath = '/nfs/livedata/pim/fielddumpdata/Hornsrev_wakeclouds/312/Hornsrev_wakeclouds_312_ql_full.nc'
f = netcdf.netcdf_file(datapath, 'r')

tsteps = -1
pfull = f.variables['ql'][:tsteps,:,:,:]
pmax = np.amax(pfull)

filename = datapath[:-3] + '_%d' % tsteps + '_8bit.raw'
if os.path.exists(filename):
    os.remove(filename)

nx, ny, nz, nframes = np.shape(pfull)[3],np.shape(pfull)[2],np.shape(pfull)[1],np.shape(pfull)[0]

pointdata = np.zeros((nx*ny*nz))

for t in range(0,nframes):
    n = 0
    print 't = ', t 
    for iii in range(0,nz):
        for ii in range(0,ny):
            for i in range(0,nx):
                pointdata[n] = pfull[t,iii,ii,i]
                n += 1
    pointdata *= 255/pmax
    binfile = open(filename, 'ab')
    pointdata.astype(np.uint8).tofile(binfile)
    binfile.close()

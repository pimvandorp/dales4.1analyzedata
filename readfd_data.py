#!/usr/bin/python2.7
# Filename: readfd_data.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 7 nov 2015
# Description: Load .nc files to single binary file

import readfielddump as rfd
import numpy as np

username = 'pim'

cbl = 'Single_turbine_CBL'
sbl = 'Single_turbine_GABLS'
nbl = 'Single_turbine_NBL'
eurocs = 'Single_turbine_EUROCS'
aitken = 'Single_turbine_Aitken_stable'
mirocha = 'Single_turbine_Mirocha_wcbl'
hornsrev = 'Single_turbine_Hornsrev'
hornsrevCBL = 'Hornsrev_CBL'

casetitle = ''

livedata = True
fielddumpdir = False

exptitle = [mirocha]
expnr = ['213']

props = ['fx']

dtav = 60.

hour = 3600.
t_start = [8*hour+900]
t_end = [9*hour]
timeav = False
netcdf = True
zslice = False
zsum = False

for i,v in enumerate(exptitle):
    for j,w in enumerate(props):
        print 'Start %s %s ' % (v, expnr[i])
        tin = rfd.readtime(v,casetitle,expnr[i],livedata=livedata,username=username)
        t = tin['t']

        t = np.ndarray.tolist(t)

        t_start[i] = dtav*int(round(t_start[i]/dtav))
        t_end[i] = dtav*int(round(t_end[i]/dtav))

        if t_start[i] > t[-1]:
            t_start[i] = t[-1]
        elif t_start[i] < t[0]:
            t_start[i] = t[0]
        t_start_in = t.index(t_start[i])

        if t_end[i] > t[-1]:
            t_end[i] = t[-1]

        t_end_in = t.index(t_end[i])

        print 't_start, t_end = ', t_start[i], t_end[i]

        t_start_in = int(t_start_in)
        t_end_in = int(t_end_in) + 1

        rfd.readfull(v,casetitle, expnr[i],w,t_start_in,t_end_in,username=username,livedata=livedata,save=True,timeav=timeav,fielddumpdir=fielddumpdir, dtav = dtav,netcdf=netcdf,zslice=zslice,zsum=zsum)


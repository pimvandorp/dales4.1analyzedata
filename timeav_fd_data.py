#!/usr/bin/python
#Filename: timeav_fd_data.py

import numpy as np

exptitle = 'Single_turbine_GABLS'
expnr = '200'

prop = 'vhoravg'

t_start_in = 539
t_end_in = 659

datadir = '/scratch/shared/pvandorp/binary_fd_data/%s/%s' % (exptitle,expnr)
filename = '%s_%s_%s_%s_%s.npy' % (exptitle,expnr, prop, t_start_in, t_end_in)
datapath = datadir + '/%s' % filename
print datapath

print 'loading data'
pfull = np.load(datapath,mmap_mode='r')
print 'calculating time average'
pfull = np.mean(pfull,axis=0)

print 'saving data'
savename = filename + '_timeav'
np.save(datadir + '/%s' % savename)






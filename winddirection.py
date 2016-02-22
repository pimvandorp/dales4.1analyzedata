#!/usr/bin/python

import numpy as np

u = 1.3
v = -7.5

M = (u**2+v**2)**.5
print 'Wind speed = ', M

winddir = np.arctan2(v,u)
print 'Wind dir rad, deg = ', winddir, 270-winddir*180/np.pi

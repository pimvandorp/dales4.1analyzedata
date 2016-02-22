#!/usr/bin/python
#Filename: animatefielddump.py
#Description: make an animation of snapshot contours

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
import pupynere as pu
import readfielddump as rfd
import readnamoptions as rno
import datetime as dt
import os
import os.path
import subprocess

username = 'pim'

exptitle = 'Hornsrev_CBL'
expnr = '002'

dpi = 100
fps = 7
bitrate = -1

prop = 'vhoravg' # property to be analysed (u,v,w,etc.)  

trange=[59,179]
t_start_in=100
t_end_in=trange[1] - trange[0] - 1

figuredir = '/home/%s/animations/%s' % (username,exptitle)

if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = '%s_%s_%s_%s_%s' % (exptitle, expnr, prop,trange[0],trange[1])
figurepath = figuredir + '/%s.mp4' % (filename)

os.system('ffmpeg -f image2 -r 7 -i \'animtemp/anim-%d.png\' -r 24 -vcodec copy animtemp/output.mp4')
#os.system('ffmpeg -r 8 -i \'animtemp/anim-%d.png\' animtemp/output.gif')
os.system('mv animtemp/output.mp4 %s' % figurepath )
    

    
    



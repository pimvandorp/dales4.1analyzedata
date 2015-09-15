#!/usr/bin/python
#Filename: fieldplot.py
#Description: simple fieldplotter

from numpy import *
import readfielddump as rfd
import matplotlib.pyplot as plt
import matplotlib
from datetime import *
import readnamoptions as rno
import os.path
import os

def simplefieldplot(X,Y,Z,exptitle='',expnr='',prop='',N = 300,plot_title=0,xlabel = 'x', ylabel = 'y', optinfo = 0, optitle = '',turbine=False):

    tdy = datetime.today()
    
    figuredir = '/home/pim/figures/%s' % (exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
    figurepath = figuredir + '/%s.pdf' % (filename)
    optfilepath = figuredir + '/%s.txt' % (filename)

    font = {'family' : 'computer modern',
        'weight' : 'medium',
        'size'   : 12}
    matplotlib.rc('font', **font)

    plt.contourf(X,Y,Z,N) #filled contours 
    plt.contour(X,Y,Z,N) #contour lines
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar()

    if turbine == True: #plot turbine
        namopt = rno.readnamoptions(exptitle,expnr)
        turbh = namopt['turbh']
        turbr = namopt['turbr']
        turbloc = namopt['turbloc']
        plt.plot([turbloc,turbloc],[turbh-turbr,turbh+turbr],color='0.85',lw=1)

    if plot_title != 0:
        plt.title(plot_title)
    else:
        plt.title('%s \#%s: field plot of %s ' %  (exptitle,expnr,prop)+ optitle )

    plt.savefig(figurepath,bbox_inches='tight')
    
    if optinfo != 0:
        with open(optfilepath, 'w') as opt:
            opt.write(optinfo)

def lineplot(X,Y,exptitle='',expnr='',prop='',project = 'les_data_analysis',plot_title=0,xlabel = 'x', ylabel = 'y', optinfo = 0, optitle = ''):

    tdy = datetime.today()
    
    figuredir = '/home/pim/figures/%s' % (exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
    figurepath = figuredir + '/%s.pdf' % (filename)
    optfilepath = figuredir + '/%s.txt' % (filename)

    font = {'family' : 'computer modern',
        'weight' : 'medium',
        'size'   : 12}
    matplotlib.rc('font', **font)
    
    plt.plot(X,Y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if plot_title != 0:
        plt.title(plot_title)
    else:
        plt.title('%s \#%s: line plot of %s ' %  (exptitle,expnr,prop)+ optitle )

    plt.savefig(figurepath,bbox_inches='tight')
    
    if optinfo != 0:
        with open(optfilepath, 'w') as opt:
            opt.write(optinfo)








#!/usr/bin/python
#Filename: fieldplot.py
#Description: simple fieldplotter

from numpy import *
import readfielddump as rfd
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches
from datetime import *
import os.path
import os

def simplefieldplot(X,Y,Z,exptitle='',expnr='',prop='',N = 300,
                    plot_title=0,xlabel ='x',ylabel ='y',optinfo=0,optitle='',nchartitle=-1,
                    turbine=False,turxlow=0,turzlow=0,width=0,height=0,username='pim'):

    tdy = datetime.today()
    
    figuredir = '/home/%s/figures/%s' % (username,exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s_%s_%s' % (exptitle, expnr, prop, xlabel, ylabel, tdy.strftime('%d%m_%H%M%S'))
    figurepath = figuredir + '/%s.pdf' % (filename)
    optfilepath = figuredir + '/%s.txt' % (filename)

    datadir = '/home/%s/figures/%s' % (username,exptitle)

    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    datafilename = '%s_%s_%s_%s_%s_%s_DATA' % (exptitle, expnr, prop, xlabel, ylabel, tdy.strftime('%d%m_%H%M%S'))
    datapath = datadir + '/%s.txt' % (datafilename)

    savetxt(datapath,Z,fmt='%5.1d')

    font = {'family' : 'computer modern',
        'weight' : 'medium',
        'size'   : 12}
    matplotlib.rc('font', **font)
    
    print 'Plotting contours'
    plt.contourf(X,Y,Z,N) #filled contours 
    #plt.contour(X,Y,Z,N) #contour lines
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar()

    if turbine == True: #plot turbine
        print 'Plotting wind turbine. Note: assumed equidistant grid!'

        plt.gca().add_patch(patches.Rectangle((turxlow,turzlow),width,height,facecolor='k',zorder=10))

    if plot_title != 0:
        plt.title(plot_title + ' \#%s: field plot of %s ' % (expnr, prop) + optitle)
    else:
        plt.title('%s \#%s: field plot of %s ' %  (exptitle[0:nchartitle],expnr,prop)+ optitle )
    
    print 'Saving figure'
    plt.gca().set_aspect('equal')
    plt.savefig(figurepath,bbox_inches='tight')
    
    if optinfo != 0:
        with open(optfilepath, 'w') as opt:
            opt.write(optinfo)

def lineplot(X,Y,exptitle='',expnr='',prop='',project = 'les_data_analysis',plot_title=0,xlabel = 'x', ylabel = 'y', optinfo = 0, optitle = '',nchartitle=-1,username='pim'):

    tdy = datetime.today()
    
    figuredir = '/home/%s/figures/%s' % (username,exptitle)

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
        plt.title('%s \#%s: line plot of %s ' %  (exptitle[0:nchartitle],expnr,prop)+ optitle )

    plt.savefig(figurepath,bbox_inches='tight')
    
    if optinfo != 0:
        with open(optfilepath, 'w') as opt:
            opt.write(optinfo)
    plt.close()








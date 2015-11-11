#!/usr/bin/python
#Filename: fieldplot.py
#Description: simple fieldplotter

import numpy as np
import readfielddump as rfd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
from datetime import *
import os.path
import os

def simplefieldplot(X,Y,Z,exptitle='',expnr='',prop='',N = 200,
                    plot_title=0,xlabel ='x',ylabel ='y',filetype='pdf',width=0,height=0,username='pim',colorbar=True,usr_size=False,figwidth=2.7,figheight=2.7,aspectratio=1):

    tdy = datetime.today()
    
    figuredir = '/home/%s/figures/%s' % (username,exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
    figurepath = figuredir + '/%s.%s' % (filename,filetype)
    optfilepath = figuredir + '/%s.txt' % (filename)

    font = {'family' : 'computer modern',
        'weight' : 'medium',
        'size'   : 10}
    mpl.rc('font', **font)

    fig,ax = plt.subplots()
    
    ax.set_aspect(aspectratio)
    if usr_size == True:
        fig.set_size_inches(figwidth,figheight)

    print 'Plotting contours'
    #minval = round(np.amin(Z),2)
    #minval = np.amin(Z)
    #V = np.linspace(minval,1,100)
    cax = ax.contourf(X,Y,Z,N,rasterized=True) 
    ax.contour(X,Y,Z,N,rasterized=True) 
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if (colorbar==True):
        #colorbar setting for one large plot:
        #cbaxes = fig.add_axes([0.8,0.2,0.03,0.3])
        #cbar = fig.colorbar(cax,ticks=[0,np.amax(Z)],cax=cbaxes,orientation='vertical')
        #cbar = fig.colorbar(cax,ticks=[np.amin(Z),np.amax(Z)],fraction=0.036, pad=0.04,orientation='vertical')
        #cbar.ax.set_yticklabels(['$%s$' % round(np.amin(Z),1), '$1.0$'])
        #colorbar settings for three small plots next to each other:
        #cbaxes = fig.add_axes([0.3,1.10,0.4,0.03])
        #cbar = fig.colorbar(cax,ticks=[round(np.amin(Z),2),round(np.amax(Z),2)],cax=cbaxes,orientation='horizontal')
        cbar = fig.colorbar(cax,ticks=[minval,round(1.,1)],pad=0.1,orientation='horizontal')

    if plot_title != 0:
        ax.set_title(plot_title)

    #ax.set_yticks([-100,0, 100])
    ax.set_yticks([100, 200])
    
    print 'Saving figure'
    fig.savefig(figurepath,bbox_inches='tight',format='%s' % filetype)
    

def lineplot(X,Y,exptitle='',expnr='',prop='',plot_title=0,xlabel = 'x', ylabel = 'y', username='pim'):

    tdy = datetime.today()
    
    figuredir = '/home/%s/figures/%s' % (username,exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s' % (exptitle, expnr, prop, tdy.strftime('%d%m_%H%M%S'))
    figurepath = figuredir + '/%s.pdf' % (filename)

    font = {'family' : 'computer modern',
        'weight' : 'medium',
        'size'   : 12}
    mpl.rc('font', **font)
    
    plt.plot(X,Y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if plot_title != 0:
        plt.title(plot_title)

    plt.savefig(figurepath,bbox_inches='tight')
    
    plt.close()








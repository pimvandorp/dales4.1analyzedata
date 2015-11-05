#!/usr/bin/python
# Filename: poweryawanalysis.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics
# Description: 

import numpy as np
import readnamoptions as rno
import matplotlib.pyplot as plt
import matplotlib as mpl
from fieldplot import lineplot
from datetime import *
import os.path
import os

#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------

username = 'pim'

#exptitle = 'Single_turbine_stability'
exptitle = 'PVD_WINDFARM'
#plot_title = 'Single-turbine-stability' # Required for LATEX handling when e.g. underscores are present in exptitle 
plot_title = 'PVD-WINDFARM' # Required for LATEX handling when e.g. underscores are present in exptitle 
expnr = ['430']#,'002', '003']
optylabel = ''

tdev = 3600

yaw = False
power = True
plotall = True
plotmean = True
show = True
save = False
legend = True

namopt = rno.readnamoptions(exptitle,expnr[0],username=username)
ntur = namopt['ntur'] 
turr = namopt['turr'][0]
tura = namopt['tura']

nsubfigures = 1
a4height = 11.7
a4width = 8.27
margin = 1.7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = 0.5*figwidth

def readwindturbinedata(exptitle,expnr,tdev=3600,username='pim'):
    namopt = rno.readnamoptions(exptitle,expnr,username=username)
    ntur = namopt['ntur'] 

    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    windturbinedata = np.loadtxt(expdir + '/windturbinedata.%s' % (expnr),skiprows=1)

    m = np.shape(windturbinedata)[0]
    n = np.shape(windturbinedata)[1]
    turdata = np.zeros((ntur,m/ntur,n))

    for i in range(0,ntur):
        turdata[i,:,:] = windturbinedata[i::ntur,:] #select data of single turbine

    k=0
    while turdata[0,k,1]<tdev:
        k+=1

    time = turdata[:,k:,1]
    yawangle = turdata[:,k:,2]
    windangle = turdata[:,k:,3]
    yawerror = turdata[:,k:,2]
    Pext = turdata[:,k:,5]
    Puse = turdata[:,k:,6]
    
    return {'time':time,'yawangle':yawangle,'windangle':windangle,'yawerror':yawerror, 'Pext':Pext, 'Puse': Puse}

figuredir = '/home/%s/figures/%s' % (username,exptitle)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = 'Poweranalysis_%s' % exptitle
for i,v in enumerate(expnr):
    filename += '_%s' % v
    
tdy = datetime.today()
filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

figurepath = figuredir + '/%s.pdf' % (filename)

fig = plt.figure()
ax = plt.subplot(111)
fig.set_size_inches(figwidth,figheight)


font = {'family' : 'computer modern',
    'weight' : 'bold',
    'size'   : 10}
mpl.rc('font', **font)

box = ax.get_position()
ax.set_position([box.x0, box.y0,
                 box.width, box.height * 0.9])

color = ['k', 'r', 'g', 'b', 'y'] 

for i,v in enumerate(expnr):
    data = readwindturbinedata(exptitle,v,tdev=tdev)

    t = data['time']
    yawangle = data['yawangle']
    yawanglemean = np.ones((np.shape(yawangle)))
    Puse = data['Puse']
    Pusemean = np.ones((np.shape(Puse)))

    if plotmean:
        for j in range(0,ntur):
            if yaw:
                yawanglemean[j,:] = np.mean(yawangle[j,:])*yawanglemean[j,:]
                plt.plot(t[j,:],yawanglemean[j,:],'%s' % color[j],label='Wind turbine %s' % (j+1))
            if power:
                Pusemean[j,:] = np.mean(Puse[j,:])*Pusemean[j,:]
                plt.plot(t[j,:],Pusemean[j,:],'%s' % color[j],label='Wind turbine %s' % (j+1),alpha=1,zorder=10)

    if plotall:
        for j,w in enumerate(Puse[:,0]):
            if yaw:
                plt.plot(t[j,:],yawangle[j,:],'%s' % color[j]) 
            if power:
                plt.plot(t[j,:],Puse[j,:],'%s' % color[j],alpha=0.5,zorder=0) 


if legend:
#ax.legend()#loc='upper center', bbox_to_anchor=(0.5, 1.40),ncol=4)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax.legend()

plt.xlabel('$t \ [\mathrm{s}]$')
if yaw:
    plt.ylabel('Yaw angle'+ optylabel)
if power:
    plt.ylabel('$P \ [\mathrm{MW}]$'+ optylabel)

if show:
    plt.show()
if save:
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()


#!/usr/bin/python
# Filename: wakemodels.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics
# Description: 

import numpy as np
import readfielddump as rfd
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

eurocs = True
comparison = False

if eurocs:
    exptitle = 'Single_turbine_EUROCS'
    expnr = ['001']
    plot_title = 'Single-turbine-EUROCS' # Required for LATEX handling when e.g. underscores are present in exptitle 
    optlabel = ['EUROCS']
if comparison:
    expnr = ['001','011', '012']

optylabel = ''#'at turbine axis'

ataxis = True
overdisk = True

plotall= False
plotmean = False
plothourlymean = True
plotmedian = False
save = False
show = True
savedata = False

tophat = True
ntophat = 1
kwake = [0.075]

firsthour = 9
skiprows = 4

namopt = rno.readnamoptions(exptitle,expnr[0],username=username)
turr = namopt['turr'][0]
tura = namopt['tura']

nsubfigures = 1
a4height = 11.7
a4width = 8.27
margin = 1.7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = 0.5*figwidth

def readwakeanalysis(exptitle,expnr,username='pim',skiprows=0):
    namopt = rno.readnamoptions(exptitle,expnr,username=username)

    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    wakedata = np.loadtxt(expdir + '/wakeanalysis.%s' % (expnr),skiprows=1)
    wakeaxisdata = np.loadtxt(expdir + '/wakeaxisanalysis.%s' % (expnr),skiprows=1)

    time = wakedata[skiprows:,0]
    yawdir = wakedata[skiprows:,1]
    s = wakedata[0,3:]
    V = wakedata[skiprows+1:,3:]
    Vaxis = wakeaxisdata[skiprows+1:,3:]
    Vfs = wakedata[skiprows+1:,2]

    wakeDelV = V
    wakeaxisDelV = Vaxis
    for i,v in enumerate(V):
        wakeDelV[i,:] = Vfs[i] - wakeDelV[i,:]
        wakeDelV[i,:] = wakeDelV[i,:]/Vfs[i]
        wakeaxisDelV[i,:] = Vfs[i] - wakeaxisDelV[i,:]
        wakeaxisDelV[i,:] = wakeaxisDelV[i,:]/Vfs[i]

    return {'s': s,'wakeDelV': wakeDelV, 'wakeaxisDelV': wakeaxisDelV} 

gamma = ((1-tura)/(1-2*tura))**0.5
Ct=1-(1-tura)**2

figuredir = '/home/%s/figures/%s' % (username,exptitle)
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)

filename = 'Wakeanalysis_%s' % exptitle
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

color = ['k', 'r', 'g'] 

for i,v in enumerate(expnr):
    data = readwakeanalysis(exptitle,v)

    s = data['s']
    snorm = data['s']/(2*turr)

    wakeDelV = data['wakeDelV']
    wakeaxisDelV = data['wakeaxisDelV']

    wakeDelVmean = np.mean(wakeDelV,axis=0)
    wakeaxisDelVmean = np.mean(wakeaxisDelV,axis=0)
    wakeDelVmedian = np.median(wakeDelV,axis=0)
    wakeaxisDelVmedian = np.median(wakeaxisDelV,axis=0)

    if plothourlymean:
        hour = firsthour
        k = 0 
        for j in range(0,len(wakeDelV[:,0]),6):
            jmax = j + 6
            if jmax>len(wakeDelV[:,0]):
                jmax = len(wakeDelV[:,0])
            wakeDelVhourlymean = np.mean(wakeDelV[j:jmax,:],axis=0)
            ax.plot(snorm[:],wakeDelVhourlymean,'%so' % (color[k]),label='hour = %s' % hour)
            hour += 1
            k += 1

    if savedata:
        np.savetxt(figuredir + '/data_%s.txt' %v, wakeDelV,fmt='%5.2f')

    if plotall:
        for j,w in enumerate(wakeDelV):
            if overdisk:
                plt.plot(snorm[:],wakeDelV[j,:],'^%s' % color[i]) 
            if ataxis:
                plt.plot(snorm[:],wakeaxisDelV[j,:],'^%s' % color[i]) 

    if plotmean:
        if overdisk:
            ax.plot(snorm[:],wakeDelVmean,'%so' % (color[i]),label='%s disk averaged' % optlabel[i])
        if ataxis:
            ax.plot(snorm[:],wakeaxisDelVmean,'%s+' % (color[i]),label='%s at axis' % optlabel[i])
    if plotmedian:
        if overdisk:
            ax.plot(snorm[:],wakeDelVmedian,'go',label='median of $\Delta V/V_{\infty}$ disk averaged')
        if ataxis:
            ax.plot(snorm[:],wakeaxisDelVmedian,'g+',label='median of $\Delta V/V_{\infty}$ at axis')




if tophat:
    stophat = np.arange(s[0],s[-1],1)
    for i in range(0,ntophat):
        wakeDelVth= (2*tura)/((1+kwake[i]*stophat/(gamma*turr))**2)
        snormtophat = stophat/(2*turr)
        ax.plot(snormtophat,wakeDelVth,'k',label='Jensen model, $\kappa_{\mathrm{wake}}$ = %s' % kwake[i])

plt.xlim([0,np.amax(snorm)+1])
#plt.ylim([-0.1,0.60])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.7),ncol=4,prop={'size':10})
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


plt.xlabel('$s/D$')
plt.ylabel('$\Delta V/V_{\infty}$'+ optylabel)
plt.gca().set_aspect(10)
if show:
    plt.show()
if save:
    plt.savefig(figurepath,bbox_inches='tight')

plt.close()





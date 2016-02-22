import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker
import os.path
import datetime

presentation = True
mpl.rcParams['font.size']=10.
if presentation:
    mpl.rcParams['font.family']='sans-serif'
    mpl.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']   
    mpl.rcParams['font.sans-serif']='cm'

nsubfigures = 2
a4height = 11.7
a4width = 8.27
margin = .7
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth
if presentation:
    def cm2inch(value):
        return value/2.54
#12.8cm x 9.6cm
    figwidth = cm2inch(9)
    figheight = cm2inch(6)

print 'figheight, figwidth = ', figheight, figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

exptitle = 'Single_turbine_EUROCS'
expnr = '450'
expsdir = '/home/pim/Les/Experiments'
expdir = expsdir + '/%s/%s' % (exptitle, expnr)

colorstab = ['#939393','#00A6D6']

cturid = '001'
turdata = np.loadtxt(expdir + '/windturbinedata.' + expnr,skiprows=1)
kk = 0
while turdata[kk,1] <= 3600:
    kk += 1

ax.plot(turdata[kk:,1]/3600,turdata[kk:,3]*1e-6,'k')
plt.xlim(1,24)
plt.ylim(0,.6)
ax.set_xticks(np.arange(4,24,4))
ax.set_yticks(np.arange(0.1,0.7,0.2))
plt.xlabel('Time [h]')
plt.ylabel('Power production [MW]')

figuredir = '/home/pim/figures/poweranalysis/NorthHoyle' 
if not os.path.isdir(figuredir):
    os.makedirs(figuredir)
filename = 'poweranalysis'
for i,v in enumerate(expnr):
    filename += '_' + v
tdy = datetime.datetime.today()
filename += '_' + tdy.strftime('%d%m_%H%M%S')
figurepath = figuredir + '/%s.pdf' % (filename)
plt.savefig(figurepath,bbox_inches='tight')
#plt.show()



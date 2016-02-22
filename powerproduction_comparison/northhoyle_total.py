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
    figwidth = cm2inch(10)
    figheight = cm2inch(7)

print 'figheight, figwidth = ', figheight, figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

exptitle = ['NorthHoyle_NBL','NorthHoyle_CBL','NorthHoyle_NBL','NorthHoyle_CBL']
expnr = ['102', '104', '111', '111']
expsdir = '/home/pim/Les/Experiments'

colorstab = ['#939393','#00A6D6','#939393','#00A6D6']
markerdir = ['-', '-', ':', ':']
labelstab = ['Neutral (north)', 'Convective (north)','Neutral (west)', 'Convective (west)']
#labelstab = ['Neutral', 'Convective','Neutral (west)', 'Convective (west)']
upwindrow = [27,28,29]
upwindrow_west = [6,11,16,21]

for e, ee in enumerate(exptitle):
    print 'exp ', ee

    expdir = expsdir + '/%s/%s' %(ee,expnr[e])

    windfarmdata = np.loadtxt(expdir + '/windfarmdata.inp.' + expnr[e],skiprows=1)
    turid = windfarmdata[:,0]

    k = 0
    kk = 0
    Pref = 0
    for i,v in enumerate(turid):
        cturid = '%03i' % int(v)
        print 'turid ', cturid
        turdata = np.loadtxt(expdir + '/windturbinedata.' + cturid + '.' + expnr[e],skiprows=1)
        if k == 0:
            while turdata[kk,1] <= 0:
                kk += 1
                print 'kk = ', kk
        P = turdata[kk:,3]
        if i == 0:
            Ptot = P
        else:
            Ptot = Ptot + P 
        if e < 2:
            if v in upwindrow:
                if v == upwindrow[0]:
                    Pref = P
                else:
                    Pref = Pref + P
        else:
            if v in upwindrow_west:
                if v == upwindrow_west[0]:
                    Pref = P
                else:
                    Pref = Pref + P
        k += 1

    if e < 2:
        ax.plot(turdata[kk:,1]/3600.-6,Ptot/(30*Pref/3.),markerdir[e], color = colorstab[e], label = labelstab[e])
    else: 
        ax.plot(turdata[kk:,1]/3600.-6,Ptot/(30*Pref/4.),markerdir[e], color = colorstab[e], label = labelstab[e])
    #ax.plot(turdata[kk:,1]/3600.,Ptot*1e-6,'-', color = colorstab[1])

plt.xlabel('Time [h]')
plt.ylabel('Relative power of wind farm')
plt.xticks(np.arange(0.5,3,0.5))

plt.xlim(0.2,3)
plt.ylim(0,1.2)
if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax.set_xticklabels(ax.get_xticks(), fontProperties)
    ax.set_yticklabels(ax.get_yticks(), fontProperties)
    ax.legend(fontsize=9,frameon=False,loc='best',ncol=2)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    ax.set_yticks(np.arange(0.2,1.4,.2))

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



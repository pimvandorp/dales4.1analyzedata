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

exptitle = ['NorthHoyle_NBL', 'NorthHoyle_CBL']
expnr = ['111', '111']

expsdir = '/home/pim/Les/Experiments'

row1 = np.array([21,22,23,24,25])
row2 = np.array([21,22,23,24,25])-5
row3 = np.array([21,22,23,24,25])-10
row4 = np.array([21,22,23,24,25])-15
rows = np.zeros((5,4))
rows[:,0] = row1
rows[:,1] = row2
rows[:,2] = row3
rows[:,3] = row4

P = np.zeros((len(rows),2))
Pmean = np.zeros((len(rows),2))

x = np.arange(1,6,1)

colorstab = ['#939393','#00A6D6']
labelstab = ['Neutral', 'Convective']

for e, ee in enumerate(exptitle):
    print 'exp ', ee

    expdir = expsdir + '/%s/%s' %(ee,expnr[e])

    windfarmdata = np.loadtxt(expdir + '/windfarmdata.inp.' + expnr[e],skiprows=1)
    turid = windfarmdata[:,0]

    for r in range(len(rows[0,:])):
        print 'row ', r
        k = 0
        kk = 0
        for i,v in enumerate(turid):
            if v in rows[:,r]: 
                cturid = '%03i' % int(v)
                print 'k, turid ', k, cturid
                turdata = np.loadtxt(expdir + '/windturbinedata.' + cturid + '.' + expnr[e],skiprows=1)
                P[k,0] = v
                if k == 0:
                    while turdata[kk,1] <= 7200:
                        kk += 1
                P[k,1] = np.mean(turdata[kk:,3])

                k += 1
        #P = np.flipud(np.sort(P,axis=0))
        Pmean = Pmean + P
        #plt.plot(x,P/P[0,1])

    Pmean = Pmean/len(rows[0,:])
    ax.plot(x,Pmean[:,1]/Pmean[0,1],'o', color = colorstab[e], label = labelstab[e],zorder=10,clip_on=False)

s = 0
for stab in ['neutral', 'vu']:
    obsdata = np.loadtxt('./northhoyle_ALBLAS/258_%s.txt' % stab)
    obsdata_lower = np.loadtxt('./northhoyle_ALBLAS/258_%s_lower.txt' % stab)
    obsdata_upper = np.loadtxt('./northhoyle_ALBLAS/258_%s_upper.txt' % stab)
    #ax.plot(x,obsdata[:,1],'-',color = colorstab[s], zorder=2)
    ax.plot(x,np.append(1,obsdata_lower[:,1]),'-',color = colorstab[s], zorder=2)
    ax.plot(x,np.append(1,obsdata_upper[:,1]),'-',color = colorstab[s], zorder=2)
    ax.fill_between(x, np.append(1,obsdata_lower[:,1]),np.append(1,obsdata_upper[:,1]), color=colorstab[s], alpha='0.2',zorder=1)
    s += 1
plt.xlabel('Wind turbine row')
plt.ylabel('Power relative to upwind row')

if presentation:
    fontProperties = {'family':'sans-serif', 'size' : 10}
    ax.set_xticklabels(ax.get_xticks(), fontProperties)
    ax.set_yticklabels(ax.get_yticks(), fontProperties)
    ax.legend(fontsize=9,frameon=False,loc='lower right')
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    ax.set_xticks(np.arange(1,6))
    ax.set_yticks(np.arange(0.2,1.2,.2))

plt.xlim(1,5)
plt.ylim(0,1)


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



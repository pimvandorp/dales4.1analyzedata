import numpy as np
import matplotlib.pyplot as plt

exptitle = 'Hornsrev_CBL'
expnr = '002'
expsdir = '/home/pim/Les/Experiments'
expdir = expsdir + '/%s/%s' %(exptitle,expnr)

windfarmdata = np.loadtxt(expdir + '/windfarmdata.inp.' + expnr,skiprows=1)
turid = windfarmdata[:,0]
row = [8,17,26,35,44,53,62,71]
P = np.zeros((len(row),2))

#Prow1 = 0
#Prow2 = 0
#for i,v in enumerate(turid):
#    if v < 10:
#        cturid = '%03i' % int(v)
#        turdata = np.loadtxt(expdir + '/windturbinedata.' + cturid + '.' + expnr,skiprows=1)
#        Prow1 = Prow1 + np.mean(turdata[:,3])
#    elif 10 <= v < 20:
#        cturid = '%03i' % int(v)
#        turdata = np.loadtxt(expdir + '/windturbinedata.' + cturid + '.' + expnr,skiprows=1)
#        Prow2 = Prow2 + np.mean(turdata[:,3])
#print Prow1
#print Prow2

obsdata = np.loadtxt('./hornsrev_PORTEAGEL/neutral_270deg2.5.txt')

k = 0
kk = 0
for i,v in enumerate(turid):
    if v in row: 
        cturid = '%03i' % int(v)
        turdata = np.loadtxt(expdir + '/windturbinedata.' + cturid + '.' + expnr,skiprows=1)
        P[k,0] = v
        if k == 0:
            while turdata[kk,1] <= 3600:
                kk += 1
        P[k,1] = np.mean(turdata[kk:,3])
        k += 1

x = np.arange(1,len(row)+1,1)
plt.plot(x,P/P[0,1])
plt.plot(obsdata[:,0],obsdata[:,1],'kd')
plt.ylim(0.6,1)
plt.show()


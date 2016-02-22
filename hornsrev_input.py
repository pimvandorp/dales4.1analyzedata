#/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pupynere as pu
import matplotlib as mpl
import datetime
import os.path

hour = 3600
username = 'pim'

Rd = 287.06         #value from ECMWF IFS 21r4 287.04
Rv = 461.5          #gas constant for water vapor [J/K/kg]
eps = Rv/Rd
cp = 1004.703       #        
Lv = 2.5008e6       #latent heat of condensation
p0 = 1.e5           #reference pressure
g  = 9.80665        #gravity acceleration
pi = 3.14159
Tkel = 273.16

mpl.rcParams['font.size']=10.

nsubfigures = 2
a4height = 11.7
a4width = 8.27
margin = 1
figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth

fig = plt.figure()
ax = plt.subplot(111)

fig.set_size_inches(figwidth,figheight)

def readproptmser(exptitle,expnr,prop,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    f = pu.netcdf_file(expdir + '/tmser.%s.nc' % (expnr))

    time = f.variables['time'][:]

    prop = f.variables[prop][:] 

    return {'time': time, 'prop':prop} 


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def readprop(exptitle,expnr,prop,username='pim'):
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    f = pu.netcdf_file(expdir + '/profiles.%s.nc' % (expnr))

    # columns of data
    zt = f.variables['zt'][:] # full levels
    zm = f.variables['zm'][:] # half levels

    # rows of data
    time = f.variables['time'][:]

    p = f.variables[prop][:,:] 

    return {'zt' : zt, 'zm' : zm, 'time': time, prop:p} 



datain = np.loadtxt('/home/pim/dales4.1inputgen/hornsrev/radiosond_day.txt', skiprows=6)
datanight = np.loadtxt('/home/pim/dales4.1inputgen/hornsrev/radiosond_night.txt', skiprows=6)

heightasc = datain[:,1]
presasc = datain[:,0]
tempasc = datain[:,2]
relhasc = datain[:,4]
wsasc = datain[:,7]

heightnight = datanight[:,1]
presnight = datanight[:,0]
tempnight = datanight[:,2]
relhnight = datanight[:,4]
wsnight = datanight[:,7]

tempmetmast = 273.16 + np.array([4,3.6])
heightmetmast = np.array([16,64])

cp = 1004.703 
g = 9.81
Rd = 287.06  
Rv = 461.5
p0 = 1.e5

psurf = 1.037e5 

Tsurf = 273.16+4.7
csurf = ((psurf/p0)**(Rd/cp))
thetasurf = Tsurf/csurf

exptitle = 'Hornsrev_wakeclouds'
expnr = ['203' , '206'] 

marker = [ '-', ':','.-','-^']
t_start = 2.5*hour

Tn = .8+273.16
preshn = 96700
esatn = 610.78 * np.exp ((17.2694*(Tn-273.16))/(Tn-35.86))
rsatn = Rd/Rv * esatn/(preshn-esatn)
qsatn = rsatn/(1+rsatn)
print qsatn

# fit : 276.38
height = np.arange(0,400,1)
Tfit = []
for i,v in enumerate(height):
    Tfit = np.append(Tfit,277.2-4.201e-3*v)

for i,v in enumerate(expnr):
    if v == '936':
        exptitle = 'Single_turbine_Hornsrev'
        t_start = 6000
    data = readprop(exptitle,v,'thl')
    zt = data['zt']
    zm = data['zm']
    time = data['time']
    t_start_in = find_nearest(time,t_start)
    print 't_start = ', time[t_start_in]

    thl = data['thl'][t_start_in,:] 
    presh = readprop(exptitle,v,'presh')['presh'][t_start_in,:]
    qtsim = readprop(exptitle,v,'qt')['qt'][t_start_in,:]
    qlsim = readprop(exptitle,v,'ql')['ql'][t_start_in,:]
    w2r = readprop(exptitle,v,'w2r')['w2r'][t_start_in,:]

    qsat = np.zeros((len(thl)))
    qsat2 = np.zeros((len(thl)))
    T = np.zeros((len(thl)))
    esat = np.zeros((len(thl)))
    rsat = np.zeros((len(thl)))

    for j,w in enumerate(thl):
        T[j] = (presh[j]/p0)**(Rd/cp)*w
        esat[j] = 610.78 * np.exp ((17.2694*(T[j]-273.16))/(T[j]-35.86))
        rsat[j] = Rd/Rv * esat[j]/(presh[j]-esat[j])
        qsat[j] = rsat[j]/(1+rsat[j])

        temperature = False

    if temperature:
        T = np.append(Tsurf,T)
        thl = np.append(thetasurf,thl)
        zt = np.append(0,zt)
        ax.plot(T,zt,'%sg' % marker[i],label='T (%s)' % v, zorder = 3)
        ax.plot(thl,zt,'%sk' % marker[i],label='$\\theta_l$ (%s)' % v, zorder = 3)
        #ax.plot(273.16+tempasc[:6],heightasc[:6],'-dg',label = 'RS day')
        #ax.plot(273.16+tempnight[:6],heightnight[:6],'-^g',label = 'RS')
        ax.plot(274.991*csurf,0,'og',clip_on=False,zorder = 10)
        ax.plot(273.16+4.7,0,'dr',clip_on=False, zorder = 10)
        #ax.plot(Tfit,height,'y',label = 'Translated fit of RS')
        ax.plot(tempmetmast,heightmetmast,'dr', label = 'Met. mast', zorder = 6)
        ax.set_xlabel('Temperature $\mathrm{[K]}$')
        ax.set_ylabel('Height $\mathrm{[m]}$')
        ax.set_xticks(np.arange(274,279,1))
        ax.set_yticks(np.arange(50,250,50))
    else:
        ax.plot(1000*qsat,zt,'%sg' % marker[i],label='$q_{\mathrm{sat}}$ (%s)' % v)
        ax.plot(1000*qtsim,zt,'%sk' % marker[i],label='$q_{\mathrm{sim}}$ (%s)' % v)
        #ax.plot(1000*qsat,zt,'g' ,label='$q_{\mathrm{sat}}$ (%s)' % v)
        #ax.plot(1000*qtsim,zt,'k' ,label='$q_{\mathrm{t}}$ (%s)' % v)
        #ax.plot(100000*qlsim,zt,'b',label='$10^3 \\times q_{l,\mathrm{sim}}$')
        ax.set_xlabel('Humidity $\mathrm{[g/kg]}$')
        ax.set_ylabel('Height $\mathrm{[m]}$')
        plt.xlim(4.,5.5)
        #ax.set_xticks(np.arange(4.,5.2,0.2))
        ax.set_yticks(np.arange(50,250,50))

qt2h = 5.1e-3 - (5.1e-3-4.0e-3)*(1-np.exp(-1/100.*(zt)))
#ax.plot(1000*qt2h,zt)

ax.plot(ax.get_xlim(),[70,70],':k',zorder = 1, alpha = 0.5)
ax.plot(ax.get_xlim(),[110,110],':k',zorder = 1, alpha = 0.5)
ax.plot(ax.get_xlim(),[30,30],':k',zorder = 1, alpha = 0.5)
plt.ylim(0,400)
ax.legend(loc='upper right',frameon=False,fontsize = 8)
#plt.title('%s s after initialization' % t_start)

save = False
if save:
    figuredir = '/home/%s/figures/profilesanalysis/hornsrev' % (username )
    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)

    filename = 'profile'
    for i,v in enumerate(expnr):
        filename += '_%s' % v
        
    tdy = datetime.datetime.today()
    filename += '_%s' % tdy.strftime('%d%m_%H%M%S')

    figurepath = figuredir + '/%s.pdf' % (filename)
    print figurepath
    print 'Saving figure'
    plt.savefig(figurepath,bbox_inches='tight')
else:
    plt.show()
    plt.close()


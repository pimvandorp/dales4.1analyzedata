#!/usr/bin/python2.7
# Filename: fielddumpanalysis_2.py
# By Pim van Dorp, TU Delft, section Atmospheric Physics, 7 nov 2015
# Description: Extract, analyze and plot data from DALES' fielddump .nc files, in a smart way

#-----------------------------------------------------------------
#                  0 Import Python packages             
#-----------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
import readnamoptions as rno
from scipy import ndimage
import os.path
import os
import datetime as dt

def simplefieldplot(X,Y,Z,exptitle='',expnr='',prop='',N = 200,
                    plot_title=0,xlabel ='x',ylabel ='y',filetype='pdf',width=0,height=0,username='pim',colorbar=True,usr_size=False,figwidth=2.7,figheight=2.7,aspectratio=1):

    tdy = dt.datetime.today()
    
    figuredir = '/home/%s/figures/%s' % (username,exptitle)

    if not os.path.isdir(figuredir):
        os.makedirs(figuredir)
    
    filename = '%s_%s_%s_%s_%s_%s_%s_%s' % (exptitle, expnr, prop, xlabel[1],ylabel[1],t_start_title,t_end_title, tdy.strftime('%d%m_%H%M%S'))
    if presentation:
        filename += '_presentation'
    if windfarm:
        filename += '_windfarm'
    figurepath = figuredir + '/%s.%s' % (filename,filetype)
    optfilepath = figuredir + '/%s.txt' % (filename)

    mpl.rcParams['font.size']=10.
    if presentation:
        mpl.rcParams['font.family']='sans-serif'
        mpl.rcParams['text.latex.preamble'] = [r'\usepackage{sansmath}',r'\sansmath',r'\usepackage{siunitx}',r'\sisetup{detect-all}']           

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1,aspect='equal')

    if usr_size == True:
        fig.set_size_inches(figwidth,figheight)

    print np.shape(Z)

    print 'Plotting contours'
    minval = np.amin(Z[1:,:])
    maxval = np.amax(Z)
    
    print 'minval, maxval', minval, maxval
    minvalrnd = round(minval,2)
    maxvalrnd = round(maxval,2)



    if axis:
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if plot_title != 0:
            ax.set_title(plot_title)

        if presentation:
            fontProperties = {'family':'sans-serif', 'size' : 10}
            ax.set_xticklabels(ax.get_xticks(), fontProperties)
            ax.set_yticklabels(ax.get_yticks(), fontProperties)
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

        if colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            if diag:
                if prop == 'fx':
                    cbar = plt.colorbar(CF, cax = cax,ticks=[minval,0])
                    cbar.set_ticklabels(['$-1$', '$0$' ]) 
                    ax.set_title('Force in $x^*$-direction')
                elif prop == 'fy' or prop == 'fz':
                    cbar = plt.colorbar(CF, cax = cax,ticks=[minval,0,maxval])
                    cbar.set_ticklabels(['$-1$' ,'$0$', '$1$']) 
                    if prop == 'fy':
                        ax.set_title('Force in $y^*$-direction')
                    else:
                        ax.set_title('Force in $z^*$-direction')
            else:
                cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                cbar.set_ticklabels(['$%s$' % minvalrnd, '$%s$' % maxvalrnd ]) 
                #tick_locator = ticker.MaxNLocator(nbins=5)
                #cbar.locator = tick_locator
                #if presentation:
                    #cbar.set_ticklabels([3.0,6.7])
                    #cax.tick_params(labelsize=10)
                    #for l in cbar.ax.yaxis.get_ticklabels():
                    #    print l
                    #    l.set_family('monospace')

                #cbar.solids.set_rasterized(True)  
            cbar.update_ticks()

        if diag:
            if prop == 'towergeoN':
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar = plt.colorbar(CF, cax = cax)
                #cbar.set_ticklabels(['$0$', '$1$']) 
                ax.set_title('$\mathcal{T}$ at $x^*=0$')
            elif prop == 'nacgeoN':
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar = plt.colorbar(CF, cax = cax)
                #cbar.set_ticklabels(['$0$', '$%s$' % maxvalrnd]) 
                ax.set_title('$\mathcal{N}$ at $x^*=0$')
            elif prop == 'rotorgeoN':
                maxvalrnd = int(maxvalrnd)
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar = plt.colorbar(CF, cax = cax)
                #cbar.set_ticklabels(['$0$', '$%s$' % maxvalrnd]) 
                ax.set_title('$\mathcal{R}$ at $x^*=0$')
            elif prop == 'annugeoN_1':
                maxvalrnd = int(maxvalrnd)
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar.set_ticklabels(['$0$', '$%s$' % maxvalrnd]) 
                ax.set_title('$\mathcal{A}_1$ at $x^*=0$')
            elif prop == 'annugeoN_3':
                maxvalrnd = int(maxvalrnd)
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar.set_ticklabels(['$0$', '$%s$' % maxvalrnd]) 
                ax.set_title('$\mathcal{A}_3$ at $x^*=0$')
            elif prop == 'annugeoN_5':
                maxvalrnd = int(maxvalrnd)
                #cbar = plt.colorbar(CF, cax = cax,ticks=[minval,maxval])
                #cbar.set_ticklabels(['$0$', '$%s$' % maxvalrnd]) 
                ax.set_title('$\mathcal{A}_5$ at $x^*=0$')
            if xlabel == '$y/D$':
                ax.set_xticks([-0.5,0, 0.5])
            if ylabel == '$z/D$':
                ax.set_yticks([0.5,1, 1.5])

            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax.set_xlabel('$y^*/D$')
            ax.set_ylabel('$z^*/D$')

        if not windfarm and not diag:
            if ylabel == '$y$':
                ax.set_yticks([-100,0, 100])
            elif ylabel == '$y/D$':
                ax.set_yticks([-1,0, 1])
            elif ylabel == '$z$':
                ax.set_yticks([100, 200])
            elif ylabel == '$z/D$':
                ax.set_yticks([1, 2])
            
            if xlabel == '$x$':
                ax.set_xticks([0, 500,1000,1500,2000])

            elif xlabel == '$x/D$':
                ax.set_xticks([0,5,10,15,20])
                ax.set_xlim(-0.90,20)


        #ax.plot([0,0],[0.5,1.5], 'k-', lw=1.2)


    else:
        ax.set_axis_off()
        #ax = plt.axes([0, 0, 1, 1])
        #x.axis('off')

    V = np.linspace(minvalrnd,maxval,N)
    CF = ax.contourf(X,Y,Z,V,rasterized=True) 
    #CL = ax.contour(X,Y,Z,V,rasterized=True) 
    for c in CF.collections:
        c.set_edgecolor("face")

    print 'Saving figure'

    if filetype == 'eps':
        fig.savefig('%s.eps' % filename ,bbox_inches='tight',format='%s' % filetype,dpi=100)
        os.system('cat %s.eps | epstopdf --filter >%s.pdf' % (filename,filename)) 
        os.system('mv %s.pdf %s' % (filename, figuredir))
        os.system('rm %s.eps' % filename)
    else:
        fig.savefig(figurepath,bbox_inches='tight',format='%s' % filetype,dpi=100)

#-----------------------------------------------------------------
#                            1  Input            
#-----------------------------------------------------------------
username = 'pim'
livedata = True

presentation = True
axis = True

eurocs = True
day = True
night = False

gabls = False
cbl = False
nbl = False
diag = False

expnr = '410'
windfarm = False

if gabls:
    exptitle = 'Single_turbine_GABLS'
if eurocs:
    exptitle = 'Single_turbine_EUROCS'
if cbl:
    exptitle = 'Single_turbine_CBL'
if nbl:
    exptitle = 'Single_turbine_NBL'
if diag:
    exptitle = 'DIAG'

readnamopt = True
if readnamopt:
    namopt = rno.readnamoptions(exptitle,expnr,username)
    dy = namopt['dy']
    dx = namopt['dx']
    dz = namopt['dz']
    xsize = namopt['xsize']
    ysize = namopt['ysize']
    zsize = namopt['zsize']
    turhx = namopt['turhx']
    turhy = namopt['turhy']
    turhz = namopt['turhz']
    ntur = namopt['ntur']
    for i in range(0,ntur):
        turhxgr = int(round(turhx[i]/dx)) 
        turhygr = int(round(turhy[i]/dy)) 
        turhzgr = int(round(turhz[i]/dz)) 
        turhx[i] = 0.5*dx + dx*(turhxgr-1) 
        turhy[i] = 0.5*dy + dy*(turhygr-1) 
        turhz[i] = 0.5*dz + dz*(turhzgr-1)
    print 'turhx, turhy, turhz = ' , turhx[0], turhy[0], turhz[0]
    print 'dx, dy, dz = ', dx, dy, dz
else:
    dy = 12.5
    dx = 12.5
    dz = 10
    xsize = 2500
    ysize = 2500
    turhz = 100
    turhzgr = int(round(turhz/dz)) 

prop = 'vhoravg'
scale = 1000

xa = 'x' 
ya = 'y'

if windfarm:
    xa = 'x' 
    ya = 'y'
    xa_start = 0
    xa_end = xsize
    ya_start = 0
    ya_end = ysize
    plane = turhz[0]
else:
    if xa == 'y' and ya == 'z':
        xa_start = turhy[0]-80
        xa_end = turhy[0]+80
        ya_start = 0
        ya_end = turhz[0]+60
        plane = turhx[0]
    elif xa == 'x' and ya == 'y':
        xa_start = turhx[0]-100
        xa_end = turhx[0]+2000
        ya_start = turhy[0]-200
        ya_end = turhy[0]+200
        plane = turhz[0]
    elif xa == 'x' and ya == 'z':
        xa_start = turhx[0]-100
        xa_end = turhx[0]+2000
        ya_start = 0 
        ya_end = 250
        plane = turhy[0]
    

print 'Plane at %s' % plane

plotdata = True
save = True

filetype = 'eps'

wakeanalysis = False
if wakeanalysis:
    prop = 'vhoravg'
    plotdata = False
    save = False

turbanalysis = False
if turbanalysis:
    calctke = False
    if calctke:
        prop = 'vhoravg'
    plotdata = False
    save = False

savesubgrid = False
if savesubgrid:
    prop = 'e12'
    plotdata = False
    save = False

useyawdir = True

if windfarm:
    rotate = False
    appenddomain = False
    trans = False
elif diag:
    rotate = False
    appenddomain = False
    trans = True
    transx = 0
    transy = -turhy[0]
else:
    rotate = True
    appenddomain = True
    trans = True
    transx = -turhx[0]
    transy = -turhy[0]

halflvlx = False
halflvly = False
halflvlz = False

if windfarm:
    normaxes = False
else:
    normaxes = True


if diag:
    normprop = True
else:
    normprop = False


hour = 3600.
if eurocs:
    t_start = 0*hour 
    t_end = 1*hour
else:
    t_start = 3*hour 
    t_end = 3*hour+1800

dtav = 60.

if cbl:
    trange_start = 3*hour
    trange_end = 6*hour
    if expnr == '320':
        trange_start = 0*hour+1
        trange_end = 9*hour
    trange = [int((trange_start)/dtav-1),int((trange_end)/dtav-1)]
elif nbl or gabls:
    trange_start = 8*hour
    trange_end = 11*hour
    trange = [int((trange_start)/dtav-1),int((trange_end)/dtav-1)]
elif eurocs:
    if day:
        trange_start = 11*hour
        trange_end = 12*hour
    elif night:
        trange_start = 23*hour
        trange_end = 24*hour
    trange = [int((trange_start)/dtav-1),int((trange_end)/dtav-1)]
elif diag:
    trange=[0,19]
print 'trange = ', trange

t_start_title = int(t_start/hour + (trange[0]*dtav)/hour)+1
t_end_title = int(t_end/hour + (trange[0]*dtav)/hour)+1

#-----------------------------------------------------------------
#                         1.2 Plot options
#-----------------------------------------------------------------
usr_size = True

nsubfigures = 1
a4height = 11.7
a4width = 8.27
if nsubfigures == 1:
    margin = 1.7
else:
    margin = 0.3

figwidth = (a4width-2*margin)/float(nsubfigures)
figheight = figwidth

if presentation:
    def cm2inch(value):
        return value/2.54
#12.8cm x 9.6cm
    figwidth = cm2inch(9)
    figheight = cm2inch(9)

if usr_size:
    print 'figwidth, figheight = ', figwidth, figheight

colorbar = False

#-----------------------------------------------------------------
#                      2 Read and analyze data
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#                               2.1 Time
#-----------------------------------------------------------------
t_start_in = int(t_start/dtav)
t_end_in = int(t_end/dtav-1)

print 't_start, t_end = ', t_start, t_end
print 't_start_in, t_end_in = ', t_start_in, t_end_in

#-----------------------------------------------------------------
#                               2.2 Data
#-----------------------------------------------------------------
print 'Loading array from disk'
if livedata:
    datadir = '/nfs/livedata/%s/binary_fd_data/%s/%s' % (username,exptitle,expnr)
else:
    datadir = '/home/%s/fd_data/%s' % (username,exptitle)

filename = '%s_%s_%s_%s_%s.npy' % (exptitle, expnr, prop,trange[0],trange[1])
datapath = datadir + '/%s' % (filename)

pfull = np.load(datapath,mmap_mode='r')


if turbanalysis:
    print 'Start turbanalysis'
    filename = '%s_%s_w_%s_%s.npy' % (exptitle, expnr, trange[0],trange[1])
    datapath = datadir + '/%s' % (filename)
    w = np.load(datapath,mmap_mode='r')
    if calctke:
        print 'Calculating TKE'
        TKE = 0.5*(np.var(pfull,axis=0) + np.var(w,axis=0))
    else:
        print 'Multiplying prop and w arrays'
        pfull = np.multiply(pfull,w) 


print 'Calculating time average'
pfull = np.mean(pfull[t_start_in:t_end_in,:,:,:],axis=0)
print np.shape(pfull)

if appenddomain:
    print 'Appending domain'
    pfull = np.append(pfull,pfull,axis=2)
    pfull = np.append(pfull,pfull,axis=1)

if rotate:
    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)

    ntur = namopt['ntur']

    winddirdata = np.loadtxt(expdir + '/winddir.%s' % (expnr),skiprows=1)
    m = np.shape(winddirdata)[0]
    n = np.shape(winddirdata)[1]
    winddiravg = np.zeros((ntur,m/ntur))
    yawdir = np.zeros((ntur,m/ntur))
    winddirinst = np.zeros((ntur,m/ntur))

    for i in range(0,ntur):
        winddirinst[i,:] = winddirdata[i::ntur,2] 
        winddiravg[i,:] = winddirdata[i::ntur,3] 
        yawdir[i,:] = winddirdata[i::ntur,4] 
        if ntur == 1:
            winddirinst = winddirinst[0,trange[0]:trange[1]]
            winddiravg = winddiravg[0,trange[0]:trange[1]]
            yawdir = yawdir[0,trange[0]:trange[1]]

    pshp = np.shape(pfull)
    pa = turhxgr
    pb = pshp[2]-turhxgr
    pe = pshp[2]
    pc = turhygr
    pd = pshp[1]-turhygr
    pf = pshp[1]

    print 'Start rotation'
    if useyawdir:
        angle = (180/3.14)*np.mean(yawdir[t_start_in:t_end_in])
    else:
        angle = (180/3.14)*np.mean(winddiravg[t_start_in:t_end_in])
    print 'Angle (deg,rad) = ', angle, np.mean(winddiravg[t_start_in:t_end_in])

    for j in range(0,pshp[0]):
        pfullpad = np.mean(pfull[j,:,:])*np.ones((2*pf,2*pe))
        pfullpad[pd:pd+pf,pb:pb+pe] = pfull[j,:,:]
        pfullpad = ndimage.interpolation.rotate(pfullpad,angle,reshape=False,cval=np.mean(pfull[j,:,:]))
        pfull[j,:,:] = pfullpad[pd:pd+pf,pb:pb+pe]

x = np.arange(0,np.shape(pfull)[2])*dx+0.5*dx #xt
y = np.arange(0,np.shape(pfull)[1])*dy+0.5*dy #yt
z = np.arange(0,np.shape(pfull)[0])*dz+0.5*dz #zt

if halflvlx:
    x = x - 0.5*dx
if halflvly:
    y = y - 0.5*dy
if halflvlz:
    z = z - 0.5*dz

if trans:
    x = x + transx
    y = y + transy

#-----------------------------------------------------------------
#                           4 Wake analysis
#-----------------------------------------------------------------
if wakeanalysis:
    datadir = '/home/%s/dales4.1analyzedata/wakeanalysis/data' % (username)

    if not os.path.isdir(datadir):
        os.makedirs(datadir)
    
    filename = '%s_%s_Vw_ax' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    Vw_ax = pfull[turhz[0]/dz,turhy[0]/dy,:]
    np.save(datapath,Vw_ax)

    filename = '%s_%s_vhoravg_xy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    vhoravg_xy = pfull[turhz[0]/dz,0:ysize/dy,:]
    np.save(datapath,vhoravg_xy)

    filename = '%s_%s_vhoravg_xz' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    vhoravg_xz = pfull[:,turhy[0]/dy,:]
    np.save(datapath,vhoravg_xy)

    filename = '%s_%s_xt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,x)
    filename = '%s_%s_yt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,y)
    filename = '%s_%s_zt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,z)

if savesubgrid:
    datadir = '/home/%s/dales4.1analyzedata/sgsanalysis/data' % (username)

    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    filename = '%s_%s_e12_xy' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    e12_xy = pfull[turhz[0]/dz,0:ysize/dy,:]
    np.save(datapath,e12_xy)

    filename = '%s_%s_e12_xz' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    e12_xz = pfull[:,turhy[0]/dy,:]
    np.save(datapath,e12_xz)

if turbanalysis:
    datadir = '/home/%s/dales4.1analyzedata/turbanalysis/data' % (username)

    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    filename = '%s_%s_%swavg_xy' % (exptitle, expnr,prop)
    datapath = datadir + '/%s' % (filename)
    propwavg_xy = pfull[turhz[0]/dz,0:ysize/dy,:]
    np.save(datapath,propwavg_xy)

    filename = '%s_%s_%swavg_xz' % (exptitle, expnr,prop)
    datapath = datadir + '/%s' % (filename)
    propwavg_xz = pfull[:,turhy[0]/dy,:]
    np.save(datapath,propwavg_xz)

    filename = '%s_%s_xt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,x)
    filename = '%s_%s_yt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,y)
    filename = '%s_%s_zt' % (exptitle, expnr)
    datapath = datadir + '/%s' % (filename)
    np.save(datapath,z)

    if calctke:
        filename = '%s_%s_TKE_xz' % (exptitle, expnr)
        datapath = datadir + '/%s' % (filename)
        TKE_xz = TKE[:,turhy[0]/dy,:]
        np.save(datapath,TKE_xz)

        filename = '%s_%s_TKE_xy' % (exptitle, expnr)
        datapath = datadir + '/%s' % (filename)
        TKE_xy = TKE[turhz[0]/dz,0:ysize/dy,:]
        np.save(datapath,TKE_xy)

#-----------------------------------------------------------------
#                            5 Plot data
#-----------------------------------------------------------------
pfull = pfull/scale

print np.shape(pfull)

if plotdata:
    if xa == 'x' and ya == 'z':
        xa_start = min(abs(int(round(xa_start/dx))),0)
        xa_end = int(round(xa_end/dx))
        ya_start = int(round(ya_start/dz))
        ya_end = int(round(ya_end/dz))
        print xa_start, xa_end, ya_start, ya_end
        if normprop:
            pfull = pfull/np.amax(pfull[ya_start:ya_end,plane/dy,xa_start:xa_end])

        if normaxes:
            xlabel = '$x/D$'
            ylabel='$z/D$'
            x = x/100.
            z = z/100.
        else:
            xlabel = '$x$'
            ylabel='$z$'
        if save:
            simplefieldplot(x[xa_start:xa_end+1],z[ya_start:ya_end+1],
                    pfull[ya_start:ya_end+1,plane/dy,xa_start:xa_end+1],exptitle,expnr,prop,
                    xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
        else:
            plt.contourf(x[xa_start:xa_end],y[ya_start:ya_end],pfull[plane/dz,ya_start:ya_end,xa_start:xa_end],N=200)

            plt.show()

    elif xa == 'x' and ya == 'y':
        xa_start = min(abs(int(round(xa_start/dx))),0)
        xa_end = int(round(xa_end/dx))
        ya_start = int(round(ya_start/dy))
        ya_end = int(round(ya_end/dy))
        print xa_start, xa_end, ya_start, ya_end

        if normprop:
            pfull = pfull/np.amax(pfull[plane/dz,ya_start:ya_end,xa_start:xa_end])

        if normaxes:
            xlabel = '$x/D$'
            ylabel='$y/D$'
            x = x/100.
            y = y/100.
        else:
            xlabel = '$x$'
            ylabel='$y$'

        if save:
            simplefieldplot(x[xa_start:xa_end+1],y[ya_start:ya_end+1],
                    pfull[plane/dz,ya_start:ya_end+1,xa_start:xa_end+1],exptitle,expnr,prop,
                    xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
        else:
            fig,ax = plt.subplots()

            cax = ax.contourf(x[xa_start:xa_end],y[ya_start:ya_end],pfull[plane/dz,ya_start:ya_end,xa_start:xa_end],N=200)
            cbaxes = fig.add_axes([0.2,1.0,0.6,0.03])
            cbar = fig.colorbar(cax,ticks=[0,1],cax=cbaxes,orientation='horizontal')
            plt.show()

    elif xa == 'y' and ya == 'z':
        xa_start = int(round(xa_start/dy))
        xa_end = int(round(xa_end/dy))
        ya_start = int(round(ya_start/dz))
        ya_end = int(round(ya_end/dz))

        if normprop:
            pfull = pfull/np.amax(abs(pfull[ya_start:ya_end,xa_start:xa_end,plane/dx]))

        if normaxes:
            xlabel = '$y/D$'
            ylabel='$z/D$'
            y = y/100.
            z = z/100.
        else:
            xlabel = '$y$'
            ylabel='$z$'

        if save:
            simplefieldplot(y[xa_start:xa_end+1],z[ya_start:ya_end+1],
                    pfull[ya_start:ya_end+1,xa_start:xa_end+1,plane/dx],exptitle,expnr,prop,
                    xlabel=xlabel,ylabel=ylabel,filetype=filetype,colorbar=colorbar,username=username,usr_size=usr_size,figwidth=figwidth,figheight=figheight) 
        else:
            fig,ax = plt.subplots()

            cax = ax.contourf(x[xa_start:xa_end],y[ya_start:ya_end],pfull[ya_start:ya_end,xa_start:xa_end,plane/dx],N=200)
            cbaxes = fig.add_axes([0.2,1.0,0.6,0.03])
            cbar = fig.colorbar(cax,ticks=[0,1],cax=cbaxes,orientation='horizontal')
            plt.show()

plt.close()


                

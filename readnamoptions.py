#!/umsr/bin/python
#Filename: readnamoptions.py
#Description: reads some useful namoptions from namoptions in directory ../exptitle/expnr

from numpy import *

def readnamoptions(exptitle,expnr,username='pim',turbine=True):

    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)
  
    #Read windturbinemonitor
    filename = '/windturbinemonitor.001.%s' % expnr

    with open(expdir + filename , 'r') as wtdata:
        header = 5
        for i, line in enumerate(wtdata):
            if i in range(header,header+12):
                if i==header+1:
                    size = line.split()
                    xsize = float(size[4])
                    ysize = float(size[5])
                    zsize = float(size[6])
                if i==header+2:
                    grid = line.split()
                    dx = float(grid[4])
                    dy = float(grid[5])
                    dz = float(grid[6])


    #Read namoptions
    with open(expdir + '/namoptions', 'r') as namopt:
        namopt = list(namopt)

    for i in range(len(namopt)):

        if namopt[i].find('runtime')!=-1:
            runtime = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('dtav')!=-1:
            dtav = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('itot')!=-1:
            itot = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('jtot')!=-1:
            jtot = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('kmax')!=-1:
            kmax = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('cu')!=-1:
            cu = float(namopt[i].rstrip()[namopt[i].index('=')+1:]) 
        if namopt[i].find('cv')!=-1:
            cv = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if turbine:
            if namopt[i].find('ntur')!=-1:
                ntur = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
            if namopt[i].find('tura')!=-1:
                tura = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        else:
            ntur = 0
            tura = 0

    #Read windfarmdata.inp
    windfarmdata = zeros((ntur+1,12))
    windfarmdata[:-1,:] = loadtxt(expdir + '/windfarmdata.inp.%s' % expnr,skiprows=1)
    turid = windfarmdata[:,0] 
    turhx = windfarmdata[:,1] 
    turhy = windfarmdata[:,2] 
    turhz = windfarmdata[:,3] 
    turr = windfarmdata[:,4] 

        
    return {'ntur': ntur, 'runtime': runtime, 'dtav': dtav, 'itot': itot, 'jtot': jtot, 'kmax': kmax, 'xsize': xsize, 'ysize': ysize, 'zsize':zsize,'cu': cu, 'cv': cv, 'dx': dx, 'dy': dy, 'dz': dz, 'turhx': turhx, 'turhy':turhy, 'turhz':turhz,'turr':turr}


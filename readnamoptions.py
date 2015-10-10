#!/umsr/bin/python
#Filename: readnamoptions.py
#Description: reads some useful namoptions from namoptions in directory ../exptitle/expnr

from numpy import *

def readnamoptions(exptitle,expnr,username='pim'):

    expsdir = '/home/%s/Les/Experiments' % (username)
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)
  
    with open(expdir + '/windturbinemonitor.%s' % expnr, 'r') as wtdata:
        for i, line in enumerate(wtdata):
            if i in range(0, 12):
                if i==6:
                    size = line.split()
                    xsize = float(size[4])
                    ysize = float(size[5])
                    zsize = float(size[6])
                if i==7:
                    grid = line.split()
                    dx = float(grid[4])
                    dy = float(grid[5])
                    dz = float(grid[6])
                if i==10:
                    turhxyz = line.split()
                    turhx = float(turhxyz[5])
                    turhy = float(turhxyz[6])
                    turhz = float(turhxyz[7])


    with open(expdir + '/namoptions', 'r') as namopt:
        namopt = list(namopt)

    for i in range(len(namopt)):
        if namopt[i].find('nprocx')!=-1:
            nprocx = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('nprocy')!=-1:
            nprocy = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('runtime')!=-1:
            runtime = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('dtav')!=-1:
            dtav = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('itot')!=-1:
            itot = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('jtot')!=-1:
            jtot = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('kmax')!=-1:
            kmax = int(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('cu')!=-1:
            cu = float(namopt[i].rstrip()[namopt[i].index('=')+1:]) 
        if namopt[i].find('cv')!=-1:
            cv = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('turr')!=-1:
            turr = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('Ct')!=-1:
            Ct = float(namopt[i].rstrip()[namopt[i].index('=')+1:])

        
    return {'nprocx': nprocx, 'nprocy': nprocy, 'runtime': runtime, 'dtav': dtav, 'itot': itot, 'jtot': jtot, 'kmax': kmax, 'xsize': xsize, 'ysize': ysize, 'zsize':zsize,'cu': cu, 'cv': cv, 'turhx': turhx, 'turhy': turhy, 'turhz': turhz, 'turr': turr, 'Ct': Ct, 'dx': dx, 'dy': dy, 'dz': dz}




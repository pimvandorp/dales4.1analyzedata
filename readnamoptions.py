#!/umsr/bin/python
#Filename: readnamoptions.py
#Description: reads some useful namoptions from namoptions in directory ../exptitle/expnr

from numpy import *

def readnamoptions(exptitle,expnr):

    expsdir = '/home/pim/Les/Experiments'
    expdir = expsdir + '/%s/%s' %(exptitle,expnr)
  
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
        if namopt[i].find('xsize')!=-1:
            xsize = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('ysize')!=-1:
            ysize = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('cu')!=-1:
            cu = float(namopt[i].rstrip()[namopt[i].index('=')+1:]) 
        if namopt[i].find('cv')!=-1:
            cv = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('turbh')!=-1:
            turbh = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('turbr')!=-1:
            turbr = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('turbloc')!=-1:
            turbloc = float(namopt[i].rstrip()[namopt[i].index('=')+1:])
        if namopt[i].find('Ct')!=-1:
            Ct = float(namopt[i].rstrip()[namopt[i].index('=')+1:])

        
    return {'nprocx': nprocx, 'nprocy': nprocy, 'runtime': runtime, 'dtav': dtav, 'itot': itot, 'jtot': jtot, 'kmax': kmax, 'xsize': xsize, 'ysize': ysize, 'cu': cu, 'cv': cv, 'turbh': turbh, 'turbr': turbr, 'turbloc': turbloc, 'Ct': Ct}


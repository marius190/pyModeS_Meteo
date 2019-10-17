import pyModeS as pms
import functions
# import numpy as np

# file_in = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/DF17in_sorted.txt'
file_in = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_fuenlabrada/DF17in_sorted.txt'
text = open(file_in, 'r')
text = text.readlines()

# file_out='C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/Salidas_pyModeS/CPRout_all.txt'
file_out='C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/Salidas_pyModeS/CPRout_fuenla.txt'
f=open(file_out, 'w+')

ICAO=[]
for msg in text:
    ICAO.append(pms.adsb.icao(msg[:28]))
    # ICAO = text[i][2:8]

# planes=list(set(ICAO)) #functions.unique(ICAO) (does not sort in appearing order)
Planes = sorted(set(ICAO), key=ICAO.index)

f.write('ICAO Latitude Longitude Altitude Timestamp k\n')
ini = 0
for i in range(len(Planes)):
    if len(Planes) > 1: # este if se puede poner antes del for!

        if i < len(Planes)-1: # Para el ultimo plane... ver como mejorar, !Locura!
            end = ICAO.index(Planes[i+1])
        elif i == len(Planes)-1:
            end = len(ICAO)

        pos = functions.adsb_cpr(text[ini:end])
        for p in pos:
            f.write(ICAO[ini] + ' '+str(p[0])+' '+str(p[1])+' '+str(p[2])+' '+str(p[4])+' '+str(p[3])+'\n') # Do not format, i.e. % f.4
            #f.write('%s %s %s %s %s\n' %ICAO, %p[0], p[1], p[3], p[2])
            #f.write(f'{ICAO} {p[0]:.7f} {p[1]:.7f} {p[3]} {p[2]}\n')
        ini = end
    else:
        pos = functions.adsb_cpr(text)
        for p in pos:
            f.write(ICAO[ini] + ' '+str(p[0])+' '+str(p[1])+' '+str(p[2])+' '+str(p[4])+' '+str(p[3])+'\n')

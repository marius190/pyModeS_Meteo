import pyModeS as pms


file_in = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/Salidas_pyModeS/test/BDSin_test.txt'
text = open(file_in, 'r')
text = text.readlines()  #.split(',')

for t in text:
    flag=pms.bds.bds50.is50(t[0:28])
    if flag:
        print(t)
        break

pms.commb.gs50('A0001718001307340004D988B6E2')
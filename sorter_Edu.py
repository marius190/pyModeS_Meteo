## Ordenar por dos valores

# Ordenar por un valor:
# datos.sort(key=lambda x: x[1])
# print datos
#

import operator

#file_in = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/DF17in.txt'
#file_out = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_torre_2/DF17in_sorted.txt'

file_in = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_fuenlabrada/DF17in.txt'
file_out = 'C:/Users/UX490U/Universidad Rey Juan Carlos/Ernesto Staffetti Giammaria - phd_marius/data_fuenlabrada/DF17in_sorted.txt'
text = open(file_in, 'r')
file_out = open(file_out, 'w')
text = text.readlines()  #.split(',')


data_list = []
for row in text:
    code, timestamp, tiempo = row.split(' ')[:3]
    data_list.append([code, code[2:8], timestamp, int(tiempo)])
data_sorted=sorted(data_list, key=operator.itemgetter(1, 3))
#print(data_sorted)

# define list of places
#places = ['Berlin', 'Cape Town', 'Sydney', 'Moscow']

#with open('listfile.txt', 'w') as filehandle:
for listitem in data_sorted:
    file_out.write('%s ' % listitem[0])
    file_out.write('%s ' % listitem[2])
    file_out.write('%s\n' % listitem[3])
#file_out.write("\n".join(data_sorted))
import pyModeS as pms
import operator


def adsb_flag(text):
    bits = []
    for i in text:  # i in range(len(text)): #text: #len(text):
        code = i[0:28]
        tc = pms.adsb.typecode(code)
        if tc is not None and 9 <= tc <= 18:  # 20-22??
            bit = pms.hex2bin(code)  # Convert hexadecimal string to binary string
            bit = bit[54 - 1]
            bit = pms.bin2int(bit)  # Convert binary string to integer # Or use just int(bit)
            if bit == 0 or bit == 1:
                bits.append(bit)
            # elif bit==1:
            else:
                print("Warning: No bit value!")
        else:
            bits.append('None')
    return bits


def adsb_cpr(text):
    # Cogemos los flag even-odd de todos los mensajes.
    bits = adsb_flag(text)
    #  print(bits)

    # Warning: Se supone datos en orden cronologico y un solo ICAO
    # Warning: Latitud/phi entre 0,90 longitud/theta -180,180. Barajas 40.4, -3.5
    pos = []
    while_flag = 0  # flag de entrada o no en el segundo bucle
    k = 1  # por que entra en k-1=0
    n = len(bits)
    while k <= n - 1:
        try:  # se pone try por que puede dar error si no encuentra even-odd. El metodo char.find es igual para char y no da
            # error sino -1 cuando no encuentra
            even = bits.index(0, k - 1, n)  # index devuelve posicion python: 0,...n-1,
            odd = bits.index(1, k - 1, n)

            text0 = text[even]
            text1 = text[odd]

            code0 = text0[0:28]
            code1 = text1[0:28]
            t0 = int(text0[39:49])
            t1 = int(text1[39:49])

            if abs(t1 - t0) <= 5:
                # devuelve tuple: (phi, theta) print(pms.adsb.airborne_position(code0, code1, t0, t1))
                # A veces sale None cuando chequea la latidude zone:
                # aux = pms.adsb.airborne_position(code0, code1, t0, t1)  # (even, odd, t_even, t_odd)
                # if aux is not None:
                [phi, theta] = pms.adsb.airborne_position(code0, code1, t0, t1)  # (even, odd, t_even, t_odd)

                ##
                alt = pms.adsb.altitude(code1)
                ##
                pos.append([phi, theta, alt, k, t0])  # k en posicion python
                # Lat.append(phi)
                # Lon.append(theta)

                k = max(even, odd) + 1  # Cogemos el ultimo que es el mas reciente en tiempo
                while k <= n - 1 and bits[k] == 'None':  # para negacion: != <>
                    k += 1  # Este while y el otro similar de abajo se podria modelar mas estetico con .index tambien!
                if k == n:
                    break

                t = max(t0, t1)

                text2 = text[k]
                code2 = text2[0:28]
                t2 = int(text2[39:49])
                while k <= n - 1 and abs(t2 - t) <= 5:
                    while_flag = 1
                    [phi, theta] = pms.adsb.airborne_position_with_ref(code2, phi, theta)

                    ##
                    alt = pms.adsb.altitude(code2)
                    ##
                    pos.append([phi, theta, alt, k, t2])

                    k += 1
                    t = t2
                    while k <= n - 1 and bits[k] == 'None':  # para negacion: != <>
                        k += 1
                    if k == n:
                        break

                    text2 = text[k]
                    code2 = text2[0:28]
                    t2 = int(text2[39:49])
                if while_flag == 1:  # Parece que este if sobra
                    while_flag = 0
                    k += 2  # Poner +1 si tiempos t2,2 y t2,t1 tiene distinta comparacion temporal. Ahora ambos 5 seg.
                # else:
                # k = max(even, odd) + 1  # += 1 vamos al siguiente par even-odd
            else:
                k = max(even, odd) + 1  # += 1 vamos al siguiente par even-odd
        except ValueError:  # Se puede poner except sin mas pero puede enmasacar otro tipo de erores
            print('No even-odd flag found')  # or write pass or nothing?
            break
    return pos


def unique(list):
    # insert the list to the set
    list_set = set(list)
    # convert the set to the list
    return list(list_set)


def sorter_icao_time(file_in, file_out):
    # Makes a "group by ICAO, Timestamp" on ADS-B data with format:
    # 8C343542F9004602884A38EE8263 TIMESTAMP 1524164066
    # ICAO is suppose to be the 3:8 element at each row. In previous message, 343542
    text = open(file_in, 'r')
    file_out = open(file_out, 'w')
    text = text.readlines()

    data_list = []
    for row in text:
        code, timestamp, tiempo = row.split(' ')[:3]
        data_list.append([code, code[2:8], timestamp, int(tiempo)])
    data_sorted = sorted(data_list, key=operator.itemgetter(1, 3))

    for listitem in data_sorted:
        file_out.write('%s ' % listitem[0])
        file_out.write('%s ' % listitem[2])
        file_out.write('%s\n' % listitem[3])

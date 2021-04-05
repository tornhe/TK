from math import sin, cos
#from TK_main import df

def sjekk_float(x):
    x.replace(',', '.')
    try:
        float(x)
        return True
    except ValueError:
        return False


def utbetpros(df, sheets, idx):
    siste_rad_kamp = 0
    siste_rad_resultat = 0

    siste_rad_kamp = df[idx][df[idx]['Dato'] == "None"].index[0]
    siste_rad_resultat = df[idx][df[idx]['Bet inn?'] == "None"].index[0]
    prosent = []
    temp_tuple = ()
    for i in range(0, siste_rad_resultat):
        val = sheets[idx].cell(i+2, 13).value
        val = float(val.replace(',','.'))
        val = int(val)
        temp_tuple = (i+1, val)
        prosent.append((temp_tuple),)
    return prosent

def alle_kampar(df, data_attr1, data_attr2, idx):
    martin_kampar = []
    sindre_kampar = []
    tor_kampar = []

    siste_rad_kamp_martin = df[0][df[0]['Dato'] == "None"].index[0]
    siste_rad_kamp_sindre = df[1][df[1]['Dato'] == "None"].index[0]
    siste_rad_kamp_tor = df[2][df[2]['Dato'] == "None"].index[0]

    spelarar = [martin_kampar, sindre_kampar, tor_kampar]
    spelar_rader = [siste_rad_kamp_martin, siste_rad_kamp_sindre, siste_rad_kamp_tor]

    spelar_idx = 0
    for spelar in spelarar: # Her får vi kanskje vere litt selektiv på kva data vi vil ha med
        for rad in range(spelar_rader[spelar_idx]):
            if rad % 2 == 0:
                data_attr = data_attr1
            else:
                data_attr = data_attr2
            temp_data = {'text': str(df[spelar_idx].at[rad, "Runde"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Kamp"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Dato"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Heimelag"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Bortelag"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Bet"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Odds"])}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Innsats"]) + "kr"}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            if str(df[spelar_idx].at[rad, "Bet inn?"] == "None"):
                temp_data = {'text': " - "}
            else:
                temp_data = {'text': str(df[spelar_idx].at[rad, "Bet inn?"])}

            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Total innsats"]) + "kr"}
            temp_data.update(data_attr)
            spelar.append(temp_data)

            temp_data = {'text': str(df[spelar_idx].at[rad, "Total gevinst"]) + "kr"}
            temp_data.update(data_attr)
            spelar.append(temp_data)


        spelar_idx += 1

    return spelarar[idx]

def testdata1():
    return [(x, sin(x / 10.)) for x in range(0, 101)]

def testdata2():
    return [(x, cos(x / 10.)) for x in range(0, 101)]
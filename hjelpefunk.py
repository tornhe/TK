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
    '''for i in range(len(df)):
        if df[i][df[i]['Dato'] == "None"].index[0] > siste_rad_kamp:
            siste_rad_kamp = df[i][df[i]['Dato'] == "None"].index[0]
        if df[i][df[i]['Bet inn?'] == "None"].index[0] > siste_rad_resultat:
            siste_rad_resultat = df[i][df[i]['Bet inn?'] == "None"].index[0]
    '''
    siste_rad_kamp = df[idx][df[idx]['Dato'] == "None"].index[0]
    siste_rad_resultat = df[idx][df[idx]['Bet inn?'] == "None"].index[0]
    prosent = []
    temp_tuple = ()
    for i in range(0, siste_rad_resultat):
        val = sheets[idx].cell(i+2, 13).value
        print(val)
        val = float(val.replace(',','.'))
        val = int(val)
        temp_tuple = (i+1, val)
        prosent.append((temp_tuple),)
    print(prosent)
    return prosent


def testdata1():
    return [(x, sin(x / 10.)) for x in range(0, 101)]

def testdata2():
    return [(x, cos(x / 10.)) for x in range(0, 101)]
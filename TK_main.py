'''
TODO:
- Dato og odds formaterar feil i Excel med ' forran (av og til?) talet
- Ved lagt inn bet oppdaterar ikkje "*navn* sin neste kamp er kamp x runde y" verdiane
- Om vi skal regne statistikk i Excel: odds må vere på format x,y (ikkje x.y), men i Python er floats x.y. Må finne ut av det.
Mulig vi kunne unngått formateringsfeilen om vi skriver til Excel med odds-tekst konvertert til float
- Bets nylig lagt til visast som None i hint_text når du blar vekk og så tilbake. Må få på plass hint_text
- Samme med inn/ut: oppdatering blir ikkje henta inn når du blar vekk
- Endre tekst til "...neste kamp er RUNDE x KAMP y"? Eg blir forvirra når spinnerane står i motsatt rekkefølge
- Har tidligare hatt errorinfo på legg inn bets som viser kva som er feil når du trykke submit. Den visast ikkje lenger, så må tilbake
- Hemmelig runde
- Resultat
- Plot må oppdatere seg når vi legger inn resultat
- Plot må bli dynamisk
- Leggge til andre typar plots? Tabellar? Mulighet til å velge kva grafar vi vil vise med knappar i bunnen?


- Ligger litt debug prints her og der som kan vekk etterkvart
'''


import kivy
import os
import sys
import gspread
import pandas as pd
from kivy.uix.widget import Widget
from oauth2client.service_account import ServiceAccountCredentials
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from gdrive import load, data_to_df

# Sindre testar litt
from math import sin, cos
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from hjelpefunk import*
Builder.load_file('legg_inn_bets.kv')
Builder.load_file('sja_resultat.kv')

martin_sheet = load('Martin')
martin_data = data_to_df(martin_sheet)

sindre_sheet = load('Sindre')
sindre_data = data_to_df(sindre_sheet)

tor_sheet = load('Tor')
tor_data = data_to_df(tor_sheet)

sheets = [martin_sheet, sindre_sheet, tor_sheet]
df = [martin_data, sindre_data, tor_data]

class VelgSpelar(Screen):
    pass

class HovudMeny(Screen):
    pass


class LeggInnBets(Screen):
    inputerror = StringProperty("")


class LeggInnResultat(Screen):
    pass


class SjaResultat(Screen):
    #vis_tabell = ObjectProperty()
    def vis_tabell(self):
        self.ids.btn_vis_tabell.disabled = True
        self.ids.btn_vis_prosplot.disabled = False
        self.ids.prosentplot.opacity = 0
        self.ids.tabell.opacity = 1
    def vis_prosentplot(self):
        self.ids.btn_vis_prosplot.disabled = True
        self.ids.btn_vis_tabell.disabled = False
        self.ids.prosentplot.opacity = 1
        self.ids.tabell.opacity = 0

    def build(self):
        '''
        scroll_view = ScrollView()
        #grid_layout = GridLayout(cols=1, padding=20, spacing=20, size_hint_y=None)
        #grid_layout.bind(minimum_size=grid_layout.setter('size'))
        self.prosentplot = ProsentPlot(size_hint_y=None, height=500)
        #Kan visst ha fleire grafar
        #graph2 = ProsentPlot(size_hint_y=None, height=500)
        #label = Label(text="Hello World!", size_hint_y=None)
        #label2 = Label(text="Hello World!", size_hint_y=None)
        self.add_widget(self.prosentplot)
        #grid_layout.add_widget(label)
        #grid_layout.add_widget(graph)
        #grid_layout.add_widget(label2)
        #grid_layout.add_widget(graph2)
        #scroll_view.add_widget(grid_layout)

        # return grid_layout
        #return scroll_view
        '''
        pass

class Cell(Label):
    pass
class Tabell(ScrollView):
    '''https://stackoverflow.com/questions/45153225/packaged-kivy-app-visually-incorrect
    Kan kanskje vere ei grei løysing på tabell.
    Tenkte: En tabell for nøkkeldata (forsøkt på her)
    Kan og lage endå en knapp for å vise alle kampar med resultat for kvar spelar (valgmeny for spelar)
    '''
    #grid = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Tabell, self).__init__(**kwargs)
        #grid_layout = GridLayout(cols=3, padding=20, spacing=20, size_hint_y=None)
        #grid_layout.bind(minimum_size=grid_layout.setter('size'))

        martin_siste_rad = df[0][df[0]['Bet inn?'] == "None"].index[0]
        sindre_siste_rad = df[1][df[1]['Bet inn?'] == "None"].index[0]
        tor_siste_rad = df[2][df[2]['Bet inn?'] == "None"].index[0]

        martin_siste_data = []
        martin_siste_data.append(sheets[0].cell(martin_siste_rad, 10).value) # Total innsats
        martin_siste_data.append(sheets[0].cell(martin_siste_rad, 12).value)  # Total gevinst
        martin_siste_data.append(sheets[0].cell(martin_siste_rad, 13).value)  # Utbetalingsprosent

        sindre_siste_data = []
        sindre_siste_data.append(sheets[0].cell(sindre_siste_rad, 10).value)  # Total innsats
        sindre_siste_data.append(sheets[0].cell(sindre_siste_rad, 12).value)  # Total gevinst
        sindre_siste_data.append(sheets[0].cell(sindre_siste_rad, 13).value)  # Utbetalingsprosent

        tor_siste_data = []
        tor_siste_data.append(sheets[0].cell(tor_siste_rad, 10).value)  # Total innsats
        tor_siste_data.append(sheets[0].cell(tor_siste_rad, 12).value)  # Total gevinst
        tor_siste_data.append(sheets[0].cell(tor_siste_rad, 13).value)  # Utbetalingsprosent

        spelar_data = [martin_siste_data, sindre_siste_data, tor_siste_data]
        #martin_rad = Label(text=str(martin_siste_rad))
        #sindre_rad = Label(text=str(sindre_siste_rad))
        #tor_rad = Label(text=str(tor_siste_rad))
''' Funkar ikkje
        for i in range(3): # Kvar spelar
            for j in range(3): # Kvar data
                self.ids.grid.add_widget(Cell(text=str(spelar_data[i][j])))
'''


class ProsentPlot(RelativeLayout):
    def __init__(self, **kwargs):
        super(ProsentPlot, self).__init__(**kwargs)
        self.graph = Graph(x_ticks_minor=1, x_ticks_major=5, y_ticks_major=25,
                           y_grid_label=True, x_grid_label=True, x_grid=True, y_grid=True,
                           xmin=1, ymin=0, ymax=200, draw_border=False)
        # graph.size = (1200, 400)
        # self.graph.pos = self.center
        self.graph.xlabel="Runde"
        self.graph.ylabel="Prosent"
        self.graph.xmax = 20 # Må gjere denna dynamisk!!
        self.graph.background_normal = ''
        self.graph.background_color = [0, 0, 0, 1]

        self.martin_prosent = MeshLinePlot(color=[1, 0, 0, 1])
        self.martin_prosent.points = utbetpros(df, sheets, 0)

        self.sindre_prosent = MeshLinePlot(color=[1, 1, 0, 1])
        self.sindre_prosent.points = utbetpros(df, sheets, 1)

        self.tor_prosent = MeshLinePlot(color=[0, 1, 0, 1])
        self.tor_prosent.points = utbetpros(df, sheets, 2)

        self.graph.add_plot(self.martin_prosent)
        self.graph.add_plot(self.sindre_prosent)
        self.graph.add_plot(self.tor_prosent)

        self.add_widget(self.graph)



class MyScreenManager(ScreenManager):
    spelar = StringProperty(None)
    spelar_idx = NumericProperty(None)
    siste_runde = ObjectProperty(None)
    siste_kamp = ObjectProperty(None)
    siste_resultat = ObjectProperty(None)
    data = ObjectProperty(df)
    runde = ObjectProperty("1")
    kamp = ObjectProperty("1")
    heimelag = ObjectProperty(None)
    bortelag = ObjectProperty(None)
    bet = ObjectProperty(None)
    odds = NumericProperty(None)
    innsats = NumericProperty(None)
    dato = ObjectProperty(None)
    row = ObjectProperty(0)
    bet_inn = ObjectProperty(None)
    bet_ut = ObjectProperty(None)

    #def __init__(self, **kwargs):
     #   super(MyScreenManager, self).__init__(**kwargs)

    def update_table(self):
        if self.runde is not None and self.kamp is not None:
            self.row = ((int(self.runde)) - 1) * 5 + int(self.kamp) - 1

    def submit(self):
        new_data = [int(self.ids.legg_inn_bets.ids.runde.text), int(self.ids.legg_inn_bets.ids.kamp.text), self.ids.legg_inn_bets.ids.dato.text,
                    self.ids.legg_inn_bets.ids.heimelag.text, self.ids.legg_inn_bets.ids.bortelag.text, self.ids.legg_inn_bets.ids.bet.text,
                    self.ids.legg_inn_bets.ids.odds.text, float(self.ids.legg_inn_bets.ids.innsats.text)]

        # Må fikse det her - insert/delete row fjernar formlane i Excel
        sheets[self.spelar_idx].insert_row(new_data, self.row+2)
        sheets[self.spelar_idx].delete_rows(self.row+3)
        self.submit_clean()

    def submit_edit(self):
        runde = int(self.ids.legg_inn_bets.ids.runde.text)
        kamp = int(self.ids.legg_inn_bets.ids.kamp.text)
        rad = (runde * 5) - (5 - kamp) + 1
        print("Runde: ", int(runde)," Kamp: ", int(kamp))
        if (self.ids.legg_inn_bets.ids.dato.text != ""):
            temp_dato = self.ids.legg_inn_bets.ids.dato.text
            sheets[self.spelar_idx].update_cell((rad), 3, str(temp_dato))
        else:
            self.ids.legg_inn_bets.ids.dato.text = self.ids.legg_inn_bets.ids.dato.hint_text

        if (self.ids.legg_inn_bets.ids.heimelag.text != ""):
            temp_heimelag = self.ids.legg_inn_bets.ids.heimelag.text
            sheets[self.spelar_idx].update_cell((rad), 4, temp_heimelag)
        else:
            self.ids.legg_inn_bets.ids.heimelag.text = self.ids.legg_inn_bets.ids.heimelag.hint_text

        if (self.ids.legg_inn_bets.ids.bortelag.text != ""):
            temp_bortelag = self.ids.legg_inn_bets.ids.bortelag.text
            sheets[self.spelar_idx].update_cell((rad), 5, temp_bortelag)
        else:
            self.ids.legg_inn_bets.ids.bortelag.text = self.ids.legg_inn_bets.ids.bortelag.hint_text

        if (self.ids.legg_inn_bets.ids.bet.text != ""):
            temp_bet = self.ids.legg_inn_bets.ids.bet.text
            sheets[self.spelar_idx].update_cell((rad), 6, temp_bet)
        else:
            self.ids.legg_inn_bets.ids.bet.text = self.ids.legg_inn_bets.ids.bet.hint_text

        if (self.ids.legg_inn_bets.ids.odds.text != ""):
            temp_odds = self.ids.legg_inn_bets.ids.odds.text
            sheets[self.spelar_idx].update_cell((rad), 7, temp_odds)
        else:
            self.ids.legg_inn_bets.ids.odds.text = self.ids.legg_inn_bets.ids.odds.hint_text

        if (self.ids.legg_inn_bets.ids.innsats.text != ""):
            temp_innsats = self.ids.legg_inn_bets.ids.innsats.text
            sheets[self.spelar_idx].update_cell((rad), 8, temp_innsats)
        else:
            self.ids.legg_inn_bets.ids.innsats.text = self.ids.legg_inn_bets.ids.innsats.hint_text

        self.submit_clean()

    def submit_clean(self):
        # Restart jævelskapen - legg til hint_text, fjern text så det går an å bla
        self.ids.legg_inn_bets.ids.dato.hint_text = self.ids.legg_inn_bets.ids.dato.text
        self.ids.legg_inn_bets.ids.heimelag.hint_text = self.ids.legg_inn_bets.ids.heimelag.text
        self.ids.legg_inn_bets.ids.bortelag.hint_text = self.ids.legg_inn_bets.ids.bortelag.text
        self.ids.legg_inn_bets.ids.bet.hint_text = self.ids.legg_inn_bets.ids.bet.text
        self.ids.legg_inn_bets.ids.odds.hint_text = self.ids.legg_inn_bets.ids.odds.text
        self.ids.legg_inn_bets.ids.innsats.hint_text = self.ids.legg_inn_bets.ids.innsats.text

        self.ids.legg_inn_bets.ids.dato.text = ""
        self.ids.legg_inn_bets.ids.heimelag.text = ""
        self.ids.legg_inn_bets.ids.bortelag.text = ""
        self.ids.legg_inn_bets.ids.bet.text = ""
        self.ids.legg_inn_bets.ids.odds.text = ""
        self.ids.legg_inn_bets.ids.innsats.text = ""

    def sjekk_siste_kamp(self):
        if self.spelar == 'Martin':
            self.spelar_idx = 0
        elif self.spelar == 'Sindre':
            self.spelar_idx = 1
        elif self.spelar == 'Tor':
            self.spelar_idx = 2

        siste_rad_kamp = df[self.spelar_idx][df[self.spelar_idx]['Dato'] == "None"].index[0]
        siste_rad_resultat = df[self.spelar_idx][df[self.spelar_idx]['Bet inn?'] == "None"].index[0]

        self.siste_runde = df[self.spelar_idx]['Runde'][siste_rad_kamp]
        self.siste_kamp = df[self.spelar_idx]['Kamp'][siste_rad_kamp]

        if siste_rad_kamp == siste_rad_resultat:
            self.siste_resultat = "Alle resultat lagt inn. Applaus!"
        elif siste_rad_kamp > siste_rad_resultat:
            self.siste_resultat = str(self.spelar) + " sitt siste resultat er kamp " + str(df[self.spelar_idx]['Kamp'][siste_rad_resultat]) + " i runde " + str(df[self.spelar_idx]['Runde'][siste_rad_resultat])
        else:
            self.siste_resultat = "Noke er feil med kampar/resultat. Sjekk excelfila."

    def neste_kamp(self):
        if int(self.kamp) < 5:
            self.kamp = str(int(self.kamp) + 1)
        elif int(self.kamp) == 5 and int(self.runde) != int(df[self.spelar_idx]['Runde'].max()):
            self.kamp = 1
            self.runde = str(int(self.runde) + 1)

        return str(self.runde), str(self.kamp)

    def forrige_kamp(self):
        if int(self.kamp) > 1:
            self.kamp = str(int(self.kamp) - 1)
        elif int(self.kamp) == 1 and int(self.runde) == 1:
            self.kamp = 1
            self.runde = 1
        else:
            self.kamp = 5
            self.runde = str(int(self.runde) - 1)
            
        return str(self.runde), str(self.kamp)
    
    def legg_inn_resultat(self):
        print(self.ids.legg_inn_resultat.bet_inn_ja.active)
        print(self.ids.legg_inn_resultat.bet_inn_nei.active)
       
        #if self.bet_inn_ja.active:
        #    print(self.runde)
        #    print(df[self.spelar_idx]['Bet inn?'][self.row])
        #elif self.bet_inn_nei.active:
        #    print(df[self.spelar_idx]['Bet inn?'][self.row])

    def validate_submit(self):
        self.ids.legg_inn_bets.ids.odds.text = self.ids.legg_inn_bets.ids.odds.text.replace('.', ',')
        self.ids.legg_inn_bets.ids.innsats.text = self.ids.legg_inn_bets.ids.innsats.text.replace('.', ',')

        siste_rad_kamp = df[self.spelar_idx][df[self.spelar_idx]['Dato'] == "None"].index[0]
        siste_rad_resultat = df[self.spelar_idx][df[self.spelar_idx]['Bet inn?'] == "None"].index[0]

        self.siste_runde = df[self.spelar_idx]['Runde'][siste_rad_kamp]
        self.siste_kamp = df[self.spelar_idx]['Kamp'][siste_rad_kamp]

        kampar_spelt = int(self.siste_runde) * 5 - (5 - int(self.siste_kamp))
        kamp_resultat = int(self.runde) * 5 - (5 - int(self.runde))

        print(kampar_spelt, " vs ", kamp_resultat)
        # Sjekk om det er snakk om redigering av runde -> hopp over heile validate greiene (lettvint)
        if kamp_resultat <= kampar_spelt:
            self.inputerror = ""
            print("Bypass!")
            self.submit_edit()
        # Fortsett om det er snakk om ny runde
        elif self.ids.legg_inn_bets.ids.runde.text == "Velg runde":
            print(1)
            self.ids.legg_inn_bets.ids.inputerror = "Velg runde"
        elif self.ids.legg_inn_bets.ids.kamp.text == "Velg kamp":
            print(2)
            self.ids.legg_inn_bets.ids.inputerror = "Velg kamp"
        elif self.ids.legg_inn_bets.ids.dato.text == "" or self.ids.legg_inn_bets.ids.dato.text == "None":
            print(3)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn dato"
        elif self.ids.legg_inn_bets.ids.heimelag.text == "" or self.ids.legg_inn_bets.ids.heimelag.text == "None":
            print(4)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn heimelag"
        elif self.ids.legg_inn_bets.ids.bortelag.text == "" or self.ids.legg_inn_bets.ids.bortelag.text == "None":
            print(5)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn bortelag"
        elif self.ids.legg_inn_bets.ids.bet.text == "" or self.ids.legg_inn_bets.ids.bet.text == "None":
            print(6)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn bet"
        elif self.ids.legg_inn_bets.ids.odds.text == "" or self.ids.legg_inn_bets.ids.odds.text == "None":
            print(7)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn odds"
        # Sjekk under funkar dårlig, må fiksast
        #elif not sjekk_float(self.ids.legg_inn_bets.ids.odds.text):
        #    print(8)
        #    self.ids.legg_inn_bets.ids.inputerror = "Odds er ikkje eit tal"
        elif self.ids.legg_inn_bets.ids.innsats.text == "" or self.ids.legg_inn_bets.ids.odds.text == "None":
            print(9)
            self.ids.legg_inn_bets.ids.inputerror = "Fyll inn innsats"
        elif not sjekk_float(self.ids.legg_inn_bets.ids.innsats.text):
            print(10)
            self.ids.legg_inn_bets.ids.inputerror = "Innsats er ikkje eit tal"
        else:
            print(11)
            self.ids.legg_inn_bets.ids.inputerror = ""
            self.submit()

    # For å skrive bet inn/ut til Excel
    def bet_inn_ut(self, value):
        if(value == 0):
            sheets[self.spelar_idx].update_cell(self.row+2, 9, "Nei")
        if(value == 1):
            sheets[self.spelar_idx].update_cell(self.row+2, 9, "Ja")

    # Sjekk om bet_inn er true i Excel
    def sjekk_inn(self):
        rad = (int(self.runde) * 5) - (5 - int(self.kamp)) - 1
        if (df[self.spelar_idx]['Bet inn?'][rad] == "Ja"):
            print("True")
            return True
        else:
            print("False")
            return False

    # Sjekk om bet_ut er true i Excel
    def sjekk_ut(self):
        rad = (int(self.runde) * 5) - (5 - int(self.kamp)) - 1
        if (df[self.spelar_idx]['Bet inn?'][rad] == "Nei"):
            return True
        else:
            return False
class legg_inn_resultat(Screen):
    pass

class TK_Main(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    TK_Main().run()
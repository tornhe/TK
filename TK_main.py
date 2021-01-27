import kivy
import os
import sys
import gspread
import pandas as pd
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
from gdrive import load, data_to_df

Builder.load_file('legg_inn_bets.kv')

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
    pass
    
class LeggInnResultat(Screen):
    pass


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

    #def __init__(self, **kwargs):
     #   super(MyScreenManager, self).__init__(**kwargs)

    def update_table(self):
        if self.runde is not None and self.kamp is not None:
            self.row = ((int(self.runde)) - 1) * 5 + int(self.kamp) - 1

    def submit(self):
        new_data = [self.ids.legg_inn_bets.ids.runde.text, self.ids.legg_inn_bets.ids.kamp.text, self.ids.legg_inn_bets.ids.dato.text, 
                    self.ids.legg_inn_bets.ids.heimelag.text, self.ids.legg_inn_bets.ids.bortelag.text, self.ids.legg_inn_bets.ids.bet.text, 
                    self.ids.legg_inn_bets.ids.odds.text, self.ids.legg_inn_bets.ids.innsats.text]

        sheets[self.spelar_idx].insert_row(new_data, self.row+2)
        sheets[self.spelar_idx].delete_rows(self.row+3)

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
            self.siste_resultat = str(self.spelar) + " sitt siste resultat er " + str(df[self.spelar_idx]['Kamp'][siste_rad_resultat]) + "i runde " + str(df[self.spelar_idx]['Runde'][siste_rad_resultat])
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

class TK_Main(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    TK_Main().run()
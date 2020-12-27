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

class Start_menu(Screen):
    pass

class legg_inn_bets(Screen):
    spelar = ObjectProperty(None)
    data = ObjectProperty(df)
    name = ObjectProperty(None)
    runde = ObjectProperty(None)
    kamp = ObjectProperty(None)
    heimelag = ObjectProperty(None)
    bortelag = ObjectProperty(None)
    bet = ObjectProperty(None)
    odds = ObjectProperty(None)
    innsats = ObjectProperty(None)
    dato = ObjectProperty(None)
    row = ObjectProperty(None)
    spelar_idx = NumericProperty(None)
    siste_runde = ObjectProperty(None)
    siste_kamp = ObjectProperty(None)

    def sjekk_siste_kamp(self):
        if self.spelar == 'Martin':
            self.spelar_idx = 0
        elif self.spelar == 'Sindre':
            self.spelar_idx = 1
        elif self.spelar == 'Tor':
            self.spelar_idx = 2

        siste_rad = df[self.spelar_idx][df[self.spelar_idx]['Dato'] == "None"].index[0]
        self.siste_runde = df[self.spelar_idx]['Runde'][siste_rad]
        self.siste_kamp = df[self.spelar_idx]['Kamp'][siste_rad]

    def update_table(self):
        if self.runde is not None and self.kamp is not None:
            self.row = ((int(self.runde)) - 1) * 5 + int(self.kamp)

    def submit(self):
        new_data = [self.runde, self.kamp, self.dato.text, self.heimelag.text, self.bortelag.text, self.bet.text, self.odds.text, self.innsats.text]
        
        sheets[self.spelar_idx].insert_row(new_data, self.row+1)
        sheets[self.spelar_idx].delete_rows(self.row+2)

class legg_inn_resultat(Screen):
    pass

class TK_Main(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Start_menu(name='start'))
        sm.add_widget(legg_inn_bets(name='legg inn bets'))
        sm.add_widget(legg_inn_resultat(name='legg inn resultat'))
        return sm
    
if __name__ == '__main__':
    TK_Main().run()
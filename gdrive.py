import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def load(spelar):
    # create scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope)

    #create gspread authorize using that credential
    client = gspread.authorize(creds)

    # client.open for opening a spreadsheet
    sheet = client.open(spelar).sheet1

    #print(sheet.get_all_records())

    #data = sheet.get_all_values()
    #headers = data.pop(0)
    #df = pd.DataFrame(data, columns=headers)

    return sheet

def data_to_df(sheet):
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df
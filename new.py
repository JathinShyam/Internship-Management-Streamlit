import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
from cachetools import cached, TTLCache


# def authenticate_google_sheets():
#     # Authenticate with Google Sheets API

#     scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets'","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

#     # creds = Credentials.from_service_account_file('creds.json', scope)
#     # creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

#     # Load the service account credentials from the JSON file
#     creds = Credentials.from_service_account_file("creds.json", scope)

#     # Authenticate with Google Sheets API

#     client = gspread.authorize(creds)

#     # Open the Google Sheet (replace 'Your Sheet Name' with the name of your Google Sheet)
#     sheet_name = 'CRM'
#     client = client.open(sheet_name).sheet1
#     worksheet = client.get_worksheet(0)

#     return worksheet
 

@cached(cache=TTLCache(maxsize=1, ttl=3600))
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    return gspread.authorize(creds)
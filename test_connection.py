import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("secrets.json", scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open("Music Rankings Data").sheet1
print("Connection successfull!")
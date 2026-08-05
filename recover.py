import gspread
from google.oauth2.service_account import Credentials
import json

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("secrets.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open("Music Rankings Data").sheet1

# Read entire first row
row = sheet.row_values(1)
print(f"Found {len(row)} chunks")

# Save raw chunks to file
json_str = "".join(row)
with open("raw_backup.txt", "w") as f:
    f.write(json_str)

print(f"Saved {len(json_str)} characters to raw_backup.txt")
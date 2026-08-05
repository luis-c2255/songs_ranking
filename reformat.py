import gspread
from google.oauth2.service_account import Credentials
import json

scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("secrets.json", scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open("Music Rankings Data").sheet1

# Read all chunks from columns
chunks = []
col = 1
while True:
    value = sheet.cell(1, col).value
    if not value:
        break
    chunks.append(value)
    col += 1

# Join and parse
json_str = "".join(chunks)
data = json.loads(json_str)

# Save back in new format (rows instead of columns)
new_chunks = [[chunk] for chunk in [json_str[i:i+40000] for i in range(0, len(json_str), 40000)]]
sheet.clear()
sheet.update(values=new_chunks, range_name="A1")

print("Data reformatted successfully!")
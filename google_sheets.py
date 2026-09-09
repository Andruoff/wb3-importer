import gspread
from google.oauth2.service_account import Credentials

# Load Google Sheets API credentials
SERVICE_ACCOUNT_FILE = "wb3-tts-importer-416c2c5a00d4.json"  # Update with your JSON file
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Authenticate and create the client
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = "1RyVuXuTbjReXnPB0BYGq-aMEtmI_Z3HK2iEkngKHFN4"  # Replace with your actual sheet ID
sheet = client.open_by_key(SHEET_ID).sheet1  # Access the first worksheet
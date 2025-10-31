from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

SERVICE_FILE = "service_account.json"
SPREADSHEET_ID = "1F35AssYCuXGnUtBbyBZHjof-CHXpSlRMdEDLBNsY2jI"
RANGE = "Form Responses 1"

def get_data():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE
    ).execute()

    rows = result.get("values", [])
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


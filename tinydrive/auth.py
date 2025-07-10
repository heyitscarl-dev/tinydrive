import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from tinydrive import ui

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

TOKEN_PATH = ".credentials/token.json"
CREDS_PATH = ".credentials/credentials.json"

def get_token():
    """
    Checks if there's a file at `TOKEN_PATH`. If so, tries to extract
    credentials from the file. Returns `None` otherwise.
    """
    if os.path.exists(TOKEN_PATH):
        return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return None

def refresh_token(creds: Credentials):
    """
    If credentials are expired, and there's a refresh token supplied,
    tries to refresh the credentials.
    """

    creds.refresh(Request())
    return creds

def request_token():
    """
    Allows the user to log in, requestion an entirely new token.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDS_PATH, SCOPES
    )
    
    try:
        creds = flow.run_local_server(port=0)
    except:
        return None
    if isinstance(creds, Credentials):
        return creds
    else:
        raise TypeError("invalid credentials type")

def save_token(credentials: Credentials):
    with open(TOKEN_PATH, "w") as token:
      token.write(credentials.to_json())

def get_credentials():
    creds = get_token()

    if creds and creds.expired and creds.refresh_token:
        creds = refresh_token(creds)
        save_token(creds)
        ui.info("refreshed token")

    if not creds:
        creds = request_token()

        if creds:
            save_token(creds)
            ui.info("login complete")
        else:
            ui.error("user login failed")
            exit(1)

    if not creds:
        ui.error("authentication failed (internal)")
        exit(2)
    else:
        ui.success("authentication complete")
        

    return creds

def get_service():
    creds = get_credentials()

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError:
        print("service building failed.")
        exit(-2)

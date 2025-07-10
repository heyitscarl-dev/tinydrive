import os.path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

TOKEN_PATH = ".credentials/token.json"
CREDS_PATH = ".credentials/credentials.json"

def try_get_token():
    """
    Checks if there's a file at `TOKEN_PATH`. If so, tries to extract
    credentials from the file. Returns `None` otherwise.
    """
    if os.path.exists(TOKEN_PATH):
        return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return None

def try_refresh_token(creds: Credentials):
    """
    If credentials are expired, and there's a refresh token supplied,
    tries to refresh the credentials.
    """
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        write_as_token(creds.to_json())
        return creds
    else:
        return None

def new_token():
    """
    Allows the user to log in, creating a fully new token.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDS_PATH, SCOPES
    )
    return flow.run_local_server(port=0)

def write_as_token(content: Any):
    with open(TOKEN_PATH, "w") as token:
      token.write(content)

def get_credentials():
    creds = try_get_token()

    if creds:
        creds = try_refresh_token(creds)

    if not creds:
        creds = new_token()
        write_as_token(creds.to_json())

    if not creds:
        print("authorization failed.")
        exit(-1)

    return creds

def get_service():
    creds = get_credentials()

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError:
        print("service building failed.")
        exit(-2)

import os.path
from typing import cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import rich

from tinydrive import ui

SCOPES = ["https://www.googleapis.com/auth/drive"]

TOKEN_PATH = ".credentials/token.json"
CREDS_PATH = ".credentials/credentials.json"

def load_token() -> Credentials | None:
    """
    Creates a Credentials instance from an authorized user json file.

    Returns:
        Credentials | None: The constructed credentials or None, 
                            if no file can be found at TOKEN_PATH.
        
    """
    if os.path.exists(TOKEN_PATH):
        return Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return None

def refresh_creds(creds: Credentials) -> Credentials | None:
    """
    Refreshes the given Credentials instance if possible.

    Returns:
        Credentials | None: The now refreshed credentials or None,
                            if refreshing failed.

    Args:
        creds (Credentials): The potentially expired Credentials instance.
        
    """
    try:
        creds.refresh(Request())
        return creds
    except:
        return None

def request_creds() -> Credentials | None:
    """
    Requests an entirely new Credentials instance by allowing the user to log in.

    Returns:
        Credentials | None: The newly created Credentials or None,
                            if auth failed.
        
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDS_PATH, SCOPES
    )
    
    try:
        creds = flow.run_local_server(port=0)

        # according to documentation, flow.run_local_server
        # will never return google.auth.external_account_authorized_user.Credentials.
        # thus, we can safely cast it to a Credentials instance.
        return cast(Credentials, creds)
    except:
        return None


def save_creds(credentials: Credentials | None):
    """
    If supplied with credentials, saves them to the token file.

    Args:
        credentials (Credentials | None): Either valid Credentials to be saved,
                                          or None, which leads to an early return (i.e. nothing happens).
    """
    if not credentials:
        return

    with open(TOKEN_PATH, "w") as token:
      token.write(credentials.to_json())

def get_credentials() -> Credentials:
    """
    Walks through the auth flow and ensures a valid Credentials instance.

    Returns:
        Credentials: The constructed Credentials

    Raises:
        SystemExit: If authentication or authorization fails at any point.
        
    """
    creds = load_token()

    # credentials exists, but is expired
    if creds and creds.expired and creds.refresh_token:
        creds = refresh_creds(creds)
        save_creds(creds)
        ui.info("refreshed credentials.")

    # credentials didn't exist or couldn't be refreshed
    if not creds:
        creds = request_creds()
        save_creds(creds)
        ui.info("requested credentials.")

    # credentials couldn't be newly requested
    # -> auth failed
    if not creds:
        ui.error("auth flow failed.")
        exit(1)
    else:
        ui.success("auth flow complete.")

    return creds

def get_service(credentials: Credentials):
    """
    Builds a Google Drive service using the supplied credentials.

    Args:
        credentials (Credentials): A valid Credentials instance with all required scopes.

    Raises:
        SystemExit: If building the service fails.
    """

    try:
        service = build("drive", "v3", credentials=credentials)
        return service
    except HttpError:
        ui.error("service building failed.")
        exit(2)

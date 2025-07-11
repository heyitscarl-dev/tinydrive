from pathlib import Path

import tinydrive.auth as auth
import dotenv
import os

from tinydrive.download import download_by_query

def main():
    dotenv.load_dotenv()
    print(f"gd_folder_id: {os.getenv("GD_FOLDER_ID") or "none supplied"}")

    folder_id = os.getenv("GD_FOLDER_ID") or exit(3)

    credentials = auth.get_credentials()
    service = auth.get_service(credentials)

    download_by_query(service, f"'{folder_id}' in parents and trashed = false", lambda file: Path(".downloads") / (
        file.get("name") or ""
    ))


if __name__ == "__main__":
  main()

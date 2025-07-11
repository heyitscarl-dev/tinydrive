from rich.status import Status

import tinydrive.auth as auth
import dotenv
import os

def main():
    dotenv.load_dotenv()
    print(f"gd_folder_id: {os.getenv("GD_FOLDER_ID") or "none supplied"}")

    folder_id = os.getenv("GD_FOLDER_ID") or exit(3)

    credentials = auth.get_credentials()
    service = auth.get_service(credentials)

    with Status("querying files..."):
        results = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false", 
                fields="nextPageToken, files(id, name, mimeType)"
            )
            .execute()
        )
        items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item.get("name")} ({item.get("mimeType")})")


if __name__ == "__main__":
  main()

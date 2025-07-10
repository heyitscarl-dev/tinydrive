from tinydrive.auth import get_service
from rich.status import Status

FOLDER_ID = "YOUR_FOLDER_ID"

def main():
    service = get_service()

    with Status("querying files..."):
        results = (
            service.files()
            .list(
                q=f"'{FOLDER_ID}' in parents and trashed = false", 
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

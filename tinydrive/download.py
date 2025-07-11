from pathlib import Path
from typing import Any, Callable
from googleapiclient.http import MediaIoBaseDownload
from rich.progress import Progress

from tinydrive.types import DriveFile
import tinydrive.ui as ui

# google doesn't provide static types, so Any 
# will have to do :(

def download_by_id(service: Any, remote_id: str, local_path: Path):
    request = service.files().get_media(fileId=remote_id)

    with open(local_path, "wb") as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False 

        with Progress() as progress:
            task = progress.add_task(f"🔽 downloading {local_path.name}...")

            while not done:
                status, done = downloader.next_chunk()
                if status:
                    progress.update(task, completed=int(status.progress() * 100))
    
    ui.success("download complete!")

def download_by_query(service: Any, query: str, local_path: Callable[[DriveFile], Path]) -> list[Path] | None:
    results = service.files().list(
        q=query,
        fields="nextPageToken, files(id, name, mimeType, size)"
    ).execute()

    files = results.get("files", [])

    for file in files:
        download_by_id(service, file.get("id") or "", local_path(file or ""))

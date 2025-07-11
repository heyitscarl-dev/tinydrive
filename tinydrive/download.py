from pathlib import Path
from typing import Any
from googleapiclient.http import MediaIoBaseDownload
from rich.progress import Progress

import ui

# google doesn't provide static types, so Any 
# will have to do :(

def download_by_id(service: Any, remote_id: str, local_path: Path) -> Path | None:
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

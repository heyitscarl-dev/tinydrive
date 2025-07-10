from rich import print
from rich.panel import Panel
from rich.prompt import Confirm
from rich.console import Console

import shutil

console = Console()

def info(msg: str):
    print(f"[cyan]🔵 {msg}[/cyan]")

def success(msg: str):
    print(f"[green]🟢 {msg}[/green]")

def warn(msg: str):
    print(f"[yellow]🟡 {msg}[/yellow]")

def error(msg: str, title="Error"):
    width = shutil.get_terminal_size().columns
    panel = Panel(
        f"[bold red]{msg}[/bold red]",
        title=title,
        width=width
    )
    print(panel)

def ask_confirm(msg: str, default: bool = False) -> bool:
    return Confirm.ask(msg, default=default)

#src/text_ranking_tool/ux/admin_iu/data_admin.py
"""
Data Admin - Minimal data management with enhanced safety
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import os
import shutil
from .admin_main_ui import (get_admin_choice_with_navigation,handle_navigation_action)
from ...config.constants import INTERNAL_DATA_DIR, INTERNAL_EXPORT_DIR, INTERNAL_USERS_DIR

def data_management_mode():
    """Data management with dynamic navigation"""
    console = Console()
    
    while True:
        _clear_screen()
        console.print(Panel("⚠️  Data Management", style="bold red"))
        console.print("[1] Reset Internal Data [CAUTION]")
        choice, nav_action = get_admin_choice_with_navigation(
            "Select option", 
            ["1"],
            console
        )
        
        if handle_navigation_action(nav_action):
            break
            
        if choice == "1":
            _reset_internal_data(console)
            return "exit_to_main"


def _reset_internal_data(console):
    """Reset with red warning and CONFIRM requirement"""
    _clear_screen()
    
    # RED WARNING
    console.print(Panel(
        "[bold red]⚠️  DANGER - DATA RESET WARNING ⚠️[/bold red]\n\n"
        "[red]This will PERMANENTLY DELETE:[/red]\n"
        "[red]• All internal data files[/red]\n"
        "[red]• All completed rankings[/red]\n"
        "[red]• All user sessions[/red]\n\n"
        "[green]This will PRESERVE:[/green]\n"
        "[green]• Original research files (external_data)[/green]\n"
        "[green]• Manual exports (external_exports)[/green]",
        title="[bold red]DESTRUCTIVE OPERATION[/bold red]",
        border_style="bold red"
    ))
    
    # Three tries to type CONFIRM
    for attempt in range(3):
        remaining = 3 - attempt
        console.print(f"\n[yellow]Type 'CONFIRM' to proceed ({remaining} attempts remaining):[/yellow]")
        
        user_input = Prompt.ask("Confirmation").strip()
        
        if user_input == "CONFIRM":
            # Execute reset
            _execute_reset(console)
            return
        else:
            console.print(f"[red]Invalid input: '{user_input}' (expected: CONFIRM)[/red]")
    
    # Failed after 3 tries
    console.print(Panel(
        "[yellow]Reset cancelled - too many failed attempts[/yellow]\n"
        "Returning to admin menu for safety.",
        title="[yellow]Operation Cancelled[/yellow]",
        border_style="yellow"
    ))
    
    Prompt.ask("Press Enter to continue")

def _execute_reset(console):
    """Execute the actual reset operation"""
    deleted_dirs = []
    
    # Delete internal directories
    for directory in [INTERNAL_DATA_DIR, INTERNAL_EXPORT_DIR, INTERNAL_USERS_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
            deleted_dirs.append(directory.name)
        
        # Recreate empty directory
        directory.mkdir(parents=True, exist_ok=True)
    
    # Show completion
    console.print(Panel(
        "[green]✓ Reset completed successfully[/green]\n\n"
        "Deleted and recreated:\n" + 
        "\n".join([f"[dim]• {d}[/dim]" for d in deleted_dirs]),
        title="[green]Reset Complete[/green]",
        border_style="green"
    ))
    
    Prompt.ask("Press Enter to continue")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

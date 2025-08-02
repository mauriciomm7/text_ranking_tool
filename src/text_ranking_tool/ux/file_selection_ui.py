# src/text_ranking_tool/ux/file_selection_ui.py

from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.panel import Panel
from rich import box

import os
from ..config.constants import get_user_color
from ..ranking.session_manager import get_session_manager
from ..data.file_scanner import scan_data_directory

def clear_screen():
    """Clear screen for clean display"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_file_selection(username: str) -> Optional[str]:
    """
    Display file selection interface for user.
    Returns selected filename stem or None if quit.
    """
    console = Console()
    session_manager = get_session_manager()
    user_color = get_user_color(username)
    
    while True:
        clear_screen()

        # Display Header
        header_text = "Select your text files for ranking analysis"
        header_panel = Panel(
            Align.center(header_text),
            title=f"[{user_color}]Text Ranking Tool - File Selection[/{user_color}]",
            subtitle=f"[dim]User: [{user_color}]{username}[/{user_color}][/dim]",
            border_style=user_color,
            padding=(1, 2)
        )
        console.print(header_panel)
        console.print()
        
        # Scan for available CSV files
        available_files = scan_data_directory()
        
        if not available_files:
            console.print("[red]No CSV files found in data directory.[/red]")
            console.print("[yellow]Please add CSV files and try again.[/yellow]")
            return None
    
        # Display file selection Table
        display_file_selection_table(available_files, session_manager, username, console)

        # Get user choice
        choice = Prompt.ask("Enter your choice").strip().lower()
        
        if choice == "b" or choice == "back":
            console.print("[yellow]Returning to user selection...[/yellow]")
            return None
        
        elif choice == "r" or choice == "refresh":
            continue 
        
        else:
            # Handle numeric file selection
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(available_files):
                    selected_file = available_files[choice_num - 1]
                    file_stem = selected_file["stem"]
                    
                    console.print(f"[green]✓ Selected: {selected_file['filename']}[/green]")
                    
                    # Show status based on existing progress
                    progress = session_manager.get_session_progress(username, file_stem)
                    if progress["exists"] and progress["comparisons_made"] > 0:
                        console.print(f"[green]✓ Loading your previous session ({progress['comparisons_made']} comparisons completed)[/green]")
                    else:
                        console.print(f"[blue]✓ Starting fresh ranking session for {username}[/blue]")
                    
                    console.print("[cyan]✓ Initializing algorithm...[/cyan]")
                    console.print()
                    
                    return file_stem
                else:
                    console.print(f"[red]Invalid choice. Please enter 1-{len(available_files)}, 'r', or 'q'[/red]")
                    input("Press Enter to continue...")
            except ValueError:
                console.print(f"[red]Invalid input. Please enter 1-{len(available_files)}, 'r', or 'q'[/red]")
                input("Press Enter to continue...")

def show_file_loading_status(filename: str, text_count: int):
    """Display file loading confirmation"""
    console = Console()
    
    console.print(f"[green]✓ Loaded {text_count} texts from {filename}[/green]")
    console.print("[cyan]Ready to begin comparisons...[/cyan]")
    console.print()



def display_file_selection_table(available_files, session_manager, username, console):
    # CREATE TABLE Object
    file_table = Table(title="[bold green]Available CSV Files[/bold green]",
                    show_lines=False,
                    show_header=True,  
                    show_edge=True,      
                    box=box.SIMPLE)
    
    file_table.add_column("File", style="bold bright_cyan", width=6, justify="center")
    file_table.add_column("Dataset", style="bright_white", width=25)  # Changed from white to bright_white
    file_table.add_column("Your Progress", style="bright_white", width=17)  # Changed from white to bright_white
    file_table.add_column("Status", style="bright_white", width=18)  # Changed from white to bright_white

    for i, file_info in enumerate(available_files, 1):
        filename = file_info["filename"]
        file_stem = file_info["stem"]

        progress = session_manager.get_session_progress(username, file_stem)
        
        # Determine comparisons count
        comparisons = progress.get("comparisons_made", 0) if progress["exists"] else 0
        
        # Set progress and status text based on comparisons
        if comparisons > 0:
            progress_text = f"{comparisons} comparisons"
            status_text = "[green dim]Resume Session[/green dim]"
        else:
            progress_text = "0 comparisons"
            status_text = "[dim green]Start New[/dim green]"

        file_table.add_row(
            f"[dim white]{i}[/dim white]",
            f"[dim green]{filename}[/dim green]",
            f"[dim green]{progress_text}[/dim green]",
            f"[dim green]{status_text}[/dim green]",

        )

    console.print(Align.center(file_table))
    console.print()

    max_choice = len(available_files)
    instruction = (
        "Select file: "
        f"[bright_green][1-{max_choice}][/bright_green] to choose dataset    |    "
        f"[bright_yellow]\[b][/bright_yellow] go back    |    "
        f"[light_salmon1]\[r][/light_salmon1] to refresh"

    )
    console.print(Align.center(instruction))
    console.print()
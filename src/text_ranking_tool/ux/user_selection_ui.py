# src/text_ranking_tool/ux/user_selection_ui.py

import os
import time
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
from rich.align import Align
from ..config.constants import USER_MAPPING, get_user_color

def clear_screen():
    """Clear screen for clean display"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_user_selection() -> Optional[str]:
    """
    Display user selection interface and return chosen username.
    Returns display name (e.g., "Tom Pavone") or None if quit.
    """
    console = Console()
    clear_screen()

    welcome_text = (
        "[bold white]TEXT RANKING RESEARCH TOOL[/bold white]\n"
        "[dim grey70]   User Authentication[/dim grey70]"
    )

    header_panel = Panel(
        Align.center(welcome_text, vertical="middle"),
        style="white on black",
        border_style="grey70",
        padding=(1, 6),
        subtitle="[dim]v1.0 | Multi-User Session Management[/dim]"
    )

    console.print(header_panel)
    console.print("\n")

    user_table = Table(
        title="[bold cyan]Researcher Selection[/bold cyan]",
        show_header=True,
        header_style="cyan",
        border_style="grey42",
        show_lines=False,
        padding=(0, 2)
    )

    user_table.add_column("ID", style="bold bright_cyan", width=4, justify="center")
    user_table.add_column("Researcher Name", style="bold white", width=20)
    user_table.add_column("Status", style="cyan", width=28)

    for i, (display_name, user_id) in enumerate(USER_MAPPING.items(), 1):
        user_color = get_user_color(display_name)
        colored_name = f"[{user_color}]{display_name}[/{user_color}]"
        user_table.add_row(
            f"[bold white]{i}[/bold white]",
            colored_name,
            "[green dim]Ready to rank texts[/green dim]"
        )

    console.print(Align.center(user_table))
    console.print()
    
    # Instructions
    instruction_text = Text()
    instruction_text.append("Select user: ", style="white")
    instruction_text.append("[1-3]", style="bold green")
    instruction_text.append(" for user selection | ", style="white")
    instruction_text.append("[q]", style="bold red")
    instruction_text.append(" to quit", style="white")
    
    console.print(Align.center(instruction_text))
    console.print()
    
    # Get user choice
    while True:
        choice = Prompt.ask("Enter your choice").strip().lower()
        
        if choice == "q" or choice == "quit":
            console.print("[yellow]Exiting text ranking tool...[/yellow]")
            return None
       
        # ✅ HIDDEN ADMIN ACCESS - Add this check
        elif choice == "admin":
            console.print("[cyan]✓ Admin access granted[/cyan]")
            return "ADMIN"
        
        # Handle numeric choices
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(USER_MAPPING):
                # Get the display name for the chosen number
                selected_user = list(USER_MAPPING.keys())[choice_num - 1]
                user_color = get_user_color(selected_user)
                
                console.print(f"[{user_color}]✓ Selected user: {selected_user}[/{user_color}]\n")
                return selected_user
            else:
                console.print(f"[red]Invalid choice. Please enter 1-{len(USER_MAPPING)} or 'q'[/red]")
        except ValueError:
            console.print(f"[red]Invalid input. Please enter 1-{len(USER_MAPPING)} or 'q'[/red]")

def show_user_welcome(username: str):
    """Display personalized welcome message for selected user"""
    console = Console()
    user_color = get_user_color(username)
    
    # Create welcome panel
    welcome_text = f"Welcome, {username}!\nPreparing your text ranking session..."
    welcome_panel = Panel(
        Align.center(welcome_text),
        title=f"[{user_color}]User Session Starting[/{user_color}]",
        border_style=user_color,
        padding=(1, 2)
    )
    
    console.print()
    console.print(welcome_panel)
    console.print()
    time.sleep(1)
    
def show_user_session_info(username: str, session_count: int = 0):
    """Display user session information"""
    console = Console()
    user_color = get_user_color(username)
    
    info_text = Text()
    info_text.append("Active user: ", style="white")
    info_text.append(f"{username}", style=f"bold {user_color}")
    
    if session_count > 0:
        info_text.append(" | Previous sessions: ", style="dim")
        info_text.append(f"{session_count}", style="bold cyan")
    
    console.print(info_text)

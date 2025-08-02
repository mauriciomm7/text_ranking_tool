#src/text_ranking_tool/ux/admin_iu/export_ui.py
"""
Minimal Export UI - Just copy files and show results
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import os
import shutil
from .admin_main_ui import (get_admin_choice_with_navigation,handle_navigation_action)
from ...config.constants import INTERNAL_EXPORT_DIR, EXTERNAL_EXPORT_DIR

def export_mode():
    """Export mode with dynamic navigation"""
    console = Console()
    
    while True:
        _clear_screen()
        console.print(Panel("📤 Export Mode", style="bold blue"))
        console.print("[1] Per User Export")
        console.print("[2] Per Dataset Export") 
        console.print("[3] Overall Export")
        choice, nav_action = get_admin_choice_with_navigation(
            "Select export type", 
            ["1", "2", "3"],
            console
        )
        
        if handle_navigation_action(nav_action):
            break
            
        if choice == "1":
            _per_user_export(console)
        elif choice == "2":
            _per_dataset_export(console)
        elif choice == "3":
            _overall_export(console)

def _per_user_export(console):
    files = list(INTERNAL_EXPORT_DIR.glob("*.csv"))
    if not files:
        console.print("[yellow]No files to export[/yellow]")
        Prompt.ask("Press Enter")
        return
    
    EXTERNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)  # parents=True for safety
    copied_count = 0
    
    for f in files:
        user = f.name.split('_')[0]
        user_dir = EXTERNAL_EXPORT_DIR / user
        user_dir.mkdir(exist_ok=True)
        shutil.copy(f, user_dir / f.name)
        copied_count += 1
    
    console.print(f"[green]✓ Copied {copied_count} files by user[/green]")  # Added checkmark
    Prompt.ask("Press Enter")

def _per_dataset_export(console):
    files = list(INTERNAL_EXPORT_DIR.glob("*.csv"))
    if not files:
        console.print("[yellow]No files to export[/yellow]")
        Prompt.ask("Press Enter")
        return
    
    EXTERNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)  # parents=True for safety
    copied_count = 0
    
    for f in files:
        parts = f.name.split('_')
        dataset = parts[1] if len(parts) > 1 else 'unknown'
        dataset_dir = EXTERNAL_EXPORT_DIR / dataset
        dataset_dir.mkdir(exist_ok=True)
        shutil.copy(f, dataset_dir / f.name)
        copied_count += 1
    
    console.print(f"[green]✓ Copied {copied_count} files by dataset[/green]")  # Added checkmark
    Prompt.ask("Press Enter")

def _overall_export(console):
    files = list(INTERNAL_EXPORT_DIR.glob("*.csv"))
    if not files:
        console.print("[yellow]No files to export[/yellow]")
        Prompt.ask("Press Enter")
        return
    
    output_dir = EXTERNAL_EXPORT_DIR / "overall"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    for f in files:
        shutil.copy(f, output_dir / f.name)
        copied_count += 1
    
    console.print(f"[green]✓ Copied {copied_count} files to overall folder[/green]")  # Added checkmark
    Prompt.ask("Press Enter")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

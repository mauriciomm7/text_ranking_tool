# src\text_ranking_tool\ux\admin_iu\algorithm_config.py
"""
Algorithm Configuration - Runtime algorithm selection
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import os
import json
from .admin_main_ui import get_admin_choice_with_navigation, handle_navigation_action
from ...config.constants import (get_available_algorithms, 
                                 CONFIGURED_ALGORITHM, 
                                 set_algorithm, 
                                 CONFIG_FILE,
                                 _config)

def algorithm_config_mode():
    """Algorithm configuration with dynamic navigation"""
    console = Console()
    
    while True:
        _clear_screen()
        console.print(Panel("⚙️ Algorithm Configuration", style="bold yellow"))
        console.print(f"Current: [green]{CONFIGURED_ALGORITHM}[/green]")
        console.print()
        
        # List algorithms
        algorithms = get_available_algorithms()
        for i, algo in enumerate(algorithms, 1):
            status = " ✅" if algo == CONFIGURED_ALGORITHM else ""
            console.print(f"[{i}] {algo}{status}")
        
        choices = [str(i) for i in range(1, len(algorithms) + 1)]
        choice, nav_action = get_admin_choice_with_navigation(
            "Select algorithm", 
            choices,
            console
        )
        
        if handle_navigation_action(nav_action):
            break
            
        if choice.isdigit():
            algo_index = int(choice) - 1
            if 0 <= algo_index < len(algorithms):
                selected_algo = algorithms[algo_index]
                _switch_algorithm(console, selected_algo)

def _switch_algorithm(console, algorithm_id):
    """Switch algorithm with session/permanent choice"""
    if algorithm_id == CONFIGURED_ALGORITHM:
        console.print(f"[yellow]{algorithm_id} is already current[/yellow]")
        Prompt.ask("Press Enter")
        return
    
    console.print(f"Switch to: [cyan]{algorithm_id}[/cyan]")
    console.print("[1] Temporary (session only)")
    console.print("[2] Permanent (save to config)")
    
    choice, nav_action = get_admin_choice_with_navigation(
        "Select change type", 
        ["1", "2"], 
        console
    )
    
    if handle_navigation_action(nav_action):
        return
        
    # Apply the algorithm change
    success = set_algorithm(algorithm_id)
    if not success:
        console.print(f"[red]Failed to switch to {algorithm_id}[/red]")
        Prompt.ask("Press Enter")
        return
    
    if choice == "2":
        # Save permanently
        try:
            _config["algorithm"] = algorithm_id
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(_config, f, indent=2)
            console.print(f"[green]✓ Permanently switched to {algorithm_id}[/green]")
        except Exception:
            console.print("[yellow]✓ Switched temporarily (save failed)[/yellow]")
    else:
        console.print(f"[green]✓ Temporarily switched to {algorithm_id}[/green]")
    
    Prompt.ask("Press Enter")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

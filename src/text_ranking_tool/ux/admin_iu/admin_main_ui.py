#src/text_ranking_tool/ux/admin_iu/admin_main_ui.py

"""
Admin Main UI - Entry point for analysis and administration system
Single integration point with main.py application
Located in ux/admin/ subdirectory for better organization
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
import os

def show_admin_menu():
    """
    Main admin menu entry point - 4 modes now
    This is the ONLY function that gets called from main.py
    """
    console = Console()
    
    while True:
        _clear_screen()
        _show_main_header(console)
        _show_four_mode_options(console)

        choice, nav_action = get_admin_choice_with_navigation(
            "Select mode", ["1", "2", "3", "4"], console 
        )

        if handle_navigation_action(nav_action):
            break

        if choice == "1":
            _launch_statistical_analysis_mode()
        elif choice == "2":
            _launch_export_mode()
        elif choice == "3":
            result = _launch_data_management_mode()
            if result == "exit_to_main":
                break  # Exit to  main app
        elif choice == "4":  
            _launch_algorithm_config_mode()


def _show_main_header(console: Console):
    """Display the main admin header panel"""
    header_text = Text()
    header_text.append("🔬 ANALYSIS & ADMINISTRATION MENU", style="bold cyan")
    header_text.append("\n")
    header_text.append("Advanced Statistical Analysis & Data Export", style="dim cyan")
    
    header_panel = Panel(
        Align.center(header_text),
        border_style="bold cyan",
        padding=(1, 2),
        title="[bold white]Admin System[/bold white]"
    )
    console.print(header_panel)
    console.print()

def _show_four_mode_options(console: Console):
    """Display the 4 mode selection panel"""
    modes_panel = Panel(
        "[bold white]1.[/bold white] [green]📊 Statistical Analysis Mode[/green]\n"
        "[dim]   Machine-as-user approach with unified metrics dashboard[/dim]\n"
        "[dim]   Inter-user agreement, ranking comparisons, overlaps[/dim]\n\n"
        
        "[bold white]2.[/bold white] [blue]📤 Export Mode[/blue]\n"
        "[dim]   Always available - not conditional on completion[/dim]\n"
        "[dim]   Per user, per file, overall project exports[/dim]\n\n"
        
        "[bold white]3.[/bold white] [red]⚠️  Data Management Mode[/red]\n"
        "[dim]   Reset all internal data, return to main menu[/dim]\n"
        "[dim]   Administrative functions and navigation[/dim]\n\n"
        
        "[bold white]4.[/bold white] [yellow]⚙️  Algorithm Configuration Mode[/yellow]\n"
        "[dim]   Switch between recursive_median, tournament, etc.[/dim]\n"
        "[dim]   Session-based or persistent algorithm selection[/dim]",
        title="[bold cyan]Select Analysis Mode[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(modes_panel)
    console.print()


def _launch_statistical_analysis_mode():
    """Launch statistical analysis mode from analysis_ui module"""
    try:
        from .analysis_ui import statistical_analysis_mode
        statistical_analysis_mode()
    except ImportError:
        _show_module_error("Statistical Analysis", "analysis_ui.py")

def _launch_export_mode():
    """Launch export mode from export_ui module"""
    try:
        from .export_ui import export_mode
        export_mode()
    except ImportError:
        _show_module_error("Export", "export_ui.py")

def _launch_data_management_mode():
    """Launch data management mode from data_admin module"""
    try:
        from .data_admin import data_management_mode
        return data_management_mode()
    except ImportError:
        _show_module_error("Data Management", "data_admin.py")
        return None


def _launch_algorithm_config_mode():
    """Launch algorithm configuration mode"""
    try:
        from .algorithm_config import algorithm_config_mode
        algorithm_config_mode()
    except ImportError:
        _show_module_error("Algorithm Configuration", "algorithm_config.py")





def _show_module_error(mode_name: str, filename: str):
    """Display error message for missing modules"""
    console = Console()
    
    error_text = Text()
    error_text.append("MODULE NOT FOUND", style="bold red")
    error_text.append(f"\n\n{mode_name} mode requires: ux/admin/{filename}")
    error_text.append("\n\nPlease implement the missing module file.")
    
    error_panel = Panel(
        error_text,
        title="[bold red]Implementation Error[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    
    console.print(error_panel)
    console.print()
    
    Prompt.ask("Press Enter to continue", default="")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Integration functions for main.py
def show_admin_menu_from_startup():
    """Wrapper for startup integration"""
    show_admin_menu()

def show_admin_menu_from_completion():
    """Wrapper for completion results integration"""
    show_admin_menu()


def get_admin_choice_with_navigation(prompt_text, functional_choices, console=None):
    """
    Dynamic choice handler for admin modes - builds choices on call
    """    
    # Display styled navigation options with better formatting
    if console:
        console.print()
        from rich.text import Text
        nav_text = Text()
        nav_text.append("[b] ", style="bold yellow")
        nav_text.append("Back to Ranking Menu", style="dim white")
        nav_text.append(" | ", style="white")
        nav_text.append("[q] ", style="bold red")
        nav_text.append("Quit Application", style="dim white")
        console.print(nav_text)
    
    choice = Prompt.ask(prompt_text)
    
    # Handle universal navigation
    if choice == "b":
        return choice, "back"
    elif choice == "q":
        return choice, "quit" 
    else:
        return choice, None


def handle_navigation_action(action):
    """Execute the navigation action"""
    if action == "back":
        return True  # Signal to break
    elif action == "quit":
        exit()
    return False  

# src/text_ranking_tool/ux/comparison_ui.py
import os
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from ..config.constants import DEBUG

def get_user_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Dispatch to algorithm-specific comparison UI"""
    
    algorithm = comparison_data.get("algorithm", "")
    
    if algorithm == "tournament":
        return get_tournament_comparison_choice(comparison_data)
    elif algorithm == "recursive_median":
        return get_recursive_median_comparison_choice(comparison_data)
    else:
        # Fallback to generic comparison
        return get_generic_comparison_choice(comparison_data)

def get_tournament_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Tournament-specific UI: Competitor vs Competitor bracket advancement"""
    
    console = Console()
    text1 = comparison_data["text1"]
    text2 = comparison_data["text2"] 
    comparison_num = comparison_data["comparison_number"]
    
    # Get tournament context
    context = comparison_data.get("bracket_info", {})
    current_round = context.get("current_round", 1)
    
    _clear_screen()
    
    # Tournament header (consistent with recursive median styling)
    console.rule("[dim dark_sea_green]Tournament Bracket[/dim dark_sea_green]", style="dim dark_sea_green")
    console.print(f"[dim dark_sea_green]Round {current_round} - Match #{comparison_num}[/dim dark_sea_green]", justify="center")
    console.rule(style="dim dark_sea_green")

    # Competitor A panel (standardized styling)
    competitor_a_panel = Panel(
        Align.center(text1["text"]),
        title="[bold turquoise2]COMPETITOR A[/bold turquoise2]",
        border_style="dim turquoise2",
        style="turquoise2",
        padding=(1, 2)
    )

    # Competitor B panel (standardized styling)
    competitor_b_panel = Panel(
        Align.center(text2["text"],),
        title="[bold gold3]COMPETITOR B[/bold gold3]",
        border_style="dim gold3",
        style="gold3",
        padding=(1, 2)
    )

    console.print(competitor_a_panel)
    console.print()
    console.print(competitor_b_panel)
    console.print()

    # Tournament-specific instructions (consistent formatting)
    instruction = Text()
    instruction.append("Which text is ", style="white")
    instruction.append("MORE NEGATIVE", style="indian_red")
    instruction.append(" ?", style="white ")
    console.print(instruction)

    # Input options (standardized format)
    options = Text()
    options.append("Enter: ", style="white")
    options.append("[A] or [a]", style="bold turquoise2")
    options.append(" | ", style="white")
    options.append("[B] or [b]", style="bold gold3")
    console.print(options)

    
    # Special commands (consistent with recursive median)
    extra_options = Text()
    extra_options.append("Special: ", style="dim")
    extra_options.append("[u] undo", style="dim violet")
    extra_options.append(" | ", style="dim")
    extra_options.append("[q] quit", style="dim red")
    console.print(extra_options)
    console.print()
    
    # Handle tournament input (with undo support)
    while True:
        choice = Prompt.ask("Your choice").lower().strip()
        
        if choice in ["a", "competitor a"]:
            console.print("[green]✓ COMPETITOR A advances (more negative)[/green]\n")
            return text1["id"]
        elif choice in ["b", "competitor b"]:
            console.print("[red]✓ COMPETITOR B advances (more negative)[/red]\n")
            return text2["id"]
        elif choice == "u":
            console.print("[yellow]⟲ Undoing last comparison...[/yellow]")
            return "UNDO"
        elif choice == "q":
            console.print("[yellow]Exiting tournament bracket...[/yellow]")
            raise KeyboardInterrupt("User requested quit")
        else:
            console.print("[red]Invalid choice. Try: A, B, u, or q[/red]")


def get_recursive_median_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Recursive median UI: Your proven PIVOT vs COMPARISON TEXT paradigm"""
    
    console = Console()
    
    # SWAP THE ROLES - text2 is actually the pivot, text1 is the comparison
    pivot_text = comparison_data["text2"]      # The text that stays consistent  
    comparison_text = comparison_data["text1"] # The text that changes each comparison
    comparison_num = comparison_data["comparison_number"]
    
    if DEBUG:
        print(f"DEBUG UI: Received text1 (COMPARISON) = {comparison_text['id']}")
        print(f"DEBUG UI: Received text2 (PIVOT) = {pivot_text['id']}")
        print(f"DEBUG UI: PIVOT text preview: {pivot_text['text'][:50]}...")
        print(f"DEBUG UI: COMPARISON text preview: {comparison_text['text'][:50]}...")
    
    _clear_screen()
    
    # Recursive median header
    console.rule("[dim violet]Recursive Median Sort[/dim violet]", style="dim violet")
    console.print(f"[dim violet dim]Comparison #{comparison_num}[/dim violet dim]", justify="center")
    console.rule(style="dim violet")
    
    # PIVOT panel (now using pivot_text)
    pivot_panel = Panel(
        Align.center(pivot_text["text"]),
        title="[bold white]PIVOT[/bold white]",
        border_style="dim white",
        padding=(1, 2)
    )
    
    # COMPARISON TEXT panel (now using comparison_text)
    comparison_panel = Panel(
        comparison_text["text"],
        title="[bold cyan]COMPARISON TEXT[/bold cyan]",
        border_style="cyan",
        style="cyan",
        padding=(1, 2)
    )
    
    console.print(pivot_panel)
    console.print()
    console.print(comparison_panel)
    console.print()
    
    # Your exact instruction styling
    instruction = Text()
    instruction.append("Is the ", style="white")
    instruction.append("COMPARISON TEXT", style="bold cyan")
    instruction.append(" more ", style="white")
    instruction.append("POSITIVE", style="dim green")
    instruction.append(" or more ", style="white")
    instruction.append("NEGATIVE", style="dim red")
    instruction.append("?", style="white")
    console.print(instruction)
    
    # Your exact input options
    options = Text()
    options.append("Enter: ", style="white")
    options.append("[+] or [positive]", style="bold green")
    options.append(" | ", style="white")
    options.append("[-] or [negative]", style="bold red")
    console.print(options)
    
    # Your exact special commands
    extra_options = Text()
    extra_options.append("Special: ", style="dim")
    extra_options.append("[u] undo", style="dim violet")
    extra_options.append(" | ", style="dim")
    extra_options.append("[q] quit", style="dim blue")
    console.print(extra_options)
    console.print()
    
    # Handle input with corrected return logic
    while True:
        choice = Prompt.ask("Your choice").lower().strip()
        if choice in ["+", "positive"]:
            console.print("[green]✓ COMPARISON TEXT is more positive (PIVOT is more negative)[/green]\n")
            return pivot_text["id"]  # Return the PIVOT's id (text2)
        elif choice in ["-", "negative"]:
            console.print("[red]✓ COMPARISON TEXT is more negative[/red]\n")
            return comparison_text["id"]  # Return the COMPARISON TEXT's id (text1)
        elif choice == "u":
            console.print("[yellow]⟲ Undoing last comparison...[/yellow]")
            return "UNDO"
        elif choice == "q":
            console.print("[yellow]Exiting recursive median sort...[/yellow]")
            raise KeyboardInterrupt("User requested quit")
        else:
            console.print("[red]Invalid choice. Try: +, -, positive, negative, u, or q[/red]")


def get_generic_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Fallback generic comparison for unknown algorithms"""
    
    console = Console()
    text1 = comparison_data["text1"]
    text2 = comparison_data["text2"]
    comparison_num = comparison_data["comparison_number"]
    
    _clear_screen()
    
    console.print("\n" + "="*80)
    console.print(f"[bold cyan]Text Comparison #{comparison_num}[/bold cyan]")
    console.print("="*80 + "\n")
    
    # Simple A vs B panels
    panel_a = Panel(
        Align.center(text1["text"]),
        title=f"[bold green]TEXT A[/bold green] (ID: {text1['id']})",
        border_style="green",
        padding=(1, 2)
    )
    
    panel_b = Panel(
        Align.center(text2["text"]),
        title=f"[bold red]TEXT B[/bold red] (ID: {text2['id']})",
        border_style="red",
        padding=(1, 2)
    )
    
    console.print(panel_a)
    console.print()
    console.print(panel_b)
    console.print()
    
    console.print("[bold yellow]Which text is MORE NEGATIVE?[/bold yellow]")
    
    while True:
        choice = Prompt.ask("Enter your choice", choices=["A", "B", "a", "b", "q"]).lower()
        
        if choice == "a":
            console.print(f"[green]✓ You chose Text A ({text1['id']})[/green]\n")
            return text1["id"]
        elif choice == "b":
            console.print(f"[red]✓ You chose Text B ({text2['id']})[/red]\n")
            return text2["id"]
        elif choice == "q":
            console.print("[yellow]Exiting comparison...[/yellow]")
            raise KeyboardInterrupt("User requested quit")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

# src/text_ranking_tool/ux/comparison_ui.py
import os
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from ..config.constants import DEBUG
from ..utils.text_formatters import format_text

def get_user_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Dispatch to algorithm-specific comparison UI"""
    
    algorithm = comparison_data.get("algorithm", "")
    
    if algorithm == "tournament":
        return get_tournament_comparison_choice(comparison_data)
    elif algorithm == "recursive_median":
        return get_recursive_median_comparison_choice(comparison_data)
    else:
        return get_generic_comparison_choice(comparison_data)

def get_tournament_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Tournament-specific UI: Competitor vs Competitor bracket advancement"""
    
    console = Console()
    text1 = comparison_data["text1"]
    text2 = comparison_data["text2"] 
    comparison_num = comparison_data["comparison_number"]
    
    context = comparison_data.get("bracket_info", {})
    current_round = context.get("current_round", 1)
    
    _clear_screen()
    
    console.rule("[dim dark_sea_green]Tournament Bracket[/dim dark_sea_green]", style="dim dark_sea_green")
    console.print(f"[dim dark_sea_green]Round {current_round} - Match #{comparison_num}[/dim dark_sea_green]", justify="center")
    console.rule(style="dim dark_sea_green")

    competitor_a_panel = Panel(
        Align.center(format_text(text1["text"])),  # ← CHANGED
        title="[bold turquoise2]COMPETITOR A[/bold turquoise2]",
        border_style="dim turquoise2",
        style="turquoise2",
        padding=(1, 2)
    )

    competitor_b_panel = Panel(
        Align.center(format_text(text2["text"])),  # ← CHANGED
        title="[bold gold3]COMPETITOR B[/bold gold3]",
        border_style="dim gold3",
        style="gold3",
        padding=(1, 2)
    )

    console.print(competitor_a_panel)
    console.print()
    console.print(competitor_b_panel)
    console.print()

    instruction = Text()
    instruction.append("Which text is ", style="white")
    instruction.append("MORE NEGATIVE", style="indian_red")
    instruction.append(" ?", style="white ")
    console.print(instruction)

    options = Text()
    options.append("Enter: ", style="white")
    options.append("[A] or [a]", style="bold turquoise2")
    options.append(" | ", style="white")
    options.append("[B] or [b]", style="bold gold3")
    console.print(options)

    extra_options = Text()
    extra_options.append("Special: ", style="dim")
    extra_options.append("[u] undo", style="dim violet")
    extra_options.append(" | ", style="dim")
    extra_options.append("[q] quit", style="dim red")
    console.print(extra_options)
    console.print()
    
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
    """Recursive median UI: Standardized A vs B direct selection."""
    
    console = Console()
    
    text_a_data = comparison_data["text1"]
    text_b_data = comparison_data["text2"]
    comparison_num = comparison_data["comparison_number"]
    
    _clear_screen()
        
    if DEBUG:
        from rich.console import Console as _C
        formatted_a = format_text(text_a_data["text"])
        _C().print(f"[dim]FORMATTER DEBUG — plain: {repr(formatted_a.plain[:60])}[/dim]")
        _C().print(f"[dim]FORMATTER DEBUG — spans: {formatted_a._spans[:5]}[/dim]")
        print(f"DEBUG UI: Received text1 (COMPARISON) = {text_a_data['id']}")
        print(f"DEBUG UI: Received text2 (PIVOT) = {text_b_data['id']}")
        print(f"DEBUG UI: PIVOT text preview: {text_b_data['text'][:50]}...")
        print(f"DEBUG UI: COMPARISON text preview: {text_a_data['text'][:50]}...")
    
    console.rule("[dim violet]Recursive Median Sort[/dim violet]", style="violet")
    console.print(f"[dim violet]Comparison #{comparison_num}[/dim violet]", justify="center")
    console.rule(style="violet")

    title_a = "[bold turquoise2]TEXT A[/bold turquoise2]"
    title_b = "[bold gold3]TEXT B[/bold gold3]"
    if DEBUG:
        title_a += " [dim grey53](Comparison)[/dim grey53]"
        title_b += " [dim grey53](Pivot)[/dim grey53]"

    panel_a = Panel(
        Align.center(format_text(text_a_data["text"])),  # ← CHANGED
        title=title_a,
        border_style="dim turquoise2",
        style="turquoise2",
        padding=(1, 2)
    )

    panel_b = Panel(
        Align.center(format_text(text_b_data["text"])),  # ← CHANGED
        title=title_b,
        border_style="dim gold3",
        style="gold3",
        padding=(1, 2)
    )

    console.print(panel_a)
    console.print()
    console.print(panel_b)
    console.print()

    instruction = Text()
    instruction.append("Which text is ", style="white")
    instruction.append("MORE NEGATIVE", style="indian_red")
    instruction.append("?", style="white")
    console.print(instruction)

    options = Text()
    options.append("Enter: ", style="white")
    options.append("[A] or [a]", style="bold turquoise2")
    options.append(" | ", style="white")
    options.append("[B] or [b]", style="bold gold3")
    console.print(options)
    
    extra_options = Text()
    extra_options.append("Special: ", style="dim")
    extra_options.append("[u] undo", style="dim violet")
    extra_options.append(" | ", style="dim")
    extra_options.append("[q] quit", style="dim blue")
    console.print(extra_options)
    console.print()
    
    while True:
        choice = Prompt.ask("Your choice").lower().strip()
        if choice in ["a"]:
            console.print("[red]✓ Text A selected (more negative)[/red]\n")
            return text_a_data["id"]
        elif choice in ["b"]:
            console.print("[green]✓ Text B selected (more negative)[/green]\n")
            return text_b_data["id"]
        elif choice == "u":
            console.print("[yellow]⟲ Undoing last comparison...[/yellow]")
            return "UNDO"
        elif choice == "q":
            console.print("[yellow]Exiting recursive median sort...[/yellow]")
            raise KeyboardInterrupt("User requested quit")
        else:
            console.print("[red]Invalid choice. Try: a, b, u, or q[/red]")


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
    
    panel_a = Panel(
        Align.center(format_text(text1["text"])),  # ← CHANGED
        title=f"[bold green]TEXT A[/bold green] (ID: {text1['id']})",
        border_style="green",
        padding=(1, 2)
    )
    
    panel_b = Panel(
        Align.center(format_text(text2["text"])),  # ← CHANGED
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

def get_transitive_quick_comparison_choice(comparison_data: Dict[str, Any]) -> str:
    """Transitive Quick UI: Simple A vs B direct selection."""
    
    console = Console()
    
    text_a_data = comparison_data["text1"]
    text_b_data = comparison_data["text2"]
    comparison_num = comparison_data["comparison_number"]
    
    _clear_screen()
    
    dim_magenta = "dim magenta"
    console.rule("[dim magenta]Transitive Quick Rank[/]", style=dim_magenta)
    console.print(f"[dim magenta]Comparison #{comparison_num}[/]", justify="center")
    console.rule(style=dim_magenta)

    title_a = "[bold turquoise2]TEXT A[/bold turquoise2]"
    title_b = "[bold gold3]TEXT B[/bold gold3]"
    if DEBUG:
        title_a += " [dim grey53](Comparison)[/dim grey53]"
        title_b += " [dim grey53](Anchor)[/dim grey53]"

    panel_a = Panel(
        Align.center(format_text(text_a_data["text"])),  # ← CHANGED
        title=title_a,
        border_style="dim turquoise2",
        style="turquoise2",
        padding=(1, 2)
    )

    panel_b = Panel(
        Align.center(format_text(text_b_data["text"])),  # ← CHANGED
        title=title_b,
        border_style="dim gold3",
        style="gold3",
        padding=(1, 2)
    )

    console.print(panel_a)
    console.print()
    console.print(panel_b)
    console.print()

    instruction = Text()
    instruction.append("Which text is ", style="white")
    instruction.append("MORE NEGATIVE", style="red")
    instruction.append("?", style="white")
    console.print(instruction)

    options = Text()
    options.append("Enter: ", style="white")
    options.append("[A] or [a]", style="bold turquoise2")
    options.append(" | ", style="white")
    options.append("[B] or [b]", style="bold gold3")
    console.print(options)
    
    extra_options = Text()
    extra_options.append("Special: ", style="dim")
    extra_options.append("[u] undo", style="dim violet")
    extra_options.append(" | ", style="dim")
    extra_options.append("[q] quit", style="dim blue")
    console.print(extra_options)
    console.print()
    
    while True:
        choice = Prompt.ask("Your choice").lower().strip()
        if choice in ["a"]:
            console.print("[red]✓ Text A selected (more negative)[/red]\n")
            return text_a_data["id"]
        elif choice in ["b"]:
            console.print("[green]✓ Text B selected (more negative)[/green]\n")
            return text_b_data["id"]
        elif choice == "u":
            console.print("[yellow]⟲ Undoing last comparison...[/yellow]")
            return "UNDO"
        elif choice == "q":
            console.print("[yellow]Exiting transitive ranking...[/yellow]")
            raise KeyboardInterrupt("User requested quit")
        else:
            console.print("[red]Invalid choice. Try: a, b, u, or q[/red]")

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

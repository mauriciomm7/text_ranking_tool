# src\text_ranking_tool\ux\auto_export_ui.py
"""
Auto Export UI - Ultra-clean completion flow with automatic exports
Handles ranking completion results and next action selection with context-aware navigation
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from ..config.constants import get_user_color

def show_completion_results(username: str, file_stem: str, algorithm, final_ranking: list, text_data: list):
    """Ultra-clean completion flow - simple ranking workflow continuation"""
    
    console = Console()
    user_color = get_user_color(username)
    
    # Success message
    success_panel = Panel(
        f"🎉 Ranking Complete & Exported!\n\n"
        f"User: {username}\n"
        f"File: {file_stem}.csv\n"
        f"Algorithm: {algorithm.NAME}\n"
        f"Texts ranked: {len(final_ranking)}\n\n"
        f"✓ Files automatically exported to deliverables folder",
        title=f"[{user_color}]Success![/{user_color}]",
        border_style=user_color
    )
    
    console.print()
    console.print(success_panel)
    console.print()
    
    # Show top 10 results
    console.print("[bold]Top 10 Most Negative Texts:[/bold]")
    
    results_table = Table(show_header=True, header_style="bold")
    results_table.add_column("Rank", width=6)
    results_table.add_column("ID", width=10)
    results_table.add_column("Text Preview", width=50)
    
    text_lookup = {item['id']: item for item in text_data}
    
    for i, text_id in enumerate(final_ranking[:10], 1):
        text_info = text_lookup.get(text_id, {})
        text_preview = text_info.get('text', 'N/A')[:47] + "..." if len(text_info.get('text', '')) > 50 else text_info.get('text', 'N/A')
        
        results_table.add_row(
            str(i),
            text_id,
            text_preview
        )
    
    console.print(results_table)
    console.print()
    
    # Simple 2-option completion flow
    while True:
        console.print("What's next?")
        console.print("[green]1.[/green] Rank another dataset")
        console.print("[green]2.[/green] Exit")
        
        choice = input("\nChoose (1-2): ").strip()
        
        if choice == "1":
            from ..main import main
            return main()  # New ranking session
        elif choice == "2":
            console.print("[yellow]Thank you for using the Text Ranking Tool![/yellow]")
            return
        else:
            console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")

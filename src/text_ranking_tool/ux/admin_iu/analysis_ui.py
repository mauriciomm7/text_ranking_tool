#src/text_ranking_tool/ux/admin_iu/analysis_ui.py
"""
Statistical Analysis UI - Clean architecture with separated concerns
Machine-as-user approach with unified metrics dashboard
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
import os
from typing import Dict, List, Optional, Tuple
from ...stats.stats_for_ui import StatsForUI
from .admin_main_ui import (get_admin_choice_with_navigation,handle_navigation_action)
from ...config.constants import INTERNAL_EXPORT_DIR, INTERNAL_DATA_DIR, USER_MAPPING, get_user_color
from ...utils.formatters_ui import (format_correlation, format_percentage, format_rank_diff, format_integer,
                         format_participant_name, format_strength_display, 
                         get_strength_color,interpret_correlation_strength)

def statistical_analysis_mode():
    """Main statistical analysis UX with dynamic navigation"""
    console = Console()
    
    while True:
        _clear_screen()
        _show_statistical_analysis_header(console)
        _show_analysis_options(console)
        
        choice, nav_action = get_admin_choice_with_navigation(
            "Select analysis", ["1", "2", "3"], console)

        if handle_navigation_action(nav_action):
            break
            
        # Handle functional choices
        if choice == "1":
            show_correlation_matrices(console)
        elif choice == "2":
            show_unified_metrics_dashboard(console)
        elif choice == "3":
            show_direct_comparison(console)

def _show_statistical_analysis_header(console: Console):
    """Display statistical analysis mode header"""
    header_text = Text()
    header_text.append("📊 Statistical Analysis Mode", style="bold green")
    header_text.append("\n")
    header_text.append("Machine-as-User Approach with Unified Metrics", style="dim green")
    
    header_panel = Panel(
        Align.center(header_text),
        border_style="bold green",
        padding=(1, 2),
        title="[bold white]Advanced Correlation Analysis[/bold white]"
    )
    console.print(header_panel)
    console.print()

def _show_analysis_options(console: Console):
    """Display analysis options with standardized navigation"""
    options_panel = Panel(
        "[bold white]1.[/bold white] [green]Complete Correlation Matrices[/green]\n"
        "[dim]   Separate matrices for Kendall's τ, Spearman ρ, overlaps[/dim]\n\n"
        
        "[bold white]2.[/bold white] [cyan]⭐ Unified Metrics Dashboard[/cyan]\n"
        "[dim]   ALL metrics in columns - the beautiful unified view[/dim]\n\n"
        
        "[bold white]3.[/bold white] [blue]Direct Ranking Comparison[/blue]\n"
        "[dim]   Head-to-head analysis between any 2 participants[/dim]",
        title="[bold green]📊 Statistical Analysis Options[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(options_panel)
# ===============================
# OPTION 1: CORRELATION MATRICES
# ===============================

def show_correlation_matrices(console: Console):
    """Option 1: Beautiful separate matrices for each metric"""
    _clear_screen()
    console.print(Panel(
        "[bold green]📊 Complete Correlation Matrices[/bold green]\n"
        "[dim]Separate matrices for each statistical metric[/dim]",
        border_style="green"
    ))
    
    try:
        dataset_stem = _select_dataset(console)
        if not dataset_stem:
            return
        
        participants_data = StatsForUI.load_all_participants_data(
            dataset_stem, INTERNAL_EXPORT_DIR, INTERNAL_DATA_DIR, USER_MAPPING
        )
        
        if len(participants_data) < 2:
            _show_insufficient_data_message(console, dataset_stem)
            return
        
        matrices = StatsForUI.generate_correlation_matrices(participants_data)
        
        _display_correlation_matrix(console, matrices['kendall'], "Kendall's τ", "green")
        console.print()
        _display_correlation_matrix(console, matrices['spearman'], "Spearman ρ", "blue")
        console.print()
        _display_correlation_matrix(console, matrices['overlap_10'], "Top-10 Overlap", "cyan")
        console.print()
        _display_correlation_matrix(console, matrices['overlap_20'], "Top-20 Overlap", "magenta")
        
    except Exception as e:
        _show_error_message(console, "Correlation Matrices", str(e))
    
    console.print()
    Prompt.ask("Press Enter to continue", default="")

# ===============================
# OPTION 2: UNIFIED DASHBOARD ⭐
# ===============================

def show_unified_metrics_dashboard(console: Console):
    """Option 2: THE CROWN JEWEL - Unified dashboard with all metrics"""
    _clear_screen()
    console.print(Panel(
        "[bold cyan]⭐ Unified Metrics Dashboard[/bold cyan]\n"
        "[dim]All participants and metrics in beautiful unified view[/dim]",
        border_style="cyan"
    ))
    
    try:
        dataset_stem = _select_dataset(console)
        if not dataset_stem:
            return
        
        participants_data = StatsForUI.load_all_participants_data(
            dataset_stem, INTERNAL_EXPORT_DIR, INTERNAL_DATA_DIR, USER_MAPPING
        )
        
        if len(participants_data) < 2:
            _show_insufficient_data_message(console, dataset_stem)
            return
        
        dashboard_df = StatsForUI.generate_unified_dashboard_data(participants_data)
        _display_unified_dashboard_table(console, dashboard_df, dataset_stem)
        
        console.print()
        _display_inter_user_comparisons(console, participants_data)
        
    except Exception as e:
        _show_error_message(console, "Unified Dashboard", str(e))
    
    console.print()
    Prompt.ask("Press Enter to continue", default="")

# ===============================
# OPTION 3: DIRECT COMPARISON
# ===============================

def show_direct_comparison(console: Console):
    """Option 3: Head-to-head analysis between any 2 participants"""
    _clear_screen()
    console.print(Panel(
        "[bold blue]📊 Direct Ranking Comparison[/bold blue]\n"
        "[dim]Detailed head-to-head analysis between two participants[/dim]",
        border_style="blue"
    ))
    
    try:
        dataset_stem = _select_dataset(console)
        if not dataset_stem:
            return
        
        participants_data = StatsForUI.load_all_participants_data(
            dataset_stem, INTERNAL_EXPORT_DIR, INTERNAL_DATA_DIR, USER_MAPPING
        )
        
        if len(participants_data) < 2:
            _show_insufficient_data_message(console, dataset_stem)
            return
        
        participant1, participant2 = _select_two_participants(console, list(participants_data.keys()))
        if not participant1 or not participant2:
            return
        
        comparison_data = StatsForUI.compare_two_participants_detailed(
            participant1, participant2, participants_data
        )
        
        _display_detailed_comparison(console, comparison_data, dataset_stem)
        
    except Exception as e:
        _show_error_message(console, "Direct Comparison", str(e))
    
    console.print()
    Prompt.ask("Press Enter to continue", default="")

# ===============================
# DISPLAY FUNCTIONS
# ===============================

def _display_unified_dashboard_table(console: Console, dashboard_df, dataset_stem: str):
    """Display the unified dashboard table using clean formatting utilities"""
    
    dashboard_table = Table(
        title=f"📊 Unified Metrics Dashboard - Dataset: {dataset_stem}",
        show_header=True, 
        header_style="bold white"
    )
    
    dashboard_table.add_column("Participant", style="bold", width=12)
    dashboard_table.add_column("Kendall τ", justify="center", width=10)
    dashboard_table.add_column("Spearman ρ", justify="center", width=10)
    dashboard_table.add_column("K-Distance", justify="center", width=10)
    dashboard_table.add_column("Avg Rank Δ", justify="center", width=11)
    dashboard_table.add_column("Top-10", justify="center", width=8)
    dashboard_table.add_column("Top-20", justify="center", width=8)
    dashboard_table.add_column("Strength", justify="center", width=12)
    
    for _, row in dashboard_df.iterrows():
        participant_display = format_participant_name(row['Participant'], get_user_color)
        kendall_display = format_correlation(row['Kendall τ'])
        spearman_display = format_correlation(row['Spearman ρ'])
        distance_display = format_integer(row['Kendall Distance'])
        rank_diff_display = format_rank_diff(row['Avg Rank Diff'])
        top10_display = format_percentage(row['Top 10 Overlap'])
        top20_display = format_percentage(row['Top 20 Overlap'])
        strength_display = format_strength_display(row['Kendall τ'])
        
        dashboard_table.add_row(
            participant_display,
            kendall_display,
            spearman_display,
            distance_display,
            rank_diff_display,
            top10_display,
            top20_display,
            strength_display
        )
    
    console.print(dashboard_table)

def _display_inter_user_comparisons(console: Console, participants_data: Dict[str, List[str]]):
    """Display inter-user comparison matrix (human participants only)"""
    
    human_participants = [p for p in participants_data.keys() if p != 'Machine']
    
    if len(human_participants) < 2:
        return
    
    inter_table = Table(
        title="👥 Inter-User Agreement (Human vs Human)", 
        show_header=True, 
        header_style="bold white"
    )
    inter_table.add_column("User Pair", style="bold", width=20)
    inter_table.add_column("Kendall τ", justify="center", width=10)
    inter_table.add_column("Spearman ρ", justify="center", width=10)
    inter_table.add_column("Top-10 Overlap", justify="center", width=13)
    inter_table.add_column("Agreement", justify="center", width=12)
    
    for i, user1 in enumerate(human_participants):
        for j, user2 in enumerate(human_participants):
            if i < j:
                comparison = StatsForUI.compare_two_participants_detailed(user1, user2, participants_data)
                
                user1_display = format_participant_name(user1, get_user_color)
                user2_display = format_participant_name(user2, get_user_color)
                pair_display = f"{user1_display} vs {user2_display}"
                
                kendall_display = format_correlation(comparison['kendall_tau'])
                spearman_display = format_correlation(comparison['spearman_rho'])
                overlap_display = format_percentage(comparison['overlap_at_10'])
                agreement_display = format_strength_display(comparison['kendall_tau'])
                
                inter_table.add_row(
                    pair_display,
                    kendall_display,
                    spearman_display,
                    overlap_display,
                    agreement_display
                )
    
    console.print(inter_table)

def _display_correlation_matrix(console: Console, matrix_df, metric_name: str, color: str):
    """Display correlation matrix with clean formatting"""
    
    matrix_table = Table(
        title=f"{metric_name} Correlation Matrix", 
        show_header=True, 
        header_style=f"bold {color}"
    )
    
    matrix_table.add_column("", style="bold", width=12)
    
    for participant in matrix_df.columns:
        matrix_table.add_column(participant, justify="center", width=10)
    
    for idx, participant in enumerate(matrix_df.index):
        row_data = [participant]
        
        for col_participant in matrix_df.columns:
            value = matrix_df.loc[participant, col_participant]
            
            if idx == matrix_df.columns.get_loc(col_participant):
                row_data.append(f"[bright_green]1.000[/bright_green]")
            else:
                strength_color = get_strength_color(interpret_correlation_strength(value))
                formatted_value = format_correlation(value)
                row_data.append(f"[{strength_color}]{formatted_value}[/{strength_color}]")
        
        matrix_table.add_row(*row_data)
    
    console.print(matrix_table)

def _display_detailed_comparison(console: Console, comparison_data: Dict, dataset_stem: str):
    """Display detailed head-to-head comparison with clean formatting"""
    
    participant1 = comparison_data['participant1']
    participant2 = comparison_data['participant2']
    
    p1_display = format_participant_name(participant1, get_user_color)
    p2_display = format_participant_name(participant2, get_user_color)
    
    comparison_title = f"📊 Head-to-Head: {participant1} vs {participant2} (Dataset: {dataset_stem})"
    
    detail_table = Table(title=comparison_title, show_header=True, header_style="bold white")
    detail_table.add_column("Metric", style="bold", width=20)
    detail_table.add_column("Value", justify="center", width=15)
    detail_table.add_column("Interpretation", width=25)
    
    detail_table.add_row("Participants", f"{p1_display} vs {p2_display}", "Head-to-head comparison")
    detail_table.add_row("Common Items", format_integer(comparison_data['common_items']), "Texts ranked by both")
    detail_table.add_row("Kendall's τ", format_correlation(comparison_data['kendall_tau']), format_strength_display(comparison_data['kendall_tau']))
    detail_table.add_row("Spearman ρ", format_correlation(comparison_data['spearman_rho']), format_strength_display(comparison_data['spearman_rho']))
    detail_table.add_row("Kendall Distance", format_integer(comparison_data['kendall_distance']), "Pairwise disagreements")
    detail_table.add_row("Avg Rank Difference", format_rank_diff(comparison_data['avg_rank_diff']), "Average position difference")
    detail_table.add_row("Top-10 Overlap", format_percentage(comparison_data['overlap_at_10']), "Most negative agreement")
    detail_table.add_row("Top-20 Overlap", format_percentage(comparison_data['overlap_at_20']), "Extended agreement")
    
    console.print(detail_table)

# ===============================
# HELPER FUNCTIONS
# ===============================

def _select_dataset(console: Console) -> Optional[str]:
    """Dataset selection interface"""
    available_datasets = StatsForUI.get_available_datasets(INTERNAL_EXPORT_DIR, INTERNAL_DATA_DIR)
    
    if not available_datasets:
        console.print(Panel(
            "[red]No datasets found[/red]\n"
            "Complete some rankings first.",
            title="[red]No Data Available[/red]",
            border_style="red"
        ))
        Prompt.ask("Press Enter to continue", default="")
        return None
    
    dataset_panel = Panel(
        "\n".join([f"[bold white]{i+1}.[/bold white] [cyan]{dataset}[/cyan]" 
                  for i, dataset in enumerate(available_datasets)]),
        title="[bold cyan]Available Datasets[/bold cyan]",
        border_style="cyan"
    )
    console.print(dataset_panel)
    
    if len(available_datasets) == 1:
        console.print(f"[green]Auto-selecting: {available_datasets[0]}[/green]\n")
        return available_datasets[0]
    
    choice = Prompt.ask(
        f"Select dataset (1-{len(available_datasets)})", 
        choices=[str(i+1) for i in range(len(available_datasets))]
    )
    
    return available_datasets[int(choice) - 1]

def _select_two_participants(console: Console, participants: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Select two participants for direct comparison"""
    
    participant_panel = Panel(
        "\n".join([f"[bold white]{i+1}.[/bold white] [green]{p}[/green]" 
                  for i, p in enumerate(participants)]),
        title="[bold green]Available Participants[/bold green]",
        border_style="green"
    )
    console.print(participant_panel)
    
    choice1 = Prompt.ask(
        f"Select first participant (1-{len(participants)})",
        choices=[str(i+1) for i in range(len(participants))]
    )
    
    participant1 = participants[int(choice1) - 1]
    remaining_participants = [p for p in participants if p != participant1]
    
    console.print(f"[green]Selected: {participant1}[/green]\n")
    
    remaining_panel = Panel(
        "\n".join([f"[bold white]{i+1}.[/bold white] [blue]{p}[/blue]" 
                  for i, p in enumerate(remaining_participants)]),
        title="[bold blue]Select Second Participant[/bold blue]",
        border_style="blue"
    )
    console.print(remaining_panel)
    
    choice2 = Prompt.ask(
        f"Select second participant (1-{len(remaining_participants)})",
        choices=[str(i+1) for i in range(len(remaining_participants))]
    )
    
    participant2 = remaining_participants[int(choice2) - 1]
    
    return participant1, participant2

def _show_insufficient_data_message(console: Console, dataset_stem: str):
    """Show insufficient data message"""
    console.print(Panel(
        f"[yellow]Insufficient data for analysis[/yellow]\n\n"
        f"Dataset: [cyan]{dataset_stem}[/cyan]\n"
        f"Need at least 2 participants with completed rankings.",
        title="[yellow]Not Enough Data[/yellow]",
        border_style="yellow"
    ))
    Prompt.ask("Press Enter to continue", default="")

def _show_error_message(console: Console, operation: str, error: str):
    """Show user-friendly error message"""
    console.print(Panel(
        f"[red]Operation failed: {operation}[/red]\n\n"
        f"Error: {error}",
        title="[red]Analysis Error[/red]",
        border_style="red"
    ))

def _clear_screen():
    """Clear screen helper"""
    os.system('cls' if os.name == 'nt' else 'clear')

# src\text_ranking_tool\utils\formatters_ui.py
"""
Clean formatting utilities for analysis displays
All formatting logic centralized and pristine
"""

def format_correlation(value: float) -> str:
    """Format correlation to 3 decimal places"""
    if value is None:
        return "N/A"
    return f"{value:.3f}"

def format_percentage(value: float) -> str:
    """Format decimal as percentage"""
    if value is None:
        return "N/A"
    return f"{value:.0%}"

def format_rank_diff(value: float) -> str:
    """Format rank difference to 1 decimal"""
    if value is None:
        return "N/A"
    return f"{value:.1f}"

def format_integer(value: int) -> str:
    """Format integer value"""
    if value is None:
        return "N/A"
    return str(int(value))

def interpret_correlation_strength(correlation: float) -> str:
    """Return correlation strength label without markup"""
    if correlation is None:
        return "No Data"
    
    if correlation >= 0.8:
        return "Strong"
    elif correlation >= 0.6:
        return "Moderate"
    elif correlation >= 0.4:
        return "Weak"
    elif correlation >= 0.2:
        return "Very Weak"
    elif correlation >= -0.2:
        return "Minimal"
    else:
        return "Negative"

def get_strength_color(strength: str) -> str:
    """Map strength labels to Rich colors"""
    color_map = {
        'Perfect': 'bright_green',
        'Strong': 'green',
        'Moderate': 'yellow', 
        'Weak': 'red',
        'Very Weak': 'bright_red',
        'Minimal': 'dim',
        'Negative': 'bright_red',
        'No Data': 'dim'
    }
    return color_map.get(strength, 'white')

def format_participant_name(participant: str, get_user_color_func) -> str:
    """Format participant name with appropriate color"""
    if participant == 'Machine':
        return f"[bright_blue]{participant}[/bright_blue]"
    else:
        user_color = get_user_color_func(participant)
        return f"[{user_color}]{participant}[/{user_color}]"

def format_strength_display(correlation: float) -> str:
    """Format correlation strength with color coding"""
    strength = interpret_correlation_strength(correlation)
    strength_color = get_strength_color(strength)
    return f"[{strength_color}]{strength}[/{strength_color}]"

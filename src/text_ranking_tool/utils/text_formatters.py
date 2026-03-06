# src/text_ranking_tool/utils/text_formatters.py

import re
from typing import Optional, List
from rich.text import Text

from ..config.constants import TEXT_FORMATTING_RULE, resolve_path

def _load_patterns_file(path_str: str) -> Optional[List[str]]:
    """Load raw patterns from .txt — one per line, optional trailing *."""
    try:
        file_path = resolve_path(path_str)
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            patterns = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]
        if not patterns:
            print(f"Warning: Patterns file is empty: {file_path}")
            return None
        return patterns
    except FileNotFoundError:
        print(f"Error: Patterns file not found: {path_str}")
        return None
    except Exception as e:
        print(f"Error loading patterns file: {e}")
        return None


def _stylize_matches(text_obj: Text, patterns: Optional[List[str]], style: str) -> Text:
    """Core engine: compile wildcard patterns, apply Rich style to all matches.
    Case-sensitive, handles multi-word phrases correctly."""
    if not patterns:
        return text_obj
    
    raw = text_obj.plain
    for stem in patterns:
        if stem.endswith('*'):
            prefix = stem[:-1]
            if ' ' in prefix:
                # Multi-word phrase with wildcard on last word only
                words = prefix.rsplit(' ', 1)  # Split on last space
                fixed_prefix = words[0]
                last_word_prefix = words[1]
                # Match: \b fixed_prefix last_word_prefix\w*
                pat_str = rf'\b{re.escape(fixed_prefix)}\s+{re.escape(last_word_prefix)}\w*'
            else:
                # Single word wildcard
                pat_str = rf'\b{re.escape(prefix)}\w*'
        else:
            # Exact phrase match
            pat_str = rf'\b{re.escape(stem)}\b'
        
        pat = re.compile(pat_str)
        for match in pat.finditer(raw):
            text_obj.stylize(style, match.start(), match.end())
    
    return text_obj



def _apply_strike(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "strike")

def _apply_bold(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "bold")

def _apply_highlight(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "reverse")

def _apply_dim(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "dim")

def _apply_underline(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "underline")

def _apply_italic(text_obj: Text, patterns: List[str]) -> Text:
    return _stylize_matches(text_obj, patterns, "italic")


_FORMATTERS = {
    "strike":     _apply_strike,
    "bold":       _apply_bold,
    "highlight":  _apply_highlight,
    "dim":        _apply_dim,
    "underline":  _apply_underline,
    "italic":     _apply_italic,
}


def format_text(raw_text: str) -> Text:
    """
    Apply the configured formatting rule to raw text.
    Returns a plain Rich Text object if formatting is disabled,
    not configured, or if the patterns file fails to load.
    """
    if TEXT_FORMATTING_RULE is None:
        return Text(raw_text)

    formatter_type = TEXT_FORMATTING_RULE.get("type")
    patterns_file  = TEXT_FORMATTING_RULE.get("patterns_file")

    if formatter_type not in _FORMATTERS:
        print(f"Warning: Unknown text formatter type '{formatter_type}' — skipping formatting.")
        return Text(raw_text)

    patterns = _load_patterns_file(patterns_file) if patterns_file else None
    if not patterns:
        return Text(raw_text)

    return _FORMATTERS[formatter_type](Text(raw_text), patterns)

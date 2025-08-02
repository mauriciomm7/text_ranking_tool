# src\text_ranking_tool\utils\startup_helpers.py
"""
Startup and completion helper functions
Clean utilities for main application workflow
"""


def auto_export_completed_ranking(username: str, file_stem: str, final_ranking: list, text_data: list): 
    """Automatically export ranking (internal only)"""
    try:
        # Internal export (for admin analysis)
        from ..export.formatters import export_user_ranking_internal
        internal_result = export_user_ranking_internal(username, file_stem, final_ranking, text_data)
        print(f"✓ Internal ranking saved: {internal_result['total_records']} texts")
        
    except Exception as e:
        print(f"⚠ Auto-export failed: {e}")



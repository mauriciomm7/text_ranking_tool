# src/text_ranking_tool/data/file_scanner.py

from typing import List, Dict, Any
from ..config.constants import INTERNAL_DATA_DIR

def scan_data_directory() -> List[Dict[str, Any]]:
    """
    Scan DATA_DIR for CSV files and return file information.
    Returns list of file info dictionaries.
    """
    
    try:
        # Ensure data directory exists
        if not INTERNAL_DATA_DIR.exists():
            return []
        
        # Find all CSV files
        csv_files = list(INTERNAL_DATA_DIR.glob("*.csv"))
        
        if not csv_files:
            return []
        
        # Build file information list
        file_info_list = []
        for csv_file in csv_files:
            file_info = {
                "filename": csv_file.name,
                "stem": csv_file.stem,  # filename without .csv extension
                "path": csv_file,
                "size_bytes": csv_file.stat().st_size if csv_file.exists() else 0
            }
            file_info_list.append(file_info)
        
        # Sort by filename for consistent display
        file_info_list.sort(key=lambda x: x["filename"])
        
        return file_info_list
        
    except Exception as e:
        print(f"Error scanning data directory: {e}")
        return []

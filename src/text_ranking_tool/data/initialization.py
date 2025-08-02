# src/text_ranking_tool/data/initialization.py
# type: ignore
import shutil
from ..config.constants import (
    EXTERNAL_DATA_DIR, 
    INTERNAL_DATA_DIR,  
    INTERNAL_EXPORT_DIR, 
    INTERNAL_USERS_DIR
)

def initialize_data_directories():
    """Create internal directories and mirror external data"""
    
    # Create internal directories
    INTERNAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    INTERNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    INTERNAL_USERS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Mirror CSV files from external to internal
    if EXTERNAL_DATA_DIR.exists():
        for csv_file in EXTERNAL_DATA_DIR.glob("*.csv"):
            shutil.copy2(csv_file, INTERNAL_DATA_DIR / csv_file.name)

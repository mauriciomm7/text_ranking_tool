from typing import List, Dict, Any
from .schema import REQUIRED_COLUMNS

def validate_input_data(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate input data for transitive quick algorithm"""
    
    if not data:
        return {"valid": False, "error": "No data provided"}
    
    # Check required columns exist
    first_row = data[0]
    missing_cols = [col for col in ["id", "valence", "ranking", "text"] if col not in first_row]
    
    if missing_cols:
        return {"valid": False, "error": f"Missing columns: {missing_cols}"}
    
    # Transitive quick needs at least 2 items to compare
    if len(data) < 2:
        return {"valid": False, "error": "Transitive quick needs at least 2 texts"}
    
    # Validate valence scores are numeric (needed for smart anchors)
    try:
        for item in data[:3]:  # Check first few items
            if 'valence' in item and item['valence'] is not None:
                float(item['valence'])
    except (ValueError, TypeError):
        return {"valid": False, "warning": "Non-numeric valence scores detected - will use random anchors"}
    
    return {"valid": True}

def validate_export_data(rankings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate export data has required columns"""
    
    if not rankings:
        return {"valid": False, "error": "No ranking data to export"}
    
    # Check required columns for export
    first_row = rankings[0]
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in first_row]
    
    if missing_cols:
        return {"valid": False, "error": f"Export missing columns: {missing_cols}"}
    
    return {"valid": True}

# src/text_ranking_tool/data/csv_loader.py

import csv
from typing import List, Dict, Any, Optional
from ..config.constants import REQUIRED_COLUMNS

def load_ranking_data(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """
    Load ranking data from CSV file.
    Expects file to have columns: id, valence, ranking, text
    """
    try:
        text_data = [] 
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate required columns exist
            if not reader.fieldnames or not all(col in reader.fieldnames for col in REQUIRED_COLUMNS):
                print(f"Error: CSV file missing required columns: {REQUIRED_COLUMNS}")
                return None
            
            # Load data rows
            for row in reader:
                text_item = {
                    'id': row['id'].strip(),
                    'valence': row['valence'].strip(),
                    'ranking': row['ranking'].strip(), 
                    'text': row['text'].strip()
                }
                text_data.append(text_item)
        
        return text_data if text_data else None
        
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

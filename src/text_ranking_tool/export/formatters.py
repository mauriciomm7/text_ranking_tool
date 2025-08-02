#src\text_ranking_tool\export\formatters.py

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Iterator, Tuple, Optional
from ..config.constants import (EXTERNAL_EXPORT_DIR, INTERNAL_EXPORT_DIR, CONFIGURED_ALGORITHM, get_user_id)
from ..ranking.session_manager import get_session_manager
from ..data.file_scanner import scan_data_directory
from ..data.csv_loader import load_ranking_data

class RankingExporter:
    """Handles exporting user ranking data in several formats - adapted for comparison engine sessions"""
    
    def __init__(self):
        self.session_manager = get_session_manager()
        self.algorithm = CONFIGURED_ALGORITHM
        
        # Ensure export directories exist
        EXTERNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        INTERNAL_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_timestamp(self) -> str:
        """Return the export timestamp string"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _get_available_files_data(self) -> Dict[str, Optional[Dict[str, Any]]]:
        """Get all available CSV files and their text data"""
        available_files = scan_data_directory()
        files_data = {}
        
        for file_info in available_files:
            file_stem = file_info["stem"]
            try:
                # Load text data for this file
                text_data = load_ranking_data(str(file_info["path"]))
                if text_data:
                    # Convert to lookup dict by ID
                    files_data[file_stem] = {item['id']: item for item in text_data}
                else:
                    files_data[file_stem] = None
            except Exception:
                files_data[file_stem] = None
        
        return files_data
    
    def _get_user_ranking_from_session(self, username: str, file_stem: str) -> Optional[List[str]]:
        """Get user's final ranking from their internal export CSV"""
        try:
            user_id = get_user_id(username)
            
            # Look for the most recent internal export CSV for this user/file
            pattern = f"{user_id}_{file_stem}_{self.algorithm}_*.csv"
            matching_files = list(INTERNAL_EXPORT_DIR.glob(pattern))
            
            if not matching_files:
                return None
            
            # Get the most recent file (by filename which includes timestamp)
            latest_file = max(matching_files, key=lambda f: f.name)
            
            # Read the CSV and extract the ranking order
            ranking = []
            with open(latest_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ranking.append(row['id'])
            
            return ranking if ranking else None
            
        except Exception:
            return None
    
    def _yield_ranking_records(
        self, 
        files_data: Dict[str, Optional[Dict[str, Any]]], 
        usernames: List[str],
        with_text: bool = False
    ) -> Iterator[Tuple[str, Dict[str, Any]]]:
        """Yield (file_stem, record_dict) for all file/user combinations with ranking data"""
        
        for file_stem, text_data in files_data.items():
            if not text_data:
                continue
                
            for username in usernames:
                # Get user's ranking for this file
                user_ranking = self._get_user_ranking_from_session(username, file_stem)
                if not user_ranking:
                    continue
                
                # Create records for each ranked text
                for rank_position, text_id in enumerate(user_ranking, 1):
                    if text_id not in text_data:
                        continue
                    
                    text_info = text_data[text_id]
                    record = {
                        'file_name': file_stem,
                        'id': text_id,
                        'valence': text_info.get('valence', ''),
                        'ranking': text_info.get('ranking', ''),
                        'new_ranking': rank_position,
                        'algorithm': self.algorithm,
                        'user_name': username
                    }
                    
                    if with_text:
                        record['text'] = text_info.get('text', '')
                    
                    yield file_stem, record
    
    def _write_records_to_csv(self, path: Path, fieldnames: List[str], records: List[Dict[str, Any]]):
        """Write the given records to CSV at the given path with error handling"""
        try:
            with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(records)
        except (IOError, OSError) as e:
            raise RuntimeError(f"Failed to write CSV file {path}: {e}")
    
    def export_per_user_internal(self, username: str, file_stem: str, final_ranking: List[str], text_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Export single user's ranking to internal directory (automatic after algorithm completion)"""
        timestamp = self._get_timestamp()
        user_id = get_user_id(username)
        output_path = INTERNAL_EXPORT_DIR / f"{user_id}_{file_stem}_{self.algorithm}_{timestamp}.csv"
        
        # Create text lookup
        text_lookup = {item['id']: item for item in text_data}
        
        # Build records for this user's ranking
        records = []
        for rank_position, text_id in enumerate(final_ranking, 1):
            if text_id in text_lookup:
                text_info = text_lookup[text_id]
                record = {
                    'user_name': username,
                    'file_name': file_stem,
                    'algorithm': self.algorithm,
                    'id': text_id,
                    'valence': text_info.get('valence', ''),
                    'ranking': text_info.get('ranking', ''),
                    'new_ranking': rank_position,
                    'text': text_info.get('text', '')
                }
                records.append(record)
        
        # Write to internal directory
        fieldnames = ['user_name', 'file_name', 'algorithm', 'id', 'valence', 'ranking', 'new_ranking', 'text']
        self._write_records_to_csv(output_path, fieldnames, records)
        
        return {
            'file': str(output_path),
            'total_records': len(records),
            'export_type': 'per_user_internal'
        }
    
    def export_per_user_external(self, usernames: List[str]) -> Dict[str, Any]:
        """Export all rankings for each user into separate CSV files (external directory)"""
        timestamp = self._get_timestamp()
        files_data = self._get_available_files_data()
        fieldnames = ['user_name', 'file_name', 'algorithm', 'id', 'valence', 'ranking', 'new_ranking', 'text']
        created_files = []
        total_records = 0
        
        # Group records by username
        user_records_map: Dict[str, List[Dict[str, Any]]] = {username: [] for username in usernames}
        for _, record in self._yield_ranking_records(files_data, usernames, with_text=True):
            user_records_map[record['user_name']].append(record)
        
        # Write a file for each user
        for username, user_records in user_records_map.items():
            if user_records:
                user_id = get_user_id(username)
                output_path = EXTERNAL_EXPORT_DIR / f"{user_id}_data_{timestamp}.csv"
                self._write_records_to_csv(output_path, fieldnames, user_records)
                created_files.append(str(output_path))
                total_records += len(user_records)
        
        return {
            'files': created_files,
            'total_records': total_records,
            'export_type': 'per_user_external'
        }
    
    def export_per_file_external(self, usernames: List[str]) -> Dict[str, Any]:
        """Export rankings for each file (all users) as separate CSV files (external directory)"""
        timestamp = self._get_timestamp()
        files_data = self._get_available_files_data()
        fieldnames = ['file_name', 'id', 'valence', 'ranking', 'new_ranking', 'algorithm', 'user_name', 'text']
        created_files = []
        total_records = 0
        
        # Group records by file
        file_records_map: Dict[str, List[Dict[str, Any]]] = {}
        for file_stem, record in self._yield_ranking_records(files_data, usernames, with_text=True):
            file_records_map.setdefault(file_stem, []).append(record)
        
        # Write a file for each dataset
        for file_stem, file_records in file_records_map.items():
            if file_records:
                output_path = EXTERNAL_EXPORT_DIR / f"{file_stem}_all_users_data_{timestamp}.csv"
                self._write_records_to_csv(output_path, fieldnames, file_records)
                created_files.append(str(output_path))
                total_records += len(file_records)
        
        return {
            'files': created_files,
            'total_records': total_records,
            'export_type': 'per_file_external'
        }
    
    def export_overall_project_external(self, usernames: List[str]) -> Dict[str, Any]:
        """Export all available rankings to a single CSV (external directory)"""
        timestamp = self._get_timestamp()
        output_path = EXTERNAL_EXPORT_DIR / f"overall_project_data_{timestamp}.csv"
        files_data = self._get_available_files_data()
        
        # Collect all records
        records = [record for _, record in self._yield_ranking_records(files_data, usernames, with_text=False)]
        fieldnames = ['file_name', 'id', 'valence', 'ranking', 'new_ranking', 'algorithm', 'user_name']
        
        if records:
            self._write_records_to_csv(output_path, fieldnames, records)
        
        return {
            'files': [str(output_path)],
            'total_records': len(records),
            'export_type': 'overall_project_external'
        }

# Global instance
_ranking_exporter_instance: Optional[RankingExporter] = None

def get_ranking_exporter() -> RankingExporter:
    """Get global ranking exporter instance"""
    global _ranking_exporter_instance
    if _ranking_exporter_instance is None:
        _ranking_exporter_instance = RankingExporter()
    return _ranking_exporter_instance

def export_user_ranking_internal(username: str, file_stem: str, final_ranking: List[str], text_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convenience function for automatic internal export after algorithm completion"""
    exporter = get_ranking_exporter()
    return exporter.export_per_user_internal(username, file_stem, final_ranking, text_data)

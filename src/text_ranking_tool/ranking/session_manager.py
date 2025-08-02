# src/text_ranking_tool/ranking/session_manager.py

import json
from datetime import datetime
from pathlib import Path
from ..config.constants import INTERNAL_USERS_DIR, CONFIGURED_ALGORITHM, get_user_id
from typing import Dict, Tuple, Optional, List, Any


class SessionManager:
    """Manages multi-user session persistence with comparison memory"""
    
    def __init__(self):
        self.users_dir = INTERNAL_USERS_DIR
    
    def get_session_path(self, username: str, data_file_stem: str) -> Path:
        """Get session file path for user/file combination"""
        user_id = get_user_id(username)
        return self.users_dir / user_id / f"{data_file_stem}.json"  # ✅ Simplified consistent path
    
    def save_session(self, username: str, 
                     data_file_stem: str, 
                     comparison_memory: Dict[Tuple[str, str], bool], 
                     comparison_order: List[Tuple[str, str]] = None): # type: ignore
        """Save user session with comparison memory AND undo history"""
        
        session_file = self.get_session_path(username, data_file_stem)  # ✅ Use consistent path method
        
        # Ensure user directory exists
        session_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert tuples to serializable strings for comparison_memory
        serializable_memory = {}
        for (text1, text2), result in comparison_memory.items():
            key_str = f"{text1}||{text2}"
            serializable_memory[key_str] = result
        
        # Convert tuples to serializable strings for comparison_order
        serializable_order = []
        if comparison_order:
            for text1, text2 in comparison_order:
                serializable_order.append(f"{text1}||{text2}")
        
        # Save session data with undo history
        session_data = {
            'comparison_memory': serializable_memory,
            'comparison_order': serializable_order,
            'timestamp': datetime.now().isoformat(),
            'username': username,
            'data_file': data_file_stem,
            'algorithm': CONFIGURED_ALGORITHM,  # ✅ Added algorithm field
            'comparisons_count': len(comparison_memory)
        }
        
        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load_session(self, username: str, data_file_stem: str) -> Tuple[Dict[Tuple[str, str], bool], List[Tuple[str, str]]]:
        """Load user session and return both comparison memory AND undo history"""
        
        session_file = self.get_session_path(username, data_file_stem)  # ✅ Use consistent path method
        
        if not session_file.exists():
            return {}, []  # Return empty memory and empty order
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Convert back to tuples for comparison_memory
            comparison_memory = {}
            for key_str, result in session_data.get('comparison_memory', {}).items():
                try:
                    text1, text2 = key_str.split('||')
                    comparison_memory[(text1, text2)] = result
                except ValueError:
                    continue
            
            # Convert back to tuples for comparison_order
            comparison_order = []
            for key_str in session_data.get('comparison_order', []):
                try:
                    text1, text2 = key_str.split('||')
                    comparison_order.append((text1, text2))
                except ValueError:
                    continue
            
            return comparison_memory, comparison_order
            
        except Exception as e:
            print(f"Error loading session: {e}")
            return {}, []

    def delete_session(self, username: str, data_file_stem: str) -> bool:
        """Delete session file (for F4 reset)"""
        session_path = self.get_session_path(username, data_file_stem)
        
        try:
            if session_path.exists():
                session_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def has_session(self, username: str, data_file_stem: str) -> bool:
        """Check if session exists for user/file"""
        return self.get_session_path(username, data_file_stem).exists()
    
    def get_session_progress(self, username: str, data_file_stem: str) -> Dict[str, Any]:
        """Get session progress information for UI display"""
        session_path = self.get_session_path(username, data_file_stem)
        
        if not session_path.exists():
            return {
                "exists": False,
                "comparisons_made": 0,
                "last_updated": None
            }
        
        try:
            with open(session_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            return {
                "exists": True,
                "comparisons_made": session_data.get('comparisons_count', 0),  # ✅ Fixed field name
                "last_updated": session_data.get('timestamp'),
                "algorithm": session_data.get('algorithm', CONFIGURED_ALGORITHM)
            }
            
        except Exception:
            return {
                "exists": False,
                "comparisons_made": 0,
                "last_updated": None
            }
    
    def list_user_sessions(self, username: str) -> List[Dict[str, Any]]:
        """List all sessions for a user with progress info"""
        user_id = get_user_id(username)
        user_dir = self.users_dir / user_id
        
        if not user_dir.exists():
            return []
        
        sessions = []
        for session_file in user_dir.glob("*.json"):  # ✅ Updated glob pattern for new naming
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                sessions.append({
                    'filename': session_file.name,
                    'data_file': session_data.get('data_file', 'unknown'),
                    'algorithm': session_data.get('algorithm', 'unknown'),
                    'timestamp': session_data.get('timestamp', 'unknown'),
                    'comparisons_made': session_data.get('comparisons_count', 0)  # ✅ Fixed field name
                })
            except Exception:
                # Skip corrupted session files
                continue
        
        return sessions

# Global instance
_session_manager_instance: Optional[SessionManager] = None

def get_session_manager() -> SessionManager:
    """Get global session manager instance"""
    global _session_manager_instance
    if _session_manager_instance is None:
        _session_manager_instance = SessionManager()
    return _session_manager_instance

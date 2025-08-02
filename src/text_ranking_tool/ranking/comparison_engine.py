# src/text_ranking_tool/ranking/comparison_engine.py

from typing import Dict, Any, List, Optional, Tuple

from .session_manager import get_session_manager
from ..config.constants import CONFIGURED_ALGORITHM

class ComparisonEngine:
    """Intelligent comparison engine with multi-user session management"""
    
    def __init__(self):
        self.text_data: Dict[str, Dict[str, Any]] = {}
        self.current_user: Optional[str] = None
        self.current_file: Optional[str] = None
        self.comparison_memory: Dict[Tuple[str, str], bool] = {}
        self.comparison_order: List[Tuple[str, str]] = [] 
        self.session_manager = get_session_manager()
    
    def initialize_session(self, text_data: List[Dict[str, Any]], username: str, data_file_stem: str):
        """Initialize comparison engine for specific user and file"""
        
        # Store text data for comparisons
        self.text_data = {item['id']: item for item in text_data}
        self.current_user = username
        self.current_file = data_file_stem
        
        # Load existing comparison memory AND undo history
        existing_memory, existing_order = self.session_manager.load_session(username, data_file_stem)
        self.comparison_memory = existing_memory if existing_memory else {}
        self.comparison_order = existing_order if existing_order else [] 
        
        print(f"Initialized session for {username} on {data_file_stem}")
        if existing_memory:
            print(f"Loaded {len(existing_memory)} previous comparisons")
            if existing_order:
                print(f"Restored {len(existing_order)} undo history entries")

    
    def ask_if_more_negative(self, text_id_1: str, text_id_2: str) -> bool:
        """
        Core method: Check cache first, then delegate to UI if needed
        Returns True if text_id_1 is more negative than text_id_2
        """
        
        # Check comparison memory first - HUGE efficiency gain
        comparison_key = (text_id_1, text_id_2)
        reverse_key = (text_id_2, text_id_1)
        
        # If we've compared these texts before, return cached result
        if comparison_key in self.comparison_memory:
            return self.comparison_memory[comparison_key]
        
        # Check reverse comparison (text2 vs text1)
        if reverse_key in self.comparison_memory:
            # If text2 was more negative than text1, then text1 is NOT more negative than text2
            return not self.comparison_memory[reverse_key]
        
        # Loop to handle undo functionality
        while True:
            # New comparison needed - prepare data for algorithm-specific UI
            comparison_data = self._get_comparison_data(text_id_1, text_id_2)
            
            # Delegate to algorithm-specific UI
            winner_id = self._get_user_comparison_choice(comparison_data)
            
            # Handle undo response
            if winner_id == "UNDO":
                if self.undo_last_comparison():
                    continue  # Ask the same comparison again
                else:
                    continue  # Nothing to undo, ask again
            
            # Normal comparison result
            # Determine result: True if text_id_1 won (is more negative)
            result = (winner_id == text_id_1)
            
            # Cache result for future efficiency
            self._cache_comparison_result(text_id_1, text_id_2, result)
            
            return result

    def undo_last_comparison(self) -> bool:
        """Delete last comparison as if it never happened"""
        if not self.comparison_order:
            return False
        
        # Get last comparison and delete it
        last_comparison = self.comparison_order.pop()
        if last_comparison in self.comparison_memory:
            del self.comparison_memory[last_comparison]
        
        # Save updated session WITH updated undo history
        if self.current_user and self.current_file:
            self.session_manager.save_session(
                self.current_user, 
                self.current_file, 
                self.comparison_memory,
                self.comparison_order
            )
        return True

    
    def get_progress_info(self) -> Dict[str, Any]:
        """Get current session progress"""
        return {
            "user": self.current_user,
            "file": self.current_file,
            "comparisons_made": len(self.comparison_memory),
            "total_texts": len(self.text_data)
        }
    
    def reset_session(self) -> bool:
        """Reset current session (F4 functionality)"""
        if not self.current_user or not self.current_file:
            return False
        
        success = self.session_manager.delete_session(self.current_user, self.current_file)
        if success:
            self.comparison_memory = {}
            print(f"Reset session for {self.current_user} on {self.current_file}")
        return success
    
    # Private helper methods
    def _get_comparison_data(self, text_id_1: str, text_id_2: str) -> Dict[str, Any]:
        """Prepare data for algorithm-specific UI"""
        
        text1_data = self.text_data.get(text_id_1, {})
        text2_data = self.text_data.get(text_id_2, {})
        
        return {
            "text1": {
                "id": text_id_1,
                "text": text1_data.get('text', f'Text {text_id_1}'),
                "valence": text1_data.get('valence', 0),
                "ranking": text1_data.get('ranking', 0)
            },
            "text2": {
                "id": text_id_2,
                "text": text2_data.get('text', f'Text {text_id_2}'),
                "valence": text2_data.get('valence', 0),
                "ranking": text2_data.get('ranking', 0)
            },
            "comparison_number": len(self.comparison_memory) + 1,
            "algorithm": CONFIGURED_ALGORITHM
        }
    
    def _get_user_comparison_choice(self, comparison_data: Dict[str, Any]) -> str:
        """Delegate to algorithm-specific UI"""
        
        # Import here to avoid circular imports
        if CONFIGURED_ALGORITHM == "tournament":
            from ..ux.comparison_ui import get_tournament_comparison_choice
            return get_tournament_comparison_choice(comparison_data)
        elif CONFIGURED_ALGORITHM == "recursive_median":
            from ..ux.comparison_ui import get_recursive_median_comparison_choice
            return get_recursive_median_comparison_choice(comparison_data)
        else:
            # Fallback to generic UI
            from ..ux.comparison_ui import get_generic_comparison_choice
            return get_generic_comparison_choice(comparison_data)
    
    def _cache_comparison_result(self, text_id_1: str, text_id_2: str, result: bool):
        """Cache comparison result and save to session"""
        # Store in memory
        self.comparison_memory[(text_id_1, text_id_2)] = result
        # Track order for undo functionality
        self.comparison_order.append((text_id_1, text_id_2))
        # Persist to disk WITH undo history
        if self.current_user and self.current_file:
            self.session_manager.save_session(
                self.current_user, 
                self.current_file, 
                self.comparison_memory,
                self.comparison_order
                )
            
# Global instance management
_comparison_engine_instance: Optional[ComparisonEngine] = None

def get_comparison_engine() -> ComparisonEngine:
    """Get global comparison engine instance"""
    global _comparison_engine_instance
    if _comparison_engine_instance is None:
        _comparison_engine_instance = ComparisonEngine()
    return _comparison_engine_instance

def initialize_comparison_engine(text_data: List[Dict[str, Any]], username: str, data_file_stem: str) -> ComparisonEngine:
    """Initialize comparison engine for specific user/file session"""
    engine = get_comparison_engine()
    engine.initialize_session(text_data, username, data_file_stem)
    return engine

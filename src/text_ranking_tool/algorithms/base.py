# src/text_ranking_tool/algorithms/base.py

from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from ..ranking.comparison_engine import ComparisonEngine

class SortingAlgorithm(ABC):
    """Base class for all sorting algorithms"""
    
    def __init__(self, name: str, description: str, algorithm_id: str, schema_key: str):
        self.NAME = name
        self.description = description
        self.algorithm_id = algorithm_id
        self.schema_key = schema_key
        self.comparison_count = 0
        self.comparison_engine: Optional[ComparisonEngine] = None
    
    @abstractmethod
    def initialize_from_data(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """Initialize algorithm with data - must be implemented by subclasses"""
        pass 
    
    @abstractmethod
    def sort(self, ids: List[str], **kwargs) -> List[str]:
        """Sort the text IDs - must be implemented by subclasses"""
        pass
    
    def reset_counters(self):
        """Reset comparison counters"""
        self.comparison_count = 0

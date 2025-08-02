# src/text_ranking_tool/algorithms/registry.py
# type: ignore

from typing import Dict, Type, Any
from .base import SortingAlgorithm


class AlgorithmRegistry:
    """Simple registry for auto-discovering ranking algorithms"""
    def __init__(self):
        self._algorithms: Dict[str, Type[SortingAlgorithm]] = {}
    
    def register(self, algorithm_class: Type[SortingAlgorithm]):
        """Decorator for auto-registering algorithm classes"""
        self._algorithms[algorithm_class().algorithm_id] = algorithm_class
        return algorithm_class
    
    def get_algorithm(self, algorithm_id: str) -> Type[SortingAlgorithm]:
        """Get algorithm class by ID"""
        if algorithm_id not in self._algorithms:
            raise ValueError(f"Algorithm '{algorithm_id}' not found")
        return self._algorithms[algorithm_id]
    
    def list_algorithms(self) -> Dict[str, Dict[str, Any]]:
        """List all registered algorithms with metadata"""
        algorithms = {}
        for algo_id, algo_class in self._algorithms.items():
            instance = algo_class()
            algorithms[algo_id] = {
                "name": instance.name,
                "description": instance.description,
                "algorithm_id": instance.algorithm_id
            }
        return algorithms
    
    def create_algorithm(self, algorithm_id: str) -> SortingAlgorithm:
        """Create new instance of algorithm"""
        algorithm_class = self.get_algorithm(algorithm_id)
        return algorithm_class()

# Global registry instance
algorithm_registry = AlgorithmRegistry()

def discover_algorithms():
    """Import all algorithm modules to trigger registration"""
    try:
        from .tournament.tournament_core import TournamentSort
        from .recursive_median.recursive_median_core import RecursiveMedianSort

        # from .pairwise.pairwise import PairwiseSort
        # from .merge_sort.merge_sort import MergeSortSort  

    except ImportError as e:
        print(f"Warning: Could not import algorithm: {e}")

# Auto-discover on import
discover_algorithms()

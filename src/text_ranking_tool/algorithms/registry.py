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
        # Using the class attribute directly avoids creating an instance here
        self._algorithms[algorithm_class.ALGORITHM_ID] = algorithm_class
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
            # Using class attributes directly for efficiency
            algorithms[algo_id] = {
                "name": algo_class.NAME,
                "description": algo_class.DESCRIPTION,
                "algorithm_id": algo_class.ALGORITHM_ID
            }
        return algorithms
    
    def create_algorithm(self, algorithm_id: str) -> SortingAlgorithm:
        """Create new instance of algorithm"""
        algorithm_class = self.get_algorithm(algorithm_id)
        return algorithm_class()

# Global registry instance
algorithm_registry = AlgorithmRegistry()

# THE DISCOVERY LOGIC HAS BEEN REMOVED FROM THIS FILE

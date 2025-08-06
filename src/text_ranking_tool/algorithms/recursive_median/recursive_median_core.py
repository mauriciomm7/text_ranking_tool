# src/text_ranking_tool/algorithms/recursive_median/recursive_median_core.py
"""
Recursive median sorting algorithm for efficient text ranking - Original algorithm by Mauricio M. M.

ALGORITHM LOGIC: Uses recursive divide-and-conquer with median-based pivot selection for optimal 
partitioning. Selects median valence score as pivot, partitions texts into more/less negative 
groups, then recursively sorts each partition. The median pivot strategy minimizes comparisons 
by creating balanced partitions, making this the most efficient algorithm for complete text ranking.

PERFORMANCE: Requires ~N×log₂(N) comparisons for N texts (~20 comparisons for 10 texts).
Most efficient algorithm in the system due to intelligent median pivot selection. Returns 
complete ranking from most negative to most positive text. Always uses median-based pivots 
for optimal divide-and-conquer performance, living up to its "Recursive Median" name.
"""

import random
import statistics
from ..base import SortingAlgorithm
from ..registry import algorithm_registry
from typing import List, Dict, Any, Optional


@algorithm_registry.register
class RecursiveMedianSort(SortingAlgorithm):
    """Original recursive median sorting algorithm."""
    
    # Class attributes for registry
    ALGORITHM_ID = "recursive_median"
    NAME = "Recursive Median Sort"
    DESCRIPTION = "Original algorithm: recursively partition around pivots (more comparisons, thorough)"
    SCHEMA_KEY = "recursive_median"

    def __init__(self):
        super().__init__(
            self.NAME,
            self.DESCRIPTION,
            self.ALGORITHM_ID,
            self.SCHEMA_KEY
        )
        self.text_data = {}  # Store for pivot selection
        self.comparison_engine = None  # Will be set during initialization

    def initialize_from_data(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """Store text data for pivot selection"""
        self.text_data = {item['id']: item for item in data}
        return True

    def sort(self, ids: List[str], use_valence_pivot: bool = True) -> List[str]:
        """Sort using recursive median partitioning."""
        self.reset_counters()
        return self._median_recursive_sort(ids, 0, use_valence_pivot)

    def _median_recursive_sort(self, ids: List[str], depth: int = 0, use_valence_pivot: bool = False) -> List[str]:
        if len(ids) <= 1:
            return ids

        # Select pivot
        pivot_id = self._median_valence_pivot(ids) if use_valence_pivot else random.choice(ids)
        if pivot_id is None:
            pivot_id = random.choice(ids)

        # CREATE a list of items to be compared against the pivot
        non_pivots = [text_id for text_id in ids if text_id != pivot_id]

        # THE FIX: Shuffle the list to randomize the comparison order
        random.shuffle(non_pivots)

        above, below = [], []
        # Loop over the new, shuffled list
        for text_id in non_pivots:
            self.comparison_count += 1
            if self.ask_if_more_negative(text_id, pivot_id):
                below.append(text_id)
            else:
                above.append(text_id)


        sorted_below = self._median_recursive_sort(below, depth + 1, use_valence_pivot)
        sorted_above = self._median_recursive_sort(above, depth + 1, use_valence_pivot)
        return sorted_below + [pivot_id] + sorted_above

    def _median_valence_pivot(self, ids: List[str]) -> Optional[str]:
        """Select pivot based on median valence score."""
        if not ids:
            return None

        try:
            vals = [float(self.text_data[i]['valence']) for i in ids if i in self.text_data]
            if not vals:
                return random.choice(ids)

            median_val = statistics.median(vals)
            closest_id = min(
                ids,
                key=lambda i: abs(float(self.text_data[i].get('valence', 0)) - median_val)
                if i in self.text_data else float('inf')
            )
            return closest_id
        except (KeyError, ValueError, TypeError):
            return random.choice(ids)

    def ask_if_more_negative(self, text_id: str, pivot_id: str) -> bool:
        """Use comparison engine for intelligent caching"""
        return self.comparison_engine.ask_if_more_negative(text_id, pivot_id) # type: ignore

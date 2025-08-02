# src/text_ranking_tool/algorithms/tournament/tournament_core.py
"""
Tournament bracket sorting algorithm for complete text ranking.

ALGORITHM LOGIC: Runs multiple single-elimination tournaments to build complete rankings.
Tournament 1 finds most negative text from all items, Tournament 2 finds most negative 
from remaining items, continuing until all texts are ranked. Each tournament uses 
bracket-style head-to-head comparisons ("Which text is more negative?") with winners 
advancing until a single champion emerges.

PERFORMANCE: Requires ~N×log₂(N) comparisons for N texts (~30 comparisons for 10 texts).
More comparisons than recursive median but provides intuitive tournament bracket structure
familiar to users. Returns complete ranking from most negative to most positive text.
Optional ranking-based seeding available for strategic bracket placement.
"""

import random
from ..base import SortingAlgorithm
from ..registry import algorithm_registry
from typing import List, Dict, Any

@algorithm_registry.register
class TournamentSort(SortingAlgorithm):
    """Tournament bracket sorting algorithm."""
    
    ALGORITHM_ID = "tournament"
    NAME = "Tournament Bracket" 
    DESCRIPTION = "Sports-style tournament: texts compete in brackets"
    SCHEMA_KEY = "tournament"

    def __init__(self):
        super().__init__(
            self.NAME,
            self.DESCRIPTION,
            self.ALGORITHM_ID, 
            self.SCHEMA_KEY
        )
        self.text_data = {}
        self.comparison_engine = None

    def initialize_from_data(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """Store text data for tournament"""
        self.text_data = {item['id']: item for item in data}
        return True

    def sort(self, ids: List[str], use_ranking_seed: bool = False) -> List[str]:
        """Sort using sequential tournament elimination for complete ranking."""
        self.reset_counters()
        
        result = []
        remaining_ids = ids.copy()
        
        # Run tournaments until all items are ranked
        while remaining_ids:
            # Run tournament on remaining items to find "most negative"
            current_round = self._seed_tournament(remaining_ids, use_ranking_seed)
            
            # Tournament elimination rounds
            while len(current_round) > 1:
                current_round = self._run_tournament_round(current_round)
            
            # Winner of this tournament is most negative of remaining items
            winner = current_round[0]
            result.append(winner)
            remaining_ids.remove(winner)
        
        return result  # Complete ranking from most negative to most positive


    def _seed_tournament(self, ids: List[str], use_ranking_seed: bool) -> List[str]:
        """Seed tournament bracket"""
        if use_ranking_seed and self.text_data:
            # Seed by existing ranking (best vs worst, etc.)
            try:
                return sorted(ids, key=lambda x: float(self.text_data[x].get('ranking', 0)))
            except (KeyError, ValueError):
                pass
        
        # Random seeding
        seeded = ids.copy()
        random.shuffle(seeded)
        return seeded

    def _run_tournament_round(self, competitors: List[str]) -> List[str]:
        """Run one round of tournament brackets"""
        winners = []
        
        # Process pairs
        for i in range(0, len(competitors) - 1, 2):
            competitor1 = competitors[i]
            competitor2 = competitors[i + 1]
            
            self.comparison_count += 1
            
            # Use comparison engine (handles UI and caching)
            if self.ask_if_more_negative(competitor1, competitor2):
                winners.append(competitor1)  # Competitor1 wins (more negative)
            else:
                winners.append(competitor2)  # Competitor2 wins (more negative)
        
        # Handle bye (odd number of competitors)
        if len(competitors) % 2 == 1:
            winners.append(competitors[-1])  # Last competitor gets bye
        
        return winners

    def ask_if_more_negative(self, text_id: str, other_id: str) -> bool:
        """Use comparison engine for intelligent caching"""
        return self.comparison_engine.ask_if_more_negative(text_id, other_id) # type: ignore

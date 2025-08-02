"""
Statistical analysis functionality for text ranking tool
Assumes perfect data - no validation, pure calculations
"""
import csv
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple
from scipy.stats import kendalltau, spearmanr
import numpy as np

class RankingComparisonResult(NamedTuple):
    """Results from comparing two rankings"""
    kendall_tau: float
    spearman_rho: float
    kendall_distance: int
    avg_rank_diff: float
    common_items: int
    overlap_at_10: float
    overlap_at_20: float

class StatisticsCalculator:
    """Pure statistical calculations for text rankings - assumes perfect data"""

    @staticmethod
    def calculate_kendall_tau(list1: List[int], list2: List[int]) -> float:
        """Calculate Kendall Tau"""
        tau, _ = kendalltau(list1, list2)
        return float(tau) # type: ignore

    @staticmethod
    def calculate_spearman_correlation(list1: List[int], list2: List[int]) -> float:
        """Calculate Spearman rank correlation"""
        rho, _ = spearmanr(list1, list2)
        return float(rho) # type: ignore

    @staticmethod
    def calculate_kendall_distance(list1: List[int], list2: List[int]) -> int:
        """Calculate Kendall tau distance (number of pairwise disagreements)"""
        n = len(list1)
        arr1 = np.array(list1)
        arr2 = np.array(list2)
        
        disagreements = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (arr1[i] < arr1[j]) != (arr2[i] < arr2[j]):
                    disagreements += 1
        
        return disagreements

    @staticmethod
    def calculate_normalized_kendall_distance(list1: List[int], list2: List[int]) -> float:
        """Calculate normalized Kendall tau distance (0-1 scale)"""
        distance = StatisticsCalculator.calculate_kendall_distance(list1, list2)
        n = len(list1)
        max_distance = n * (n - 1) // 2
        return distance / max_distance

    @staticmethod
    def calculate_top_k_overlap(ranking1: List[str], ranking2: List[str], k: int) -> float:
        """Calculate overlap between top-k items in two rankings"""
        top_k_1 = set(ranking1[:k])
        top_k_2 = set(ranking2[:k])
        overlap = len(top_k_1 & top_k_2)
        return overlap / k

    @staticmethod
    def load_ranking_from_export_csv(csv_file_path: Path) -> List[str]:
        """Load ranking from exported CSV file"""
        ranking = []
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = sorted(reader, key=lambda x: int(x['new_ranking']))
            ranking = [row['id'] for row in rows]
        return ranking

    @staticmethod
    def compare_two_csv_files(csv_file1: Path, csv_file2: Path) -> RankingComparisonResult:
        """Compare rankings from two exported CSV files"""
        ranking1 = StatisticsCalculator.load_ranking_from_export_csv(csv_file1)
        ranking2 = StatisticsCalculator.load_ranking_from_export_csv(csv_file2)
        
        return StatisticsCalculator.compare_rankings_from_lists(ranking1, ranking2)

    @staticmethod
    def compare_rankings_from_lists(ranking1: List[str], ranking2: List[str]) -> RankingComparisonResult:
        """Compare two ranking lists directly"""
        
        # Find common texts
        common_texts = list(set(ranking1) & set(ranking2))
        
        # Create position mappings (1-based ranking)
        pos1 = {text: i + 1 for i, text in enumerate(ranking1)}
        pos2 = {text: i + 1 for i, text in enumerate(ranking2)}
        
        # Extract positions for common texts
        positions1 = [pos1[text] for text in common_texts]
        positions2 = [pos2[text] for text in common_texts]
        
        # Calculate all metrics
        tau = StatisticsCalculator.calculate_kendall_tau(positions1, positions2)
        spearman = StatisticsCalculator.calculate_spearman_correlation(positions1, positions2)
        kendall_dist = StatisticsCalculator.calculate_kendall_distance(positions1, positions2)
        
        # Average rank difference
        rank_diffs = [abs(p1 - p2) for p1, p2 in zip(positions1, positions2)]
        avg_rank_diff = statistics.mean(rank_diffs)
        
        # Top-k overlaps
        overlap_10 = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 10)
        overlap_20 = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 20)
        
        return RankingComparisonResult(
            kendall_tau=tau,
            spearman_rho=spearman,
            kendall_distance=kendall_dist,
            avg_rank_diff=avg_rank_diff,
            common_items=len(common_texts),
            overlap_at_10=overlap_10,
            overlap_at_20=overlap_20
        )

    @staticmethod
    def batch_compare_csv_files(csv_files: List[Path]) -> Dict[Tuple[str, str], RankingComparisonResult]:
        """Compare all pairs of CSV files in a batch"""
        results = {}
        
        for i in range(len(csv_files)):
            for j in range(i + 1, len(csv_files)):
                file1, file2 = csv_files[i], csv_files[j]
                key = (file1.name, file2.name)
                comparison = StatisticsCalculator.compare_two_csv_files(file1, file2)
                results[key] = comparison
        
        return results

    @staticmethod
    def calculate_pearson_correlation(list1: List[float], list2: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        n = len(list1)
        mean_x = sum(list1) / n
        mean_y = sum(list2) / n
        
        numerator = sum((list1[i] - mean_x) * (list2[i] - mean_y) for i in range(n))
        sum_sq_x = sum((list1[i] - mean_x) ** 2 for i in range(n))
        sum_sq_y = sum((list2[i] - mean_y) ** 2 for i in range(n))
        
        denominator = (sum_sq_x * sum_sq_y) ** 0.5
        return numerator / denominator

    @staticmethod
    def calculate_rank_biased_overlap(ranking1: List[str], ranking2: List[str], p: float = 0.9) -> float:
        """Calculate Rank-Biased Overlap (RBO) between two rankings"""
        max_len = min(len(ranking1), len(ranking2))
        rbo_sum = 0.0
        
        for d in range(1, max_len + 1):
            set1 = set(ranking1[:d])
            set2 = set(ranking2[:d])
            overlap_size = len(set1 & set2)
            rbo_sum += overlap_size / d * (p ** (d - 1))
        
        return (1 - p) * rbo_sum

    @staticmethod
    def calculate_average_precision_at_k(ranking1: List[str], ranking2: List[str], k: int) -> float:
        """Calculate Average Precision at K (how many of top-k from ranking1 appear in top-k of ranking2)"""
        top_k_1 = set(ranking1[:k])
        
        precision_sum = 0.0
        relevant_found = 0
        
        for i in range(min(k, len(ranking2))):
            if ranking2[i] in top_k_1:
                relevant_found += 1
                precision_sum += relevant_found / (i + 1)
        
        return precision_sum / min(k, len(top_k_1))

    @staticmethod
    def calculate_weighted_tau(list1: List[int], list2: List[int], weights: List[float]) -> float:
        """Calculate weighted Kendall's tau where weights give more importance to certain positions"""
        n = len(list1)
        weighted_concordant = 0.0
        weighted_discordant = 0.0
        
        for i in range(n):
            for j in range(i + 1, n):
                weight = (weights[i] + weights[j]) / 2
                
                if (list1[i] < list1[j]) == (list2[i] < list2[j]):
                    weighted_concordant += weight
                else:
                    weighted_discordant += weight
        
        total_weight = weighted_concordant + weighted_discordant
        return (weighted_concordant - weighted_discordant) / total_weight

    @staticmethod
    def calculate_footrule_distance(ranking1: List[str], ranking2: List[str]) -> float:
        """Calculate Spearman's footrule distance (normalized)"""
        common_texts = list(set(ranking1) & set(ranking2))
        
        pos1 = {text: i + 1 for i, text in enumerate(ranking1)}
        pos2 = {text: i + 1 for i, text in enumerate(ranking2)}
        
        footrule_sum = sum(abs(pos1[text] - pos2[text]) for text in common_texts)
        n = len(common_texts)
        max_footrule = n * (n - 1) // 2 if n % 2 == 0 else n * n // 2
        
        return footrule_sum / max_footrule

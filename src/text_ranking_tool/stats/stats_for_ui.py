"""
Statistics functions specifically designed for UI consumption
Handles data loading, aggregation, and formatting for analysis displays
Simple error handling - any error bubbles up to UX
"""

import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List
import statistics
from .statistics_calculator import StatisticsCalculator

class StatsForUI:
    """UI-focused statistics functions with simple error handling"""

    @staticmethod
    def load_ranking_from_export_csv(csv_file_path: Path) -> List[str]:
        """Load human ranking from exported CSV file (new_ranking column)"""
        ranking = []
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = sorted(reader, key=lambda x: int(x['new_ranking']))
            ranking = [row['id'] for row in rows]
        return ranking

    @staticmethod
    def load_machine_ranking_from_csv(csv_file_path: Path) -> List[str]:
        """Load machine ranking from internal data CSV file (ranking column)"""
        ranking = []
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = sorted(reader, key=lambda x: int(x['ranking']))
            ranking = [row['id'] for row in rows]
        return ranking

    @staticmethod
    def get_available_datasets(internal_exports_dir: Path, internal_data_dir: Path) -> List[str]:
        """Get list of available dataset stems"""
        dataset_stems = set()
        
        # Only use internal_data_dir - this contains the actual dataset files
        for csv_file in internal_data_dir.glob("*.csv"):
            dataset_stems.add(csv_file.stem)
        
        return sorted(list(dataset_stems))


    @staticmethod
    def load_all_participants_data(dataset_stem: str, internal_exports_dir: Path, 
                                 internal_data_dir: Path, user_mapping: Dict[str, str]) -> Dict[str, List[str]]:
        """Load rankings for all participants including machine for a specific dataset"""
        participants_data = {}
        
        # Load machine ranking
        machine_file = internal_data_dir / f"{dataset_stem}.csv"
        if machine_file.exists():
            participants_data['Machine'] = StatsForUI.load_machine_ranking_from_csv(machine_file)
        
        # LOAD human rankings
        for display_name, user_id in user_mapping.items():
            # FIND export file for this user and dataset inside INTERNAL_EXPORTS_DIR
            pattern = f"{user_id}_{dataset_stem}_*.csv"
            matching_files = list(internal_exports_dir.glob(pattern))
            
            if matching_files:
                # USE most recent file if multiple exist
                latest_file = max(matching_files, key=lambda f: f.stat().st_mtime)
                participants_data[display_name] = StatsForUI.load_ranking_from_export_csv(latest_file)
                # PRINT warning
                print(f"\033[1;38;5;208m⚠ {display_name}\033[0m has multiple exports for dataset " 
                      f"\033[1;38;5;208m{dataset_stem}\033[0m. Using latest: {latest_file.name}\n")
                
        return participants_data

    @staticmethod
    def generate_correlation_matrices(participants_data: Dict[str, List[str]]) -> Dict[str, pd.DataFrame]:
        """Generate correlation matrices for all metrics"""
        participants = list(participants_data.keys())
        n = len(participants)
        
        # Initialize matrices
        matrices = {
            'kendall': pd.DataFrame(index=participants, columns=participants, dtype=float),
            'spearman': pd.DataFrame(index=participants, columns=participants, dtype=float),
            'overlap_10': pd.DataFrame(index=participants, columns=participants, dtype=float),
            'overlap_20': pd.DataFrame(index=participants, columns=participants, dtype=float)
        }
        
        # Calculate all pairwise comparisons
        for i, participant1 in enumerate(participants):
            for j, participant2 in enumerate(participants):
                if i == j:
                    # Perfect self-correlation
                    matrices['kendall'].iloc[i, j] = 1.0
                    matrices['spearman'].iloc[i, j] = 1.0
                    matrices['overlap_10'].iloc[i, j] = 1.0
                    matrices['overlap_20'].iloc[i, j] = 1.0
                else:
                    # Calculate metrics between participants
                    ranking1 = participants_data[participant1]
                    ranking2 = participants_data[participant2]
                    
                    # Find common items
                    common_items = list(set(ranking1) & set(ranking2))
                    
                    if len(common_items) >= 2:
                        pos1 = [ranking1.index(item) + 1 for item in common_items]
                        pos2 = [ranking2.index(item) + 1 for item in common_items]
                        
                        matrices['kendall'].iloc[i, j] = StatisticsCalculator.calculate_kendall_tau(pos1, pos2)
                        matrices['spearman'].iloc[i, j] = StatisticsCalculator.calculate_spearman_correlation(pos1, pos2)
                        matrices['overlap_10'].iloc[i, j] = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 10)
                        matrices['overlap_20'].iloc[i, j] = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 20)
                    else:
                        # Not enough common items
                        matrices['kendall'].iloc[i, j] = 0.0
                        matrices['spearman'].iloc[i, j] = 0.0
                        matrices['overlap_10'].iloc[i, j] = 0.0
                        matrices['overlap_20'].iloc[i, j] = 0.0
        
        return matrices

    @staticmethod
    def generate_unified_dashboard_data(participants_data: Dict[str, List[str]]) -> pd.DataFrame:
        """Generate unified dashboard DataFrame with all metrics as columns"""
        participants = list(participants_data.keys())
        machine_ranking = participants_data.get('Machine', [])
        
        dashboard_data = []
        
        for participant in participants:
            participant_ranking = participants_data[participant]
            
            if participant == 'Machine':
                # Perfect baseline for machine
                row_data = {
                    'Participant': participant,
                    'Kendall τ': 1.0,
                    'Spearman ρ': 1.0,
                    'Kendall Distance': 0,
                    'Avg Rank Diff': 0.0,
                    'Top 10 Overlap': 1.0,
                    'Top 20 Overlap': 1.0,
                    'Correlation Strength': 'Perfect'
                }
            else:
                # Compare against machine baseline
                common_items = list(set(machine_ranking) & set(participant_ranking))
                
                if len(common_items) >= 2:
                    # Create position mappings
                    machine_positions = [machine_ranking.index(item) + 1 for item in common_items]
                    participant_positions = [participant_ranking.index(item) + 1 for item in common_items]
                    
                    # Calculate all metrics
                    kendall_tau = StatisticsCalculator.calculate_kendall_tau(machine_positions, participant_positions)
                    spearman_rho = StatisticsCalculator.calculate_spearman_correlation(machine_positions, participant_positions)
                    kendall_distance = StatisticsCalculator.calculate_kendall_distance(machine_positions, participant_positions)
                    avg_rank_diff = statistics.mean([abs(m - p) for m, p in zip(machine_positions, participant_positions)])
                    top_10_overlap = StatisticsCalculator.calculate_top_k_overlap(machine_ranking, participant_ranking, 10)
                    top_20_overlap = StatisticsCalculator.calculate_top_k_overlap(machine_ranking, participant_ranking, 20)
                    
                    # Determine correlation strength
                    if kendall_tau >= 0.8:
                        strength = 'Strong'
                    elif kendall_tau >= 0.6:
                        strength = 'Moderate' 
                    elif kendall_tau >= 0.4:
                        strength = 'Weak'
                    else:
                        strength = 'Very Weak'
                    
                    row_data = {
                        'Participant': participant,
                        'Kendall τ': kendall_tau,
                        'Spearman ρ': spearman_rho,
                        'Kendall Distance': kendall_distance,
                        'Avg Rank Diff': avg_rank_diff,
                        'Top 10 Overlap': top_10_overlap,
                        'Top 20 Overlap': top_20_overlap,
                        'Correlation Strength': strength
                    }
                else:
                    # Not enough common items - all zeros
                    row_data = {
                        'Participant': participant,
                        'Kendall τ': 0.0,
                        'Spearman ρ': 0.0,
                        'Kendall Distance': 0,
                        'Avg Rank Diff': 0.0,
                        'Top 10 Overlap': 0.0,
                        'Top 20 Overlap': 0.0,
                        'Correlation Strength': 'No Data'
                    }
            
            dashboard_data.append(row_data)
        
        return pd.DataFrame(dashboard_data)

    @staticmethod
    def compare_two_participants_detailed(participant1: str, participant2: str, 
                                        participants_data: Dict[str, List[str]]) -> Dict:
        """Detailed head-to-head comparison between two specific participants"""
        ranking1 = participants_data[participant1]
        ranking2 = participants_data[participant2]
        
        # Find common items
        common_items = list(set(ranking1) & set(ranking2))
        
        # Create position mappings
        positions1 = [ranking1.index(item) + 1 for item in common_items]
        positions2 = [ranking2.index(item) + 1 for item in common_items]
        
        # Calculate all metrics
        kendall_tau = StatisticsCalculator.calculate_kendall_tau(positions1, positions2)
        spearman_rho = StatisticsCalculator.calculate_spearman_correlation(positions1, positions2)
        kendall_distance = StatisticsCalculator.calculate_kendall_distance(positions1, positions2)
        avg_rank_diff = statistics.mean([abs(p1 - p2) for p1, p2 in zip(positions1, positions2)])
        overlap_10 = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 10)
        overlap_20 = StatisticsCalculator.calculate_top_k_overlap(ranking1, ranking2, 20)
        
        return {
            'participant1': participant1,
            'participant2': participant2,
            'kendall_tau': kendall_tau,
            'spearman_rho': spearman_rho,
            'kendall_distance': kendall_distance,
            'avg_rank_diff': avg_rank_diff,
            'common_items': len(common_items),
            'overlap_at_10': overlap_10,
            'overlap_at_20': overlap_20
        }

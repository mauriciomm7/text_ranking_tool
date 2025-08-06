# tests/test_pivot_strategy.py
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.text_ranking_tool.algorithms.recursive_median.recursive_median_core import RecursiveMedianSort  # noqa: E402
from src.text_ranking_tool.data.csv_loader import load_ranking_data                                      # noqa: E402
from tests.utils import MockComparisonEngine                                                              # noqa: E402

# --- MODIFIED: Easy to toggle between datasets ---
#data_path = os.path.join('tests/data', 'percentile_set_01.csv')
data_path = os.path.join('tests/data', 'mock_data_30.csv') # Using the new 30-item file


def get_pivot_comparison_data():
    """Returns raw comparison data for both strategies"""
    
    # Setup with error checking
    try:
        data = load_ranking_data(data_path)
        if data is None or len(data) == 0:
            print("❌ ERROR: Failed to load test data")
            return None, None
        # --- MODIFIED: Clearer output ---
        print(f"✅ Loaded {len(data)} texts from {os.path.basename(data_path)}")
        
    except Exception as e:
        print(f"❌ ERROR loading data: {e}")
        return None, None
    
    try:
        algorithm = RecursiveMedianSort() # type: ignore
        success = algorithm.initialize_from_data(data)
        if not success:
            print("❌ ERROR: Failed to initialize algorithm")
            return None, None
    except Exception as e:
        print(f"❌ ERROR creating algorithm: {e}")
        return None, None
    
    # Set up mock comparison engine (no debug output for clean results)
    algorithm.comparison_engine = MockComparisonEngine(data, debug=False) # type: ignore
    ids = [item['id'] for item in data]
    
    print("🔍 Testing Pivot Strategy Comparison Counts")
    print("=" * 50)
    
    # Collect data
    valence_counts = []
    random_counts = []
    
    for run in range(10):
        try:
            # Valence pivot
            algorithm.reset_counters()
            algorithm.sort(ids.copy(), use_valence_pivot=True)
            valence_counts.append(algorithm.comparison_count)
            
            # Random pivot
            algorithm.reset_counters()
            algorithm.sort(ids.copy(), use_valence_pivot=False)
            random_counts.append(algorithm.comparison_count)
            
            # Print progress
            print(f"Run {run+1:2d}: Valence={valence_counts[-1]:3d} | Random={random_counts[-1]:3d} | Diff={random_counts[-1] - valence_counts[-1]:+4d}")
            
        except Exception as e:
            print(f"Run {run+1:2d}: ❌ ERROR - {e}")
            continue
    
    return valence_counts, random_counts

# Usage
if __name__ == "__main__":
    print("🚀 Starting Pivot Strategy Comparison Test")
    print("=" * 50)
    
    valence, random = get_pivot_comparison_data()
    
    if valence is None or random is None or len(valence) == 0 or len(random) == 0:
        print("\n❌ TEST FAILED: No valid results")
        exit(1)
    
    print("=" * 50)
    print("📊 RESULTS:")
    print(f"Valence pivot: {valence}")
    print(f"Random pivot:  {random}")
    print(f"Valence avg:   {sum(valence)/len(valence):.1f}")
    print(f"Random avg:    {sum(random)/len(random):.1f}")
    
    improvement = sum(random)/len(random) - sum(valence)/len(valence)
    improvement_pct = (improvement / (sum(random)/len(random))) * 100 if sum(random) > 0 else 0
    
    print(f"Improvement:   {improvement:.1f} fewer comparisons ({improvement_pct:.1f}% reduction)")
    
    if improvement > 0:
        print(f"🎉 Valence pivot is {improvement:.1f} comparisons more efficient!")
    elif improvement < 0:
        print(f"🤔 Random pivot was {abs(improvement):.1f} comparisons better")
    else:
        print("🤷 Both strategies performed equally")

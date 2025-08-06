# tests/test_tournament.py
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.text_ranking_tool.algorithms.tournament.tournament_core import TournamentSort  # noqa: E402
from src.text_ranking_tool.data.csv_loader import load_ranking_data                     # noqa: E402
# --- MODIFIED: Import all required helpers from your utils file ---
from tests.utils import MockComparisonEngine, get_expected_order, analyze_test_results  # noqa: E402

# --- MODIFIED: Easy to toggle between datasets ---
#data_path = os.path.join('tests/data', 'percentile_set_01.csv')
data_path = os.path.join('tests/data', 'mock_data_30.csv')


def test_tournament_with_controlled_responses():
    # Load your test data
    try:
        data = load_ranking_data(data_path)
        if not data:
            print("❌ ERROR: Data could not be loaded or is empty.")
            return None
        print(f"✅ Loaded {len(data)} texts from CSV: {os.path.basename(data_path)}")
    except Exception as e:
        print(f"❌ ERROR loading CSV: {e}")
        return None
    
    # --- NEW: Automatically generate the correct order from the data ---
    expected_order = get_expected_order(data)

    # Create tournament algorithm instance
    try:
        algorithm = TournamentSort() # type: ignore
        print("✅ Created TournamentSort instance")
    except Exception as e:
        print(f"❌ ERROR creating tournament algorithm: {e}")
        return None
    
    # Initialize algorithm
    algorithm.initialize_from_data(data)
    algorithm.comparison_engine = MockComparisonEngine(data) # type: ignore
    
    # Extract IDs for sorting
    ids = [item['id'] for item in data]
    
    print("\n🧪 Testing Tournament Algorithm with Perfect Oracle Responses")
    print(f"Dataset: {len(ids)} texts from {os.path.basename(data_path)}")
    print(f"Expected order: {expected_order[:3]}... to ...{expected_order[-3:]}")
    print("=" * 70)
    
    # Run multiple tests
    results = []
    # Note: Tournament sort is often deterministic, but running multiple times confirms stability.
    for test_run in range(10):
        try:
            algorithm.reset_counters()
            sorted_ids = algorithm.sort(ids.copy())
            
            # --- MODIFIED: Check against the dynamic expected_order variable ---
            is_correct = sorted_ids == expected_order

            results.append({
                'run': test_run + 1,
                'result': sorted_ids,
                'comparisons': algorithm.comparison_count,
                'correct_order': is_correct
            })
            
            status = "✅ PASS" if is_correct else "❌ FAIL"
            print(f"Run {test_run + 1:2d}: {algorithm.comparison_count:3d} comparisons | {status} | Result: {sorted_ids[:3]}...")
            
        except Exception as e:
            print(f"Run {test_run + 1:2d}: ❌ ERROR - {e}")
            continue
    
    return results

if __name__ == "__main__":
    print("🚀 Starting Tournament Algorithm Test")
    print("=" * 70)
    
    results = test_tournament_with_controlled_responses()
    
    # --- MODIFIED: Use the shared analyzer for a consistent report ---
    if results:
        analyze_test_results(results, "Tournament Sort")
    else:
        print("\n❌ TEST FAILED: No results to analyze")
        exit(1)

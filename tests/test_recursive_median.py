# Updated tests/test_recursive_median.py
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.text_ranking_tool.algorithms.recursive_median.recursive_median_core import RecursiveMedianSort # noqa: E402
from src.text_ranking_tool.data.csv_loader import load_ranking_data                                     # noqa: E402
from tests.utils import MockComparisonEngine, get_expected_order, analyze_test_results                  # noqa: E402

# --- You can now easily toggle between datasets ---
# Use absolute path
#data_path = os.path.join('tests/data', 'percentile_set_01.csv')
data_path = os.path.join('tests/data', 'mock_data_30.csv') # Assuming you saved the new file with this name


def test_recursive_median_with_controlled_responses():
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
    
    # Automatically generate the correct order
    expected_order = get_expected_order(data)
    
    # Create algorithm instance
    try:
        algorithm = RecursiveMedianSort() # type: ignore
        print("✅ Created RecursiveMedianSort instance")
    except Exception as e:
        print(f"❌ ERROR creating algorithm: {e}")
        return None
    
    # Initialize algorithm
    algorithm.initialize_from_data(data)
    algorithm.comparison_engine = MockComparisonEngine(data) # type: ignore
    
    # Extract IDs for sorting
    ids = [item['id'] for item in data]
    
    print("\n🧪 Testing Recursive Median Algorithm with Perfect Oracle Responses")
    print(f"Dataset: {len(ids)} texts from {os.path.basename(data_path)}")
    print(f"Expected order: {expected_order[:3]}... to ...{expected_order[-3:]}")
    print("=" * 70)
    
    # Run multiple tests
    results = []
    for test_run in range(10):
        try:
            algorithm.reset_counters()
            sorted_ids = algorithm.sort(ids.copy())
            
            is_correct = sorted_ids == expected_order
            
            results.append({
                'run': test_run + 1,
                'result': sorted_ids,
                'comparisons': algorithm.comparison_count,
                'correct_order': is_correct
            })
            
            status = "✅ PASS" if is_correct else "❌ FAIL"
            # Adjusted print formatting for larger comparison counts
            print(f"Run {test_run + 1:2d}: {algorithm.comparison_count:3d} comparisons | {status} | Result: {sorted_ids[:3]}...")
            
        except Exception as e:
            print(f"Run {test_run + 1:2d}: ❌ ERROR - {e}")
            continue
    
    return results

# --- MODIFIED: The main execution block is now much cleaner ---
if __name__ == "__main__":
    print("🚀 Starting Recursive Median Algorithm Test")
    print("=" * 70)
    
    # 1. Run the test function to get the results
    results = test_recursive_median_with_controlled_responses()
    
    # 2. Use the shared analyzer to print the detailed summary
    if results:
        analyze_test_results(results, "Recursive Median")
    else:
        print("\n❌ TEST FAILED: No results to analyze")
        exit(1)
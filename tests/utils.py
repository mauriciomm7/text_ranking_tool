# tests/utils/mock_engine.py
import math
import sys

class MockComparisonEngine:
    """
    A reusable mock comparison engine for testing ranking algorithms.
    It uses a ground truth ranking to provide perfect, automated responses.
    """
    
    def __init__(self, ground_truth_ranking: list, debug: bool = False):
        """
        Initializes the mock engine with the true ranking.
        - ground_truth_ranking: The list of dicts from the CSV, containing 'id' and 'ranking'.
        - debug: If True, prints every comparison detail to the console.
        """
        self.true_ranks = {item['id']: int(item['ranking']) for item in ground_truth_ranking}
        self.debug = debug
        if self.debug:
            print(f"📊 Mock Engine Initialized. Ground truth ranks: {self.true_ranks}")
    
    def ask_if_more_negative(self, text_id_a: str, text_id_b: str) -> bool:
        """
        Returns True if text_id_a is more negative (has a higher rank number).
        """
        rank_a = self.true_ranks.get(text_id_a, 5) # Default to mid-rank if not found
        rank_b = self.true_ranks.get(text_id_b, 5)
        
        result = rank_a > rank_b
        
        if self.debug:
            print(f"Compare: {text_id_a}(rank={rank_a}) vs {text_id_b}(rank={rank_b}) -> More negative? {result}")
        
        return result

###### ----
def get_expected_order(data: list) -> list:
    """
    Generates the expected sorted list of IDs from the mock data.
    It sorts based on the 'ranking' column in descending order, as a
    higher rank number means 'more negative'.
    """
    # Sort the data by the 'ranking' column, highest number first
    sorted_data = sorted(data, key=lambda item: int(item['ranking']), reverse=True)
    
    # Extract just the IDs from the sorted data
    expected_ids = [item['id'] for item in sorted_data]
    
    return expected_ids

###### ----
def analyze_test_results(results: list, algorithm_name: str):
    """
    Analyzes and prints a detailed summary of test run results.
    - results: A list of dicts from the test run.
    - algorithm_name: The name of the algorithm for the report header.
    """
    if not results:
        print(f"\n❌ TEST FAILED for {algorithm_name}: No results to analyze.")
        return

    print("=" * 70)
    print(f"📊 FINAL TEST RESULTS ({algorithm_name}):")

    try:
        # --- Core Metrics ---
        avg_comparisons = sum(r['comparisons'] for r in results) / len(results)
        success_rate = sum(1 for r in results if r['correct_order']) / len(results)
        min_comparisons = min(r['comparisons'] for r in results)
        max_comparisons = max(r['comparisons'] for r in results)
        n = len(results[0]['result'])

        print(f"Success Rate:        {success_rate:.0%}")
        print(f"Average Comparisons: {avg_comparisons:.1f} (for {n} items)")
        print(f"Min Comparisons:     {min_comparisons}")
        print(f"Max Comparisons:     {max_comparisons}")

        # --- Advanced Analysis ---
        theoretical_min = math.ceil(math.lgamma(n + 1) / math.log(2)) if n > 1 else 0
        print(f"Theoretical Min (Sort):{theoretical_min:.1f} comparisons (log2(n!))")
        
        if theoretical_min > 0:
            efficiency_factor = avg_comparisons / theoretical_min
            print(f"Efficiency Factor:   {efficiency_factor:.2f}x theoretical minimum")

        # --- Error Reporting ---
        if success_rate < 1.0:
            print("\n⚠️  ALGORITHM ISSUES DETECTED:")
            failed_runs = [r for r in results if not r['correct_order']]
            for run in failed_runs:
                print(f"   Run {run['run']}: Incorrect order detected.")
        else:
            print(f"\n🎉 ALGORITHM VALIDATION SUCCESSFUL!")
            print(f"   The {algorithm_name} algorithm is correct and working as expected.")

    except (ZeroDivisionError, KeyError, IndexError) as e:
        print(f"\n❌ ERROR analyzing results for {algorithm_name}: {e}")

def calculate_theoretical_bounds(n):
    """Calculate theoretical bounds for comparison-based algorithms"""
    # Minimum for complete sorting
    min_sort = n * math.log2(n) if n > 1 else 0
    
    # Minimum for median finding  
    min_median = max(n - 1, 0)
    
    # Maximum (naive pairwise)
    max_pairwise = n * (n - 1) // 2 if n > 1 else 0
    
    return {
        'min_sort': min_sort,
        'min_median': min_median, 
        'max_pairwise': max_pairwise
    }

def estimate_algorithm_performance(n):
    """Estimate performance for your specific algorithms based on empirical data"""
    
    if n <= 1:
        return {
            'recursive_median_random': 0,
            'recursive_median_valence': 0,
            'tournament': 0,
            'tournament_single_winner': 0,
            'pure_pairwise': 0
        }
    
    # Based on your test results (10 items: valence=19, random=24.4, tournament=45)
    # Extrapolate using algorithmic complexity patterns
    
    # Recursive median with valence pivot - observed O(n log n) with low constant
    recursive_median_valence = int(1.9 * n * math.log2(n)) if n > 1 else 0
    
    # Recursive median with random pivot - higher constant factor
    recursive_median_random = int(2.4 * n * math.log2(n)) if n > 1 else 0
    
    # Tournament - observed O(n²) behavior due to multiple tournaments for complete ranking
    tournament = int(n * (n + 1) / 2 * 1.35) if n > 1 else 0  # Empirically derived
    
    # Tournament single winner - just one tournament bracket to find most negative
    # Single elimination tournament: n-1 comparisons (each comparison eliminates 1 item)
    tournament_single_winner = max(n - 1, 0)
    
    # Pure pairwise
    pure_pairwise = n * (n - 1) // 2
    
    return {
        'recursive_median_valence': recursive_median_valence,
        'recursive_median_random': recursive_median_random,
        'tournament': tournament,
        'tournament_single_winner': tournament_single_winner,
        'pure_pairwise': pure_pairwise
    }

def analyze_algorithms(n):
    """Complete analysis of algorithm performance for n items"""
    
    bounds = calculate_theoretical_bounds(n)
    performance = estimate_algorithm_performance(n)
    
    print(f"📊 ALGORITHM ANALYSIS FOR {n} ITEMS")
    print("=" * 60)
    
    # Theoretical bounds
    print("🎯 THEORETICAL BOUNDS:")
    print(f"   Complete sorting minimum:  {bounds['min_sort']:.1f} comparisons")
    print(f"   Median finding minimum:    {bounds['min_median']} comparisons")  
    print(f"   Naive pairwise maximum:    {bounds['max_pairwise']} comparisons")
    print()
    
    # Your algorithm estimates
    print("🚀 YOUR ALGORITHM ESTIMATES:")
    
    algorithms = [
        ("Recursive Median (Valence)", performance['recursive_median_valence']),
        ("Recursive Median (Random)", performance['recursive_median_random']),
        ("Tournament Bracket (Complete)", performance['tournament']),
        ("Tournament (Single Winner)", performance['tournament_single_winner']),
        ("Pure Pairwise", performance['pure_pairwise'])
    ]
    
    for name, comparisons in algorithms:
        if bounds['min_sort'] > 0:
            efficiency_vs_sort = comparisons / bounds['min_sort']
            efficiency_vs_median = comparisons / bounds['min_median'] if bounds['min_median'] > 0 else 0
            
            print(f"   {name:<28} {comparisons:4d} comparisons")
            print(f"   {'':>28} {efficiency_vs_sort:4.2f}x sort minimum")
            print(f"   {'':>28} {efficiency_vs_median:4.2f}x median minimum")
            print()
    
    # Efficiency rankings
    print("🏆 EFFICIENCY RANKING (Best to Worst):")
    sorted_algos = sorted(algorithms, key=lambda x: x[1])
    for i, (name, comparisons) in enumerate(sorted_algos, 1):
        print(f"   {i}. {name}: {comparisons} comparisons")
    
    print()
    
    # User experience estimates
    print("⏱️  ESTIMATED USER EXPERIENCE:")
    for name, comparisons in algorithms:
        if comparisons > 0:
            # Assuming 3-5 seconds per comparison for thoughtful decisions
            time_min = comparisons * 3 / 60  # 3 sec per comparison
            time_max = comparisons * 5 / 60  # 5 sec per comparison
            print(f"   {name:<28} {time_min:.1f}-{time_max:.1f} minutes")
    
    return bounds, performance

def compare_list_sizes():
    """Compare performance across different list sizes"""
    sizes = [5, 10, 15, 20, 25, 30, 50, 100]
    
    print("📈 PERFORMANCE SCALING COMPARISON")
    print("=" * 90)
    print(f"{'Size':<6} {'Valence':<8} {'Random':<8} {'Tournament':<12} {'Single':<8} {'Pairwise':<10} {'Efficiency':<12}")
    print("-" * 90)
    
    for n in sizes:
        perf = estimate_algorithm_performance(n)
        bounds = calculate_theoretical_bounds(n)
        
        efficiency = perf['recursive_median_valence'] / bounds['min_sort'] if bounds['min_sort'] > 0 else 0
        
        print(f"{n:<6} {perf['recursive_median_valence']:<8} {perf['recursive_median_random']:<8} {perf['tournament']:<12} {perf['tournament_single_winner']:<8} {perf['pure_pairwise']:<10} {efficiency:<12.2f}x")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--compare':
            compare_list_sizes()
            return
        
        try:
            n = int(sys.argv[1])
            analyze_algorithms(n)
        except ValueError:
            print("❌ Please provide a valid number")
            return
    else:
        print("🔧 Algorithm Performance Analysis Tool")
        print("-" * 40)
        print("Options:")
        print("  python tests/utils.py [number]     - Analyze specific list size")
        print("  python tests/utils.py --compare    - Compare multiple sizes")
        print()
        
        try:
            n = int(input("Enter number of items to analyze: "))
            analyze_algorithms(n)
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")

if __name__ == '__main__':
    main()

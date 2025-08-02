# src\text_ranking_tool\main.py

# Core system imports
from .config.constants import CONFIGURED_ALGORITHM, INTERNAL_DATA_DIR
from .ux.user_selection_ui import show_user_selection, show_user_welcome
from .ux.file_selection_ui import show_file_selection, show_file_loading_status
from .ux.auto_export_ui import show_completion_results
from .data.csv_loader import load_ranking_data
from .ranking.comparison_engine import initialize_comparison_engine
from .data.initialization import initialize_data_directories
from .utils.startup_helpers import auto_export_completed_ranking
from .algorithms.registry import algorithm_registry


def main():
    """Main text ranking application entry point"""
    
    try:
            
        # Step 0: Initialize data directories
        initialize_data_directories()
        
        # Step 1: User Selection
        selected_user = show_user_selection()
        if not selected_user:
            return        
        
        # CHECK FOR HIDDEN ADMIN ACCESS
        if selected_user == "ADMIN":
            from .ux.admin_iu.admin_main_ui import show_admin_menu
            show_admin_menu()
            return main()
        
        # print(f"DEBUG: User selected: {selected_user}")
        show_user_welcome(selected_user)
        
        # Step 2: File Selection
        selected_file_stem = show_file_selection(selected_user)
        
        if not selected_file_stem:
            input("Press Enter to continue...")
            return main()  # Restart workflow
        
        # Step 3: Load CSV Data
        csv_file_path = INTERNAL_DATA_DIR / f"{selected_file_stem}.csv"        
        text_data = load_ranking_data(str(csv_file_path))
        
        if not text_data:
            print(f"Error: Could not load data from {csv_file_path}")
            input("Press Enter to continue...")
            return main()  
        
        show_file_loading_status(csv_file_path.name, len(text_data))
        
        # Step 4: Initialize Comparison Engine with Session
        comparison_engine = initialize_comparison_engine(
            text_data, 
            selected_user, 
            selected_file_stem
        )
        
        # Step 5: Create and Connect Algorithm
        algorithm = algorithm_registry.create_algorithm(CONFIGURED_ALGORITHM)
        if not algorithm:
            print(f"Error: Algorithm '{CONFIGURED_ALGORITHM}' not found")
            return
        
        # Connect algorithm to comparison engine
        algorithm.comparison_engine = comparison_engine
        
        # Initialize algorithm with data
        if not algorithm.initialize_from_data(text_data):
            print("Error: Failed to initialize algorithm")
            return
        
        print(f"Algorithm: {algorithm.NAME}")
        print(f"Ready to start ranking {len(text_data)} texts...")
        input("Press Enter to begin comparisons...")
        
        # Step 6: Run Algorithm with Intelligent Comparison Memory
        text_ids = [item['id'] for item in text_data]
        
        try:
            final_ranking = algorithm.sort(text_ids)
            
            # AUTOMATIC EXPORT (using helper function)
            auto_export_completed_ranking(selected_user, selected_file_stem, final_ranking, text_data)
            
            # Step 7: Clean completion flow
            show_completion_results(selected_user, selected_file_stem, algorithm, final_ranking, text_data)
            
        except KeyboardInterrupt:
            print("\n\nRanking interrupted by user.")
            progress = comparison_engine.get_progress_info()
            print(f"Progress saved: {progress['comparisons_made']} comparisons completed")
            print("You can resume this session later.")
            
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()
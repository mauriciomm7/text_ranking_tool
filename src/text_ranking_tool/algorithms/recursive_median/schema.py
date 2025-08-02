# src/text_ranking_tool/algorithms/recursive_median/schema.py

# Only the columns actually needed for recursive median functionality
REQUIRED_COLUMNS = [
    "id",
    "text",
    "original_valence", 
    "original_ranking",
    "final_rank_position"
]

ALGORITHM_METADATA = {
    "algorithm_name": "Recursive Median Sort",
    "algorithm_id": "recursive_median"
}

def get_export_schema():
    return {
        "required": REQUIRED_COLUMNS,
        "metadata": ALGORITHM_METADATA
    }

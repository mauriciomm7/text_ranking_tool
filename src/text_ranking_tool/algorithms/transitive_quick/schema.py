# Only the columns actually needed for transitive quick functionality
REQUIRED_COLUMNS = [
    "id",
    "text",
    "original_valence", 
    "original_ranking",
    "final_rank_position"
]

ALGORITHM_METADATA = {
    "algorithm_name": "Transitive Quick Rank",
    "algorithm_id": "transitive_quick"
}

def get_export_schema():
    return {
        "required": REQUIRED_COLUMNS,
        "metadata": ALGORITHM_METADATA
    }

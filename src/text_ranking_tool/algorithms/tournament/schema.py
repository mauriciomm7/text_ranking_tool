# src/text_ranking_tool/algorithms/tournament/schema.py

# Only the columns actually needed for tournament functionality
REQUIRED_COLUMNS = [
    "id",
    "text",
    "original_valence", 
    "original_ranking",
    "final_rank_position"
]

ALGORITHM_METADATA = {
    "algorithm_name": "Tournament Bracket",
    "algorithm_id": "tournament"
}

def get_export_schema():
    return {
        "required": REQUIRED_COLUMNS,
        "metadata": ALGORITHM_METADATA
    }

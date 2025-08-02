# Same as Windows launcher but for Mac file paths
import sys
import os

# Go up two levels to project root, then find src
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

# Now import and run the main function  
from text_ranking_tool.main import main  # noqa: E402

if __name__ == "__main__":
    main()

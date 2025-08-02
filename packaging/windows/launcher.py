# C:\gitprojects\text_ranking_app_v1\launcher.py
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import and run the main function
from text_ranking_tool.main import main

if __name__ == "__main__":
    main()

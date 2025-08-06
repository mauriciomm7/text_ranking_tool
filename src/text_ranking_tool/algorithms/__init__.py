# src/text_ranking_tool/algorithms/__init__.py

# This file ensures all algorithms are registered when the package is imported.

# First, import the now-simple registry object.
from .registry import algorithm_registry  # noqa: F401

# Now, import each algorithm's module. The act of importing these files
# will execute the @algorithm_registry.register decorator inside them.
from .tournament import tournament_core
from .recursive_median import recursive_median_core
from .transitive_quick import transitive_quick_core

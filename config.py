"""
Configuration settings for the TSP solver comparison project.
"""

from pathlib import Path

# Path configurations
ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data" / "dimacs8"
RESULTS_DIR = ROOT_DIR / "results"

# Solver configurations
SOLVER_CONFIGS = {
    "or_tools": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
        "solution_limit": None,  # Optional solution limit
    },
    "python_tsp": {
        "max_iterations": 100,  # Maximum iterations for Lin-Kernighan
    },
    "pyvrp": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "traveling_rustling": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "fast_tsp": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "tsbee": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "lkh": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "concorde": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
    "vroom": {
        "time_limit_seconds": 2,  # Fixed time limit in seconds
    },
}

# Benchmark configurations
MAX_PROBLEM_SIZE = 1000  # Maximum number of nodes in problems to solve
NUMBER_OF_RUNS = 1  # Number of times to run each solver for each problem

# Results configurations
SAVE_CSV = True  # Whether to save results to CSV
SAVE_TEXT = True  # Whether to save results to text file

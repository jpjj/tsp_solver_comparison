# TSP Solver Comparison

This repository aims to compare different solvers for the Traveling Salesman Problem (TSP) using benchmark instances from TSPLIB, a well-known online database of TSP benchmark instances.

## Overview

The Traveling Salesman Problem is a classic algorithmic problem in the field of computer science and operations research. It asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"

This project evaluates and compares different TSP solvers that can be called from Python:
- [Google OR-Tools](https://github.com/google/or-tools)
- [python_tsp library](https://github.com/fillipe-gsm/python-tsp)
- [PyVRP](https://github.com/PyVRP/PyVRP)

## Project Structure

The project is organized as follows:

```

## Installation

1. Ensure you have Python 3.12 or newer installed
2. Clone this repository
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Benchmark

To run the benchmark using the new improved structure:

```bash
python new_main.py
```

This will:
1. Load TSP instances from the TSPLIB dataset
2. Run each solver on each instance
3. Generate result files in the `results` directory
4. Create visualizations in the `results/plots` directory

### Configuration

Modify `config.py` to adjust:
- Maximum problem size
- Number of runs per solver
- Solver-specific parameters
- Output settings


## Data

The benchmarks use instances from [TSPLIB](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/), a library of sample instances for the TSP maintained by the University of Heidelberg.

## Results

Results are saved in two formats:
1. CSV files for quantitative analysis
2. Text files for human-readable reports

The benchmark also generates visualization plots:
- Optimality gap comparison across solvers
- Solution time comparison across solvers

## License

[MIT License](LICENSE)
tsp-solver-comparison/
├── config.py                # Configuration settings
├── main.py                  # Original main script
├── new_main.py              # New improved main script
├── run_tests.py             # Test runner script
├── pyproject.toml           # Project dependencies
├── data/                    # Directory for TSP instances
│   └── tsplib/
│       └── symmetric_tsp/   # TSPLIB instances
├── results/                 # Directory for benchmark results
│   └── plots/               # Generated visualizations
├── src/                     # Source code
│   ├── data/                # Data loading modules
│   │   ├── __init__.py
│   │   └── tsplib_loader.py # TSPLIB data loader
│   ├── domain/              # Core domain logic
│   │   ├── __init__.py
│   │   ├── solver.py        # Solver implementations
│   │   └── utils.py         # Utility functions
│   └── results/             # Results management
│       ├── __init__.py
│       └── results_manager.py # Results processing
└── tests/                   # Test suite
    ├── __init__.py
    ├── test_data_loading.py # Tests for data loading
    └── test_solvers.py      # Tests for solvers
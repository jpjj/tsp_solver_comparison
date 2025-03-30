"""
Main script for comparing TSP solvers.
"""

import time
from typing import Dict

from src.domain.solver import (
    FastTspSolver,
    GoogleORToolsSolver,
    LinKernighanSolver,
    PyVrpSolver,
    TravelingRustlingSolver,
)
from src.data.tsplib_loader import (
    get_all_instance_names,
    load_problem_with_optimal_length,
    get_distance_matrix,
    get_tour_length,
)
from src.results.results_manager import ResultsManager
from config import MAX_PROBLEM_SIZE, NUMBER_OF_RUNS


def run_solvers(problem, distance_matrix, solvers, runs=1, optimal_length=None):
    """
    Run multiple solvers on a TSP instance and collect results.

    Args:
        problem: The TSP problem instance
        distance_matrix: The distance matrix for the problem
        solvers: Dictionary of solvers {name: solver_instance}
        runs: Number of times to run each solver
        optimal_length: The optimal tour length (if known)

    Returns:
        Dictionary of results for each solver
    """
    results = {name: {"lengths": [], "times": []} for name in solvers}

    for name, solver in solvers.items():
        for _ in range(runs):
            start_time = time.time()
            tour = solver.solve(distance_matrix)
            end_time = time.time()

            results[name]["times"].append(end_time - start_time)
            length = get_tour_length(problem, tour)
            results[name]["lengths"].append(length)

    # Process results
    for name in solvers:
        avg_length = sum(results[name]["lengths"]) / runs
        avg_time = sum(results[name]["times"]) / runs

        gap = None
        if optimal_length:
            gap = ((avg_length - optimal_length) / optimal_length) * 100

        results[name].update(
            {
                "avg_length": avg_length,
                "avg_time": avg_time,
                "all_lengths": results[name]["lengths"],
                "all_times": results[name]["times"],
                "gap": gap,
            }
        )

    return results


def main():
    """Main function to run the TSP solver comparison."""
    # Initialize solvers
    solvers = {
        # "traveling_rustling": TravelingRustlingSolver(),
        # "or_tools": GoogleORToolsSolver(),
        # "python_tsp": LinKernighanSolver(),
        # "pyvrp": PyVrpSolver(),
        "fast-tsp": FastTspSolver(),
    }

    # Initialize results manager
    results_manager = ResultsManager()
    results_manager.initialize_csv(list(solvers.keys()))

    # Open text file for results
    text_file = results_manager.open_text_file()

    # Get all problem instances within size limit
    for problem_name in get_all_instance_names(MAX_PROBLEM_SIZE):
        # Load problem and its optimal tour
        problem, optimal_length = load_problem_with_optimal_length(problem_name)
        distance_matrix = get_distance_matrix(problem)

        # Run the solvers
        results = run_solvers(
            problem=problem,
            distance_matrix=distance_matrix,
            solvers=solvers,
            runs=NUMBER_OF_RUNS,
            optimal_length=optimal_length,
        )

        # Add result to manager
        results_manager.add_result(
            instance_name=problem_name,
            dimension=problem.dimension,
            optimal_length=optimal_length,
            solver_results=results,
            file_handle=text_file,
        )

    # Close text file
    results_manager.close_text_file(text_file)

    # Generate summary plots
    results_manager.generate_summary_plots()


if __name__ == "__main__":
    main()

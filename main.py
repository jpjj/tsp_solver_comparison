"""
Main script for comparing TSP solvers.
"""

import time

from src.domain.solver import (
    FastTspSolver,
    GoogleORToolsSolver,
    LinKernighanSolver,
    PyVroomSolver,
    PyVrpSolver,
    TSBeeSolver,
    TravelingRustlingSolver,
    LKHSolver,
    ConcordeSolver,
)
from src.data.dimacs_loader import (
    get_all_instance_names,
    load_problem_with_optimal_length,
    get_distance_matrix,
    get_tour_length,
)
from src.results.results_manager import ResultsManager
from config import MAX_PROBLEM_SIZE, NUMBER_OF_RUNS, SOLVER_CONFIGS


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
        print(f"  Running {name}...", end="", flush=True)
        for _ in range(runs):
            start_time = time.time()
            tour = solver.solve(distance_matrix)
            end_time = time.time()

            results[name]["times"].append(end_time - start_time)
            length = get_tour_length(problem, tour)
            results[name]["lengths"].append(length)
        print(f" done ({results[name]['times'][0]:.2f}s)")

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
    # Initialize solvers with time limits (subset for initial benchmarking)
    solvers = {
        "fast_tsp": FastTspSolver(
            time_limit_seconds=SOLVER_CONFIGS["fast_tsp"]["time_limit_seconds"]
        ),
        # "lkh": LKHSolver(
        #     time_limit_seconds=SOLVER_CONFIGS["lkh"]["time_limit_seconds"]
        # ),
        # "traveling_rustling": TravelingRustlingSolver(
        #     time_limit_seconds=SOLVER_CONFIGS["traveling_rustling"][
        #         "time_limit_seconds"
        #     ]
        # ),
        "or_tools": GoogleORToolsSolver(
            time_limit_seconds=SOLVER_CONFIGS["or_tools"]["time_limit_seconds"]
        ),
        # "python_tsp": LinKernighanSolver(),
        "tsbee": TSBeeSolver(
            time_limit_seconds=SOLVER_CONFIGS["tsbee"]["time_limit_seconds"]
        ),
        # Enable additional solvers as needed
        # "pyvrp": PyVrpSolver(time_limit_seconds=SOLVER_CONFIGS["pyvrp"]["time_limit_seconds"]),
        # "vroom": PyVroomSolver(time_limit_seconds=SOLVER_CONFIGS["vroom"]["time_limit_seconds"]),
        # "concorde": ConcordeSolver(time_limit_seconds=SOLVER_CONFIGS["concorde"]["time_limit_seconds"]),
    }

    # Initialize results manager
    results_manager = ResultsManager()
    results_manager.initialize_csv(list(solvers.keys()))

    # Open text file for results
    text_file = results_manager.open_text_file()

    # Get all problem instances within size limit
    for problem_name in get_all_instance_names(MAX_PROBLEM_SIZE):
        print(f"\nProcessing {problem_name}...")
        try:
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
        except Exception as e:
            print(f"\nError processing {problem_name}: {e}")
            print("Skipping this instance...")

    # Close text file
    results_manager.close_text_file(text_file)

    # Generate summary plots
    results_manager.generate_summary_plots()


if __name__ == "__main__":
    main()

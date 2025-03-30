import numpy as np
import tsplib95
from typing import List, Dict
from src.domain.utils import (
    get_distance_matrix,
    get_all_instance_names,
    get_tour_length,
)
from src.domain.solver import GoogleORToolsSolver, LinKernighanSolver, PyVrpSolver
import time
import os
from datetime import datetime


def run_solvers(problem, distance_matrix, solvers, runs=1, optimal_length=None):

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


def write_to_file_and_console(message, file_handler):
    """Write a message to both console and file."""
    print(message)
    file_handler.write(message + "\n")


def main():
    # Create a results directory if it doesn't exist
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)

    # Create a timestamp for the results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"tsp_results_{timestamp}.txt")

    with open(results_file, "w") as f:
        write_to_file_and_console(f"TSP Solver Comparison Results - {timestamp}", f)
        write_to_file_and_console("=" * 50, f)

        for problem_name in get_all_instance_names():
            problem = tsplib95.load(f"./data/tsplib/symmetric_tsp/{problem_name}.tsp")
            if problem.dimension > 100:
                continue
            write_to_file_and_console(f"\nProblem: {problem_name}", f)
            write_to_file_and_console("-" * 30, f)

            distance_matrix = get_distance_matrix(problem)
            opt = tsplib95.load(f"./data/tsplib/symmetric_tsp/{problem_name}.opt.tour")
            optimal_length = get_tour_length(problem, opt.tours[0])
            write_to_file_and_console(f"Optimal tour length: {optimal_length}", f)

            # Create solver instances
            solvers = {
                "or_tools": GoogleORToolsSolver(),
                "python_tsp": LinKernighanSolver(),
                "pyvrp": PyVrpSolver(),
            }

            # Run the solvers
            results = run_solvers(
                problem=problem,
                distance_matrix=distance_matrix,
                solvers=solvers,
                runs=1,
                optimal_length=optimal_length,
            )

            # Print results for each solver
            for name, result in results.items():
                write_to_file_and_console(f"\n{name.upper()} RESULTS:", f)
                write_to_file_and_console(
                    f"  Average length: {result['avg_length']:.2f}", f
                )
                write_to_file_and_console(
                    f"  Average time: {result['avg_time']:.4f} seconds", f
                )
                if result["gap"] is not None:
                    write_to_file_and_console(
                        f"  Optimality gap: {result['gap']:.2f}%", f
                    )

        write_to_file_and_console("\nResults saved to: " + results_file, f)


if __name__ == "__main__":
    main()

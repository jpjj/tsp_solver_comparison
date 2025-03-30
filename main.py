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
import csv
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

    # Create a timestamp for the results files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"tsp_results_{timestamp}.txt")
    csv_file = os.path.join(results_dir, f"tsp_results_{timestamp}.csv")

    # Initialize solvers
    solvers = {
        "or_tools": GoogleORToolsSolver(),
        "python_tsp": LinKernighanSolver(),
        "pyvrp": PyVrpSolver(),
    }

    # Create CSV file with headers
    with open(csv_file, "w", newline="") as csvf:
        fieldnames = ["instance_name", "dimension", "optimal_length"]

        # Add solver-specific columns
        for solver_name in solvers.keys():
            fieldnames.extend(
                [
                    f"{solver_name}_avg_length",
                    f"{solver_name}_avg_time",
                    f"{solver_name}_gap",
                ]
            )

        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()

    # Continue with regular text output
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

            # Run the solvers
            results = run_solvers(
                problem=problem,
                distance_matrix=distance_matrix,
                solvers=solvers,
                runs=1,
                optimal_length=optimal_length,
            )

            # Prepare CSV row
            csv_row = {
                "instance_name": problem_name,
                "dimension": problem.dimension,
                "optimal_length": optimal_length,
            }

            # Print results for each solver
            for name, result in results.items():
                write_to_file_and_console(f"\n{name.upper()} RESULTS:", f)
                write_to_file_and_console(
                    f"  Average length: {result['avg_length']:.2f}", f
                )
                write_to_file_and_console(
                    f"  Average time: {result['avg_time']:.4f} seconds", f
                )

                # Add to CSV row
                csv_row[f"{name}_avg_length"] = round(result["avg_length"], 2)
                csv_row[f"{name}_avg_time"] = round(result["avg_time"], 4)

                if result["gap"] is not None:
                    write_to_file_and_console(
                        f"  Optimality gap: {result['gap']:.2f}%", f
                    )
                    csv_row[f"{name}_gap"] = round(result["gap"], 2)
                else:
                    csv_row[f"{name}_gap"] = None

            # Append row to CSV
            with open(csv_file, "a", newline="") as csvf:
                writer = csv.DictWriter(csvf, fieldnames=fieldnames)
                writer.writerow(csv_row)

        write_to_file_and_console("\nResults saved to: " + results_file, f)
        write_to_file_and_console("CSV results saved to: " + csv_file, f)


if __name__ == "__main__":
    main()

from abc import ABC, abstractmethod
import numpy as np
from typing import List
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from python_tsp.heuristics import solve_tsp_record_to_record
import pyvrp
import traveling_rustling
import fast_tsp


class Solver(ABC):
    """Abstract base class for TSP solvers."""

    @abstractmethod
    def solve(self, distance_matrix: np.ndarray, **kwargs) -> List[int]:
        """
        Solve the TSP problem given a distance matrix.

        Args:
            distance_matrix (np.ndarray): A square matrix where distance_matrix[i][j]
                                          is the distance from node i to node j.

        Returns:
            List[int]: The tour as a list of indices
        """
        pass


class GoogleORToolsSolver(Solver):
    """TSP solver implementation using Google OR-Tools."""

    def solve(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using Google OR-Tools."""

        manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.seconds = len(distance_matrix) // 10  # Time limit
        # search_parameters.solution_limit = len(distance_matrix)  # Solution limit

        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            return [], float("inf")

        # Extract the tour
        index = routing.Start(0)
        tour = [manager.IndexToNode(index)]

        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            tour.append(manager.IndexToNode(index))

        # Remove the duplicate of the starting node at the end
        if len(tour) > 1 and tour[0] == tour[-1]:
            tour.pop()

        return tour


class LinKernighanSolver(Solver):
    """TSP solver implementation using Lin-Kernighan heuristic from python_tsp."""

    def solve(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using Lin-Kernighan heuristic."""

        # The Lin-Kernighan heuristic expects a symmetric distance matrix
        permutation, distance = solve_tsp_record_to_record(distance_matrix)

        return permutation


class PyVrpSolver(Solver):
    """TSP solver implementation using PyVRP."""

    def solve(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using PyVRP."""
        n = len(distance_matrix)
        depot = pyvrp.Depot(x=0, y=0)
        clients = [pyvrp.Client(x=0, y=0) for _ in range(n - 1)]
        vehicle_type = pyvrp.VehicleType()
        problem = pyvrp.ProblemData(
            clients=clients,
            depots=[depot],
            vehicle_types=[vehicle_type],
            distance_matrices=[distance_matrix],
            duration_matrices=[distance_matrix],
        )
        model = pyvrp.Model.from_data(problem)
        model.add_vehicle_type()

        stopping_criterion = pyvrp.stop.MaxRuntime(max_runtime=n // 10)
        res = model.solve(stop=stopping_criterion, display=False)
        return [0] + res.best.routes()[0].visits()


class TravelingRustlingSolver(Solver):
    """TSP solver implementation using Traveling Rustling."""

    def solve(self, distance_matrix: np.ndarray) -> List[int]:
        n = len(distance_matrix)
        """Solve TSP using Traveling Rustling library."""
        solution = traveling_rustling.solve(
            distance_matrix,
            time_limit=n // 10,
        )
        return solution.route


class FastTspSolver(Solver):
    """TSP solver implementation using FastTSP."""

    def solve(self, distance_matrix: np.ndarray) -> List[int]:
        """Solve TSP using FastTSP library."""
        n = len(distance_matrix)
        solution = fast_tsp.find_tour(
            distance_matrix,
            # n // 10,
        )
        return solution

import os
from typing import List
import numpy as np
import tsplib95


def get_distance_matrix(problem):
    n = problem.dimension
    distance_matrix = [[0 for _ in range(n)] for _ in range(n)]
    starting_node_index = min(problem.get_nodes())
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = int(
                    10000
                    * problem.get_weight(
                        i + starting_node_index, j + starting_node_index
                    )
                )
    return np.array(distance_matrix)


def get_tour_length(problem, tour):
    n = problem.dimension
    lowest_index = min(problem.get_nodes())
    lowest_tour_index = min(tour)
    tour_length = 0
    for i, _ in enumerate(tour):
        tour_length += problem.get_weight(
            tour[i] + lowest_index - lowest_tour_index,
            tour[(i + 1) % n] + lowest_index - lowest_tour_index,
        )
    return tour_length


def get_all_instance_names() -> List[str]:
    """
    Find all TSP instance names in the data directory by looking for .tsp files.
    Returns a list of instance names without the .tsp extension.
    """
    tsp_dir = "./data/tsplib/symmetric_tsp/"
    instance_names = []

    for filename in os.listdir(tsp_dir):
        if filename.endswith("opt.tour"):
            # Extract the name without the .tsp extension
            instance_name = filename[:-9]
            instance_names.append(instance_name)

    return sorted(instance_names)

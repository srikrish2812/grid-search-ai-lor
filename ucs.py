import random
import heapq
import numpy as np

class UCSAgentGrid:
    """Agent for solving the GridSearch problem using Uniform-Cost Search (UCS).

    The UCS uses a priority queue to expand nodes based on the cost and a visited
    set to track explored nodes.It explores in a breadth-first manner and
    finds the shortest path from the initial node to the goal node.
    """

    def __init__(self):
        """Initializing with necessary data structures."""
        # priority queue to store nodes to be expanded
        self.frontier = []
        self.visited = set()  # set to track visited nodes
        self.nodes_expanded = 0  # counts the number of nodes expanded
        self.track_path_dict = {}  # dictionary to track the path to the goal
        self.track_cost_dict = {}  # cictionary to track the cost to reach each node

    def search(self, grid, initial_node, goal_node) -> tuple:
        """Performs UCS on grid search
        Args:
            grid (np.ndarray): The grid representing the search space.
            initial_node (tuple): The starting coordinates in the grid (row, col).
            goal_node (tuple): The goal node coordinates in the grid (row, col).

        Returns:
            tuple: A tuple (path from initial node to goal node, number of nodes expanded)
        """
        # Initialize the frontier with the initial node and its initial cost(==0)
        heapq.heappush(self.frontier, (0, initial_node))
        self.track_path_dict[initial_node] = None
        self.track_cost_dict[initial_node] = 0

        while self.frontier:
            current_cost, current_node = heapq.heappop(
                self.frontier
            )  # node with the lowest cost from the frontier

            # counts the number of nodes that are being expanded
            if current_node not in self.visited:
                self.nodes_expanded += 1
                self.visited.add(current_node)  # keeps track of visited nodes

                # if goal reached then retrace the path
                if current_node == goal_node:
                    total_cost = self.track_cost_dict[goal_node]
                    path = self.reconstruct_path(goal_node)
                    return (path, self.nodes_expanded, total_cost)

            # Explore the neighbors of the current node
                for neighbor, step_cost in self.get_neighbors(current_node, grid):
                    new_cost = self.track_cost_dict[current_node] + step_cost
                    if (
                        neighbor not in self.track_cost_dict
                        or new_cost < self.track_cost_dict[neighbor]
                    ):
                        self.track_cost_dict[neighbor] = new_cost
                        heapq.heappush(self.frontier, (new_cost, neighbor))
                        self.track_path_dict[neighbor] = current_node

        return (None, self.nodes_expanded, None)  # None if no path found

    def get_neighbors(self, node, grid) -> list[tuple]:
        """
        Finding all valid neighbors out of 8 possible neighbors
        of a given node in the grid.

        Args:
            node (tuple): The current grid coordinates (row, col).
            grid (np.ndarray): The grid

        Returns:
            list[tuple]: A list of valid neighbors in a tuple (position, cost to reach them)
        """
        directions = [
            (-1, 0,1),
            (1, 0,1),
            (0, -1,1),
            (0, 1,1),
            (-1, -1,np.sqrt(2)),
            (-1, 1,np.sqrt(2)),
            (1, -1,np.sqrt(2)),
            (1, 1,np.sqrt(2)),
        ]
        neighbors = []
        rows, cols = grid.shape

        for dx, dy, step_cost in directions:
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x, y] != -1:
                neighbors.append(((x, y), step_cost))

        return neighbors

    def reconstruct_path(self, goal_node) -> list[tuple]:
        """Retraces the path from the initial node to the goal node.

        Args:
            goal_node (tuple): The goal node coordinates.

        Returns:
            list[tuple]: The path from the initial node to the goal node as a list of coordinates.
        """
        path = []
        current = goal_node
        while current is not None:
            path.append(current)
            current = self.track_path_dict.get(current)
        path.reverse()  # path from start to goal
        return path

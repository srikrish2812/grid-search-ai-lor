# import modules
import random
import heapq
import numpy as np


def euclidean_distance(node1, node2):
    """
    Heuristic function to calculate the Euclidean distance between two nodes.

    Args:
        node1 (tuple): The first node-current (row, col).
        node2 (tuple): The second node-goal (row, col).

    Returns:
        float: The Euclidean distance between the two nodes.
    """
    return np.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def octile_distance(node1, node2):
    """
    Heuristic function to calculate the octile distance between two nodes.
    cost of diagonal move is sqrt(2) times the cost of non-diagonal move

    Args:
        node1 (tuple): The first node-current (row, col).
        node2 (tuple): The second node-goal (row, col).

    Returns:
        float: The octile distance between the two nodes.
    """
    dx = abs(node1[0] - node2[0])
    dy = abs(node1[1] - node2[1])
    return max(dx, dy) + ((np.sqrt(2) - 1) * min(dx, dy))


class AStarAgentGrid:
    """
    Agent that performs A* search on the grid search problem.

    The A* algorithm uses a priority queue called frontier to expand the
    nodes based on the sum of the cost function and the heuristic function.
    It explores the nodes in the frontier and adds the neighbors to the frontier
    based on the lowest sum of the cost function and the heuristic function.
    """

    def __init__(self, heuristic_func):
        self.frontier = []  # priority queue that keeps track of the nodes to explore
        self.visited = set()  # tracks the visited nodes efficiently
        self.heuristic_func = heuristic_func  # heuristic function for the algorithm
        self.track_cost_dict = {}  # tracks the cost to reach each node
        self.track_path_dict = {}  # tracks the path to the goal
        self.nodes_expanded = 0  # counts the number of nodes expanded
        #print(self.heuristic_func)

    def get_neighbors(self, node, grid):
        """ "
        Finding all valid neighbors out of 8 possible neighbors
        of a given node in the grid.

        Args:
            node (tuple): The current grid coordinates (row, col).
            grid (np.ndarray): The grid

        Returns:
            list[tuple]: A list of valid neighbors in a tuple (position, cost to reach them)
        """
        directions = [
            (-1, 0, 1),
            (1, 0,1),
            (0, -1,1),
            (0, 1,1),
            (-1, -1, np.sqrt(2)),
            (-1, 1, np.sqrt(2)),
            (1, -1,np.sqrt(2)),
            (1, 1,np.sqrt(2)),
        ]
        neighbors = []
        rows, cols = grid.shape
        for dx, dy,step_cost in directions:
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x, y] != -1:
                neighbors.append(((x, y), step_cost ))

        return neighbors

    def reconstruct_path(self, goal_node):
        """
        Retraces the path from the initial node to the goal node.

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

    def search(self, grid, initial_node, goal_node):
        """
        Implements A* algorithm on grid_search to find the optimal path

        Args:
            grid (np.ndarray): The grid representing the search space.
            initial_node (tuple): The starting coordinates in the grid (row, col).
            goal_node (tuple): The goal node coordinates in the grid (row, col).

        Returns:
            tuple: A tuple (path from initial node to goal node, number of nodes expanded)
        """

        # Initialize the frontier with the initial node and its heuristic cost
        heapq.heappush(
            self.frontier,
            (self.heuristic_func(initial_node, goal_node), initial_node),
        )
        self.track_cost_dict[initial_node] = 0
        self.track_path_dict[initial_node] = None

        while self.frontier:
            current_cost, current_node = heapq.heappop(self.frontier)

            if current_node in self.visited:
                continue

            # Mark as visited and count expansion
            self.visited.add(current_node)
            self.nodes_expanded += 1  # increment expanded nodes count

            # if goal reached then retrace the path
            if current_node == goal_node:
                return (self.reconstruct_path(goal_node), 
                        self.nodes_expanded, 
                        self.track_cost_dict[goal_node]
                        )

            # Explore the neighbors of the current node
            for neighbor, step_cost in self.get_neighbors(current_node, grid):
                new_cost = self.track_cost_dict[current_node] + step_cost
                if (
                    neighbor not in self.track_cost_dict
                    or new_cost < self.track_cost_dict[neighbor]
                ):
                    self.track_cost_dict[neighbor] = new_cost
                    priority = new_cost + self.heuristic_func(neighbor, goal_node)
                    heapq.heappush(self.frontier, (priority, neighbor))
                    self.track_path_dict[neighbor] = current_node

        return (None, self.nodes_expanded, None)  # No path found

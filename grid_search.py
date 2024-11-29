import random
import numpy as np


class GridSearch:
    """Class for the grid search problem."""
    def __init__(self, grid_size=(16,16), difficulty=0,
                 preset_goal=None, preset_grid=None, preset_initial=None):
        """Initializes the grid search problem."""
        self.grid_size = grid_size
        if preset_grid is not None and preset_initial is not None and preset_goal is not None:
            self.grid = preset_grid
            self.initial_node = preset_initial
            self.current_node = preset_initial
            self.goal_node = preset_goal
        else:
            self.grid = np.zeros(grid_size, dtype=np.int8)
            # Randomly generate the initial and goal nodes
            self.initial_node = (0,0)
            self.current_node = self.initial_node
            self.goal_node = (grid_size[0] - 1, grid_size[1] - 1)
            # while self.goal_node == self.initial_node:
            #     self.goal_node = (random.randint(0, grid_size[0] - 1),
            #                         random.randint(0, grid_size[1] - 1))
            
            if difficulty>0:
                total_cell_num = grid_size[0] * grid_size[1]
                blocked_cell_num = int((difficulty / 100) * total_cell_num)
                blocked_coords = []
                
                while len(blocked_coords) < blocked_cell_num:
                    x = random.randint(0, grid_size[0] - 1)
                    y = random.randint(0, grid_size[1] - 1)
                    node_coord = (x, y)
                    if (node_coord!=self.initial_node) and (node_coord!=self.goal_node) and (node_coord not in blocked_coords):
                        blocked_coords.append(node_coord)
                        self.grid[node_coord] = -1
            
    def is_goal_reached(self):
        """Returns True if the goal node is reached."""
        return self.current_node == self.goal_node
    
    def get_state(self):
        """Returns the current state of the grid search problem."""
        return self.grid.copy(), self.initial_node, self.goal_node
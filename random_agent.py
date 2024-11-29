import random

class RandomAgent:
    """Agent that selects random moves for the games."""
    @classmethod
    def select_move_2048(cls):
        """Returns a random valid move direction for the 2048 game.
        
        Returns:
            str: One of 'up', 'down', 'left', or 'right'
        """
        return random.choice(['up', 'down', 'left', 'right'])
    
    @classmethod
    def select_action_grid(cls, grid, current_position):
        """Returns a random valid action for the grid search problem.
        Args:
            grid (numpy.ndarray): numpy array(2d) representing the grid
            current_position (tuple): a tuple of node coordinates
        Returns:
            a new position (tuple): a tuple representing the new node coordinates
        """
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1),  
                 (-1, -1), (-1, 1), (1, -1), (1, 1)]  
        
        valid_moves = []
        rows, cols = grid.shape
        # checks for valid moves in the grid with inactive nodes
        for i,j in moves:
            new_i = current_position[0] + i
            new_j = current_position[1] + j
            
            if (0 <= new_i < rows) and (0 <= new_j < cols) and grid[new_i, new_j] != -1:
                valid_moves.append((new_i, new_j))
        
        if valid_moves:
            return random.choice(valid_moves)# randomly select a valid move
        return current_position
        
        
    
    @classmethod
    def select_move_puzzle8(cls):
        """Returns a random valid move direction for the 8-puzzle game.
        
        Returns:
            str: One of 'up', 'down', 'left', or 'right'
        """
        return random.choice(['up', 'down', 'left', 'right'])
    
    @classmethod
    def select_action_sentence_transform(cls, sentence_length, vocabulary):
        """Returns a random valid action for the sentence transformation problem.
        
        Returns:
            str: One of 'edit', 'add', or 'delete'
        """
        action = random.choice(['edit', 'add', 'delete'])
        index = random.randint(0, sentence_length - 1)
        if action != "delete":
            word = random.choice(vocabulary)
        else:
            word = None
        return action, index, word
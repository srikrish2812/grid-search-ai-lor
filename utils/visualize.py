import random
import time
import cv2
import numpy as np


def visualize_2048(grid, delay=300):
    """Visualize the 2048 game board using OpenCV.
    
    Args:
        grid: 2D numpy array representing the game board
        move_count: number of moves made
        elapsed_time: time elapsed since game start
        delay: delay in ms between frames
        message: optional message to display
    """
    cell_size = 100
    padding = 5
    board_size = 4 * cell_size + (4 + 1) * padding
    board_image = np.ones((board_size, board_size, 3), dtype=np.uint8) * 255
    
    # colors for different numbered tiles
    colors = {
        0: (205, 193, 180),
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (236, 196, 0),
        2048: (236, 196, 0)
    }

    for i in range(4):
        for j in range(4):
            cell_value = grid[i, j]
            color = colors.get(cell_value, (60, 58, 50))
            top_left = (j * cell_size + (j + 1) * padding, i * cell_size + (i + 1) * padding)
            bottom_right = (top_left[0] + cell_size, top_left[1] + cell_size)
            cv2.rectangle(board_image, top_left, bottom_right, color, -1)

            if cell_value != 0:
                text = str(cell_value)
                font_scale = 0.6
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
                text_x = top_left[0] + (cell_size - text_size[0]) // 2
                text_y = top_left[1] + (cell_size + text_size[1]) // 2
                cv2.putText(board_image, text, (text_x, text_y), font, font_scale, (0, 0, 0), 2)
 
    cv2.imshow("2048", board_image)
    cv2.waitKey(int(delay))

def visualize_grid(grid, current_node, initial_node, goal_node, visited_nodes):
    """Visualize the grid search problem using OpenCV."""
    cell_size = 50
    img_size = (grid.shape[0] * cell_size, grid.shape[1] * cell_size,3)
    img = np.zeros(img_size, dtype=np.uint8) *255
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            color = (255, 255, 255) # empty cell - white color
            center = (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2)
            
            if grid[i,j] == -1:
                bottom_right = ((j+1)*cell_size, (i+1)*cell_size)
                top_left = (j*cell_size, i*cell_size)
                cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), -1)
                continue
            
            if (i,j) == initial_node:
                color = (0, 0, 255) # initial node - red color
            elif (i,j) == goal_node:
                if (i,j) == current_node:
                    color = (255, 255, 0) # cyan color when current becomes goal
                else:
                    color = (0, 255, 0) # green color for goal node
            elif (i,j) == current_node:
                color = (255, 0, 0) # current node - blue color
            elif (i,j) in visited_nodes:
                color = (0,165,255) # orange for visited nodes
            cv2.circle(img, center, 15, color, -1)
           
    return img

def visualize_puzzle8(grid, move_count, elapsed_time):
    cell_size = 100
    img_size = (grid.shape[0] * cell_size, grid.shape[1] * cell_size,3)
    img = np.zeros(img_size, dtype=np.uint8) *255
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            val = grid[i,j]
            if val!=0:
                top_left = (j * cell_size, i * cell_size)
                bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
                cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), -1)
                cv2.putText(img, str(val), (top_left[0] + 30, top_left[1] + 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    cv2.imshow("8-Puzzle", img)
    
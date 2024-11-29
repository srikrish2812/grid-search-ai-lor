import argparse
import time
import cv2
from grid_search import GridSearch
from random_agent import RandomAgent
from utils.visualize import visualize_grid
from utils.metrics import TrackMetrics
from ucs import UCSAgentGrid
from astar import AStarAgentGrid, octile_distance, euclidean_distance


def play_grid_search(grid_size, agent=None, heuristic=None, difficulty=0,
                     preset_goal=None, preset_grid=None, preset_initial=None):
    """Play GridSearch with the specified agent."""
    # instantiate the game
    game = GridSearch(grid_size, difficulty=difficulty, preset_goal=preset_goal,
                      preset_grid=preset_grid, preset_initial=preset_initial)
    metrics = TrackMetrics()  # instantiate the metrics tracker
    if agent == "random":
        agent = RandomAgent()  # instantiate the random agent
        print("Using Random Agent")

        cv2.namedWindow("Grid Search", cv2.WINDOW_NORMAL)
        move_count = 0
        metrics.timer_on()
        visited_nodes = []
        while not game.is_goal_reached():
            if move_count <= 100:
                grid, initial_node, goal_node = game.get_state()
                current_node = game.current_node
                visited_nodes.append(current_node)  # Tracks the visited nodes

                # Visualizes the grid
                img = visualize_grid(
                    grid,
                    current_node,
                    initial_node,
                    goal_node,
                    visited_nodes=visited_nodes,
                )
                cv2.imshow("Grid Search", img)
                ms_wait_time = 500
                metrics.add_wait_time(ms_wait_time)
                cv2.waitKey(ms_wait_time)
                # the agent selects the action
                game.current_node = agent.select_action_grid(
                    grid, game.current_node
                )
                move_count += 1
                metrics.increase_steps()
                elapsed_time = time.time() - metrics.start_time - metrics.wait_time
                print(
                    f"Move {move_count}: {game.current_node} ({elapsed_time:.4f} seconds)"
                )
                # Checks if the goal node is reached ornot
                if game.is_goal_reached():
                    img = visualize_grid(
                        grid,
                        current_node,
                        initial_node,
                        goal_node,
                        visited_nodes=visited_nodes,
                    )
                    cv2.imshow("Grid Search", img)
                    print("Goal node reached")
                    cv2.waitKey(2000)
                    break
            elif move_count > 100:
                print("Maximum limit of moves = 100 reached")
                break
        metrics.metric_logger("Random Agent")
        time.sleep(2)
        cv2.destroyAllWindows()

    elif agent == "ucs":
        # instantiate the UCS agent for grid search
        agent = UCSAgentGrid()
        print("Using Uniform-Cost Search Agent")

        cv2.namedWindow("Grid Search", cv2.WINDOW_NORMAL)
        move_count = 0
        visited_nodes = set()  # Uses set to track visited nodes efficiently
        metrics.timer_on()

        # calling search() method of the UCS agent
        path, nodes_expanded, total_cost = agent.search(
            game.grid, game.initial_node, game.goal_node
        )
        # print(f"Nodes expanded: {nodes_expanded}")
        metrics.increase_nodes_expanded(
            nodes_expanded
        )  # increments the number of nodes expanded

        if path:
            metrics.set_total_cost(total_cost)
            print("Path found using UCS:")
            print(path)
            # Visualizing the path found by UCS
            for move in path:
                grid, initial_node, goal_node = game.get_state()
                current_node = move
                metrics.increase_steps()
                visited_nodes.add(current_node)  # add visited nodes
                img = visualize_grid(
                    grid,
                    current_node,
                    initial_node,
                    goal_node,
                    visited_nodes=visited_nodes,
                )
                cv2.imshow("Grid Search", img)
                ms_wait_time = 500
                metrics.add_wait_time(ms_wait_time)
                cv2.waitKey(ms_wait_time)
                move_count += 1
                elapsed_time = time.time() - metrics.start_time - metrics.wait_time
                print(f"Move {move_count}: {current_node} ({elapsed_time:.4f} seconds)")
        else:
            print("No path found by UCS.")

        metrics.metric_logger("Uniform-Cost Search Agent")
        print(len(path))
        time.sleep(2)
        cv2.destroyAllWindows()

    elif agent == "astar":
        # checks if heuristic is present or not
        if not heuristic:
            raise ValueError(
                "A* requires a heuristic function\
                Please provide a heuristic function"
            )
        elif heuristic == "euclidean":
            heuristic = euclidean_distance
            print("Implementing A* with Euclidean Heuristic")
            cv2.namedWindow("Grid Search - A* Euclidean", cv2.WINDOW_NORMAL)
        elif heuristic == "octile":
            heuristic = octile_distance
            print("Implementing A* with Octile Heuristic")
            cv2.namedWindow("Grid Search - A* Octile", cv2.WINDOW_NORMAL)
        agent = AStarAgentGrid(heuristic)

        move_count = 0
        visited_nodes = set()  # tracks visited nodes efficiently
        metrics.timer_on()

        # calling search() method of the A* agent
        path, nodes_expanded, total_cost = agent.search(
            game.grid, game.initial_node, game.goal_node
        )
        # print(f"Nodes expanded: {nodes_expanded}")
        metrics.increase_nodes_expanded(
            nodes_expanded
        )  # increments the number of nodes expanded

        if path:
            metrics.set_total_cost(total_cost)
            print("Path found using A*:")
            print(path)
            # Displaying the path found by A*
            for move in path:
                grid, initial_node, goal_node = game.get_state()
                current_node = move
                metrics.increase_steps()
                visited_nodes.add(current_node)  # Adds visited nodes
                img = visualize_grid(
                    grid,
                    current_node,
                    initial_node,
                    goal_node,
                    visited_nodes=visited_nodes,
                )
                cv2.imshow("Grid Search - A*", img)
                ms_wait_time = 500
                metrics.add_wait_time(ms_wait_time)
                cv2.waitKey(ms_wait_time)
                move_count += 1
                elapsed_time = time.time() - metrics.start_time - metrics.wait_time
                print(f"Move {move_count}: {current_node} ({elapsed_time:.4f} seconds)")
        else:
            print("No path found by A*.")

        metrics.metric_logger("A* Agent")
        print(len(path))
        time.sleep(2)
        cv2.destroyAllWindows()

    else:
        print(
            f"Unknown agent type: {agent}. Please choose 'random' or 'ucs' or 'astar'."
        )
        return


def main(
    game_name,
    agent_name,
    initial_sentence,
    goal_sentence,
    max_moves=100,
    grid_size=None,
    heuristic=None,
    difficulty=0,
):
    
    if game_name == "grid_search":
        max_attempts = 500
        attempt = 0
        solvable_initial = None
        solvable_goal = None
        solvable_grid = None
    
        while attempt < max_attempts:
            attempt += 1
            game = GridSearch(grid_size, difficulty=difficulty)
            astar_agent = AStarAgentGrid(euclidean_distance)
            path,_, total_cost = astar_agent.search(game.grid, game.initial_node, game.goal_node)
            
            if path is not None:
                print(f"Path/Solvable grid is found in {attempt} attempts")
                solvable_initial = game.initial_node
                solvable_goal = game.goal_node
                solvable_grid = game.grid.copy()
                break
            print(f"Attempt {attempt}: Grid has no solution, retrying")
        if solvable_grid is not None:
            play_grid_search(
                grid_size,
                agent=agent_name,
                heuristic=heuristic,
                difficulty=difficulty,
                preset_goal=solvable_goal,
                preset_grid=solvable_grid,
                preset_initial=solvable_initial,
            )
        else:
            print(f"Could not find a solvable grid in {max_attempts} attempts")
    else:
        raise ValueError(f"Invalid game_name or agent_name: {game_name}, {agent_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play games with different agents.")
    parser.add_argument("--game", type=str, required=True, help="Game to play ('2048')")
    parser.add_argument(
        "--agent", type=str, required=True, help="Agent to use ('random')"
    )
    parser.add_argument(
        "--grid_size", type=int, nargs=2, help="Grid size for GridSearch(eg: 16 16)"
    )
    parser.add_argument(
        "--initial_sentence", type=str, help="Initial sentence for SentenceTransform"
    )
    parser.add_argument(
        "--goal_sentence", type=str, help="Goal sentence for SentenceTransform"
    )
    parser.add_argument(
        "--heuristic", type=str, help="Heuristic function for A* (euclidean, octile)"
    )
    parser.add_argument(
        "--difficulty", type=int, default=0, help="Difficulty level(0-90) for GridSearch"
    )

    args = parser.parse_args()
    
    if not 0 <= args.difficulty <= 90:
        raise ValueError("Please ensure difficulty should be between 0 and 90")
    
    if args.difficulty > 70:
        print("Warning: It may take longer to generate a solvable grid")
        
    if args.grid_size:
        grid_size = tuple(args.grid_size)
    else:
        grid_size = None
    if args.initial_sentence:
        initial_sentence = args.initial_sentence
    else:
        initial_sentence = "The quick brown fox jumps over the lazy dog"
    if args.goal_sentence:
        goal_sentence = args.goal_sentence
    else:
        goal_sentence = "The lazy dog jumps over the quick brown fox"
    main(
        args.game,
        args.agent,
        initial_sentence=initial_sentence,
        goal_sentence=goal_sentence,
        grid_size=grid_size,
        heuristic=args.heuristic,
        difficulty=args.difficulty,
    )

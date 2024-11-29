import json
import time
import numpy as np
from grid_search import GridSearch
from random_agent import RandomAgent
from astar import AStarAgentGrid, euclidean_distance, octile_distance
from ucs import UCSAgentGrid
from utils.metrics import TrackMetrics
import os

def find_solvable_grid(grid_size, difficulty, max_attempts=500):
    """
    Generate a solvable grid using A* verification
    Returns None if no solvable grid is found within max_attempts
    """
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        game = GridSearch(grid_size, difficulty=difficulty)
        astar_agent = AStarAgentGrid(euclidean_distance)
        path, _, _ = astar_agent.search(game.grid, game.initial_node, game.goal_node)

        if path is not None:
            print(f"Solvable grid found in {attempt} attempts")
            return game.grid, game.initial_node, game.goal_node

        if attempt % 100 == 0:
            print(f"Attempt {attempt}: Still searching for solvable grid...")

    return None, None, None

def test_ucs_agent(grid, initial_node, goal_node, grid_size):
    """
    Test UCS agent on a given grid and return metrics
    """
    metrics = TrackMetrics()
    metrics.timer_on()

    ucs_agent = UCSAgentGrid()
    path, nodes_expanded, total_cost = ucs_agent.search(grid, initial_node, goal_node)

    runtime = metrics.timer_off()

    return {
        "steps": len(path) if path else 0,
        "runtime": runtime,
        "path_found": path is not None,
        "max_steps_reached": False,  # Not applicable for UCS Agent
        "total_cost": total_cost,
        "nodes_expanded": nodes_expanded
    }

def run_experiments_ucs():
    # Configuration
    grid_size = (32, 32)
    difficulties = range(0, 91, 10)
    runs_per_difficulty = 100
    results = {}
    
    # Create results directory if it doesn't exist
    results_dir = "./results/ucs"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    for difficulty in difficulties:
        print(f"\n{'='*50}")
        print(f"Testing difficulty level: {difficulty}")
        print(f"{'='*50}")
        
        difficulty_results = []
        successful_runs = 0
        grid_generation_failures = 0
        
        while successful_runs < runs_per_difficulty:
            try:
                # Adjust max_attempts based on difficulty
                max_attempts = 1000 if difficulty >= 70 else 500
                
                # Find a solvable grid
                grid, initial_node, goal_node = find_solvable_grid(
                    grid_size, 
                    difficulty,
                    max_attempts
                )
                
                if grid is None:
                    grid_generation_failures += 1
                    print(f"Failed to generate solvable grid after {max_attempts} attempts")
                    if grid_generation_failures >= 5:
                        print(f"Too many failures at difficulty {difficulty}. Moving to next difficulty.")
                        break
                    continue
                
                # Test UCS agent
                run_results = test_ucs_agent(grid, initial_node, goal_node, grid_size)
                
                # Add additional information
                run_results.update({
                    "run_number": successful_runs + 1,
                    "difficulty": difficulty
                })
                
                difficulty_results.append(run_results)
                successful_runs += 1
                
                if successful_runs % 10 == 0:
                    print(f"Completed {successful_runs}/{runs_per_difficulty} runs")
                
            except Exception as e:
                print(f"Error during run: {str(e)}")
                continue
        
        results[f"difficulty_{difficulty}"] = {
            "runs": difficulty_results,
            "summary": {
                "total_successful_runs": successful_runs,
                "grid_generation_failures": grid_generation_failures,
                "average_steps": np.mean([r["steps"] for r in difficulty_results]) if difficulty_results else 0,
                "average_runtime": np.mean([r["runtime"] for r in difficulty_results]) if difficulty_results else 0,
                "average_total_cost": np.mean([r["total_cost"] for r in difficulty_results]) if difficulty_results else 0,
                "average_nodes_expanded": np.mean([r["nodes_expanded"] for r in difficulty_results]) if difficulty_results else 0,
                "success_rate": np.mean([r["path_found"] for r in difficulty_results]) if difficulty_results else 0
            }
        }
        
        # Save intermediate results
        with open(os.path.join(results_dir, f'ucs_agent_results_difficulty_{difficulty}.json'), 'w') as f:
            json.dump({f"difficulty_{difficulty}": results[f"difficulty_{difficulty}"]}, f, indent=4)
            
    # Save final results
    with open(os.path.join(results_dir, 'ucs_agent_results_final.json'), 'w') as f:
        json.dump(results, f, indent=4)
    
    return results

def test_astar_agent(grid, initial_node, goal_node, grid_size, heuristic):
    """
    Test A* agent on a given grid and return metrics
    """
    metrics = TrackMetrics()
    metrics.timer_on()
    
    # Create A* agent with given heuristic
    if heuristic == "euclidean":
        astar_agent = AStarAgentGrid(euclidean_distance)
    else:
        astar_agent = AStarAgentGrid(octile_distance)
    
    path, nodes_expanded, total_cost = astar_agent.search(grid, initial_node, goal_node)
    runtime = metrics.timer_off()
    
    return {
        "steps": len(path) if path else 0,
        "runtime": runtime,
        "path_found": path is not None,
        "max_steps_reached": False,  # Not applicable for A* Agent
        "total_cost": total_cost,
        "nodes_expanded": nodes_expanded,
        "heuristic": heuristic
    }
    
def run_experiments_astar():
    """
    Run experiments for A* agent with both the heuristics
    """
    # configuration
    grid_size = (32, 32)
    difficulties = range(0, 91, 10)
    runs_per_difficulty = 100
    results = {
        "euclidean": {},
        "octile": {}
    }
    
    # creaet result dict if doesn't exist
    results_dir = "./results/astar"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    for difficulty in difficulties:
        print(f"\n{'='*50}")
        print(f"Testing difficulty level: {difficulty}")
        print(f"{'='*50}")
        
        difficulty_results_euclidean = []
        difficulty_results_octile = []
        successful_runs = 0
        grid_generation_failures = 0
        
        while successful_runs < runs_per_difficulty:
            try:
                # Adjust max_attempts based on difficulty
                max_attempts = 1000 if difficulty >= 70 else 500
                
                # Find a solvable grid
                grid, initial_node, goal_node = find_solvable_grid(
                    grid_size, 
                    difficulty,
                    max_attempts
                )
                
                if grid is None:
                    grid_generation_failures += 1
                    print(f"Failed to generate solvable grid after {max_attempts} attempts")
                    if grid_generation_failures >= 5:
                        print(f"Too many failures at difficulty {difficulty}. Moving to next difficulty.")
                        break
                    continue
                
                # Test A* agent with Euclidean distance heuristic
                run_results_euclidean = test_astar_agent(grid, initial_node, goal_node, grid_size, "euclidean")
                run_results_euclidean.update({
                    "run_number": successful_runs + 1,
                    "difficulty": difficulty
                })
                difficulty_results_euclidean.append(run_results_euclidean)
                
                # Test A* agent with Octile distance heuristic
                run_results_octile = test_astar_agent(grid, initial_node, goal_node, grid_size, "octile")
                run_results_octile.update({
                    "run_number": successful_runs + 1,
                    "difficulty": difficulty
                })
                difficulty_results_octile.append(run_results_octile)
                
                successful_runs += 1
                
                if successful_runs % 10 == 0:
                    print(f"Completed {successful_runs}/{runs_per_difficulty} runs")
                    
            except Exception as e:
                print(f"Error during run: {str(e)}")
                continue
            
        # store result for heuristics
        for heuristic, difficulty_results in [
            ('euclidean', difficulty_results_euclidean),
            ('octile', difficulty_results_octile)
        ]:
            results[heuristic][f"difficulty_{difficulty}"] = {
                "runs": difficulty_results,
                "summary": {
                    "total_successful_runs": successful_runs,
                    "grid_generation_failures": grid_generation_failures,
                    "average_steps": np.mean([r["steps"] for r in difficulty_results]) if difficulty_results else 0,
                    "average_runtime": np.mean([r["runtime"] for r in difficulty_results]) if difficulty_results else 0,
                    "average_total_cost": np.mean([r["total_cost"] for r in difficulty_results]) if difficulty_results else 0,
                    "average_nodes_expanded": np.mean([r["nodes_expanded"] for r in difficulty_results]) if difficulty_results else 0,
                    "success_rate": np.mean([r["path_found"] for r in difficulty_results]) if difficulty_results else 0
                }
            }
            
            # Save intermediate results
            with open(os.path.join(results_dir, f'astar_{heuristic}_results_difficulty_{difficulty}.json'), 'w') as f:
                json.dump({f"difficulty_{difficulty}": results[heuristic][f"difficulty_{difficulty}"]}, f, indent=4)
    # save heuristics results
    for heuristic in ['euclidean', 'octile']:
        with open(os.path.join(results_dir, f'astar_{heuristic}_results_final.json'), 'w') as f:
            json.dump(results[heuristic], f, indent=4)
    
    return results

def test_random_agent(grid, initial_node, goal_node, grid_size):
    """
    Test random agent on a given grid and return metrics
    """
    metrics = TrackMetrics()
    metrics.timer_on()

    current_node = initial_node
    path_found = False
    max_steps = grid_size[0] * grid_size[1] * 2  # Empirical limit

    while metrics.steps < max_steps:
        next_node = RandomAgent.select_action_grid(grid, current_node)
        metrics.increase_steps()

        if next_node == goal_node:
            path_found = True
            break

        current_node = next_node

    runtime = metrics.timer_off()

    return {
        "steps": metrics.steps,
        "runtime": runtime,
        "path_found": path_found,
        "max_steps_reached": metrics.steps >= max_steps,
        "total_cost": None,  # Not applicable for Random Agent
        "nodes_expanded": None  # Not applicable for Random Agent
    }

def run_experiments_random():
    # Configuration
    grid_size = (32, 32)
    difficulties = range(0, 91, 10)
    runs_per_difficulty = 100
    results = {}

    # Create results directory if it doesn't exist
    results_dir = "./results/random"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    for difficulty in difficulties:
        print(f"\n{'='*50}")
        print(f"Testing difficulty level: {difficulty}")
        print(f"{'='*50}")

        difficulty_results = []
        successful_runs = 0
        grid_generation_failures = 0

        while successful_runs < runs_per_difficulty:
            try:
                # Adjust max_attempts based on difficulty
                max_attempts = 1000 if difficulty >= 70 else 500

                # Find a solvable grid
                grid, initial_node, goal_node = find_solvable_grid(
                    grid_size, 
                    difficulty,
                    max_attempts
                )

                if grid is None:
                    grid_generation_failures += 1
                    print(f"Failed to generate solvable grid after {max_attempts} attempts")
                    if grid_generation_failures >= 5:
                        print(f"Too many failures at difficulty {difficulty}. Moving to next difficulty.")
                        break
                    continue

                # Test random agent
                run_results = test_random_agent(grid, initial_node, goal_node, grid_size)

                # Add additional information
                run_results.update({
                    "run_number": successful_runs + 1,
                    "difficulty": difficulty
                })

                difficulty_results.append(run_results)
                successful_runs += 1

                if successful_runs % 10 == 0:
                    print(f"Completed {successful_runs}/{runs_per_difficulty} runs")

            except Exception as e:
                print(f"Error during run: {str(e)}")
                continue

        results[f"difficulty_{difficulty}"] = {
            "runs": difficulty_results,
            "summary": {
                "total_successful_runs": successful_runs,
                "grid_generation_failures": grid_generation_failures,
                "average_steps": np.mean([r["steps"] for r in difficulty_results]) if difficulty_results else 0,
                "average_runtime": np.mean([r["runtime"] for r in difficulty_results]) if difficulty_results else 0,
                "success_rate": np.mean([r["path_found"] for r in difficulty_results]) if difficulty_results else 0
            }
        }

        # Save intermediate results in results folder
        with open(os.path.join(results_dir, f'random_agent_results_difficulty_{difficulty}.json'), 'w') as f:
            json.dump({f"difficulty_{difficulty}": results[f"difficulty_{difficulty}"]}, f, indent=4)

    # Save final results in results folder
    with open(os.path.join(results_dir, 'random_agent_results_final.json'), 'w') as f:
        json.dump(results, f, indent=4)

    return results

if __name__ == "__main__":
    try:
        print("Starting Uniform Cost Search Agent experiments...")
        results = run_experiments_ucs()
        print("\nExperiments completed successfully!")
        print("Results have been saved to the 'results' folder")
    except Exception as e:
        print(f"Fatal error in main execution: {str(e)}")


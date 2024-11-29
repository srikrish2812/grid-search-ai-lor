import json
import matplotlib.pyplot as plt
import os

print(os.getcwd())

def load_results(difficulty, algorithm):
    """
    Load results for a specific difficulty and algorithm
    """
    if algorithm == 'random_agent':
        filename = f"results/random/{algorithm}_results_difficulty_{difficulty}.json"
    elif algorithm == 'ucs_agent':
        filename = f"results/ucs/{algorithm}_results_difficulty_{difficulty}.json"
    elif algorithm == 'astar_euclidean':
        filename = f"results/astar/{algorithm}_results_difficulty_{difficulty}.json"
    elif algorithm == 'astar_octile':
        filename = f"results/astar/{algorithm}_results_difficulty_{difficulty}.json"
    try:
        #filename = f"{algorithm}_results_difficulty_{difficulty}.json"
        with open(filename, 'r') as file:
            data = json.load(file)
            runs = data[f'difficulty_{difficulty}']['runs']
            successful_paths = sum(1 for run in runs if run['path_found'])
            return successful_paths
    except FileNotFoundError:
        print(f"Warning: File {filename} not found")
        return 0
    
def load_more_data(difficulty, algorithm):
    """
    Load results for a specific difficulty and algorithm
    """
    if algorithm == 'ucs_agent':
        filename = f"results/ucs/{algorithm}_results_difficulty_{difficulty}.json"
    elif algorithm == 'astar_euclidean':
        filename = f"results/astar/{algorithm}_results_difficulty_{difficulty}.json"
    elif algorithm == 'astar_octile':
        filename = f"results/astar/{algorithm}_results_difficulty_{difficulty}.json"
    try:
        #filename = f"{algorithm}_results_difficulty_{difficulty}.json"
        with open(filename, 'r') as file:
            data = json.load(file)
            avg_cost = data[f'difficulty_{difficulty}']['summary']['average_total_cost']
            avg_nodes_expanded = data[f'difficulty_{difficulty}']['summary']['average_nodes_expanded']
            return avg_cost, avg_nodes_expanded
    except FileNotFoundError:
        print(f"Warning: File {filename} not found")
        return 0
    except KeyError:
        print(f"Warning: Key is not present in the file {filename}")
        return 0

def cost_nodes_data(algorithm):
    """
    Collect data for all difficulties for a specific algorithm
    """
    difficulties = range(0, 91, 10)  # 0, 10, 20, ..., 90
    avg_costs = []
    avg_nodes_expanded = []

    for diff in difficulties:
        avg_cost, avg_nodes = load_more_data(diff, algorithm)
        avg_costs.append(avg_cost)
        avg_nodes_expanded.append(avg_nodes)

    return avg_costs, avg_nodes_expanded

def cost_comparison_plot(algorithms, markers, colors):
    """
    Create comparison plot for all algorithms
    """
    difficulties = list(range(0, 91, 10))
    plt.figure(figsize=(12, 8))

    for algorithm, marker, color in zip(algorithms, markers, colors):
        avg_costs,_= cost_nodes_data(algorithm)
        plt.plot(difficulties, avg_costs, 
                marker=marker, 
                linestyle='-', 
                linewidth=2, 
                label=algorithm,
                color=color,
                markersize=8)

        # mark labels on top of the lines
        for x, y in zip(difficulties, avg_costs):
            plt.text(x, y + 1, str(y), ha='center', va='bottom')

    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Average Total Cost', fontsize=12)
    plt.title('Average Total Cost vs Difficulty Level by Algorithm', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.xticks(difficulties)


    plt.tight_layout()


    plt.savefig('plots/algorithm_cost_comparison.png')
    plt.show()

def nodes_comparison_plot(algorithms, markers, colors):
    """
    Create nodes expanded comparison plot for all algorithms
    """
    difficulties = list(range(0, 91, 10))
    plt.figure(figsize=(12, 8))
    
    for algorithm, marker, color in zip(algorithms, markers, colors):
        _, avg_nodes_expanded = cost_nodes_data(algorithm)
        plt.plot(difficulties, avg_nodes_expanded, 
                marker=marker, 
                linestyle='-', 
                linewidth=2, 
                label=algorithm,
                color=color,
                markersize=8)

        # mark labels on top of the lines
        for x, y in zip(difficulties, avg_nodes_expanded):
            plt.text(x, y + 1, str(y), ha='center', va='bottom')
    
    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Average Nodes Expanded', fontsize=12)
    plt.title('Average Nodes Expanded vs Difficulty Level by Algorithm', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.xticks(difficulties)
    
    plt.tight_layout()
    
    plt.savefig('plots/algorithm_nodes_comparison.png')
    plt.show()

def collect_algorithm_data(algorithm):
    """
    Collect data for all difficulties for a specific algorithm
    """
    difficulties = range(0, 91, 10)  # 0, 10, 20, ..., 90
    success_counts = []

    for diff in difficulties:
        success_count = load_results(diff, algorithm)
        success_counts.append(success_count)

    return success_counts

def plot_comparison(algorithms, markers, colors):
    """
    Create comparison plot for all algorithms
    """
    difficulties = list(range(0, 91, 10))
    plt.figure(figsize=(12, 8))

    for algorithm, marker, color in zip(algorithms, markers, colors):
        success_counts = collect_algorithm_data(algorithm)
        plt.plot(difficulties, success_counts, 
                marker=marker, 
                linestyle='-', 
                linewidth=2, 
                label=algorithm,
                color=color,
                markersize=8)

        # mark labels on top of the lines
        for x, y in zip(difficulties, success_counts):
            plt.text(x, y + 1, str(y), ha='center', va='bottom')

    plt.xlabel('Difficulty Level', fontsize=12)
    plt.ylabel('Number of Successful Paths Found', fontsize=12)
    plt.title('Path Finding Success vs Difficulty Level by Algorithm', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.xticks(difficulties)


    plt.tight_layout()


    plt.savefig('plots/algorithm_comparison.png')
    plt.show()


def main():

    algorithms = ['astar_euclidean', 'astar_octile', 'ucs_agent', 'random_agent']
    markers = ['o', 's', 'D', 'x']  
    colors = ['#2ecc71', '#e74c3c', '#3498db','black']  # green, red, blue, black

    #plot_comparison(algorithms, markers, colors)
    

if __name__ == "__main__":
    main()

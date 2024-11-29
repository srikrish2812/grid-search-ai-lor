import time


class TrackMetrics:
    """
    Class to track and log performance metrics.

    Attributes:
        start_time (float): start time of the program.
        nodes_expaned(int): nodes expanded by the algorithm
        steps(int): number of steps taken by the algorithm to reach the goal node/state
        wait_time(float): total wait_time during the visualization
    """

    def __init__(self):
        """
        Initialize the TrackMetrics class.
        """
        self.start_time = None
        self.nodes_expaned = 0
        self.steps = 0
        self.total_cost = 0
        self.wait_time = 0

    def timer_on(self):
        """
        Start the timer.
        """
        self.start_time = time.time()

    def timer_off(self):
        """
        Stop the timer.
        Returns:
            float: The elapsed time in seconds excluding the wait_time.
        """
        if self.start_time is None:
            raise ValueError(
                "Timer is not yet started. Please call timer_on() method first."
            )

        return time.time() - self.start_time - self.wait_time

    def add_wait_time(self, ms_wait_time):
        """
        Add wait time to the wait_time attribute used in visualization.
        Args:
            ms_wait_time (int): Wait time in milliseconds.
        """
        self.wait_time = (self.wait_time + ms_wait_time) / 1000

    def metric_logger(self, algo_name):
        """
        Logs performance metrics.
        Args:
            algo_name (str): Name of the algorithm.
        """
        print("-" * 15 + f"Performance Metrics for {algo_name}" + "-" * 15)
        if algo_name=="Random Agent":
            print("Cost and Nodes Expanded not valid for Random Agent")
        else:
            elapsed_time = self.timer_off()
            print(f"Number of nodes expanded: {self.nodes_expaned}")
            print(f"Total path cost: {self.total_cost:.4f}")
            print(f"Real run-time :- wait_time: {elapsed_time:.4f} seconds")
        print(f"Number of steps: {self.steps}")
        print("-" * 30 + "END" + "-" * 30)
               
    def set_total_cost(self, cost):
        """
        sets the total cost of the path.
        """
        self.total_cost = cost

    def increase_nodes_expanded(self, num_nodes):
        """
        Increase the number of nodes expanded by 1.
        """
        self.nodes_expaned += num_nodes

    def increase_steps(self):
        """
        Increase the number of steps by 1.
        """
        self.steps += 1

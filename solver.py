from point import Point
from metric import Metric
from itertools import permutations
from copy import copy

class Solver():
    """
    Solver for the TSP problem
    Must implement a step function
    """
    def __init__(self, node_coords: list[Point], metric: Metric):
        assert (len(node_coords) > 1), 'Number of nodes must be greater than 1'
        self.node_coords = node_coords
        self.current_solution = node_coords
        self.best_solution = []
        self.current = 0
        self.best = 1e10
        self.metric = metric
        self.finished = False
    
    def step(self):
        raise NotImplementedError()
    

class BruteForce(Solver):
    """
    Brute force solution - check every possible permuation of points
    """
    def __init__(self, node_coords: list[Point], metric: Metric):
        super().__init__(node_coords, metric)

        frontier = permutations([i for i in range(len(node_coords))])
        self.frontier = [f for f in frontier if f[0] == 0 and f[1] == len(node_coords)-1]
        
    def step(self):
        node_indices = self.frontier.pop()
        self.current_solution = [self.node_coords[i] for i in node_indices]
        self.current = self.metric.evaluate_solution(self.current_solution)
        if self.current < self.best:
            self.best = self.current
            self.best_solution = copy(self.current_solution)
        if not self.frontier:
            self.finished = True
        

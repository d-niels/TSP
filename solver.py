from itertools import permutations
from copy import copy
from random import shuffle, sample, randint

from selection import Selection
from crossover import Crossover
from mutation import Mutation
from fitness import Fitness

from point import Point
from metric import Metric

class Solver():
    """
    Solver for the TSP problem
    Must implement a step function
    """
    def __init__(self, fitness: Fitness):
        # Fitness function
        self.fitness_function = fitness

        # Recorded data
        self.current_solution = []
        self.best_solution = []
        self.current_score = 0
        self.best_score = 0
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
        self.current_solution = self.frontier.pop()
        self.current_score = self.fitness_function(self.current_solution)
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.best_solution = copy(self.current_solution)
        if not self.frontier:
            self.finished = True
    
    def fitness_function(self, solution: list[int]) -> float:
        coords = [self.node_coords[i] for i in solution]
        return 1 / self.metric.evaluate_solution(coords)

class GeneticAlgorithm(Solver):
    """
    Genetic algorithm with mutation, cross-over, and elitist selection
    """
    def __init__(
        self, node_coords: list[Point], metric: Metric, generation_size: int=10, crossover: str='single_point',
        selection: str='roulette_wheel', crossover_rate: float= 0.6, mutation_rate: float=0.01,
        ):
        super().__init__(node_coords, metric)
        
        selection_methods = {
            'roulette_wheel': RouletteWheel,
            'rank': None,
            'steady_state': None,
            'elitism': None,
            'tournament': None,
            'boltzmann': None,
            'stochastic_universal_sampling': None,
            'reward_based': None,
            'truncation': None,
        }

        crossover_functions = {
            'single_point': self.cross_over_single_point,
            'two_point': None,
            'n_point': None,
        }

        # Model parameters
        self.finished = False
        self.selection = selection_methods[selection]()
        self.crossover = crossover_functions[crossover]
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generation_size = generation_size

        # Initialize the generation
        self.generation = self.initialize_generation(len(node_coords))
        self.fitness_scores = [self.fitness_function(x) for x in self.generation]
        self.sort_generation_by_fitness()
        self.current_score = self.fitness_scores[0]
        self.current_solution = self.generation[0]
        self.best_score = self.fitness_scores[0]
        self.best_solution = self.generation[0]
    
    def step(self):
        # Determine how many parents and elitists there will be
        num_selections = int(self.crossover_rate * self.generation_size)
        num_selections += num_selections % 2
        num_elitists = self.generation_size - num_selections

        # Use selection to get the parents
        parents = self.selection.select(self.generation, self.fitness_scores, num_selections)

        # Keep the elitists and crossover to fill in the rest of the generation
        new_generation = self.generation[:num_elitists]
        for i in range(0, num_selections, 2):
            new_generation += self.crossover(parents[i], parents[i+1])
        self.generation = new_generation

        # Calculate fitness scores and sort the lists
        self.fitness_scores = [self.fitness_function(x) for x in self.generation]
        self.sort_generation_by_fitness()

        # Set the current solution to this generation's best
        self.current_solution = self.generation[-1]
        self.current_score = self.fitness_scores[0]

        # If the current generation's best score is better than the global best, update it
        if self.fitness_scores[0] > self.best_score:
            self.best_score = self.fitness_scores[0]
            # self.best_solution = self.generation[0]
            self.best_solution = [0 for _ in range(len(self.best_solution))]

    def sort_generation_by_fitness(self):
        self.fitness_scores, self.generation = zip(*sorted(zip(self.fitness_scores, self.generation), reverse=True))
        self.fitness_scores = list(self.fitness_scores)
        self.generation = list(self.generation)

    def initialize_generation(self, num_indices) -> list[int]:
        generation = []
        indices = [i for i in range(self.generation_size)]
        for _ in range(num_indices):
            shuffle(indices)
            generation.append(copy(indices))
        return generation

    def fitness_function(self, solution: list[int]) -> float:
        coords = [self.node_coords[i] for i in solution]
        return 1 / self.metric.evaluate_solution(coords)
    
    def mutate(self, solution: list[int], mutation_size: int=2) -> list[int]:
        new_solution = copy(solution)
        swap = sample(new_solution, k=2)
        temp = new_solution[swap[0]]
        new_solution[swap[0]] = new_solution[swap[1]]
        new_solution[swap[1]] = temp
        return new_solution
    
    def cross_over_single_point(self, solution1: list[int], solution2: list[int], cross_over_size: int=2) -> tuple[list[int], list[int]]:
        # Copy the solutions
        new_solution1 = copy(solution1)
        new_solution2 = copy(solution2)

        # Get the index to swap on
        swap_index = randint(1, len(self.node_coords)-1)

        # Random number to decide if front or back portion is picked
        # to make sure that front and back positions can be crossed over
        front = randint(0, 1)

        # Swap
        if front:
            new_solution1[:swap_index] = solution2[:swap_index]
            new_solution2[:swap_index] = solution1[:swap_index]
        else:
            new_solution1[-swap_index:] = solution2[-swap_index:]
            new_solution2[-swap_index:] = solution1[-swap_index:]

        # Edit non-swapped points to resolve constraints
        # In the segment that wasn't swapped, find any numbers that are in the swapped
        # segment and remove them. Then find the numbers that are missing from the organism.
        # Fill in the holes in the organism with the missing numbers in the order they show up
        # in the parent
        # e.g.
        #
        # organism     = [0, 3, 1, 2, 5, 6, 7, 4]
        # new_organism = [0, 3, 1, 2, 2, 6, 7, 1]
        #                             ^--------^
        #                            swapped portion
        # repeated numbers: 1, 2
        # missing numbers:  4, 5
        # since 5 comes before 4 in the parent
        #
        # new_organism = [0, 3, 5, 4, 2, 6, 7, 1]

        # Resolve solution1
        if front:
            swapped = new_solution1[:swap_index]
            not_swapped = [s for s in solution1 if s not in swapped]
            new_solution1[-len(new_solution1)+len(swapped):] = not_swapped

        else:
            swapped = new_solution1[-swap_index:]
            not_swapped = [s for s in solution1 if s not in swapped]
            new_solution1[:len(new_solution1)-len(swapped)] = not_swapped

        # Resolve solution2
        if front:
            swapped = new_solution2[:swap_index]
            not_swapped = [s for s in solution2 if s not in swapped]
            new_solution2[-len(new_solution2)+len(swapped):] = not_swapped

        else:
            swapped = new_solution2[-swap_index:]
            not_swapped = [s for s in solution2 if s not in swapped]
            new_solution2[:len(new_solution2)-len(swapped)] = not_swapped
        
        if not new_solution1 or not new_solution2:
            print(
                'swap_index:', swap_index,
                '\nfront:', front
            )

        return new_solution1, new_solution2
        

if __name__ == '__main__':
    from metric import EuclideanDistance
    points = [(0, 1), (1, 0), (3, 0), (6, 0), (6, 6)]
    x = GeneticAlgorithm([Point(x[0], x[1]) for x in points], EuclideanDistance())
    x.mutate(x.generation[0])
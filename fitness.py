from metric import Metric
from point import Point

class Fitness():
    """
    Class used for calculating the fitness score for
    each sequence in a generation
    """
    def __init__(self):
        pass

    def evaluate_generation(self, generation: list[list[int]]) -> float:
        raise NotImplementedError()

class TSP_Fitness(Fitness):
    """
    Fitness scoring for the Traveling Salesperson Problem
    Distance between every point in a sequence
    """
    def __init__(self, metric: Metric, node_coords: list[Point]):
        self.metric = metric
        self.node_coords = node_coords
    
    def distance(self, sequence: list[int]) -> float:
        """
        Distance between every point in a sequence
        """
        new_sequence = [self.node_coords[0]] + [self.node_coords[i] for i in sequence] + [self.node_coords[-1]]
        return self.metric.evaluate_sequence(new_sequence)
    
    def evaluate_generation(self, generation: list[list[int]]) -> list[float]:
        """
        Fitness score is 1 / distance of sequence
        This is so shorter distances have higher fitness scores
        """
        fitness_scores = []
        for sequence in generation:
            fitness_scores.append(self.distance(sequence))
        sum_fitness = sum(fitness_scores)
        return [f / sum_fitness for f in fitness_scores]
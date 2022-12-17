from point import Point
from random import random, choices

class Selection():
    def __init__(self):
        pass
    
    def select(self, generation: list[list[int]], fitness: list[float], num_selections: int) -> list[list[int]]:
        raise NotImplementedError()

class RouletteWheel(Selection):
    def __init__(self):
        pass

    def select(self, generation: list[list[int]], fitness_scores: list[float], num_selections: int) -> list[list[int]]:
        fitness_probability = []
        sum_fitness = sum(fitness_scores)
        for f in fitness_scores:
            fitness_probability.append(f / sum_fitness)
        
        selections = choices(
            generation,
            weights = fitness_probability,
            k = num_selections
        )
        
        return list(selections)

class Rank(Selection):
    def __init__(self):
        pass

    def select(node_coords: list[Point], fitness: list[float], num_selections: int) -> list[list[int]]:
        return node_coords[:num_selections]
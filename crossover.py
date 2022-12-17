from copy import copy
from random import randint

class Crossover():
    """
    Class that implements crossover for genetic algorithms
    """
    def __init__(self):
        pass

    def crossover(self):
        raise NotImplementedError()


class SinglePoint(Crossover):
    """
    Crossover where 1 point is picked and everything after/before that point
    is swapped with another sequence
    """
    def __init__(self):
        pass

    def crossover(self, parents: list[list[int]], cross_over_size: int=2) -> list[list[int]]:
        """
        Splits the parents into pairs and uses them for crossover
        """
        children = []
        for i in range(0, len(parents), 2):
            child1, child2 = self.cross(parents[i], parents[i+1], cross_over_size=cross_over_size)
            children += [child1, child2]
        return children

    def cross(self, sequence1: list[int], sequence2: list[int], cross_over_size: int=2) -> tuple[list[int], list[int]]:
        """
        Edit non-swapped points to resolve constraints
        In the segment that wasn't swapped, find any numbers that are in the swapped
        segment and remove them. Then find the numbers that are missing from the organism.
        Fill in the holes in the organism with the missing numbers in the order they show up
        in the parent
        e.g.
        
        organism     = [0, 3, 1, 2, 5, 6, 7, 4]
        new_organism = [0, 3, 1, 2, 2, 6, 7, 1]
                                    ^--------^
                                   swapped portion
        repeated numbers: 1, 2
        missing numbers:  4, 5
        since 5 comes before 4 in the parent
        
        new_organism = [0, 3, 5, 4, 2, 6, 7, 1]
        """

        # Copy the solutions
        new_sequence1 = copy(sequence1)
        new_sequence2 = copy(sequence2)

        # Get the index to swap on
        swap_index = randint(1, len(sequence1)-1)

        # Random number to decide if front or back portion is picked
        # to make sure that front and back positions can be crossed over
        front = randint(0, 1)

        # Swap
        if front:
            new_sequence1[:swap_index] = sequence2[:swap_index]
            new_sequence2[:swap_index] = sequence1[:swap_index]
        else:
            new_sequence1[-swap_index:] = sequence2[-swap_index:]
            new_sequence2[-swap_index:] = sequence1[-swap_index:]

        # Resolve solution1
        if front:
            swapped = new_sequence1[:swap_index]
            not_swapped = [s for s in sequence1 if s not in swapped]
            new_sequence1[-len(new_sequence1)+len(swapped):] = not_swapped

        else:
            swapped = new_sequence1[-swap_index:]
            not_swapped = [s for s in sequence1 if s not in swapped]
            new_sequence1[:len(new_sequence1)-len(swapped)] = not_swapped

        # Resolve solution2
        if front:
            swapped = new_sequence2[:swap_index]
            not_swapped = [s for s in sequence2 if s not in swapped]
            new_sequence2[-len(new_sequence2)+len(swapped):] = not_swapped

        else:
            swapped = new_sequence2[-swap_index:]
            not_swapped = [s for s in sequence2 if s not in swapped]
            new_sequence2[:len(new_sequence2)-len(swapped)] = not_swapped

        return new_sequence1, new_sequence2
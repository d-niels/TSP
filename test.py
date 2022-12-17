import unittest
from mutation import CutInsert
from crossover import SinglePoint
from random import shuffle
from copy import copy

def no_duplicates(sequence: list[int], size: int) -> bool:
        test_array = [1] * size
        for j in sequence:
            test_array[j] = test_array[j] * 0
        return sum(test_array) == 0

class TestMutate(unittest.TestCase):

    def test_cut_insert(self):
        mutation = CutInsert()
        sequence = [i for i in range(5)]
        for i in range(100):
            shuffle(sequence)
            mutated_sequence = mutation.mutate(sequence)

            self.assertNotEqual(tuple(sequence), tuple(mutated_sequence))
            self.assertTrue(no_duplicates(mutated_sequence, len(sequence)))

class TestCrossover(unittest.TestCase):

    def test_single_point(self):
        crossover = SinglePoint()
        sequence = [i for i in range(5)]
        for i in range(100):
            shuffle(sequence)
            seq1 = copy(sequence)
            shuffle(sequence)
            seq2 = copy(sequence)
            new1, new2 = crossover.crossover(seq1, seq2)

            self.assertTrue(no_duplicates(new1, len(sequence)))
            self.assertTrue(no_duplicates(new2, len(sequence)))


if __name__ == '__main__':
    unittest.main()
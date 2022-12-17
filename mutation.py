from random import randint
from copy import copy

class Mutation():
    def __init__(self):
        pass
    
    def mutate(self, sequence: list[int]) -> list[int]:
        raise NotImplementedError()

class CutInsert(Mutation):
    def __init__(self, cut_size=1):
        self.cut_size = 1
    
    def mutate(self, sequence: list[int]) -> list[int]:
        new_sequence = copy(sequence)
        cut_index = randint(0, len(new_sequence)-1)
        cut = new_sequence.pop(cut_index)
        insert_index = randint(0, len(new_sequence))
        while insert_index == cut_index:
            insert_index = randint(0, len(new_sequence))
        new_sequence.insert(insert_index, cut)
        return new_sequence
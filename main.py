import matplotlib.pyplot as plt
from random import randint
from point import Point
from metric import *
from solver import BruteForce
from selection import *
from crossover import *
from mutation import *
from fitness import *
from ga import GeneticAlgorithm

VISUALIZE = True
NUM_EPOCHS = 10000

if VISUALIZE:
    from display import Display

def initialize_points(
    num_points: int,
    xlim: tuple[int, int] = (0, 800),
    ylim: tuple[int, int] = (0, 600)
) -> list[Point]:
    """
    Function used to initialize nodes for the graph structure
    Generates points within a specific window size given by xlim and ylim
    """
    point_coords = []
    for _ in range(num_points):
        x = randint(xlim[0], xlim[1])
        y = randint(ylim[0], ylim[1])
        point_coords.append(Point(x=x, y=y))
    return point_coords


if __name__ == '__main__':
    # Initialize nodes, solver, and display
    node_coords = initialize_points(10)
    fitness = TSP_Fitness(
        EuclideanDistance(),
        node_coords
    )
    solver = GeneticAlgorithm(
        selection = RouletteWheel(),
        crossover = SinglePoint(),
        mutation = CutInsert(),
        fitness = fitness,
        generation_size = 25,
        sequence_length = len(node_coords)-2
    )

    if VISUALIZE:
        screen = Display(node_coords)
        screen.fit(node_coords)
    
    # Run the simulation
    best_list = []
    current_list = []
    for _ in range(NUM_EPOCHS):
        err = ''
        solver.step()
        current_list.append(1/solver.current_score)
        best_list.append(1/solver.best_score)

        if VISUALIZE:
            current_sequence = [node_coords[0]] + [node_coords[i] for i in solver.current_sequence] + [node_coords[-1]]
            best_sequence = [node_coords[0]] + [node_coords[i] for i in solver.best_sequence] + [node_coords[-1]]
            err = screen.update(current_sequence, best_sequence)
        if err or solver.finished:
            print(err)
            break

    # if solver.finished:
    #     screen.idle()
    
    # Plot the solution metrics over time
    plt.plot([1/x for x in current_list], label='current')
    plt.plot([1/x for x in best_list], label='best')
    plt.title('Performance over time')
    plt.ylabel('Metric')
    plt.xlabel('Epochs')
    plt.legend()
    plt.show()


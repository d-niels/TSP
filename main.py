import matplotlib.pyplot as plt
from random import randint
from display import Display
from point import Point
from metric import *
from solver import *

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
    for i in range(num_points):
        x = randint(xlim[0], xlim[1])
        y = randint(ylim[0], ylim[1])
        point_coords.append(Point(x=x, y=y))
    return point_coords

if __name__ == '__main__':
    # Initialize nodes, solver, and display
    node_coords = initialize_points(10)
    metric = EuclideanDistance()
    solver = BruteForce(node_coords, metric)
    screen = Display(node_coords)
    screen.fit(node_coords)
    
    # Run the simulation
    best_list = []
    current_list = []
    while not solver.finished:
        solver.step()
        current_list.append(solver.current)
        best_list.append(solver.best)
        err = screen.update(solver.current_solution, solver.best_solution)
        if err:
            print(err)
            break

    # if solver.finished:
    #     screen.idle()
    
    # Plot the solution metrics over time
    plt.plot(current_list, label='current')
    plt.plot(best_list, label='best')
    plt.title('Performance over time')
    plt.ylabel('Metric')
    plt.xlabel('Epochs')
    plt.legend()
    plt.show()


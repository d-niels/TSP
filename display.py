import pygame
from point import Point
from random import randint

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)

class Display():
    """
    Class for creating the pygame display
    """
    def __init__(self, node_coords: int):
        self.quit = False
        self.node_radius = 12
        self.current_line_width = 1
        self.best_line_width = 3
        self.window = pygame.display.set_mode((800, 600))
        self.fit(node_coords)

        # Initialize the window
        pygame.display.set_caption('TSP')
        self.window.fill(BLACK)
        pygame.display.flip()

    def fit(self, node_coords: list[Point]):
        """
        Calculate transforms so that the points span the whole screen
        """
        window_width, window_height = pygame.display.get_surface().get_size()
        self.min_x = min([n.x for n in node_coords])- window_width * 0.1
        self.max_x = max([n.x for n in node_coords]) + window_width * 0.1
        self.min_y = min([n.y for n in node_coords]) - window_height * 0.1
        self.max_y = max([n.y for n in node_coords]) + window_height * 0.1
        self.x_scale = window_width / (self.max_x - self.min_x)
        self.y_scale = window_height / (self.max_y - self.min_y)
    
    def transform_coords(self, node_coords: list[Point]) -> list[Point]:
        """
        Transforms the points to spread more across the screen
        """
        new_coords = []
        for coord in node_coords:
            new_x = (coord.x - self.min_x) * self.x_scale
            new_y = (coord.y - self.min_y) * self.y_scale
            new_coords.append((new_x, new_y))
        return new_coords

    def idle(self):
        """
        Allows the window to remain open until the exit button is pressed
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def update(self, current_coords: list[Point], best_coords: list[Point]) -> str:
        """
        Update the screen by updating the lines and redrawing everything
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'pygame window exited'

        # Start with a blank windown
        self.window.fill(BLACK)

        # Transform coordinates
        new_current_coords = self.transform_coords(current_coords)
        new_best_coords = self.transform_coords(best_coords)

        # Connect each node with a line
        current_line_coords = []
        best_line_coords = []
        for i in range(len(new_current_coords)-1):
            current_line_coords.append([new_current_coords[i], new_current_coords[i+1]])
            best_line_coords.append([new_best_coords[i], new_best_coords[i+1]])
        
        # Draw each line
        for i in range(len(current_line_coords)):
            pygame.draw.line(self.window, GRAY, current_line_coords[i][1], current_line_coords[i][0], width=self.current_line_width)
            pygame.draw.line(self.window, GREEN, best_line_coords[i][1], best_line_coords[i][0], width=self.best_line_width)
        
        # Draw each node
        self.nodes = []
        for coord in new_current_coords:
            node = pygame.draw.circle(self.window, RED, coord, self.node_radius)
            self.nodes.append(node)

        # Update display
        pygame.display.update()
        
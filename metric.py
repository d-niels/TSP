from point import Point

class Metric():
    """
    Metric used to evaluate a path
    """
    def calculate(self, point1: Point, point2: Point) -> float:
        """
        Function for calculating the metric between 2 Points
        """
        raise NotImplementedError()

    def evaluate_sequence(self, node_coords: list[Point]) -> float:
        """
        Function that calculates the metric over a whole path of Points
        """
        aggregate = 0
        for i in range(len(node_coords)-1):
            aggregate += self.calculate(node_coords[i], node_coords[i+1])
        aggregate += self.calculate(node_coords[0], node_coords[-1])
        return aggregate


class EuclideanDistance(Metric):
    """
    Euclidean distance
    """
    def calculate(self, point1: Point, point2: Point) -> float:
        return ((point1.x - point2.x)**2 + 
                (point1.y - point2.y)**2)**0.5

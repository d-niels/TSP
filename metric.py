from point import Point

class Metric():
    def calculate(self, point1: Point, point2: Point) -> float:
        raise NotImplementedError()

    def evaluate_solution(self, node_coords: list[Point]) -> float:
        aggregate = 0
        for i in range(len(node_coords)-1):
            aggregate += self.calculate(node_coords[i], node_coords[i+1])
        return aggregate

class EuclideanDistance(Metric):
    def calculate(self, point1: Point, point2: Point) -> float:
        return ((point1.x - point2.x)**2 + 
                (point1.y - point2.y)**2)**0.5

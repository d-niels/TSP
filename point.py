from dataclasses import dataclass

@dataclass
class Point:
    """
    Simply class for keeping track of (x, y) coords
    """
    x: int
    y: int
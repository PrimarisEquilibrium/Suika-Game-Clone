from enum import Enum

class Fruit(Enum):
    """Represents a Suika fruit with its properties.
    
    Attributes:
        id: Unique identifier for the fruit.
        radius: Radius of the fruit.
        mass: Mass of the fruit.
        color: RGB color of the fruit.
    """

    CHERRY     = (0, 12, 1.0, (239, 7, 10))
    STRAWBERRY = (1, 16, 1.2, (251, 108, 75))
    GRAPE      = (2, 24, 1.4, (166, 108, 252))
    DEKOPON    = (3, 30, 2.0, (255, 185, 2))
    ORANGE     = (4, 36, 2.5, (254, 140, 32))
    APPLE      = (5, 44, 3.0, (244, 22, 22))
    PEAR       = (6, 48, 3.2, (255, 249, 103))
    PEACH      = (7, 56, 3.5, (254, 203, 197))
    PINEAPPLE  = (8, 62, 4.5, (242, 243, 23))
    MELON      = (9, 70, 5.0, (162, 239, 30))
    WATERMELON = (10, 80, 6.0, (33, 126, 22))

    def __init__(self, id: int, radius: int, mass: int, color: tuple[int, int, int]) -> None:
        self.id = id
        self.radius = radius
        self.mass = mass
        self.color = color
import pygame
import random
import numpy
import pymunk
import pymunk.pygame_util
from typing import Any
from enum import Enum


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Relative coordinate landmarks
CTR_X = SCREEN_WIDTH / 2
CTR_Y = SCREEN_HEIGHT / 2
padding = 200  # Distance boundary sides are from the center of the screen
# Coordinates of the game boundary
LEFT = CTR_X - padding
TOP = CTR_Y + padding
BOTTOM = CTR_Y - padding
RIGHT = CTR_X + padding

# Pygame Config
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Frame / Game Loop Properties
FPS = 240.0
DT = 1.0 / FPS
steps_per_frame = 1

# Space Config
space = pymunk.Space()
space.gravity = (0.0, 900.0)


# Fruit(id, radius, mass, color)
class Fruit(Enum):
    """Represents a Suika fruit with its properties.
    
    Attributes:
        id: Unique identifier for the fruit.
        radius: Radius of the fruit.
        mass: Mass of the fruit.
        color: RGB color of the fruit.
    """

    CHERRY     = (0,  10, 1.0, (255, 0, 0)),
    STRAWBERRY = (1,  12, 1.2, (255, 105, 180)),
    GRAPE      = (2,  14, 1.4, (128, 0, 128)),
    DEKOPON    = (3,  18, 2.0, (255, 165, 0)),
    ORANGE     = (4,  20, 2.5, (255, 165, 0)),
    APPLE      = (5,  25, 3.0, (255, 0, 0)),
    PEAR       = (6,  28, 3.2, (173, 255, 47)),
    PEACH      = (7,  30, 3.5, (255, 218, 185)),
    PINEAPPLE  = (8,  35, 4.5, (255, 255, 0)),
    MELON      = (9,  40, 5.0, (196, 254, 91)),
    WATERMELON = (10, 50, 6.0, (0, 255, 0)),

    def __init__(self, id: int, radius: int, mass: int, color: tuple[int, int, int]) -> None:
        self.id = id
        self.radius = radius
        self.mass = mass
        self.color = color


def create_static_boundaries() -> None:
    """Initializes the game boundary with static line segments"""

    static_body = space.static_body
    static_lines = [
        pymunk.Segment(static_body, (LEFT, TOP), (LEFT, BOTTOM), 5.0),
        pymunk.Segment(static_body, (RIGHT, TOP), (RIGHT, BOTTOM), 5.0),
        pymunk.Segment(static_body, (LEFT, TOP), (RIGHT, TOP), 5.0),
    ]
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9
    space.add(*static_lines)


def create_circle(mass: int, radius: int, position: tuple[int, int], **custom_data: dict[str, Any]) -> None:
    """Adds a circle with the given properties to the Pymunk physics space.
    
    Args:
        mass: The mass of the circle.
        radius: The radius of the circle.
        position: The initial position of the circle.
        custom_data: Additional custom attributes to add to the circle Shape.
    """

    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position

    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0
    shape.friction = 0.8
    shape.collision_type = 1

    # Add custom attributes to the shape
    for key, value in custom_data.items():
        setattr(shape, key, value)

    space.add(body, shape)


def create_random_fruit(position: tuple[int, int]) -> None:
    fruit = random.choice(list(Fruit))
    create_circle(fruit.mass, fruit.radius, position, custom_data={"fruit": fruit})


def delete_shapes_pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict[Any, Any]) -> bool:
    """Deletes two shapes if they collide using Pymunk collision handling.
    
    Args:
        arbiter: Information about the two collided shapes.
        space: The space the collision occured in.
        data: Additional information required for handling the collision.
    
    Returns:
        True, as the collision has been processed.
    """
    shape1, shape2 = arbiter.shapes

    # Delete both the shape and the body
    space.remove(shape1, shape1.body)
    space.remove(shape2, shape2.body)

    return True  # Collision should be processed


def spawn_new_fruit_post_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict[Any, Any]) -> bool:
    """Spawns a new shape at the contact point between two collided shapes
    
    Args:
        arbiter: Information about the two collided shapes.
        space: The space the collision occured in.
        data: Additional information required for handling the collision.
    
    Returns:
        True, as the collision has been processed.
    """
    contact_point = arbiter.contact_point_set.points[0].point_a
    new_x, new_y = contact_point[0], contact_point[1]
    # create_circle(50, 25, (new_x, new_y))

    return True


def draw_fruit(fruit: Fruit, position: tuple[int, int]) -> None:
    """Renders a fruit to the screen.
    
    Args:
        fruit: The type of Fruit to draw.
        position: The position to draw the fruit.
    """

    pygame.draw.circle(screen, fruit.color, position, fruit.radius)


# Collision configuration
handler = space.add_collision_handler(1, 1)
handler.pre_solve = delete_shapes_pre_solve
handler.post_solve = spawn_new_fruit_post_solve

create_static_boundaries()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, _ = pygame.mouse.get_pos()
            mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT - 10)
            create_random_fruit((mouse_x, 50))

    screen.fill("black")

    mouse_x, _ = pygame.mouse.get_pos()
    mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT - 10)
    
    pygame.draw.circle(screen, "white", (mouse_x, 50), 25)
    
    for _ in range(1):
        space.step(DT)

    # Render shapes in the Pymunk space
    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            fruit = shape.custom_data['fruit']  # Extract the fruit attribute from the shape
            position = shape.body.position
            draw_fruit(fruit, position)
        if isinstance(shape, pymunk.Segment):
            pygame.draw.line(screen, "white", shape.a, shape.b, 5)

    # space.debug_draw(options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
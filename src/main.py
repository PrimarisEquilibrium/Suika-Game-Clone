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
# Distance boundary sides are from the center of the screen
X_RATIO = 5
Y_RATIO = 6
RATIO_SCALE = min(SCREEN_HEIGHT / 18, SCREEN_WIDTH / 32)
x_padding = X_RATIO * RATIO_SCALE
y_padding = Y_RATIO * RATIO_SCALE
# Coordinates of the game boundary
LEFT = CTR_X - x_padding
TOP = CTR_Y + y_padding
BOTTOM = CTR_Y - y_padding
RIGHT = CTR_X + x_padding

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


def create_fruit(fruit: Fruit, position: tuple[int, int]) -> None:
    """Creates a fruit with its attributes.

    Note: ('fruit' custom_data is already assigned)
    
    Args:
        fruit: The fruit to spawn.
        position: The position of the fruit.
    """
    create_circle(fruit.mass, fruit.radius, position, custom_data={"fruit": fruit})


def get_fruit_from_shape(shape: pymunk.Shape) -> Fruit:
    return shape.custom_data["fruit"]


def get_fruits_from_shape(*shapes: pymunk.Shape) -> list[Fruit]:
    fruits = []
    for shape in shapes:
        fruits.append(get_fruit_from_shape(shape))
    return fruits


MAX_FRUIT_TO_SPAWN = Fruit.APPLE
def create_random_fruit(position: tuple[int, int]) -> None:
    fruit = random.choice(list(Fruit))
    while fruit.id > MAX_FRUIT_TO_SPAWN.id:
        fruit = random.choice(list(Fruit))
    create_fruit(fruit, position)


def handle_fruit_collision(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict[Any, Any]) -> bool:
    """Handles fruit collisions
    
    Args:
        arbiter: Information about the two collided shapes.
        space: The space the collision occured in.
        data: Additional information required for handling the collision.
    
    Returns:
        True, as the collision has been processed.
    """
    shape1, shape2 = arbiter.shapes
    fruit1, fruit2 = get_fruits_from_shape(shape1, shape2)

    if fruit1.id == fruit2.id:
        next_fruit_id = fruit1.id + 1
        for fruit in Fruit:
            if fruit.id == next_fruit_id:
                # Delete original fruits
                space.remove(shape1, shape1.body)
                space.remove(shape2, shape2.body)

                # Spawn new fruit at the contact point of the two collided fruits
                contact_point = arbiter.contact_point_set.points[0].point_a
                new_x, new_y = contact_point[0], contact_point[1]
                create_fruit(fruit, (new_x, new_y))

    return True  # Collision should be processed


def draw_fruit(fruit: Fruit, position: tuple[int, int]) -> None:
    """Renders a fruit to the screen.
    
    Args:
        fruit: The type of Fruit to draw.
        position: The position to draw the fruit.
    """

    pygame.draw.circle(screen, fruit.color, position, fruit.radius)


def render_pymunk_space(space: pymunk.Space) -> None:
    """Renders the Pymunk space.
    
    Note: Only handles Fruits and Segments

    Args:
        space: The Pymunk space to render.

    """

    for shape in space.shapes:
        if isinstance(shape, pymunk.Circle):
            # If circle is a fruit
            if hasattr(shape, "custom_data") and "fruit" in shape.custom_data:
                fruit = get_fruit_from_shape(shape)
                position = shape.body.position
                draw_fruit(fruit, position)
        if isinstance(shape, pymunk.Segment):
            pygame.draw.line(screen, "white", shape.a, shape.b, 5)


# Collision configuration
handler = space.add_collision_handler(1, 1)
handler.pre_solve = handle_fruit_collision

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

    render_pymunk_space(space)

    # space.debug_draw(options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
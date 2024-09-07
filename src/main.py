import pygame
import numpy
import pymunk
import pymunk.pygame_util
from typing import Any


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

options = pymunk.pygame_util.DrawOptions(screen)

# DrawOptions Dev Flags
options.flags |= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS


def create_static_boundaries() -> None:
    """Initializes the game boundary with static line segments"""

    static_body = space.static_body
    static_lines = [
        pymunk.Segment(static_body, (LEFT, TOP), (LEFT, BOTTOM), 6.0),
        pymunk.Segment(static_body, (RIGHT, TOP), (RIGHT, BOTTOM), 6.0),
        pymunk.Segment(static_body, (LEFT, TOP), (RIGHT, TOP), 6.0),
    ]
    for line in static_lines:
        line.elasticity = 0.95
        line.friction = 0.9
    space.add(*static_lines)


def create_circle(mass: int, radius: int, position: tuple[int, int]) -> None:
    """Adds a circle with the given properties to the PyMunk physics space.
    
    Args:
        mass: The mass of the circle.
        radius: The radius of the circle.
        position: The initial position of the circle.
    """

    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = position

    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0
    shape.friction = 0.8
    shape.collision_type = 1

    space.add(body, shape)
    

def delete_shapes_pre_solve(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict[Any, Any]) -> bool:
    """Deletes two shapes if they collide using PyMunk collision handling.
    
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
    create_circle(50, 25, (new_x, new_y))


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
            mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT + 10)
            create_circle(50, 25, (mouse_x, 50))

    screen.fill("black")

    mouse_x, _ = pygame.mouse.get_pos()
    mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT + 10)
    
    pygame.draw.circle(screen, "white", (mouse_x, 50), 25)
    
    for _ in range(1):
        space.step(DT)

    space.debug_draw(options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
import pygame
import numpy
import pymunk
import pymunk.pygame_util

from config import SCREEN_WIDTH, SCREEN_HEIGHT, LEFT, RIGHT, MAX_FRUIT_TO_SPAWN
from fruits import Fruit, draw_fruit, create_fruit, create_random_fruit
from physics import create_static_boundaries, handle_fruit_collision


pygame.init()

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

# Collision configuration
handler = space.add_collision_handler(1, 1)
handler.pre_solve = handle_fruit_collision


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
                fruit = Fruit.get_fruit_from_shape(shape)
                position = shape.body.position
                draw_fruit(screen, fruit, position)
        if isinstance(shape, pymunk.Segment):
            pygame.draw.line(screen, "white", shape.a, shape.b, 5)


create_static_boundaries(space)
current_fruit = create_random_fruit(MAX_FRUIT_TO_SPAWN)
on_cooldown = False
cooldown_timer = 0
cooldown_duration = 500 # In ms
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not on_cooldown:
                # Create the fruit at the mouse location
                mouse_x, _ = pygame.mouse.get_pos()
                mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT - 10)
                create_fruit(space, current_fruit, (mouse_x, 50))
                
                # Change current fruit to spawn and start a cooldown timer
                current_fruit = create_random_fruit(MAX_FRUIT_TO_SPAWN)
                on_cooldown = True
                cooldown_timer = pygame.time.get_ticks()

    screen.fill("black")

    # Once cooldown_duration passes turn off the cooldown
    if pygame.time.get_ticks() - cooldown_timer >= cooldown_duration:
        on_cooldown = False
    
    # Only render the preview fruit when the cooldown is over
    if not on_cooldown:
        mouse_x, _ = pygame.mouse.get_pos()
        mouse_x = numpy.clip(mouse_x, LEFT + 10, RIGHT - 10)
        draw_fruit(screen, current_fruit, (mouse_x, 50))
    
    for _ in range(1):
        space.step(DT)

    render_pymunk_space(space)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
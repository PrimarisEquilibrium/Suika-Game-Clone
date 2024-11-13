import pygame
import numpy
import pymunk
import pymunk.pygame_util
from typing import Any

from config import SCREEN_WIDTH, SCREEN_HEIGHT, LEFT, RIGHT, MAX_FRUIT_TO_SPAWN, ENDGAME_BOUNDARY_Y
from fruits import Fruit, draw_fruit, create_fruit, create_random_fruit
from physics import create_static_boundaries


pygame.init()

# Pygame Config
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font('freesansbold.ttf', 32)

# Frame / Game Loop Properties
FPS = 240.0
DT = 1.0 / FPS
steps_per_frame = 1

# Space Config
space = pymunk.Space()
space.gravity = (0.0, 900.0)

# Player score
score = 0


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


def is_shape_over_end_boundary(shape: pymunk.Shape) -> bool:
    """Determines if a shape passed the end boundary y-position.
    
    Args:
        shape: A pymunk shape.
    
    Returns:
        True, if the shape collides with the end boundary; otherwise false.
    """

    return shape.point_query((shape.body.position.x, ENDGAME_BOUNDARY_Y)).distance < 0


def handle_fruit_collision(arbiter: pymunk.Arbiter, space: pymunk.Space, data: dict[Any, Any]) -> bool:
    """Handles fruit collisions
    
    Args:
        arbiter: Information about the two collided shapes.
        space: The space the collision occured in.
        data: Additional information required for handling the collision.
    
    Returns:
        True, as the collision has been processed.
    """
    global score, running
    shape1, shape2 = arbiter.shapes
    fruit1, fruit2 = Fruit.get_fruits_from_shape(shape1, shape2)

    # Computes the distance the shape is away from the y-pos of the endgame boundary
    # A value less than 0 means the shape intersects the endgame boundary
    is_shape1_over = is_shape_over_end_boundary(shape1)
    is_shape2_over = is_shape_over_end_boundary(shape2)

    if (is_shape1_over or is_shape2_over):
        print("GAME OVER!")
    
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
                create_fruit(space, fruit, (new_x, new_y))

                score += fruit.score

    return True  # Collision should be processed

# Collision configuration
handler = space.add_collision_handler(1, 1)
handler.pre_solve = handle_fruit_collision

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

    text = font.render(f"Score: {score}", True, "white")
    textRect = text.get_rect()
    textRect.center = (150, 75)
    screen.blit(text, textRect)

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
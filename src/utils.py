import pymunk
import pygame
import pickle
from typing import Any, Union

from config import ENDGAME_BOUNDARY_Y


class Button:
    def __init__(self, position: tuple[int, int], width: int, height: int, text: str) -> None:
        self.x, self.y = position
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self, screen: pygame.Surface) -> None:
        button = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (52, 52, 52), button)
        create_text(screen, self.text, 24, "white", button.center)
    
    def is_mouse_over(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x + self.width and mouse_y <= self.y + self.height:
            return True
        return False


def create_circle(space: pymunk.Space, mass: int, radius: int, position: tuple[int, int], **custom_data: dict[str, Any]) -> None:
    """Adds a circle with the given properties to the Pymunk physics space.
    
    Args:
        space: The Pymunk space to add the circle in.
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


def create_text(screen: pygame.Surface, text: str, font_size: int, color: Union[tuple[int, int, int], str], position: tuple[int, int]) -> None:
    """Outputs the given text to the pygame window.
    
    Args:
        screen: The screen to draw to.
        font_size: The font_size of the text.
        position: The position to draw the text.
    """

    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    x, y = position
    textRect.center = (x, y)
    screen.blit(text, textRect)


def set_local_highscore(score: int) -> None:
    scoreFile = "score.data"
    fw = open(scoreFile, "wb")
    pickle.dump(score, fw)
    fw.close()


def load_local_highscore() -> None:
    scoreFile = "score.data"
    try:
        fd = open(scoreFile, "rb")
        score = pickle.load(fd)
    except FileNotFoundError:
        score = 0
        set_local_highscore(score)
    return score


def is_shape_over_end_boundary(shape: pymunk.Shape) -> bool:
    """Determines if a shape passed the end boundary y-position.
    
    Args:
        shape: A pymunk shape.
    
    Returns:
        True, if the shape collides with the end boundary; otherwise false.
    """

    return shape.point_query((shape.body.position.x, ENDGAME_BOUNDARY_Y)).distance < 0


def draw_circle_image(screen: pygame.Surface, image_path: str, position: tuple[int, int], radius: int):
    # Load and scale the image
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (radius * 2, radius * 2))

    # Create a circle surface
    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, "white", (radius, radius), radius)

    # Blit the image onto the circle surface
    circle_surface.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Get the rectangle for positioning
    x, y = position
    circle_rect = circle_surface.get_rect(center=(x, y))


    # Draw the circle with the image on the screen
    screen.blit(circle_surface, circle_rect.topleft)
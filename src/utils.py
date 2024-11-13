import pymunk
import pygame
from typing import Any, Union


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
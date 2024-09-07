import pygame
import numpy
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Suika container ratio is 4:5
WIDTH = 400
HEIGHT = 500
CTR_X = SCREEN_WIDTH / 2
CTR_Y = SCREEN_HEIGHT / 2

# Coordinate positions of each corner of the Suika container
LEFT = CTR_X - (WIDTH / 2)
RIGHT = LEFT + WIDTH
TOP = CTR_Y - (HEIGHT / 2)
BOTTOM = TOP + HEIGHT

# Thickness of the container
BORDER_WIDTH = 10

TEMP_FRUIT_RADIUS = 25
fruits = []
class Fruit:
    def __init__(self, init_x: int, init_y: int) -> None:
        self.x = init_x
        self.y = init_y
        self.radius = TEMP_FRUIT_RADIUS
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

    def in_bounds(self) -> bool:
        return (
            self.x - self.radius >= LEFT 
            and self.x + self.radius <= RIGHT
            # and self.y - self.radius > TOP 
            and self.y + self.radius <= BOTTOM
        )

    def update(self) -> None:
        if self.in_bounds():
            self.y += 5

FPS = 60.0
DT = 1.0 / FPS
space = pymunk.Space()
space.gravity = (0.0, 900.0)
options = pymunk.pygame_util.DrawOptions(screen)
steps_per_frame = 1

mass = 10
radius = 25
inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
body = pymunk.Body(mass, inertia)
body.position = (100, 100)
shape = pymunk.Circle(body, 10)
shape.elasticity = 0.8
shape.friction = 0.9
space.add(body, shape)

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Fruit initially dropped at mouse-x (clamped to Suika container dimensions) and constrained y-position
            fruit_x = numpy.clip(pygame.mouse.get_pos()[0], LEFT + TEMP_FRUIT_RADIUS, RIGHT - TEMP_FRUIT_RADIUS)
            dropped_fruit = Fruit(fruit_x, 75)
            if dropped_fruit.in_bounds():
                fruits.append(dropped_fruit)

        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # # Basic cursor to show where the fruit will drop
    # mouse_x = numpy.clip(pygame.mouse.get_pos()[0], LEFT + TEMP_FRUIT_RADIUS, RIGHT - TEMP_FRUIT_RADIUS)
    # pygame.draw.circle(screen, "white", (mouse_x, 75), 25)

    # # Render Suika container
    # pygame.draw.rect(screen, "white", pygame.rect.Rect(
    #     LEFT - BORDER_WIDTH, 
    #     TOP - BORDER_WIDTH, 
    #     WIDTH + BORDER_WIDTH * 2, 
    #     HEIGHT + BORDER_WIDTH * 2
    # ))
    # pygame.draw.rect(screen, "black", pygame.rect.Rect(LEFT, TOP, WIDTH, HEIGHT))

    # for fruit in fruits:
    #     fruit.draw(screen)
    #     fruit.update()
    
    for _ in range(1):
        space.step(DT)

    space.debug_draw(options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
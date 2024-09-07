import pygame
import pymunk
import pymunk.pygame_util


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Relative coordinate landmarks
CTR_X = SCREEN_WIDTH / 2
CTR_Y = SCREEN_HEIGHT / 2

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
    shape.friction = 0.4

    space.add(body, shape)


create_circle(10, 25, (CTR_X, 50))

# Game container boundaries
static_body = space.static_body
padding = 200
static_lines = [
    pymunk.Segment(static_body, (CTR_X - padding, CTR_Y + padding), (CTR_X - padding, CTR_Y - padding), 6.0),
    pymunk.Segment(static_body, (CTR_X + padding, CTR_Y + padding), (CTR_X + padding, CTR_Y - padding), 6.0),
    pymunk.Segment(static_body, (CTR_X - padding, CTR_Y + padding), (CTR_X + padding, CTR_Y + padding), 6.0),
]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 0.9
space.add(*static_lines)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    
    for _ in range(1):
        space.step(DT)

    space.debug_draw(options)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
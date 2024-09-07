import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Frame / Game Loop Properties
FPS = 60.0
DT = 1.0 / FPS
steps_per_frame = 1

# Space Config
space = pymunk.Space()
space.gravity = (0.0, 900.0)

options = pymunk.pygame_util.DrawOptions(screen)

# DrawOptions Dev Flags
options.flags |= pymunk.SpaceDebugDrawOptions.DRAW_COLLISION_POINTS

# Demo Circle
mass = 10
radius = 25
inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
body = pymunk.Body(mass, inertia)
body.position = (100, 100)
shape = pymunk.Circle(body, radius, (0, 0))
shape.elasticity = 0.8
shape.friction = 0.4
space.add(body, shape)

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
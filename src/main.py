import pygame
import numpy

pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

fruits = []
class Fruit:
    def __init__(self, init_x: int, init_y: int) -> None:
        self.x = init_x
        self.y = init_y
        self.radius = 25
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)

    def in_bounds(self) -> bool:
        return (
            self.x - self.radius > 0 
            and self.x + self.radius < WIDTH
            and self.y - self.radius > 0 
            and self.y + self.radius < HEIGHT
        )

    def update(self) -> None:
        if self.in_bounds():
            self.y += 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Fruit initially dropped at mouse-x and constrained y-position 
            dropped_fruit = Fruit(pygame.mouse.get_pos()[0], 75)
            if dropped_fruit.in_bounds():
                fruits.append(dropped_fruit)

        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, "white", (mouse_x, 75), 25)

    for fruit in fruits:
        fruit.draw(screen)
        fruit.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
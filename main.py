#gravity simulation

from scipy.constants import gravitational_constant as G
from scipy.constants import astronomical_unit as Au
import numpy as np
import math
import pygame

class Body:
    def __init__(self, initial_position, initial_velocity, mass, radius) -> None:
        self.position = initial_position
        self.velocity = initial_velocity
        self.mass = mass
        self.radius = radius

    def resolve_velocity(self, m, p, mult):
        grav = (G * (m * self.mass)) / ((np.linalg.norm(p-self.position))**2)
        force = grav * ((p-self.position) / np.linalg.norm(p-self.position))
        self.velocity = self.velocity + (force / self.mass) * mult
        self.position = self.position + self.velocity * mult

      
pygame.init()
screen = pygame.display.set_mode((1000, 1000))

sun = Body(np.array([0, 0]), np.array([0, 0]), (1.989 * 10**30), 50)
earth_vel = math.sqrt((G * sun.mass) / Au)
earth = Body(np.array([0, Au]), np.array([earth_vel, 0]), (5.9722 * 10**24), 10)

 

#let 1 AU = 100 pix
def pixelise(position):
    scale = 200 / Au
    x=position[0] * scale
    y = position[1] * scale
    return (x+500, y+500)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, (255, 165, 0), pixelise(sun.position), sun.radius)
    pygame.draw.circle(screen, (0, 255, 100), pixelise(earth.position), earth.radius)
    pygame.display.flip()

    clock.tick(60)

    earth.resolve_velocity(sun.mass, sun.position, 35040)
    print(pixelise(earth.position))

pygame.quit()
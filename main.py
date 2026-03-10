#gravity simulation

from scipy.constants import gravitational_constant as G
from scipy.constants import astronomical_unit as Au
import numpy as np
import math
import pygame

class Body:
    def __init__(self, initial_position, initial_velocity, mass, radius, color=(255, 255, 255)) -> None:
        self.position = initial_position
        self.velocity = initial_velocity
        self.mass = mass
        self.radius = radius
        self.color = color
        self.temp_force = np.array([0, 0])
    
    def resolve_force(self, bodies):
        for b in bodies:
            if np.linalg.norm(b.position-self.position) != 0:
                grav = (G * (b.mass * self.mass)) / ((np.linalg.norm(b.position-self.position))**2)
                self.temp_force = self.temp_force + grav * ((b.position-self.position) / np.linalg.norm(b.position-self.position))

    def resolve_velocity(self, mult):
        self.velocity = self.velocity + (self.temp_force / self.mass) * mult
        self.position = self.position + self.velocity * mult
        self.temp_force = np.array([0, 0])
        
pygame.init()
screen = pygame.display.set_mode((1000, 1000))


sunmass = (1.989 * 10**30)
sun_vel = math.sqrt((G * sunmass) / Au) / 2
mars_vel = math.sqrt((G * sunmass) / (1.5 * Au))
earth_vel = math.sqrt((G * sunmass) / Au)


sun = Body(np.array([0, 0]), np.array([0, 0]), sunmass, 50, (255, 165, 0))
earth = Body(np.array([Au, 0]), np.array([0, earth_vel]), (5.9722 * 10**24), 15, (0, 255, 100))
mars = Body(np.array([0, -1.5 * Au]), np.array([-mars_vel, 0]), (6.4191 * 10**23), 10, (200, 0, 75))
evil_sun = Body(np.array([0, Au]), np.array([-sun_vel, 0]), sun.mass * 45/50, 45, (150, 10, 200))

all_bodies = [sun, earth, mars]

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

    clock.tick(60)
    for b in all_bodies:
        b.resolve_force(all_bodies)
    for b in all_bodies:
        b.resolve_velocity(17520)
        pygame.draw.circle(screen, b.color, pixelise(b.position), b.radius)
    pygame.display.flip()
    print(pixelise(sun.position))

# Quit Pygame
pygame.quit()

import pygame

class Ball:
    def __init__(self, center, radius, colour):
        self.center = center
        self.radius = radius
        self.colour = colour

    def draw(self, window):
        pygame.draw.circle(window, self.colour, self.center, self.radius)
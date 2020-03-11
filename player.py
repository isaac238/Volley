import pygame


class Player:

    def __init__(self, x, y, width, height, colour, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)
        self.score = score

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def move(self):
        while self.y < pygame.mouse.get_pos()[1] and self.y < 325:
                self.y += 1
        while self.y > pygame.mouse.get_pos()[1] and self.y < 325:
                self.y -= 1
        if self.y >= 325:
            self.y = 324

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def getScore(self):
        return self.score

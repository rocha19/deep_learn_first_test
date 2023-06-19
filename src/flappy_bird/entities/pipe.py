import pygame
import os
import random

PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets/imgs', 'pipe.png')))


class Pipe:
    DISTANCE = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top_pos = 0
        self.bottom_pos = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_pos = self.height - self.PIPE_TOP.get_height()
        self.bottom_pos = self.height + self.DISTANCE

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top_pos))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom_pos))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        distance_top = (self.x - bird.x, self.top_pos - round(bird.y))
        distance_bottom = (self.x - bird.x, self.bottom_pos - round(bird.y))

        top_point = bird_mask.overlap(top_mask, distance_top)
        bottom_point = bird_mask.overlap(bottom_mask, distance_bottom)

        if bottom_point or top_point:
            return True
        else:
            return False

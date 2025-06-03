import pygame
import random
from config import *

class Food:
    def __init__(self):
        self.position = (
            random.randint(FOOD_RADIUS, WIDTH - FOOD_RADIUS),
            random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)
        )

    def draw(self, screen):
        pygame.draw.circle(screen, FOOD_COLOR, self.position, FOOD_RADIUS)
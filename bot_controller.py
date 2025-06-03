import random
import pygame
from snake import Snake
from utils import find_closest_food
from config import *

class Bot(Snake):
    def __init__(self):
        super().__init__(is_bot=True)
        self.body = [
            (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        ]

    def update(self, _, foods):
        if not foods:
            return

        closest = find_closest_food(self.body[0], foods)
        head = pygame.Vector2(self.body[0])
        direction = (pygame.Vector2(closest.position) - head).normalize()
        new_head = head + direction * self.speed
        self.body.insert(0, (new_head.x, new_head.y))

        if len(self.body) > self.length:
            self.body.pop()

def create_bots(amount):
    return [Bot() for _ in range(amount)]
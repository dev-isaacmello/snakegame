import pygame
import math
from config import *
from utils import distance

class Snake:
    def __init__(self, is_bot=False):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.length = 1
        self.speed = BOT_SPEED if is_bot else SNAKE_SPEED
        self.radius = SNAKE_RADIUS
        self.color = BOT_COLOR if is_bot else PLAYER_COLOR
        self.direction = pygame.Vector2(1, 0)
        self.is_bot = is_bot

    def update(self, target_pos):
        if self.is_bot:
            return

        target = pygame.Vector2(target_pos)
        head = pygame.Vector2(self.body[0])
        direction = (target - head).normalize()
        new_head = head + direction * self.speed
        self.body.insert(0, (new_head.x, new_head.y))

        if len(self.body) > self.length:
            self.body.pop()

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.circle(screen, self.color, (int(segment[0]), int(segment[1])), self.radius)

    def eat(self, food):
        head = pygame.Vector2(self.body[0])
        food_pos = pygame.Vector2(food.position)
        if distance(head, food_pos) < self.radius + FOOD_RADIUS:
            self.length += 5
            return True

    def head_position(self):
        return pygame.Vector2(self.body[0])

    def collides_with_head(self, other):
        return (self.head_position() - other.head_position()).length() < self.radius * 2

    def collides_with_body(self, other):
        # Não verifica o primeiro segmento (cabeça)
        for segment in other.body[1:]:
            if (self.head_position() - pygame.Vector2(segment)).length() < self.radius + other.radius:
                return True
        return False
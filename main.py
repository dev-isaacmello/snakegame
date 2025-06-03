import pygame
from config import *
from snake import Snake
from food import Food
from bot_controller import create_bots

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Slither.io Clone")

player = Snake(is_bot=False)
foods = [Food() for _ in range(30)]
bots = create_bots(5)

def get_camera_offset(player):
    head_x, head_y = player.body[0]
    offset_x = min(max(head_x - WINDOW_WIDTH // 2, 0), WIDTH - WINDOW_WIDTH)
    offset_y = min(max(head_y - WINDOW_HEIGHT // 2, 0), HEIGHT - WINDOW_HEIGHT)
    return offset_x, offset_y

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    offset_x, offset_y = get_camera_offset(player)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    map_mouse_pos = (mouse_x + offset_x, mouse_y + offset_y)
    player.update(map_mouse_pos)
    for bot in bots:
        bot.update(None, foods)

    foods_to_remove = []
    foods_to_add = []

    for food in foods:
        food_screen_pos = (food.position[0] - offset_x, food.position[1] - offset_y)
        pygame.draw.circle(screen, FOOD_COLOR, food_screen_pos, FOOD_RADIUS)
        if player.eat(food):
            if food not in foods_to_remove:
                foods_to_remove.append(food)
                foods_to_add.append(Food())
        for bot in bots:
            if bot.eat(food):
                if food not in foods_to_remove:
                    foods_to_remove.append(food)
                    foods_to_add.append(Food())

    for food in foods_to_remove:
        if food in foods:
            foods.remove(food)
    foods.extend(foods_to_add)

    snakes = [player] + bots
    snakes_to_remove = set()
    for i, snake1 in enumerate(snakes):
        for j, snake2 in enumerate(snakes):
            if i == j or snake2 in snakes_to_remove or snake1 in snakes_to_remove:
                continue
            if snake1.collides_with_head(snake2):
                snakes_to_remove.add(snake1)
                snakes_to_remove.add(snake2)
            elif snake1.collides_with_body(snake2):
                snake2.length += len(snake1.body)
                snakes_to_remove.add(snake1)

    for snake in snakes_to_remove:
        if snake is player:
            running = False
        elif snake in bots:
            bots.remove(snake)

    def draw_snake(snake):
        for segment in snake.body:
            seg_screen = (int(segment[0] - offset_x), int(segment[1] - offset_y))
            pygame.draw.circle(screen, snake.color, seg_screen, snake.radius)

    draw_snake(player)
    for bot in bots:
        draw_snake(bot)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
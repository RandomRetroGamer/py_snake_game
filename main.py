import pygame
import time
import random
import json
from appy import f 


config = f.fancy.read_config(f.config.path)
width = config.get("window_x", 800)
height = config.get("window_y", 600)


grid_width = width // f.snake_game.cell_size
grid_height = height // f.snake_game.cell_size


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(" --- random --- ")
fps = pygame.time.Clock()


fruit_position = [
    random.randint(0, grid_width - 1) * f.snake_game.cell_size,
    random.randint(0, grid_height - 1) * f.snake_game.cell_size
]


def read_high_score(file_path, new_score):
    config = f.fancy.read_config(file_path)
    current_score = config.get("high_score", 0)
    if new_score > current_score:
        config["high_score"] = new_score
        f.fancy.write_config(file_path, config)
        print(f"New high score saved: {new_score}")
    else:
        print(f"High score not updated (current: {current_score}, new: {new_score})")


def show_Score(color, font, size, screen, current_score):
    score_font = pygame.font.SysFont(font, size)
    high_score = f.fancy.read_config(f.config.path).get("high_score", 0)
    score_text = f"Score : {current_score}  High Score : {high_score}"
    score_surface = score_font.render(score_text, True, color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_surface, score_rect)


def game_over():
    read_high_score(f.config.path, f.snake_game.score)
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your score is: ' + str(f.snake_game.score), True, f.color.red)
    game_over_rect = game_over_surface.get_rect(center=(width / 2, height / 4))
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()


def draw_grid(surface, width, height, cell_size, color):
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, color, (0, y), (width, y))


running = True
while running:
    screen.fill((0, 0, 0)) 


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                f.snake_game.change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                f.snake_game.change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                f.snake_game.change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                f.snake_game.change_to = 'RIGHT'


    if f.snake_game.change_to == 'UP' and f.snake_game.direction != 'DOWN':
        f.snake_game.direction = 'UP'
    if f.snake_game.change_to == 'DOWN' and f.snake_game.direction != 'UP':
        f.snake_game.direction = 'DOWN'
    if f.snake_game.change_to == 'LEFT' and f.snake_game.direction != 'RIGHT':
        f.snake_game.direction = 'LEFT'
    if f.snake_game.change_to == 'RIGHT' and f.snake_game.direction != 'LEFT':
        f.snake_game.direction = 'RIGHT'


    if f.snake_game.direction == 'UP':
        f.snake_game.snake_position[1] -= f.snake_game.cell_size
    if f.snake_game.direction == 'DOWN':
        f.snake_game.snake_position[1] += f.snake_game.cell_size
    if f.snake_game.direction == 'LEFT':
        f.snake_game.snake_position[0] -= f.snake_game.cell_size
    if f.snake_game.direction == 'RIGHT':
        f.snake_game.snake_position[0] += f.snake_game.cell_size

    f.snake_game.snake_body.insert(0, list(f.snake_game.snake_position))


    if f.snake_game.snake_position == fruit_position:
        f.snake_game.score += 10
        f.snake_game.fruit_spawn = False
    else:
        f.snake_game.snake_body.pop()

    if not f.snake_game.fruit_spawn:
        fruit_position = [
            random.randint(0, grid_width - 1) * f.snake_game.cell_size,
            random.randint(0, grid_height - 1) * f.snake_game.cell_size
        ]
    f.snake_game.fruit_spawn = True


    for pos in f.snake_game.snake_body:
        pygame.draw.rect(screen, f.color.green, pygame.Rect(pos[0], pos[1], f.snake_game.cell_size, f.snake_game.cell_size))


    pygame.draw.rect(screen, f.color.white, pygame.Rect(fruit_position[0], fruit_position[1], f.snake_game.cell_size, f.snake_game.cell_size))

    if f.snake_game.snake_position[0] < 0 or f.snake_game.snake_position[0] >= width or \
       f.snake_game.snake_position[1] < 0 or f.snake_game.snake_position[1] >= height:
        game_over()

    for block in f.snake_game.snake_body[1:]:
        if f.snake_game.snake_position == block:
            game_over()

    show_Score(f.color.white, 'times new roman', 20, screen, f.snake_game.score)
    draw_grid(screen, width, height, f.snake_game.cell_size, (40, 40, 40))
    pygame.display.update()
    fps.tick(f.snake_game.snake_speed)

pygame.quit()

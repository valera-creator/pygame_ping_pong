import pygame
import random
import os
from player import Player
from ball import Ball


def start_game():
    """функция для показа стартового окна"""
    pass


def end_game():
    """функция для показа финального окна"""


def check_keyboard(event, player1, player2):
    if event.key == pygame.K_w:
        player1.need_go = True
        player1.click = True
        return

    if event.key == pygame.K_UP:
        player2.need_go = True
        player2.click = True
        return

    if event.key == pygame.K_SPACE:
        return 'color'


if __name__ == '__main__':
    running = True

    width, height = 1000, 600
    fps = 60
    colors = {0: 'black', 1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'fuchsia', 6: 'white'}
    cur_color = 0

    pygame.init()

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()

    Ball(width=width, height=height, all_sprites=all_sprites, ball_sprites=ball_sprites)
    player1 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='violet', width=width, height=height)
    player2 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='yellow', width=width, height=height)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Максим Зайцев')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                res = check_keyboard(event, player1, player2)
                if res == 'color':
                    cur_color += 1
        cur_color = cur_color % len(list(colors.keys()))
        screen.fill(colors[cur_color])
        player_sprites.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

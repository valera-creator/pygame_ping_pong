import pygame
import os

from pygame import mixer

from player import Player
from ball import Ball


def start_game():
    """функция для показа стартового окна"""
    pass


def end_game(player_name):
    """функция для показа финального окна"""
    pass


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


def render_text(screen, size, x, y, text):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, pygame.Color("red"))
    text_x = x
    text_y = y
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    running = True

    width, height = 1050, 600
    fps = 60
    colors = {0: 'black', 1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'fuchsia', 6: 'white'}
    cur_color = 0
    start_seconds = 3  # задержка при начале раунда
    goal_end = 5

    pygame.init()
    sound = mixer.Sound(os.path.join('assets', 'sounds', 'background.mp3'))

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()

    ball = Ball(width=width, height=height, all_sprites=all_sprites, ball_sprites=ball_sprites)
    player1 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='violet', width=width, height=height)
    player2 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='yellow', width=width, height=height)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('PING-PONG game')

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 600)

    start_game()
    sound.play()
    mixer.music.set_volume(0.1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and start_seconds <= 0:
                res = check_keyboard(event, player1, player2)
                if res == 'color':
                    cur_color += 1
            if event.type == pygame.USEREVENT and start_seconds >= 0:
                start_seconds -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_5:
                if sound.get_busy():
                    sound.pause()
                else:
                    sound.unpause()

        cur_color = cur_color % len(list(colors.keys()))
        screen.fill(colors[cur_color])
        player_sprites.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        if start_seconds > 0:
            render_text(screen=screen, size=45, x=width // 2 - 10, y=100, text=str(start_seconds))
        if start_seconds < 0:
            ball.update()

        pygame.display.flip()

        if player1.cnt_goals == goal_end:  # передаем в end_game какой игрок, чтобы потом указать на стороне победителя
            end_game(player1.color_name)
        elif player2.cnt_goals == goal_end:
            end_game(player2.color_name)

    sound.stop()

    pygame.quit()

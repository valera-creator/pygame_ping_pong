import pygame
import os
from player import Player
from ball import Ball
from border import Border


def start_game(screen, width, height):
    bkground = os.path.join('assets', 'images', 'phon.jpg')
    fon = pygame.transform.scale(pygame.image.load(bkground), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coords_y = 125
    intro_text = ["ЦЕЛЬ:", "5 ГОЛОВ", "Правила игры:", "1) ЗАБИТЬ ГОЛ ПРОТИВНИКУ", "2) НАСЛАЖДАТЬСЯ ИГРОЙ", "", "",
                  "Авторы:", "Ларионов Валерий", "Зайцев Максим"]
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        coords_y += 5
        intro_rect.top = coords_y
        intro_rect.x = width // 2.5
        coords_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


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

    width, height = 1050, 600  # 1280 720
    fps = 60
    colors = {0: 'black', 1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'fuchsia', 6: 'white'}
    cur_color = 0
    start_seconds = 3  # задержка при начале раунда
    goal_end = 5

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('PING-PONG game')

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 600)
    start_game(screen, width, height)

    # sound = mixer.Sound(os.path.join('assets', 'sounds', 'background.mp3'))
    # sound.play()
    # mixer.music.set_volume(0.1)

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    ball = Ball(width=width, height=height, all_sprites=all_sprites, ball_sprites=ball_sprites)
    player1 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='blue', width=width, height=height, horizontal_borders=horizontal_borders)
    player2 = Player(all_sprites=all_sprites, player_sprites=player_sprites,
                     color_image='red', width=width, height=height, horizontal_borders=horizontal_borders)

    # x
    x = 56
    y = 70
    delta_x = 4
    delta_y = 5

    Border(all_sprites=all_sprites, horizontal_borders=horizontal_borders, vertical_borders=vertical_borders, x1=x,
           y1=y, x2=x, y2=height - y)
    Border(all_sprites=all_sprites, horizontal_borders=horizontal_borders, vertical_borders=vertical_borders,
           x1=width - x - delta_x, y1=y, x2=width - x - delta_x, y2=height - y)
    # y

    Border(all_sprites=all_sprites, horizontal_borders=horizontal_borders, vertical_borders=vertical_borders,
           x1=x, y1=y - delta_y, x2=width - x, y2=y - delta_y)
    Border(all_sprites=all_sprites, horizontal_borders=horizontal_borders, vertical_borders=vertical_borders,
           x1=x, y1=height - y, x2=width - x, y2=height - y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and start_seconds <= 0:
                res = check_keyboard(event, player1, player2)
                if res == 'color':
                    cur_color += 1
            if event.type == pygame.USEREVENT and start_seconds >= 0:
                start_seconds -= 1

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_5:
            #         if sound.get_busy():
            #             sound.pause()
            #         else:
            #             sound.unpause()

        cur_color = cur_color % len(list(colors.keys()))
        screen.fill(colors[cur_color])
        player_sprites.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        if start_seconds > 0:
            render_text(screen=screen, size=45, x=width // 2 - 10, y=25, text=str(start_seconds))
        if start_seconds <= 0:
            render_text(screen=screen, size=45, x=width // 2 - 20, y=25,
                        text=f'{player1.cnt_goals}-{player2.cnt_goals}')
            ball.update()

        pygame.display.flip()

        if player1.cnt_goals == goal_end:  # передаем в end_game какой игрок, чтобы потом указать на стороне победителя
            end_game(player1.color_name)
        elif player2.cnt_goals == goal_end:
            end_game(player2.color_name)

    pygame.quit()

import pygame
import os

from player import Player
from ball import Ball
from border import Border


def check_keyboard(event):
    """проверяет нажатие игроками управление своим объектом или нажатие изменения цвета фона"""
    if event.key == pygame.K_w:
        return 'player1'

    if event.key == pygame.K_UP:
        return 'player2'

    if event.key == pygame.K_SPACE:
        return 'color'


class Game:
    def __init__(self):
        self.width, self.height = 1280, 720
        self.fps = 60
        self.colors = {0: 'black', 1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'fuchsia', 6: 'white'}
        self.cur_color = 0
        self.start_seconds = 3  # задержка при начале раунда
        self.goal_end = 3

        # звук гола
        self.sound_goal = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'goal.mp3'))
        self.sound_goal.set_volume(0.01)

        # звук победы
        self.sound_winner = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'winner.mp3'))
        self.sound_winner.set_volume(0.25)

        # музыка на фон
        self.music_volume = 0.03
        self.step_volume_music = 0.025

        # звук удара мяча
        self.sound_rebound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'rebound.mp3'))
        self.sound_rebound.set_volume(0.20)

        self.cur_index_music = 2
        self.musics = {
            0: os.path.join('assets', 'sounds', 'fon1.mp3'),
            1: os.path.join('assets', 'sounds', 'fon2.mp3'),
            2: os.path.join('assets', 'sounds', 'fon3.mp3'),
            3: os.path.join('assets', 'sounds', 'fon4.mp3'),
            4: os.path.join('assets', 'sounds', 'fon5.mp3'),
            5: os.path.join('assets', 'sounds', 'fon6.mp3'),
            6: os.path.join('assets', 'sounds', 'fon7.mp3'),
            7: os.path.join('assets', 'sounds', 'fon8.mp3'),
            8: os.path.join('assets', 'sounds', 'fon9.mp3'),
        }
        self.is_misic_pause = False

        pygame.mixer.init()
        pygame.mixer.music.load(self.musics[self.cur_index_music])
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

        pygame.display.set_caption('PING-PONG game')
        pygame.time.set_timer(pygame.USEREVENT, 800)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.clock_speed_ball = pygame.time.Clock()

        # спрайты
        self.all_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()

        self.color_player1, self.color_player2 = 'blue', 'red'

        # мяч, игроки, стенки
        self.ball = Ball(width=self.width, height=self.height, all_sprites=self.all_sprites,
                         ball_sprites=self.ball_sprites, sound=self.sound_rebound, wall_sprites=self.horizontal_borders,
                         player_sprites=self.player_sprites)
        self.player1 = Player(all_sprites=self.all_sprites, player_sprites=self.player_sprites,
                              color_image=self.color_player1, width=self.width, height=self.height,
                              horizontal_borders=self.horizontal_borders)
        self.player2 = Player(all_sprites=self.all_sprites, player_sprites=self.player_sprites,
                              color_image=self.color_player2, width=self.width, height=self.height,
                              horizontal_borders=self.horizontal_borders)

        x = 56
        y = 70
        delta_x = 4
        delta_y = 5

        self.LEFT, self.RIGHT = -1, 1  # для движения мяча

        # x
        Border(all_sprites=self.all_sprites, horizontal_borders=self.horizontal_borders,
               vertical_borders=self.vertical_borders, x1=x,
               y1=y, x2=x, y2=self.height - y)
        Border(all_sprites=self.all_sprites, horizontal_borders=self.horizontal_borders,
               vertical_borders=self.vertical_borders,
               x1=self.width - x - delta_x, y1=y, x2=self.width - x - delta_x, y2=self.height - y)

        # y
        Border(all_sprites=self.all_sprites, horizontal_borders=self.horizontal_borders,
               vertical_borders=self.vertical_borders,
               x1=x, y1=y - delta_y, x2=self.width - x, y2=y - delta_y)
        Border(all_sprites=self.all_sprites, horizontal_borders=self.horizontal_borders,
               vertical_borders=self.vertical_borders,
               x1=x, y1=self.height - y, x2=self.width - x, y2=self.height - y)

    def start_game(self):
        """
        фразы в text_right нужны, чтобы отобразить их справа
        фразы в text_middle нужны, тчобы отобразить по середине
        intro_text - все фразы стартового окна
        """

        bkground = os.path.join('assets', 'images', 'phon.jpg')
        fon = pygame.transform.scale(pygame.image.load(bkground), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 35)
        coords_y = 85

        text_right = ['Авторы:', 'Ларионов Валерий', 'Зайцев Максим']
        text_middle = ['НАЖМИТЕ ЛЮБУЮ КЛАВИШУ, ЧТОБЫ ПРОДОЛЖИТЬ']
        intro_text = [
            "ЦЕЛЬ:",
            f"{self.goal_end} ГОЛА",
            "",
            "Правила игры:".upper(),
            "1) ЗАБИТЬ ГОЛ ПРОТИВНИКУ",
            "2) НАСЛАЖДАТЬСЯ ИГРОЙ",
            "",
            "Настройки:".upper(),
            "Для настройки звука во время игры прокрутите колесико мыши".upper(),
            "Для смены музыки во время игры нажмите ПКМ".upper(),
            "",
            "",
            "Авторы:",
            "Ларионов Валерий",
            "Зайцев Максим",
            "", "", "", "",  # 4 пустые строк
            "НАЖМИТЕ ЛЮБУЮ КЛАВИШУ, ЧТОБЫ ПРОДОЛЖИТЬ"
        ]

        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('WHITE'))
            intro_rect = string_rendered.get_rect()

            intro_rect.top = coords_y
            coords_y += 5

            if line in text_right:
                intro_rect.x = 950
            elif line in text_middle:
                intro_rect.x = 300
            else:
                intro_rect.x = 100
            coords_y += intro_rect.height

            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()

                if event.type == pygame.MOUSEWHEEL:
                    self.adjust_volume_sound(event.y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.replace_music(event.button)

                if event.type == pygame.KEYDOWN:
                    return
            pygame.display.flip()

    def make_event_start_second(self):
        """
        либо показывает либо таймер, если тикает таймер до начала раунда,
        либо показывает счет игры, снимает с паузы музыку и обновляет координаты мяча
        """

        if self.start_seconds > 0:
            self.render_text(size=45, text_x=self.width // 2 - 10, text_y=25,
                             text=str(self.start_seconds), color='green')
        if self.start_seconds <= 0:
            self.render_text(size=45, text_x=self.width // 2 - 20, text_y=25,
                             text=f'{self.player1.cnt_goals}-{self.player2.cnt_goals}', color='orange')
            if self.is_misic_pause:
                pygame.mixer.music.unpause()
                self.is_misic_pause = False

    def render_text(self, size, text_x, text_y, text, color='red'):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, pygame.Color(color))
        self.screen.blit(text, (text_x, text_y))

    def make_event_keyboard(self, player):
        """
        включает у объекта атрибуты-флаги движения и смены направления движения
        :param player: строковое представление игрока
        """

        if player == 'player1':
            self.player1.need_go = True
            self.player1.click = True
            return

        elif player == 'player2':
            self.player2.need_go = True
            self.player2.click = True
            return

    def check_goal(self):
        """
        возвращает объектное представление игрока, который забил гол или False, если гола нет
        """

        for elem in self.vertical_borders:
            if pygame.sprite.collide_mask(self.ball, elem):
                if elem.rect.x < self.width // 2:
                    return self.player2
                else:
                    return self.player1
        return False

    def make_event_goal(self, player):
        """
        установление таймера до начала раунда
        установление позиций для мяча и игроков
        отмена движений у игроков
        изменение времени и взаимодействие со звуком/музыкой
        изменение на стандарнтное значение скорости мяча
        :param player: объектное представление игрока для увеличение счетчика гола
        """

        self.start_seconds = 6
        self.ball.rect.x, self.ball.rect.y = (self.width // 2 - self.ball.size // 2,
                                              self.height // 2 - self.ball.size // 2)
        self.ball.make_move_value()
        player.cnt_goals += 1
        self.ball.side_move_x = self.LEFT if player.color_name == 'red' else self.RIGHT
        self.ball.make_move_value()

        self.player1.rect.x, self.player1.rect.y = self.player1.dict_coords[self.player1.color_name]
        self.player2.rect.x, self.player2.rect.y = self.player2.dict_coords[self.player2.color_name]
        self.player1.need_go = False
        self.player2.need_go = False
        self.player1.up = self.player1.down = False
        self.player2.up = self.player2.down = False
        self.player1.click = self.player2.click = False
        self.ball.cur_speed_ball = self.ball.speed_default

        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.mixer.music.pause()
        self.is_misic_pause = True
        self.ball.sound.stop()
        self.sound_goal.play()
        pygame.display.flip()

    def check_end_game(self):
        return self.player1.cnt_goals == self.goal_end or self.player2.cnt_goals == self.goal_end

    def make_event_end_game(self):
        """
        музыка на паузу
        остановка движений игроков и возвращение их на свои места
        изменение таймера и отмена звука гола (вместо нее будет звук победы)
        отрисовка спрайтов, надписи побителя
        окно победы и ожидание дальнейших действий от игроков
        """

        self.player1.need_go = False
        self.player2.need_go = False
        self.player1.up = self.player1.down = False
        self.player2.up = self.player2.down = False
        self.player1.click = self.player2.click = False
        self.ball.rect.x, self.ball.rect.y = (self.width // 2 - self.ball.size // 2,
                                              self.height // 2 - self.ball.size // 2)

        self.player1.rect.x, self.player1.rect.y = self.player1.dict_coords[self.player1.color_name]
        self.player2.rect.x, self.player2.rect.y = self.player2.dict_coords[self.player2.color_name]

        pygame.time.set_timer(pygame.USEREVENT, 800)
        self.sound_goal.stop()

        self.screen.fill(self.colors[self.cur_color])
        self.render_text(size=45, text_x=self.width // 2 - 20, text_y=25,
                         text=f'{self.player1.cnt_goals}-{self.player2.cnt_goals}', color='orange')
        self.all_sprites.draw(self.screen)

        if self.player1.cnt_goals == self.goal_end:
            self.render_text(size=45, text='WINNER', text_x=self.player1.rect.x + 47, text_y=100, color='blue')
        else:
            self.render_text(size=45, text='WINNER', text_x=self.player2.rect.x + 23, text_y=100, color='red')
        self.render_text(size=35, text='НАЖМИТЕ ЛЮБУЮ КЛАВИШУ, ЧТОБЫ ПРОДОЛЖИТЬ', text_x=self.width // 2 - 320,
                         text_y=self.height // 2 + 200, color='white')
        pygame.mixer.music.pause()
        self.ball.sound.stop()
        self.sound_winner.play(-1)
        self.ball.side_move_x = None
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.player1.cnt_goals = self.player2.cnt_goals = 0
                    self.sound_winner.stop()
                    pygame.mixer.music.unpause()
                    return
            pygame.display.flip()

    def adjust_volume_sound(self, direction):
        """
        если курсор мыши вверх, то прибавляем громкость, если курсор мыши вниз, то убавляем
        """

        if direction == 1:
            if round(self.music_volume + self.step_volume_music, 3) <= 1:
                self.music_volume += self.step_volume_music
        else:
            if round(self.music_volume - self.step_volume_music, 3) >= 0:
                self.music_volume -= self.step_volume_music
        self.music_volume = round(self.music_volume, 3)
        pygame.mixer.music.set_volume(self.music_volume)

    def replace_music(self, btn):
        """
        :param btn:  какая кнопка мыши нажата
        btn = 1 - левая
        btn = 3 - правая
        """

        if btn == 1:
            self.cur_index_music = (self.cur_index_music + 1) % len(list(self.musics.keys()))
            pygame.mixer.music.load(self.musics[self.cur_index_music])
            pygame.mixer.music.play(-1)
        elif btn == 3:
            self.cur_index_music = (self.cur_index_music - 1) % len(list(self.musics.keys()))
            pygame.mixer.music.load(self.musics[self.cur_index_music])
            pygame.mixer.music.play(-1)

    def run(self):
        self.start_game()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

                if event.type == pygame.MOUSEWHEEL:
                    self.adjust_volume_sound(event.y)

                if event.type == pygame.MOUSEBUTTONDOWN and self.start_seconds <= 0 or \
                        event.type == pygame.MOUSEBUTTONDOWN and self.player2.cnt_goals == self.player1.cnt_goals == 0:
                    self.replace_music(event.button)

                if event.type == pygame.KEYDOWN:
                    res = check_keyboard(event)
                    if res == 'color':
                        self.cur_color += 1
                    elif self.start_seconds <= 0:
                        self.make_event_keyboard(res)

                if event.type == pygame.USEREVENT and self.start_seconds >= 0:
                    self.start_seconds -= 1
                if event.type == pygame.USEREVENT and self.start_seconds < 0:
                    if round(self.ball.cur_speed_ball + self.ball.update_speed, 3) < self.ball.max_speed:
                        self.ball.cur_speed_ball = round(self.ball.cur_speed_ball + self.ball.update_speed, 3)

            self.cur_color = self.cur_color % len(list(self.colors.keys()))
            self.screen.fill(self.colors[self.cur_color])

            if self.start_seconds <= 0:
                self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.clock.tick(self.fps)
            self.make_event_start_second()

            player_goal = self.check_goal()
            if player_goal:
                self.make_event_goal(player_goal)

            if self.check_end_game():
                self.make_event_end_game()

            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

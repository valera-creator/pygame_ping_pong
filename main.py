import pygame
import os
from player import Player
from ball import Ball
from border import Border


def end_game(player_name):
    """функция для показа финального окна"""
    pass


def check_keyboard(event):
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
        self.goal_end = 5

        self.sound_goal = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'goal.mp3'))
        self.sound_goal.set_volume(0.2)

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()

        self.ball = Ball(width=self.width, height=self.height, all_sprites=self.all_sprites,
                         ball_sprites=self.ball_sprites)
        self.player1 = Player(all_sprites=self.all_sprites, player_sprites=self.player_sprites,
                              color_image='blue', width=self.width, height=self.height,
                              horizontal_borders=self.horizontal_borders)
        self.player2 = Player(all_sprites=self.all_sprites, player_sprites=self.player_sprites,
                              color_image='red', width=self.width, height=self.height,
                              horizontal_borders=self.horizontal_borders)

        x = 56
        y = 70
        delta_x = 4
        delta_y = 5

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
            f"{self.goal_end} ГОЛОВ",
            "",
            "Правила игры:",
            "1) ЗАБИТЬ ГОЛ ПРОТИВНИКУ",
            "2) НАСЛАЖДАТЬСЯ ИГРОЙ",
            "",
            "",
            "Авторы:",
            "Ларионов Валерий",
            "Зайцев Максим",
            "", "", "", "", "", "",  # 6 пустых строк
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
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()

    def make_even_start_second(self):
        if self.start_seconds > 0:
            self.render_text(size=45, text_x=self.width // 2 - 10, text_y=25,
                             text=str(self.start_seconds))
        if self.start_seconds <= 0:
            self.render_text(size=45, text_x=self.width // 2 - 20, text_y=25,
                             text=f'{self.player1.cnt_goals}-{self.player2.cnt_goals}')
            self.ball.update()

    def render_text(self, size, text_x, text_y, text):
        font = pygame.font.Font(None, size)
        text = font.render(text, True, pygame.Color("red"))
        self.screen.blit(text, (text_x, text_y))

    def make_even_keyboard(self, player):
        if player == 'player1':
            self.player1.need_go = True
            self.player1.click = True
            return

        elif player == 'player2':
            self.player2.need_go = True
            self.player2.click = True
            return

    def check_goal(self):
        """возвращает объектное представление игрока, который забил гол"""
        for elem in self.vertical_borders:
            if pygame.sprite.collide_mask(self.ball, elem):
                if elem.rect.x < self.width // 2:
                    return self.player2
                else:
                    return self.player1
        return False

    def make_event_goal(self, player):
        self.start_seconds = 3
        self.ball.rect.x, self.ball.rect.y = (self.width // 2 - self.ball.size // 2,
                                              self.height // 2 - self.ball.size // 2)
        player.cnt_goals += 1
        self.player1.rect.x, self.player1.rect.y = self.player1.dict_coords[self.player1.color_name]
        self.player2.rect.x, self.player2.rect.y = self.player2.dict_coords[self.player2.color_name]
        self.player1.need_go = False
        self.player2.need_go = False
        self.player1.up = self.player1.down = False
        self.player2.up = self.player2.down = False
        self.player1.click = self.player2.click = False
        pygame.time.set_timer(pygame.USEREVENT, 850)
        self.sound_goal.play()
        pygame.display.flip()

    def check_end_game(self):
        """возвращает строкое представление игрока, который выиграл"""
        if self.player1.cnt_goals == self.goal_end:
            return 'player1'
        elif self.player2.cnt_goals == self.goal_end:
            return 'player2'

    def run(self):
        self.start_game()
        pygame.display.set_caption('PING-PONG game')

        pygame.time.set_timer(pygame.USEREVENT, 600)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    res = check_keyboard(event)
                    if res == 'color':
                        self.cur_color += 1
                    elif self.start_seconds <= 0:
                        self.make_even_keyboard(res)

                if event.type == pygame.USEREVENT and self.start_seconds >= 0:
                    self.start_seconds -= 1

            self.cur_color = self.cur_color % len(list(self.colors.keys()))
            self.screen.fill(self.colors[self.cur_color])
            self.player_sprites.update()
            self.all_sprites.draw(self.screen)

            self.clock.tick(self.fps)
            self.make_even_start_second()

            pygame.display.flip()

            res = self.check_goal()
            if res:
                self.make_event_goal(res)

            self.check_end_game()

        pygame.quit()


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

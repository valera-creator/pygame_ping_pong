import pygame
import random
import os


def start_game():
    """функция для показа стартового окна"""
    pass


def end_game():
    """функция для показа финального окна"""


def check_keyboard(event, player1, player2):
    if event.key == pygame.K_w:
        player1.need_go = True
        player1.click = True
        # player1.update()
        return 'управление 1 игрока'
    if event.key == pygame.K_UP:
        player2.need_go = True
        player2.click = True
        return 'управление 2 игрока'


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(all_sprites, ball_sprites)
        self.size = 20
        self.image = pygame.image.load(os.path.join('assets', 'images', 'ball.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - self.size // 2, height // 2 - self.size // 2
        self.speed_nlo = 10

    def update(self, x, y):
        self.rect = self.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, color_image, width, height):
        super().__init__(all_sprites, player_sprites)

        self.color_image = color_image
        self.size = 40
        self.image = pygame.image.load(os.path.join('assets', 'images', f'{color_image}.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_player = 7
        self.rect = self.image.get_rect()

        self.up = False
        self.down = False
        self.need_go = False
        self.click = False

        dict_coords = {
            'violet': (width // 2 - width // 4 - 50 - self.size // 2, height // 2 - self.size // 2),
            'yellow': (width // 2 + width // 4 + 50, height // 2 - self.size // 2)
        }

        self.rect.x, self.rect.y = dict_coords[color_image]

    def update(self):
        """
        self.click используется для смены направления движения на противоположное
        self.up означает движение вверх
        self.down означает движение вниз
        self.need_go означает, что необходимо совершить движение у игрока

        в самом верху или низу не нужно делать смены,
        так как при достижении min/max возможных координат флаги меняются сами
        """

        if self.need_go:
            print(self.rect.y)
            if self.click and (self.up or self.down) and self.rect.y != 0 and self.rect.y != height - self.size:
                self.click = False
                self.up, self.down = self.down, self.up
            self.click = False

            if not self.up and not self.down:  # начало игры
                self.up = True
                self.rect.y -= self.speed_player

            if self.up:  # если движется вверх

                if self.rect.y >= 0:
                    self.rect.y -= self.speed_player
                else:
                    self.need_go = False
                    self.down = True
                    self.up = False

            if self.down:  # если движется вниз
                if self.rect.y + self.size < height:
                    self.rect.y += self.speed_player
                else:
                    self.need_go = False
                    self.up = True
                    self.down = False


if __name__ == '__main__':
    running = True

    width, height = 1000, 600
    fps = 60

    pygame.init()
    # pygame.key.set_repeat(1, 100)

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()

    Ball(width, height)
    player1 = Player(color_image='violet', width=width, height=height)
    player2 = Player(color_image='yellow', width=width, height=height)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Максим Зайцев')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                check_keyboard(event, player1, player2)

        screen.fill('black')
        player_sprites.update()
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

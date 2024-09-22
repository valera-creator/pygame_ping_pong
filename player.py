import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, color_image, width, height, all_sprites, player_sprites):
        super().__init__(all_sprites, player_sprites)

        self.color_image = color_image
        self.size = 40
        self.image = pygame.image.load(os.path.join('assets', 'images', f'{color_image}.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_player = 7
        self.height = height
        self.rect = self.image.get_rect()

        self.up = False
        self.down = False
        self.need_go = False
        self.click = False

        dict_coords = {
            'violet': (width // 2 - width // 4 - 50 - self.size // 2, self.height // 2 - self.size // 2),
            'yellow': (width // 2 + width // 4 + 50, self.height // 2 - self.size // 2)
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
            if self.click and (self.up or self.down) and self.rect.y != 0 and self.rect.y != self.height - self.size:
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
                if self.rect.y + self.size < self.height:
                    self.rect.y += self.speed_player
                else:
                    self.need_go = False
                    self.up = True
                    self.down = False

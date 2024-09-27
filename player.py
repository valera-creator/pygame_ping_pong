import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, color_image, width, height, all_sprites, player_sprites, horizontal_borders):
        super().__init__(all_sprites, player_sprites)

        self.color_name = color_image
        self.size = 200
        self.image = pygame.image.load(os.path.join('assets', 'images', f'{color_image}.png'))  # картинки нло
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed_player = 6
        self.height = height
        self.rect = self.image.get_rect()
        self.width = width
        self.horizontal_borders = horizontal_borders

        self.cnt_goals = 0
        self.up = False
        self.down = False
        self.need_go = False
        self.click = False

        dict_coords = {
            'blue': (self.width // 2 - self.width // 4 - 120 - self.size // 2, self.height // 2 - self.size // 2),
            'red': (self.width // 2 + self.width // 4 + 50, self.height // 2 - self.size // 2)
        }

        self.rect.x, self.rect.y = dict_coords[color_image]

    def check_intersection_walls(self):
        for elem in self.horizontal_borders:
            if pygame.sprite.collide_mask(self, elem):
                return True
        return False

    def check_distance(self, wall_sprites):
        pass

    def update(self):
        """
        self.click используется для смены направления движения на противоположное
        self.up означает движение вверх
        self.down означает движение вниз
        self.need_go означает, что необходимо совершить движение у игрока

        y1, y2 - когда не нужно менять направления из-за багов с границами сверху и снизу
        """
        y1, y2 = 29, 494

        if self.need_go:
            if self.click and (self.up or self.down) and y1 < self.rect.y < y2:
                self.click = False
                self.up, self.down = self.down, self.up
            self.click = False

            if not self.up and not self.down:  # начало игры
                self.up = True
                self.rect.y -= self.speed_player
                return

            if self.up:  # если движется вверх
                self.rect.y -= self.speed_player
                if self.check_intersection_walls():
                    self.rect.y += self.speed_player
                    self.need_go = False
                    self.down = True
                    self.up = False
                    return

            if self.down:  # если движется вниз
                self.rect.y += self.speed_player
                if self.check_intersection_walls():
                    self.rect.y -= self.speed_player
                    self.need_go = False
                    self.up = True
                    self.down = False
                    return

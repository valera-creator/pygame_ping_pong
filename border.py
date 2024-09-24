import pygame
import os


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, all_sprites, vertical_borders, horizontal_borders, x1, y1, x2, y2):
        super().__init__(all_sprites)

        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            sf = pygame.Surface((4, y2 - y1))
            sf.fill('WHITE')
            self.image = sf
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            sf = pygame.Surface((x2 - x1, 4))
            sf.fill('WHITE')
            self.image = sf
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

import pygame
import os
import random
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height, all_sprites, ball_sprites):
        super().__init__(all_sprites, ball_sprites)
        self.size = 20
        self.image = pygame.image.load(os.path.join('assets', 'images', 'ball.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - self.size // 2, height // 2 - self.size // 2
        self.speed_ball = 4

    def update(self):
        self.rect = self.rect.move(0, 0)  # рассчитать движение отскока


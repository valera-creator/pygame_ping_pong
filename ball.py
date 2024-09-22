import pygame
import os


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height, all_sprites, ball_sprites):
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

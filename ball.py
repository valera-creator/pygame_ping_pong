import pygame
import os
import random
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height, all_sprites, ball_sprites, sound, wall_sprites, player_sprites):
        super().__init__(all_sprites, ball_sprites)
        self.size = 32
        self.sound = sound
        self.wall_sprites = wall_sprites
        self.player_sprites = player_sprites
        self.image = pygame.image.load(os.path.join('assets', 'images', 'ball.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - self.size // 2, height // 2 - self.size // 2
        self.speed_ball = 3
        self.angle = random.randint(35, 60)
        self.dx = math.cos(math.radians(self.angle))
        self.dy = math.sin(math.radians(self.angle))

    def update(self):
        for elem in self.player_sprites:
            if pygame.sprite.collide_mask(self, elem):
                self.dx = -self.dx
                self.sound.play()

        for elem in self.wall_sprites:
            if pygame.sprite.collide_mask(self, elem):
                self.dy = -self.dy
                self.sound.play()

        self.rect = self.rect.move(self.dx * self.speed_ball, self.dy * self.speed_ball)  # рассчитать движение отскока

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
        self.side_move_x = None
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - self.size // 2, height // 2 - self.size // 2
        self.cur_speed_ball = 6
        self.update_speed = 0.15
        self.speed_default = 6
        self.max_speed = 15
        self.dx = self.dy = self.angle = 0
        self.make_move_value()

    def update(self):
        for elem in self.player_sprites:
            if pygame.sprite.collide_mask(self, elem):
                self.dx = -self.dx
                self.sound.play()
                break

        for elem in self.wall_sprites:
            if pygame.sprite.collide_mask(self, elem):
                self.dy = -self.dy
                self.sound.play()
                break

        self.rect = self.rect.move(self.dx * self.cur_speed_ball, self.dy * self.cur_speed_ball)

    def make_move_value(self):
        self.angle = random.randint(20, 45)
        if self.side_move_x is None:
            self.dx = math.cos(math.radians(self.angle)) * random.choice((-1, 1))
        else:
            self.dx = math.cos(math.radians(self.angle)) * self.side_move_x

        self.dy = math.sin(math.radians(self.angle)) * random.choice((-1, 1))

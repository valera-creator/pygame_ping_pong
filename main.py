import pygame
import random
import os


def start_game():
    """функция для показа стартового окна"""
    pass


def end_game():
    """функция для показа финального окна"""


def check_keyboard(event):
    if event.key == pygame.K_DOWN:
        print('test')
        return 'вниз1'
    if event.key == pygame.K_UP:
        return 'вверх1'
    if event.key == pygame.K_s:
        return 'вниз1'
    if event.key == pygame.K_w:
        return 'вверх2'


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(all_sprites, ball_sprites)
        self.size = 20
        self.image = pygame.image.load(os.path.join('assets', 'images', 'ball.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2 - self.size // 2, height // 2 - self.size // 2
        self.speed_x = 22
        self.speed_y = 22

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)


if __name__ == '__main__':
    running = True

    width, height = 800, 600
    fps = 60
    speed_nlo = 10

    pygame.init()
    pygame.key.set_repeat(1, 10)

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    ball_sprites = pygame.sprite.Group()
    Ball(width, height)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Максим Зайцев')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYUP:
                key = check_keyboard(event)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()

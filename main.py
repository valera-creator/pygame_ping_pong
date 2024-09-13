import pygame


def check_keyboard(event):
    if event.key == pygame.K_DOWN:
        return 'низ'
    if event.key == pygame.K_UP:
        return 'вверх'
    if event.key == pygame.K_LEFT:
        return 'лево'
    if event.key == pygame.K_RIGHT:
        return 'право'


def main():
    running = True
    WIDTH, HEIGHT = 800, 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Максим Зайцев')
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYUP:
                key = check_keyboard(event)
                print(key)
    pygame.quit()


if __name__ == '__main__':
    main()

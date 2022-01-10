import pygame


if __name__ == '__main__':
    pygame.init()
    size = (1200, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    background_image = pygame.image.load('arkanoid back.jpg')
    fps = 60

    running = True

    while running:  # Основной игровой цикл
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # обновление экрана
        screen.blit(background_image, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    # закрытие игры
    pygame.quit()
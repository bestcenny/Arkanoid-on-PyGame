import pygame


class Ball:
    def __init__(self, game_screen: pygame.Surface, coords: tuple, velocity=10, radius=20, color='white'):
        self.screen = game_screen
        self.x = coords[0]
        self.y = coords[1]
        self.vx = velocity / 2 ** 0.5
        self.vy = velocity / 2 ** 0.5
        self.radius = radius
        self.color = color

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen.get_height():
            self.vy = -self.vy
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen.get_width():
            self.vx = -self.vx

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)


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
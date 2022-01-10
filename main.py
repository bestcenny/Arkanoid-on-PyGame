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


class Paddle:
    # (self, game_screen: pygame.Surface, coord_x=568, coord_y=718,

    def __init__(self):
        self.paddle_image = pygame.image.load('paddleRed.png')
        self.rect = self.paddle_image.get_rect()
        self.x = 568
        self.y = 718

    # перемещение платформы по нажатию
    def move(self):
        key = pygame.key.get_pressed()
        speed = 10
        if key[pygame.K_RIGHT]:  # нажатие правой стрелки
            if (self.x + self.rect[2]) + speed >= SIZE[0]:
                self.x = SIZE[0] - self.rect[2]
            else:
                self.x += speed
        elif key[pygame.K_LEFT]:  # нажатие левой стрелки
            if self.x - speed <= 0:
                self.x = 0
            else:
                self.x -= speed

    def draw(self):
        screen.blit(self.paddle_image, (self.x, self.y))


SIZE = (1200, 750)
paddle = Paddle()





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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        paddle.move()
        # обновление экрана
        screen.blit(background_image, (0, 0))
        paddle.draw()
        pygame.display.flip()
        clock.tick(fps)

    # закрытие игры
    pygame.quit()
import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, game_screen: pygame.Surface, velocity=10):
        super().__init__()
        self.image = pygame.image.load('textures/ballGrey.png')
        self.screen = game_screen
        self.rect = self.image.get_rect()
        self.rect.center = (568, 600)
        self.vx = velocity / 2 ** 0.5
        self.vy = velocity / 2 ** 0.5
        self.radius = self.image.get_rect()[3] // 2
        print(self.image.get_rect()[3] // 2)
        print(screen.get_height())

    def update(self):
        self.rect.x += self.vx
        self.rect.y -= self.vy
        if self.rect.y - self.radius <= 0:
            self.vy = - self.vy
        if self.rect.x <= 0 or self.rect.x + self.radius * 2 >= self.screen.get_width():
            self.vx = - self.vx
        if self.rect.y + self.radius * 2 >= self.screen.get_height():
            self.kill()
        if (paddle.get_coords_x() <= self.rect.x <= paddle.get_coords_x() + paddle.get_size()[2])\
                and self.rect.y + self.radius * 2 >= paddle.get_coords_y():
            self.vy = - self.vy


class Paddle:
    # (self, game_screen: pygame.Surface, coord_x=568, coord_y=718,

    def __init__(self):
        self.paddle_image = pygame.image.load('textures/paddleRed.png')
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

    def get_coords_x(self):
        return self.x

    def get_coords_y(self):
        return self.y
    def get_size(self):
        return self.rect


SIZE = (1200, 750)
paddle = Paddle()

if __name__ == '__main__':
    pygame.init()
    size = (1200, 750)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    background_image = pygame.image.load('textures/arkanoid back.jpg')
    fps = 60

    running = True

    all_sprites = pygame.sprite.Group()
    all_sprites.add(Ball(screen))

    while running:  # Основной игровой цикл
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        all_sprites.update()
        paddle.move()
        # обновление экрана
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        paddle.draw()
        pygame.display.flip()
        clock.tick(fps)

    # закрытие игры
    pygame.quit()
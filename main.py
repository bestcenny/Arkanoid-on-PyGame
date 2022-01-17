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

    def update(self):
        self.rect.x += self.vx
        self.rect.y -= self.vy
        if self.rect.y < self.radius:
            self.vy = - self.vy
        if self.rect.x <= 0 or self.rect.x + self.radius * 2 >= self.screen.get_width():
            self.vx = - self.vx
        if self.rect.y + self.radius * 2 >= self.screen.get_height():
            self.kill()
        if (paddle.get_coords_x() <= self.rect.x <= paddle.get_coords_x() + paddle.get_size()[2])\
                and self.rect.y + self.radius * 2 >= paddle.get_coords_y():
            self.vy = - self.vy


class Paddle(pygame.sprite.Sprite):
    # (self, game_screen: pygame.Surface, coord_x=568, coord_y=718,

    def __init__(self, game_screen: pygame.Surface):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('textures/paddleRed.png')
        self.rect = self.image.get_rect()
        self.rect.center = (568, 718)

    def update(self):
        key = pygame.key.get_pressed()
        speed = 10
        if key[pygame.K_RIGHT]:  # нажатие правой стрелки
            if (self.rect.x + self.rect[2]) + speed >= SIZE[0]:
                self.rect.x = SIZE[0] - self.rect[2]
            else:
                self.rect.x += speed
        elif key[pygame.K_LEFT]:  # нажатие левой стрелки
            if self.rect.x - speed <= 0:
                self.rect.x = 0
            else:
                self.rect.x -= speed

    def get_coords_x(self):
        return self.rect.x

    def get_coords_y(self):
        return self.rect.y

    def get_size(self):
        return self.rect


class Brick(pygame.sprite.Sprite):
    def __init__(self, game_screen: pygame.Surface, x, y, brick_color: int):
        super().__init__()
        self.screen = screen
        self.x, self.y = x, y
        self.image = pygame.image.load(f'textures/{PADDLE_COLORS[brick_color]}')
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.left, self.right = self.rect[0], self.rect[2]
        self.top, self.bottom = self.rect[1], self.rect[3]

    def update(self):
        if self.left <= ball.rect.x <= self.right and \
                self.top <= ball.rect.x <= self.bottom:
            self.kill()


PADDLE_COLORS = {0: 'element_blue_rectangle.png',
                 1: 'element_grey_rectangle.png', 2: 'element_purple_rectangle.png',
                 3: 'element_red_rectangle.png', 4: 'element_yellow_rectangle.png'}

SIZE = (1200, 750)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    background_image = pygame.image.load('textures/arkanoid back.jpg')
    fps = 60

    running = True
    print(pygame.image.load('textures/element_purple_rectangle.png').get_rect()[2])
    bricks = pygame.sprite.Group()
    color_variations = 0
    brick_rect = pygame.image.load('textures/element_purple_rectangle.png').get_rect()
    for y in range(70, SIZE[1] // 2, brick_rect[3] + 5):
        if color_variations == 5:
            break
        for x in range(brick_rect[2] // 2 + 10, SIZE[0], brick_rect[2] + 10):
            bricks.add(Brick(screen, x, y, color_variations))
        color_variations += 1

    all_sprites = pygame.sprite.Group()
    ball = Ball(screen)
    all_sprites.add(ball)
    paddle = Paddle(screen)
    all_sprites.add(paddle)

    while running:  # Основной игровой цикл
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        bricks.update()
        all_sprites.update()
        # обновление экрана
        screen.blit(background_image, (0, 0))
        bricks.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

    # закрытие игры
    pygame.quit()
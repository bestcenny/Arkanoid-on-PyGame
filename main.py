import pygame
import sys


pygame.init()


# класс шарик
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
        self.pause = 0
        self.copied_speeds = (self.vx, self.vy)

    # взаимодействие шарика с различными поверхностями
    def update(self):
        global IS_BALL_KILLED
        self.rect.x += self.vx
        self.rect.y -= self.vy
        # отскакивание от стен
        if self.rect.colliderect(0, 1, SIZE[0], 1):
            self.vy = -self.vy
        if self.rect.x <= 0 or self.rect.x + self.radius * 2 >= self.screen.get_width():
            self.vx = - self.vx
        if self.rect.y + self.radius * 2 >= self.screen.get_height():
            self.kill()
            IS_BALL_KILLED = True
        # отскакивание от платформы
        if ball.rect.colliderect(paddle):
            self.vy = - self.vy
        # отскакивание от блоков
        if pygame.sprite.spritecollideany(self, bricks):
            i = pygame.sprite.spritecollideany(self, bricks)
            if self.vx > 0:
                delta_x = self.rect.right - i.rect.left
            else:
                delta_x = i.rect.right - self.rect.left
            if self.vy > 0:
                delta_y = i.rect.bottom - self.rect.top
            else:
                delta_y = self.rect.bottom - i.rect.top
            # столкновение с углом блока
            if abs(delta_x - delta_y) < 2:
                self.vx, self.vy = -self.vx, -self.vy
            # столкновение с верхней/нижней гранью
            elif delta_x > delta_y:
                self.vy = -self.vy
            # столкновение с левой/правой гранью
            elif delta_y > delta_x:
                self.vx = -self.vx

    # останавливает передвижение шарика при вызове функции в основном цикле
    def is_moving(self, is_paused: bool):
        if self.vx != 0:
            self.copied_speeds = self.vx, self.vy
        if is_paused:
            self.vx, self.vy = 0, 0
        else:
            self.vx, self.vy = self.copied_speeds


class Paddle(pygame.sprite.Sprite):

    def __init__(self, game_screen: pygame.Surface):
        super().__init__()
        self.screen = game_screen
        self.image = pygame.image.load('textures/paddleRed.png')
        self.rect = self.image.get_rect()
        self.rect.center = (568, 718)
        self.speed = 15
        self.copied_speed = 15

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:  # нажатие правой стрелки
            if (self.rect.x + self.rect[2]) + self.speed >= SIZE[0]:
                self.rect.x = SIZE[0] - self.rect[2]
            else:
                self.rect.x += self.speed
        elif key[pygame.K_LEFT]:  # нажатие левой стрелки
            if self.rect.x - self.speed <= 0:
                self.rect.x = 0
            else:
                self.rect.x -= self.speed

    # останавливает передвижение платформы при вызове функции в основном цикле
    def is_moving(self, is_paused: bool):
        if is_paused:
            self.speed = 0
        else:
            self.speed = self.copied_speed


class Brick(pygame.sprite.Sprite):
    def __init__(self, game_screen: pygame.Surface, coord_x, coord_y, brick_color: int):
        super().__init__()
        self.screen = game_screen
        self.x, self.y = coord_x, coord_y
        self.image = pygame.image.load(f'textures/{PADDLE_COLORS[brick_color]}')
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    # удаление блока из группы спрайтов при взаимодействии с ним шарика
    def update(self):
        if ball.rect.colliderect(self.rect):
            self.kill()


class Button:
    def __init__(self, game_screen: pygame.Surface, coord_x, coord_y, text: str):
        self.screen = game_screen
        self.inactive_button = 'textures/buttonDefault.jpg'
        self.active_button = 'textures/buttonSelected.jpg'
        self.width = 190
        self.height = 49
        self.image = pygame.image.load(self.inactive_button)
        self.rect = self.image.get_rect()
        self.center = coord_x, coord_y
        self.text = text

    def update(self, is_paused):

        # останавливает шарик и платформу, при повторном нажатии игра продолжается
        if is_paused:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            font = pygame.font.SysFont('calibri', 300 // len(self.text))
            message = font.render(self.text, True, 'black')

            # меняет цвет кнопки при наведении мышкой, при нажатии игра начинается с начала
            if self.center[0] - self.width // 2 < mouse[0] < self.center[0] + self.width // 2 and \
                    self.center[1] - self.height // 2 < mouse[1] < self.center[1] + self.height // 2:
                self.image = pygame.image.load(self.active_button)
                self.screen.blit(self.image, (self.center[0] - self.width // 2, self.center[1] - self.height // 2))
                if click[0] == 1:
                    main()
            else:
                self.image = pygame.image.load(self.inactive_button)
                self.screen.blit(self.image, (self.center[0] - self.width // 2, self.center[1] - self.height // 2))
            self.screen.blit(message, (self.center[0] - 70, self.center[1] - 15))


# удаляет спрайт шарика при разбивании всех блоков
def status_check():
    global IS_BALL_KILLED
    if len(bricks) == 0:
        moving_sprites.remove(ball)
        IS_BALL_KILLED = True
    if IS_BALL_KILLED:
        game_over()


# начальная заставка
def start_menu():
    font = pygame.font.SysFont('calibri', 70)
    menu_text = font.render('Чтобы начать игру, нажмите ENTER', True, 'black')
    is_started = False
    while not is_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_started = True
                    main()
        screen.blit(background_image, (0, 0))
        screen.blit(menu_text, (50, SIZE[1] // 2))
        pygame.display.flip()


# заставка конца игры
def game_over():
    global LEVEL_CHANGE, IS_BALL_KILLED
    font = pygame.font.SysFont('calibri', 70)
    line_1_text = font.render('Игра окончена', True, 'black')
    line_2_text = font.render('Чтобы начать заново, нажмите ENTER', True, 'black')
    line_3_text = font.render('Чтобы перейти к другому уровню,', True, 'black')
    line_4_text = font.render('нажмите пробел', True, 'black')
    is_clicked = False
    while not is_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_clicked = True
                    LEVEL_CHANGE += 2
                    main()
                    IS_BALL_KILLED = False
                if event.key == pygame.K_SPACE:
                    LEVEL_CHANGE += 1
                    is_clicked = True
                    main()
                    IS_BALL_KILLED = False
        screen.blit(background_image, (0, 0))
        screen.blit(line_1_text, (50, SIZE[1] // 4))
        screen.blit(line_2_text, (50, SIZE[1] // 3))
        screen.blit(line_3_text, (50, SIZE[1] // 2))
        screen.blit(line_4_text, (50, SIZE[1] // 2 + 80))
        pygame.display.flip()


# основной код; инициализация уровня, создание групп спрайтов, сам процесс игры
def main():
    global ball, paddle, bricks, moving_sprites, LEVEL_CHANGE, IS_BALL_KILLED
    pygame.init()
    clock = pygame.time.Clock()
    button_restart = Button(screen, 500, 375, 'начать заново')
    fps = 60
    running = True
    pause = 0
    paused_game = False
    # группа спрайтов с блоками
    bricks = pygame.sprite.Group()
    color_variations = 0
    brick_rect = pygame.image.load('textures/element_purple_rectangle.png').get_rect()
    # меняет расположение блоков в зависимости от выбранного уровня
    if LEVEL_CHANGE % 2 == 0:
        for y in range(70, SIZE[1] // 2, brick_rect[3] + 5):
            if color_variations == 5:
                break
            for x in range(brick_rect[2] // 2 + 10, SIZE[0], brick_rect[2] + 10):
                bricks.add(Brick(screen, x, y, color_variations))
            color_variations += 1
    else:
        for y in range(120, SIZE[1] // 2, brick_rect[3] + 5):
            if color_variations == 5:
                break
            for x in range(150, SIZE[0] - 100, brick_rect[2] + 10):
                bricks.add(Brick(screen, x, y, color_variations))
            color_variations += 1

    # группа спрайтов с шариком и платформой
    moving_sprites = pygame.sprite.Group()
    ball = Ball(screen)
    IS_BALL_KILLED = False
    moving_sprites.add(ball)
    paddle = Paddle(screen)
    moving_sprites.add(paddle)

    while running:  # Основной игровой цикл
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                # пауза, отрисовка кнопки рестарта игры
                if event.key == pygame.K_SPACE:
                    pause += 1
                    if pause % 2 == 0:
                        paused_game = False
                    else:
                        paused_game = True
                    ball.is_moving(paused_game)
                    paddle.is_moving(paused_game)

        bricks.update()
        moving_sprites.update()
        # вызывает экран окончания игры, если спрайт шарика удален
        status_check()
        # обновление экрана
        screen.blit(background_image, (0, 0))
        bricks.draw(screen)
        moving_sprites.draw(screen)
        button_restart.update(paused_game)
        pygame.display.flip()

        clock.tick(fps)


# вариации блоков
PADDLE_COLORS = {0: 'element_blue_rectangle.png',
                 1: 'element_grey_rectangle.png', 2: 'element_purple_rectangle.png',
                 3: 'element_red_rectangle.png', 4: 'element_yellow_rectangle.png'}

IS_BALL_KILLED = False
LEVEL_CHANGE = 0
SIZE = (1200, 750)
screen = pygame.display.set_mode(SIZE)
background_image = pygame.image.load('textures/arkanoid back.jpg')

# группа спрайтов с шариком и платформой
moving_sprites = pygame.sprite.Group()
ball = Ball(screen)
paddle = Paddle(screen)

# группа спрайтов с блоками
bricks = pygame.sprite.Group()


if __name__ == '__main__':
    start_menu()
    main()
    pygame.quit()

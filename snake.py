import os

import pygame
from random import randrange


def start_window():
    pygame.init()
    screen1 = pygame.display.set_mode((200, 200))
    screen1.fill((255, 255, 255))
    button_play = pygame.Surface([150, 75])
    button_play.fill((0, 235, 196))
    font1 = pygame.font.Font(None, 50)
    text11 = font1.render("Играть", True, (0, 0, 100))
    button_play.blit(text11, (20, 20))
    text12 = font1.render("Змейка", True, (0, 0, 0))
    screen1.fill((255, 255, 255))
    screen1.blit(text12, (40, 30))
    screen1.blit(button_play, (25, 100))
    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                return False
            if event1.type == pygame.MOUSEBUTTONDOWN:
                if 25 <= event1.pos[0] <= 175 and 100 <= event1.pos[1] <= 175:
                    return True
        pygame.display.flip()


running = start_window()


def load_image(name, size1=(30, 30), colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, size1)
    return image


x_change = (30, 25)
y_change = (25, 30)
x_y_change = (30, 30)
HEAD = [load_image('head0.png'), load_image('head1.png'),
        load_image('head2.png'), load_image('head3.png')]
TALE = [load_image('tale0.png', x_change), load_image('tale1.png', x_change),
        load_image('tale2.png', y_change), load_image('tale3.png'), y_change]
BODY = [load_image('body01.png', x_change), load_image('body01.png', x_change),
        load_image('body32.png', y_change), load_image('body32.png'), y_change]
TURN = {0: [load_image('up_to_left.png', x_y_change), load_image('down_to_left.png', x_y_change)],
        1: [load_image('up_to_right.png', x_y_change), load_image('down_to_right.png', x_y_change)],
        2: [load_image('down_to_right.png', x_y_change), load_image('down_to_left.png', x_y_change)],
        3: [load_image('up_to_right.png', x_y_change), load_image('up_to_left.png', x_y_change)]}


class Snake:
    def __init__(self):
        self.size = 30
        self.game_over = False
        self.direction = 0
        self.per = -1
        self.snake_body = [(30, 300, 0)]

    def render(self, s):
        head = HEAD[self.snake_body[0][2]]
        s.blit(head, (self.snake_body[0][0], self.snake_body[0][1]))
        m = self.snake_body[0][-1]
        for j in self.snake_body[1:-1]:
            if j[-1] == m:
                body = BODY[m]
                x_chan = 0
                y_chan = 0
                if j[-1] <= 1:
                    y_chan = 3
                else:
                    x_chan = 3
                s.blit(body, (j[0] + x_chan, j[1] + y_chan))
            else:
                turn = TURN[j[-1]][m % 2]
                x_chan = 0
                y_chan = 0
                if j[-1] == 2:
                    y_chan = -3
                elif j[-1] == 3:
                    if m == 3:
                        x_chan = 3
                    else:
                        x_chan = -3
                    y_chan = 3
                elif j[-1] == 1:
                    x_chan = -3
                else:
                    if m == 3:
                        x_chan = -3
                    else:
                        x_chan = 3
                s.blit(turn, (j[0] + x_chan, j[1] + y_chan))
            j, m = (j[0], j[1], m), j[-1]
        if len(self.snake_body) > 1:
            x_chan = 0
            y_chan = 0
            if self.snake_body[-1][-1] < 2:
                y_chan = 3
            else:
                x_chan = 3
            tale = TALE[self.snake_body[-1][2]]
            s.blit(tale, (self.snake_body[-1][0] + x_chan, self.snake_body[-1][1] + y_chan))
            self.snake_body[-1] = (self.snake_body[-1][0], self.snake_body[-1][1], m)

    def eat(self, direction):
        self.snake_body.append(direction)


class Board:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.board = [[0] * w for _ in range(h)]
        self.left = 10
        self.top = 10
        self.cell_size = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, s):
        x, y = self.left, self.top
        for m in range(len(self.board)):
            for j in range(len(self.board[i])):
                if m % 2 == 0:
                    if j % 2 == 0:
                        pygame.draw.rect(s, (102, 255, 255), (x, y, self.cell_size, self.cell_size), 20)
                    else:
                        pygame.draw.rect(s, (128, 218, 235), (x, y, self.cell_size, self.cell_size), 20)
                else:
                    if j % 2 != 0:
                        pygame.draw.rect(s, (102, 255, 255), (x, y, self.cell_size, self.cell_size), 20)
                    else:
                        pygame.draw.rect(s, (128, 218, 235), (x, y, self.cell_size, self.cell_size), 20)
                x += self.cell_size
            y += self.cell_size
            x = self.left


def save_res(res):
    with open('results.txt', 'w') as f:
        f.write(str(res))


def is_eating(sna, ap):
    if ap[2][0] <= sna.snake_body[0][0] <= ap[2][0] + 29 and ap[2][1] <= sna.snake_body[0][1] <= ap[2][1] + 29:
        return True
    return False


board = Board(15, 15)
board.set_view(0, 60, 30)
FPS = 8.5
clock = pygame.time.Clock()
pygame.init()
size = width, height = 450, 510
screen = pygame.display.set_mode(size)
snake = Snake()
x_change, y_change = 0, 0
screen2 = pygame.display.set_mode(size)
k = 0
game_over = False
apple = [load_image('apple_img.png'), True, (randrange(0, 421, 30), randrange(60, 471, 30))]
while running:
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_res(len(snake.snake_body))
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                save_res(len(snake.snake_body))
                game_over = False
                snake = Snake()
                x_change, y_change = 0, 0
                k = 0
        font = pygame.font.Font(None, 40)
        text = font.render("Чтобы начать игру сначала,", True, (0, 100, 100))
        text1 = font.render("Вы проиграли", True, (0, 100, 100))
        text2 = font.render("нажмите любую клавишу", True, (0, 100, 100))
        screen2.fill((0, 191, 255))
        screen2.blit(text1, (10, 10))
        screen2.blit(text, (10, 70))
        screen2.blit(text2, (10, 120))
        pygame.display.flip()
    if not running:
        break
    clock.tick(FPS)
    font = pygame.font.Font(None, 50)
    text = font.render(f"Текущий счёт: {len(snake.snake_body) - 1}", True, (0, 0, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.scancode == 79:
                if k != 1:
                    k = 0
                    x_change = 30
                    y_change = 0
            elif event.scancode == 80:
                if k != 0:
                    k = 1
                    x_change = -30
                    y_change = 0
            elif event.scancode == 81:
                if k != 3:
                    k = 2
                    x_change = 0
                    y_change = 30
            elif event.scancode == 82:
                if k != 2:
                    k = 3
                    x_change = 0
                    y_change = -30

    screen.fill((0, 191, 255))
    board.render(screen)
    x1, y1, n = snake.snake_body[0]
    x0, y0 = x1, y1
    if 0 > x0 or x0 > 450 or 60 > y0 or y0 > 510:
        game_over = True
    if game_over:
        continue
    for i in range(1, len(snake.snake_body)):
        snake.snake_body[i], x1, y1, n = ((x1, y1, n), snake.snake_body[i][0], snake.snake_body[i][1],
                                          snake.snake_body[i][2])
        if x0 == x1 and y0 == y1:
            game_over = True
    if game_over:
        continue
    snake.snake_body[0] = (snake.snake_body[0][0] + x_change, snake.snake_body[0][1] + y_change, k)
    if not apple[1]:
        apple[1] = True
        apple[2] = (randrange(0, 421, 30), randrange(60, 471, 30))
    screen.blit(apple[0], apple[2])
    snake.render(screen)
    if is_eating(snake, apple):
        snake.eat((0, 0, 0))
        apple[1] = False
    screen.blit(text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

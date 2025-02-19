import pygame
from math import floor, ceil


class Snake:
    def __init__(self):
        self.size = 20
        self.direction = 0
        self.x, self.y = 20, 300
        self.per = -1
        self.len = [0]

    def render(self, s, v=0.2):
        global zn
        x, y = self.x, self.y
        for i in self.len:
            if i == 0:
                self.x += v
                zn -= v
            elif i == 1:
                self.x -= v
                zn -= v
            elif i == 2:
                self.y += v
                zn -= v
            elif i == 3:
                self.y -= v
                zn -= v
            pygame.draw.rect(s, (255, 0, 0), (x, y, self.size, self.size), 20)

    def eat(self, direction):
        self.len.append(direction)


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
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i % 2 == 0:
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


board = Board(23, 23)
board.set_view(0, 40, 20)
running = True
pygame.init()
size = width, height = 460, 450
screen = pygame.display.set_mode(size)
snake = Snake()
k = 0
zn = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.scancode == 79:
                print(121212)
                k = 1
                if snake.len[0] == 3:
                    zn = snake.y - floor(snake.y / 20) * 20
                else:
                    zn = ceil(snake.y / 20) * 20 - snake.y
            elif event.scancode == 80:
                k = 2
                if snake.len[0] == 3:
                    zn = snake.y - floor(snake.y / 20) * 20
                else:
                    zn = ceil(snake.y / 20) * 20 - snake.y
            elif event.scancode == 81:
                k = 3
                if snake.len[0] == 0:
                    zn = ceil(snake.x / 20) * 20 - snake.x
                else:
                    zn = snake.x - floor(snake.x / 20) * 20
            elif event.scancode == 82:
                k = 4
                if snake.len[0] == 0:
                    zn = ceil(snake.x / 20) * 20 - snake.x
                else:
                    zn = snake.x - floor(snake.x / 20) * 20

    screen.fill((0, 191, 255))
    board.render(screen)
    if k:
        if zn > 0.2:
            snake.render(screen)
        elif 0 < zn < 0.2:
            snake.render(screen, v=zn)
            zn = 0
        else:
            snake.len[0] = k - 1
            k = 0
    else:
        snake.render(screen)
    pygame.display.flip()
pygame.quit()

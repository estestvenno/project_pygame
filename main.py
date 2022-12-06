import sys
import pygame
from copy import deepcopy
import noise

size = width, height = 470, 470


class Board:
    def __init__(self, board_width, board_height, cell_size=3):
        self.width, self.height = board_width, board_height
        self.left, self.top = 10, 10
        self.cell_size = cell_size
        self.board = [[0] * board_width for _ in range(board_height)]

    def set_view(self, left=None, top=None, cell_size=None):
        if left is not None:
            self.left = left
        if top is not None:
            self.top = top
        if cell_size is not None:
            self.cell_size = cell_size

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def check_pos_in_board(self, x, y):
        return self.left < x < self.left + self.width * self.cell_size \
               and self.top < y < self.top + self.height * self.cell_size

    def get_cell(self, x, y):
        if not self.check_pos_in_board(x, y):
            return None
        x = x - self.left
        y = y - self.top
        return x // self.cell_size, y // self.cell_size

    def cell_clicked(self, cell_x, cell_y, move):
        pass

    def board_clicked(self, x, y, move):
        cell = self.get_cell(x, y)
        if cell:
            return self.cell_clicked(*cell, move)
        return


class Map(Board):
    def __init__(self, board_width, board_height, seed=1):
        super().__init__(board_width, board_height)
        self.seed = seed

    def generate_relief(self):
        for x in range(self.width):
            for y in range(self.height):
                s = noise.pnoise3(float(x) * 0.1, float(y) * 0.1, self.seed, 1)
                if s < -0.45:
                    # водоёмы
                    self.board[x][y] = -1
                elif s < 0.45:
                    # равнины
                    self.board[x][y] = 0
                else:
                    # скалы, горы
                    self.board[x][y] = 1

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == -1:
                    pygame.draw.rect(screen, "blue",
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                elif self.board[x][y] == 0:
                    pygame.draw.rect(screen, "green",
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                if self.board[x][y] == 1:
                    pygame.draw.rect(screen, "gray",
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 0)


def game():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Игра «Жизнь»")
    running = True
    map = Map(300, 300, seed=1)
    map.generate_relief()
    fps = 60
    moving = False
    clock = pygame.time.Clock()
    tick = 0
    zoom = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    m_x, m_y = event.pos
                    if map.check_pos_in_board(m_x, m_y):
                        moving = True
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    map.set_view(map.left + event.rel[0], map.top + event.rel[1])
            if event.type == pygame.MOUSEBUTTONUP:
                moving = False

            if event.type == pygame.MOUSEWHEEL:
                zoom += event.y / 2
                if zoom < 1:
                    zoom = 1
                if zoom > 10:
                    zoom = 10
                map.set_view(cell_size=zoom)

        draw(screen, map)
        clock.tick(fps)
        tick += 1
        pygame.display.flip()
    pygame.quit()


def draw(screen, board):
    screen.fill(0)
    board.render(screen)


if __name__ == "__main__":
    game()

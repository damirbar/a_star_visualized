import pygame

SCREEN_HEIGHT = 600
SCREEN_WIDTH  = 800
BLOCK_SIZE    = 10

# class AStarConstants:

class Position:

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


pygame.init()

# self.clock.tick(self.snake_speed)

class Visualizer:

    def __init__(self, clock_speed=30):
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.update()
        pygame.display.set_caption("Path Find Visualization")

    def step(self, matrix):
        for i in matrix:
            for j in matrix[i]:
                if matrix[i][j]:
                    self.handle_pixel(matrix[i][j])
        self.clock.tick(self.clock_speed)



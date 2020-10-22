import pygame

SCREEN_HEIGHT = 30
SCREEN_WIDTH = 30
BLOCK_SIZE = 20

class Colors:
    red = (255, 0, 0)
    dark_red = (150, 0, 0)
    green = (0, 255, 0)
    dark_green = (0, 200, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class SnapshotNode:
    def __init__(self, pos):
        self.__position = pos
        self.__color = Colors.black

    @property
    def color(self):
        return self.__color

    @property
    def position(self):
        return self.__position

    @color.setter
    def color(self, color):
        self.__color = color

    @position.setter
    def position(self, position):
        self.__position = position

    def __str(self):
        return "Node: " + str(self.position)

    def __repr__(self):
        return "Node: " + str(self.position)


class SearchAlgo:

    def __init__(self):
        self.__nodes = []
        self.done = False

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, nodes):
        self.__nodes = nodes

    def add_node(self, node):
        self.__nodes.append(node)

    def flush_nodes(self):
        self.__nodes = []

    def step_algo(self):
        pass

    def finalize(self):
        pass

pygame.init()


class Visualizer:

    def __init__(self, search_algo=None, clock_speed=30):
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.disp = pygame.display.set_mode(
            (SCREEN_HEIGHT * BLOCK_SIZE, SCREEN_WIDTH * BLOCK_SIZE))
        pygame.display.update()
        pygame.display.set_caption("Path Find Visualization")
        self.__search_algo = search_algo

        self.update()

    @property
    def search_algo(self):
        return self.__search_algo

    @search_algo.setter
    def search_algo(self, search_algo):
        self.__search_algo = search_algo

    def update(self):
        pygame.display.update()

    def draw_rect(self, x, y, color, filled=False):
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                           BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.disp, color, rect, 0 if filled else 1)

    def draw_grid(self):
        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                self.draw_rect(x, y, Colors.white)
        self.update()

    def handle_play_event(self, evt):
        # If the user attempts to close the window
        if evt.type == pygame.QUIT:
            exit(0)

    def draw_buffered_nodes(self):
        for node in self.search_algo.nodes:
            self.draw_rect(
                node.position.x, node.position.y, node.color, filled=True)
        self.search_algo.flush_nodes()

    def user_choose_start_end(self):
        chosen_positions = []
        while len(chosen_positions) < 2:
            for evt in pygame.event.get():
                if evt.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(f"Clicked on {pos}")
                    x = (pos[0] // BLOCK_SIZE)
                    y = (pos[1] // BLOCK_SIZE)
                    chosen_positions.append(Position(x,y))
                    self.draw_rect(
                        x, y, Colors.white, filled=True)
                    self.update()
        return chosen_positions


    def run_algo(self):
        print("Running algo")
        while not self.search_algo.done:

            self.search_algo.step_algo()
            self.draw_buffered_nodes()
            
            for evt in pygame.event.get():
                self.handle_play_event(evt)

            self.update()
            self.clock.tick(self.clock_speed)
        
        self.search_algo.finalize()
        self.draw_buffered_nodes()
        self.update()

        while True:
            for evt in pygame.event.get():
                self.handle_play_event(evt)
            self.clock.tick(self.clock_speed)

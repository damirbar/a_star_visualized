import time

from visualize import Visualizer, Position, SCREEN_HEIGHT, SCREEN_WIDTH, \
    Colors, SnapshotNode, SearchAlgo


class AStarNode(SnapshotNode):
    """Node class for the A* shortest path algorithm

    For every node:
    f = g + h

    Args:
        pos (Position): x,y coordinates.
        parent (:obj:`Node`, optional): Parent node

    Attributes:
        __position (Position): x,y coordinates.
        __parent (:obj:`Node`, optional): Parent node
        __g (int): Distance from start node
        __h (int): Distance to end node (destination)
        __f (int): Total cost

    """

    def __init__(self, pos, parent=None):
        self.__parent = parent
        self.__g = self.__h = self.__f = 0
        self.__is_traversable = True
        super().__init__(pos)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    @property
    def parent(self):
        return self.__parent

    @property
    def g(self):
        return self.__g

    @property
    def h(self):
        return self.__h

    @property
    def f(self):
        return self.__f

    @property
    def is_traversable(self):
        return self.__is_traversable

    @parent.setter
    def parent(self, parent):
        self.__parent = parent

    @g.setter
    def g(self, g):
        self.__g = g

    @h.setter
    def h(self, h):
        self.__h = h

    @f.setter
    def f(self, f):
        self.__f = f

    @is_traversable.setter
    def is_traversable(self, val):
        self.__is_traversable = val


class AStarSearch(SearchAlgo):

    def __init__(self, node_matrix, start, end):
        super().__init__()

        self.node_matrix = node_matrix
        # self.visualizer = visualizer

        # Create lists for open and closed nodes
        self.open_node_list = []
        self.closed = []

        # Create a start and an end node
        self.start_node = self.generate_node(start)
        self.end_node = self.generate_node(end)

        # if self.visualizer:
        #     self.init_start_end_nodes()
        self.init_start_end_nodes()

        # Add the start node
        self.open_node_list.append(self.start_node)

        self.result_path = None

    def init_start_end_nodes(self):
        self.start_node.color = Colors.green
        self.end_node.color = Colors.green
        self.add_node(self.start_node)
        self.add_node(self.end_node)
        # self.visualizer.draw_rect(
        #     self.start_node.position.x, self.start_node.position.y, Colors.green, filled=True)
        # self.visualizer.draw_rect(
        #     self.end_node.position.x, self.end_node.position.y, Colors.green, filled=True)
        # self.visualizer.update()

    # def update_visualizer(self):
    #     if self.visualizer:
    #         for node in self.closed:
    #             self.visualizer.draw_rect(
    #                 node.position.x, node.position.y, Colors.red)
    #         for node in self.open_node_list:
    #             self.visualizer.draw_rect(
    #                 node.position.x, node.position.y, Colors.green)
    #         self.visualizer.update()

    def update_node_closed(self, curr_node):
        self.closed.append(curr_node)

        if curr_node != self.start_node:
            curr_node.color = Colors.red
            self.add_node(curr_node)
        # if self.visualizer:
        #     curr_node.color = Colors.red
        #     self.update_visualizer()

    def update_node_open(self, curr_node):
        self.open_node_list.append(curr_node)
        curr_node.color = Colors.blue
        self.add_node(curr_node)
        # if self.visualizer:
        #     curr_node.color = Colors.green
        #     self.update_visualizer()

    # def draw_path(self):
    #     for pos in self.result_path:
    #         self.visualizer.draw_rect(pos.x, pos.y, Colors.blue, filled=True)
    #         self.visualizer.update()
    #         time.sleep(0.05)

    def finalize(self):
        print("Finalizing A* Search")
        for pos in self.result_path:
            node = self.generate_node(pos)
            node.color = Colors.dark_green
            print(node)
            self.add_node(node)

    def step_algo(self):
        
        if self.done:
            return

        if len(self.open_node_list) > 0:
            # Sort the open node list to get the cheapest node
            self.open_node_list.sort()

            curr_node = self.open_node_list.pop(0)
            self.update_node_closed(curr_node)

            # Found the end node
            if curr_node == self.end_node:
                path = []
                while curr_node != self.start_node:
                    path.append(curr_node.position)
                    curr_node = curr_node.parent
                self.done = True
                self.result_path = path[::-1]
                return

            x, y = curr_node.position.x, curr_node.position.y

            neighbors = [Position(x-1, y), Position(x+1, y),
                         Position(x, y-1), Position(x, y+1)]

            for position in neighbors:

                if x < 0 or y < 0 or x > len(self.node_matrix) or y > len(self.node_matrix[0]):
                    continue

                neighbor = self.generate_node(position, curr_node)
                if neighbor in self.closed or not neighbor.is_traversable:
                    continue

                neighbor.g = abs(neighbor.position.x - self.start_node.position.x) + \
                    abs(neighbor.position.y - self.start_node.position.y)
                neighbor.h = abs(neighbor.position.x - self.end_node.position.x) + \
                    abs(neighbor.position.y - self.end_node.position.y)
                neighbor.f = neighbor.g + neighbor.f

                if add_to_open_list(self.open_node_list, neighbor):
                    self.update_node_open(neighbor)

    def perform_a_star_search(self):
        pass

    def generate_node(self, pos, parent=None):
        return AStarNode(pos, parent)


def add_to_open_list(open_node_list, neighbor_node):
    """Check if a node is in the open node list and has a lower f value

    :param open_node_list:
    :param neighbor_node:
    :return: bool
    """
    for node in open_node_list:
        if neighbor_node == node and neighbor_node.f >= node.f:
            return False
    return True


# def executeVisualizedAStarSearch():

#     matrix = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

#     visualizer = Visualizer()

#     visualizer.draw_grid()
#     visualizer.update()

#     a_star_search = AStarSearch(node_matrix=matrix, start=Position(
#         40, 40), end=Position(50, 50), visualizer=visualizer)

#     while not a_star_search.done:
#         a_star_search.step_a_star_search()

#     print(a_star_search.result_path)
#     a_star_search.draw_path()

#     # while(True):
#     #     pass


def main():
    pass
    # executeVisualizedAStarSearch()


if __name__ == '__main__':
    main()

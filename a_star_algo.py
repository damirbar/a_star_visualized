import enum

from visualize import Visualizer, Position


class AStarNode:
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
        self.__position = pos
        self.__parent = parent
        self.__g = self.__h = self.__f = 0
        self.__is_traversable = True

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    @property
    def position(self):
        return self.__position

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

    @position.setter
    def position(self, position):
        self.__position = position

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

    def __str(self):
        return "Node: " + str(self.position)

    def __repr__(self):
        return "Node: " + str(self.position)


class NodeColor(enum.Enum):
    white = 0
    green = 1
    red = 2


class VisualizedAStarNode(AStarNode):

    def __init__(self, pos, parent):
        AStarNode.__init__(self, pos, parent)
        self.__color = NodeColor.white

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color


class AStarSearch:

    def __init__(self, node_matrix, start, end, visualizer=None):
        self.node_matrix = node_matrix
        self.visualizer = visualizer
        self.done = False

        # Create lists for open and closed nodes
        self.open_node_list = []
        self.closed = []

        # Create a start and an end node
        self.start_node = self.generate_node(start)
        self.end_node = self.generate_node(end)

        # Add the start node
        self.open_node_list.append(self.start_node)

        self.result_path = None

    def step_a_star_search(self):
        if self.done:
            return

        if len(self.open_node_list) > 0:
            # Sort the open node list to get the cheapest node
            self.open_node_list.sort()

            curr_node = self.open_node_list.pop(0)
            self.closed.append(curr_node)

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
                    self.open_node_list.append(neighbor)

    def perform_a_star_search(self):

        iteration = 0
        # Go on until the open node list is empty
        while len(self.open_node_list) > 0:
            # Sort the open node list to get the cheapest node
            self.open_node_list.sort()

            curr_node = self.open_node_list.pop(0)
            self.closed.append(curr_node)

            if iteration % 100 == 0:
                print(f"iteration {iteration}")
                print(f"open size = {len(open_node_list)}")
                print(f"closed size = {len(closed)}")
                print(f"curr node = {curr_node}")
            iteration += 1

            # Found the end node
            if curr_node == self.end_node:
                path = []
                while curr_node != self.start_node:
                    path.append(curr_node.position)
                    curr_node = curr_node.parent

                return path[::-1]

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
                    self.open_node_list.append(neighbor)

        # No path was found
        return None

    def generate_node(self, pos, parent=None):
        if self.visualizer is None:
            return VisualizedAStarNode(pos, parent)
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


def main():

    width = 800
    height = 600
    matrix = [[0 for x in range(width)] for y in range(height)]

    visualizer = Visualizer()
    a_star_search = AStarSearch(node_matrix=matrix, start=Position(
        6, 6), end=Position(20, 20), visualizer=visualizer)

    while not a_star_search.done:
        a_star_search.step_a_star_search()

    print(a_star_search.result_path)


if __name__ == '__main__':
    main()

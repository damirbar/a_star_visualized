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

    def __init__(self, node_matrix, start, end, diagonal_allowed=False):
        super().__init__()

        self.diagonal_allowed = diagonal_allowed
        self.node_matrix = node_matrix

        # Create lists for open and closed nodes
        self.open_node_list = []
        self.closed = []

        # Create a start and an end node
        self.start_node = self.generate_node(start)
        self.end_node = self.generate_node(end)

        self.init_start_end_nodes()

        # Add the start node
        self.open_node_list.append(self.start_node)

        self.result_path = None

    def init_start_end_nodes(self):
        self.start_node.color = Colors.green
        self.end_node.color = Colors.green
        self.add_node(self.start_node)
        self.add_node(self.end_node)

    def update_node_closed(self, curr_node, color=Colors.red):
        self.closed.append(curr_node)

        if curr_node != self.start_node:
            curr_node.color = color
            self.add_node(curr_node)
        # if self.visualizer:
        #     curr_node.color = Colors.red
        #     self.update_visualizer()

    def update_node_open(self, curr_node):
        self.open_node_list.append(curr_node)
        curr_node.color = Colors.blue
        self.add_node(curr_node)

    def finalize(self):
        print("Finalizing A* Search")
        for pos in self.result_path:
            node = self.generate_node(pos)
            node.color = Colors.dark_green
            self.add_node(node)

    def get_node_neighbours(self, x, y):
        if self.diagonal_allowed:
            return [Position(x - 1, y), Position(x + 1, y),
                    Position(x, y - 1), Position(x, y + 1),
                    Position(x - 1, y - 1), Position(x - 1, y + 1),
                    Position(x + 1, y - 1), Position(x + 1, y + 1)]

        return [Position(x-1, y), Position(x+1, y),
                Position(x, y-1), Position(x, y+1)]
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

            neighbors = self.get_node_neighbours(x, y)

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
                neighbor.f = neighbor.g + neighbor.h

                if add_to_open_list(self.open_node_list, neighbor):
                    self.update_node_open(neighbor)

    def generate_node(self, pos, parent=None):
        return AStarNode(pos, parent)


def add_to_open_list(open_node_list, neighbor_node):
    """Check if a node is in the open node list and has a lower f value

    :param open_node_list:
    :param neighbor_node:
    :return: bool
    """
    for node in open_node_list:
        if neighbor_node == node and neighbor_node.f <= node.f:
            return False
    return True

def main():
    pass

if __name__ == '__main__':
    main()

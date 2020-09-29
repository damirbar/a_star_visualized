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

    def __str(self):
        return "Node: " + str(self.position)

    def __repr__(self):
        return "Node: " + str(self.position)


def a_star_search(matrix, start, end):

    # Create lists for open and closed nodes
    open_node_list   = []
    closed = []

    # Create a start and an end node
    start_node = AStarNode(start, None)
    end_node = AStarNode(end, None)

    # Add the start node
    open_node_list.append(start_node)

    iteration = 0
    # Go on until the open node list is empty
    while len(open_node_list) > 0:
        # Sort the open node list to get the cheapest node
        open_node_list.sort()

        curr_node = open_node_list.pop(0)
        closed.append(curr_node)

        if iteration % 100 == 0:
            print(f"iteration {iteration}")
            print(f"open size = {len(open_node_list)}")
            print(f"closed size = {len(closed)}")
            print(f"curr node = {curr_node}")
        iteration += 1

        # Found the end node
        if curr_node == end_node:
            path = []
            while curr_node != start_node:
                path.append(curr_node.position)
                curr_node = curr_node.parent

            return path[::-1]

        x,y = curr_node.position.x, curr_node.position.y

        neighbors = [Position(x-1, y), Position(x+1, y), Position(x, y-1), Position(x, y+1)]

        for position in neighbors:
            if x < 0 or y < 0 or x > len(matrix) or y > len(matrix[0]):
                continue

            neighbor = AStarNode(position, curr_node)
            if neighbor in closed:
                continue

            neighbor.g = abs(neighbor.position.x - start_node.position.x) + \
                          abs(neighbor.position.y - start_node.position.y)
            neighbor.h = abs(neighbor.position.x - end_node.position.x) + \
                          abs(neighbor.position.y - end_node.position.y)
            neighbor.f = neighbor.g + neighbor.f

            if add_to_open_list(open_node_list, neighbor):
                open_node_list.append(neighbor)

    # No path was found
    return None


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

    width  = 800
    height = 600
    matrix = [[0 for x in range(width)] for y in range(height)]

    print(a_star_search(matrix, Position(6,6), Position(20,20)))

    return

if __name__ == '__main__':
    main()

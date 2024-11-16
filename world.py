import cell
import math


class Grid:
    def __init__(self, width: int, height: int):
        self.cells = [[cell.Cell(x, y, cell.CellType.ROAD)
                       for x in range(width)] for y in range(height)]
        self.start_cell = self.cells[0][0]
        self.end_cell = self.cells[0][0]
        self.discovered_nodes = [self.start_cell]
        self.path = []
        self.true_path = []
        self.completed_path = False
        self.first_run = True

    def get_cells(self):
        return self.cells

    def validate_cell_position(self, pos: (int, int)):
        print("validating pos: ", pos)

        if pos[0] < 0 or pos[0] > len(self.cells[0]):
            print("invalid X position for cell")

        if pos[1] < 0 or pos[1] > len(self.cells):
            print("invalid Y position for cell")

    def set_start_cell(self, pos: (int, int)):
        self.validate_cell_position(pos)
        self.cells[pos[1]][pos[0]].state = cell.CellState.START
        self.start_cell = self.cells[pos[1]][pos[0]]
        self.first_run = True

    def set_end_cell(self, pos: (int, int)):
        self.validate_cell_position(pos)
        self.cells[pos[1]][pos[0]].state = cell.CellState.END
        self.end_cell = self.cells[pos[1]][pos[0]]
        self.first_run = True

    def set_cell_type(self, pos: (int, int), type: cell.CellType):
        self.validate_cell_position(pos)
        self.cells[pos[1]][pos[0]].set_cell_type(type)

    def get_chebyshev_distance(self, a: cell.Cell, b: cell.Cell):
        return max(abs(a.x-b.x), abs(a.y-b.y))*10

    def get_all_valid_neighbors(self, cell):

        valid_cells = []

        if cell.x - 1 >= 0:
            valid_cells.append(self.cells[cell.y][cell.x-1])
            if cell.y - 1 >= 0:
                valid_cells.append(self.cells[cell.y-1][cell.x-1])

        if cell.x + 1 <= len(self.cells[0])-1:
            valid_cells.append(self.cells[cell.y][cell.x+1])
            if cell.y+1 <= len(self.cells)-1:
                valid_cells.append(self.cells[cell.y+1][cell.x+1])

        if cell.y - 1 >= 0:
            valid_cells.append(self.cells[cell.y-1][cell.x])
            if cell.x + 1 <= len(self.cells[0])-1:
                valid_cells.append(self.cells[cell.y-1][cell.x+1])

        if cell.y + 1 <= len(self.cells)-1:
            valid_cells.append(self.cells[cell.y+1][cell.x])
            if cell.x - 1 >= 0:
                valid_cells.append(self.cells[cell.y+1][cell.x-1])

        return valid_cells

    def get_g_score(self, a: cell.Cell, b: cell.Cell) -> int:
        if a.x == b.x or a.y == b.y:
            return 10
        else:
            return 14

    def get_g_core_of_path(self, current_cell: cell.Cell, path: [cell.Cell]) -> int:
        sum_g_score = 0

        for c in path:
            sum_g_score = sum_g_score + c.g_score

        sum_g_score = sum_g_score + self.get_g_score(current_cell, path[-1])

        return sum_g_score

    def reconstruct_path(self, start_cell: cell.Cell, current_cell: cell.Cell) -> [cell.Cell]:
        print("Contructing path, start: ", current_cell)

        path = [current_cell]
        c = current_cell

        while c:
            # print("At: ", c)
            path.append(c.came_from)
            c = c.came_from
            if c.equals(start_cell):
                break

        return path

    def get_cell_with_lowest_f(self, nodes: [cell.Cell]) -> cell.Cell:
        lowest_score_node = nodes[0]
        for node in nodes:
            if node.f_score < lowest_score_node.f_score:
                lowest_score_node = node

        return lowest_score_node

    def print(self, nodes: [cell.Cell]):
        for value in nodes:
            print(value)

    def reset_scores(self):
        for y, row in enumerate(self.cells):
            for x, c in enumerate(row):
                self.cells[y][x].g_score = 10000000
                self.cells[y][x].h_score = 10000000
                self.cells[y][x].f_score = 10000000
                self.cells[y][x].state = cell.CellState.UNTOUCHED

    def start_a_star(self):
        self.reset_scores()
        start_cell = self.start_cell
        end_cell = self.end_cell

        h: int = self.get_chebyshev_distance(start_cell, end_cell)

        start_cell.g_score = 0
        start_cell.f_score = h
        self.cells[start_cell.y][start_cell.x].f_score = h
        self.cells[start_cell.y][start_cell.x].g_score = 0
        discovered_nodes = [start_cell]
        # came_from = []

        # total_g_score = 1000000  # infinite

        # total_f_score = 1000000
        # start_cell.h_score = h

        print("!!! START !!!")
        print("Start cell score: ", start_cell.f_score)
        while len(discovered_nodes) != 0:
            print("In main algo loop: ", len(discovered_nodes), " nodes.")
            # self.print(discovered_nodes)

            current = self.get_cell_with_lowest_f(discovered_nodes)

            print("Curent cell: ", current)

            if current.equals(self.end_cell):
                print("!!! SOLVED !!!")
                path = self.reconstruct_path(start_cell, current)
                for node in path:
                    # if (node.equals(start_cell) or node.equals(end_cell)):
                    #     continue

                    self.cells[node.y][node.x].state = cell.CellState.PATH
                    node.state = cell.CellState.PATH
                return

            current_cell_neighbors = self.get_all_valid_neighbors(current)

            discovered_nodes.remove(current)

            # print("neighbors: ")
            # self.print(current_cell_neighbors)

            for neighbor in current_cell_neighbors:
                if neighbor.type == cell.CellType.WALL:
                    continue

                tentative_g_score = current.g_score + \
                    self.get_g_score(current, neighbor)

                # self.cells[neighbor.y][neighbor.x].state = cell.CellState.VISITED
                # neighbor.state = cell.CellState.VISITED

                # print(neighbor, "g score: ", neighbor.g_score)
                # print(neighbor, "tentative g score: ", tentative_g_score)

                if tentative_g_score < neighbor.g_score:
                    self.cells[neighbor.y][neighbor.x].state = cell.CellState.COMPUTED
                    neighbor.state = cell.CellState.COMPUTED

                    neighbor.came_from = current
                    neighbor.g_score = tentative_g_score
                    neighbor.f_score = tentative_g_score + \
                        self.get_chebyshev_distance(self.end_cell, neighbor)

                    if neighbor not in discovered_nodes:
                        # print("Adding neighbor ", neighbor,
                        #       "f score: ", neighbor.f_score)
                        discovered_nodes.append(neighbor)

        print("!!! FAILED !!!")
        return []

    def clear_path(self):
        for node in self.path:
            self.cells[node.y][node.x].state = cell.CellState.COMPUTED
        self.path = []

    def interate_a_star(self):
        h: int = self.get_chebyshev_distance(self.start_cell, self.end_cell)

        if self.first_run:
            self.reset_scores()

            self.start_cell.g_score = 0
            self.start_cell.f_score = h
            self.cells[self.start_cell.y][self.start_cell.x].f_score = h
            self.cells[self.start_cell.y][self.start_cell.x].g_score = 0
            self.discovered_nodes = [self.start_cell]
            self.path = []

            self.first_run = False
            self.completed_path = False

        # if not self.completed_path:
        #     self.clear_path()

        if len(self.discovered_nodes) == 0:
            print("empty discovered_nodes")
            return

        print("In main algo loop: ", len(self.discovered_nodes), " nodes.")

        current = self.get_cell_with_lowest_f(self.discovered_nodes)

        print("Curent cell: ", current)

        if not current.equals(self.start_cell):
            self.path = self.reconstruct_path(self.start_cell, current)

        for node in self.path:
            self.cells[node.y][node.x].state = cell.CellState.PATH
            node.state = cell.CellState.PATH

        if current.equals(self.end_cell):
            print("!!! SOLVED !!!")
            self.completed_path = True
            self.true_path = self.reconstruct_path(self.start_cell, current)
            for node in self.true_path:
                self.cells[node.y][node.x].state = cell.CellState.DONE

            return

        current_cell_neighbors = self.get_all_valid_neighbors(current)

        self.discovered_nodes.remove(current)
        print("remove current.")
        print("Existing", len(self.discovered_nodes), " nodes.")

        for neighbor in current_cell_neighbors:
            if neighbor.type == cell.CellType.WALL:
                continue

            tentative_g_score = current.g_score + \
                self.get_g_score(current, neighbor)

            if tentative_g_score < neighbor.g_score:
                self.cells[neighbor.y][neighbor.x].state = cell.CellState.COMPUTED
                neighbor.state = cell.CellState.COMPUTED

                neighbor.came_from = current
                neighbor.g_score = tentative_g_score
                neighbor.f_score = tentative_g_score + \
                    self.get_chebyshev_distance(self.end_cell, neighbor)

                if neighbor not in self.discovered_nodes:
                    print("Adding neighbor ", neighbor,
                          "f score: ", neighbor.f_score)
                    self.discovered_nodes.append(neighbor)
        # print("!!! FAILED !!!")
        # return []

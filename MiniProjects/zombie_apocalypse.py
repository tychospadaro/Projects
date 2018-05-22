"""
Student portion of Zombie Apocalypse mini-project
view poc_XXX modules at http://www.codeskulptor.org/#poc_XXX.py
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            self._obstacle_list = list(obstacle_list)
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._obstacle_list = []
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        distance_field = [[self.get_grid_width() * self.get_grid_height()\
                                    for dummy_col in range(self.get_grid_width())]\
                                    for dummy_row in range(self.get_grid_height())]
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        boundary = poc_queue.Queue()

        if entity_type == HUMAN:				# enqueue entities
            for human in self.humans():
                boundary.enqueue(human)
        elif entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        else:
            return 'Entity type error'

        for entity in boundary:					# 'visit' initial entities
            distance_field[entity[0]][entity[1]] = 0
            visited.set_full(*entity)

        for obstacle in self._obstacle_list:	# 'visit' obstacles
            visited.set_full(*obstacle)

        while len(boundary) > 0:				# iterate over boundary cells
            cell = boundary.dequeue()
            cell_val = distance_field[cell[0]][cell[1]]
            neighbors = visited.four_neighbors(*cell)

            for neighbor in neighbors:
                if visited.is_empty(*neighbor):	# update and enqueue unvisted neighbors
                    distance_field[neighbor[0]][neighbor[1]] = cell_val + 1
                    visited.set_full(*neighbor)
                    boundary.enqueue(neighbor)

        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for dummy_index in range(self.num_humans()):
            human = self._human_list.pop(0)				# remove human to move from list

            moves = [human]								# intitalize moves with current loc, add valid moves
            moves.extend(filter(lambda loc: loc not in self._obstacle_list, self.eight_neighbors(*human)))

            best_val = max((zombie_distance_field[row][col] for row, col in moves))
            best_moves = list(filter(lambda move: zombie_distance_field[move[0]][move[1]] == best_val, moves))

            self.add_human(*random.choice(best_moves))	# return human to list


    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for dummy_index in range(self.num_zombies()):
            zombie = self._zombie_list.pop(0)			# remove zombie to move from list

            moves = [zombie]							# intitalize moves with current loc, add valid moves
            moves.extend(filter(lambda loc: loc not in self._obstacle_list, self.four_neighbors(*zombie)))

            best_val = min((human_distance_field[row][col] for row, col in moves))
            best_moves = list(filter(lambda move: human_distance_field[move[0]][move[1]] == best_val, moves))

            self.add_zombie(*random.choice(best_moves))	# return zombie to list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#test_case = Apocalypse(3, 4)
##print test_case.num_zombies()
#test_case.add_zombie(0,0)
#test_case.add_zombie(1,1)
##print test_case.num_zombies()
##zomb_gen = test_case.zombies()
##print zomb_gen
##print zomb_gen.next()
##print zomb_gen.next()
##print zomb_gen.next()
#print test_case.compute_distance_field(ZOMBIE)

#obj = Apocalypse(3, 3, [(1,1)], [(0,2)], [(2, 2)])
#obj = Apocalypse(3, 3, [(1,1)], [], [(2, 2)])
#print obj.compute_distance_field(HUMAN), obj.compute_distance_field(ZOMBIE)
#z_d_f = obj.compute_distance_field(ZOMBIE)
#obj.move_humans(z_d_f)
#print obj.compute_distance_field(HUMAN), obj.compute_distance_field(ZOMBIE)
#obj.move_humans(z_d_f)
#print obj.compute_distance_field(HUMAN), obj.compute_distance_field(ZOMBIE)
#obj.move_humans(z_d_f)
#h_d_f = obj.compute_distance_field(HUMAN)
#print obj.compute_distance_field(HUMAN), obj.compute_distance_field(ZOMBIE)
#obj.move_zombies(h_d_f)
#print obj.compute_distance_field(HUMAN), obj.compute_distance_field(ZOMBIE)


# [[4, 3, 2], [3, 9, 1], [2, 1, 0]]

# poc_zombie_gui.run_gui(Apocalypse(30, 40))

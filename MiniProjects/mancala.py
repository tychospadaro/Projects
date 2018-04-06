#!python2
"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]

    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)

    def __str__(self):
        """
        Return string representation for Mancala board
        """
        return str(self._board[::-1])

    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        return all(house == 0 for house in self._board[1:])

    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        return house_num == self._board[house_num] and house_num != 0

    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            self._board[house_num] = 0
            for idx in range(house_num):
                self._board[idx] += 1

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for idx, house in enumerate(self._board[:]):
            if idx > 0 and idx == house:
                return house
        else:
            return 0

    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic:
        After each move, move the seeds in the house closest to the store
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        clone = SolitaireMancala()
        clone.set_board(list(self._board))
        choice = float('inf')
        plan = []
        while choice > 0:
            choice = clone.choose_move()
            plan.append(choice)
            clone.apply_move(choice)

        return plan[:-1] if plan[-1] is 0 else plan

my_board = SolitaireMancala()

my_board.set_board([0, 1, 2, 3, 4, 5, 6])
print [0, 1, 2, 3, 4, 5, 6]
print my_board._board

my_board.set_board([0, 1, 2, 3])
print my_board.plan_moves()

# Create tests to check the correctness of your code

def test_mancala():
    """
    Test code for Solitaire Mancala
    """

    my_game = SolitaireMancala()
    print "Testing init - Computed:", my_game, "Expected: [0]"
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", True

    config1 = [0, 0, 1, 1, 3, 5, 0]
    my_game.set_board(config1)

    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing plan_moves - Computed:", my_game.plan_moves(), "Expected:", [5, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(1), "Expected:", config1[1]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(3), "Expected:", config1[3]
    print "Testing get_num_seeds - Computed:", my_game.get_num_seeds(5), "Expected:", config1[5]
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(5), "Expected:", True
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(1), "Expected:", False
    print "Testing is_legal_move - Computed:", my_game.is_legal_move(0), "Expected:", False
    print "Testing is_game_won - Computed:", my_game.is_game_won(), "Expected:", False
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 5
    print "Testing apply_move - Computed:", my_game.apply_move(0), "Expected:", None
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 5, 3, 1, 1, 0, 0])
    print "Testing apply_move - Computed:", my_game.apply_move(5), "Expected:", None
    print "Testing set_board - Computed:", str(my_game), "Expected:", str([0, 0, 4, 2, 2, 1, 0])
    print "Testing choose_move - Computed:", my_game.choose_move(), "Expected:", 1

    config2 = [0, 0, 1, 1, 3, 0, 0]
    my_game.set_board(config2)
    print "Testing plan_moves - Computed:", my_game.plan_moves(), "Expected:", []

    # add more tests here

test_mancala()


# Import GUI code once you feel your code is correct
# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())

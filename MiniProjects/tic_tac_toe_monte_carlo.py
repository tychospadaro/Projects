#!python2
"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 20        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4


def mc_trial(board, player):
    '''
    A function that takes...
    board 	- a current board (TTTBoard) (ideally, this
            is a copy of the actual game board as it will
            be mutated in liue of returning a value)
    player	- the next player to move (ai)

    The function then alertnates random moves between
    players until the game is resolved (i.e. winner/draw).
    The function does not return anything, but has instead
    returned the input board in the finished state.

    Note: modeled on provided.play_game()
    '''
    curplayer = player
    winner = board.check_win()
#    print 'Run trial'		# Comment out

    while winner == None:
        # play a random empty square
        empties = board.get_empty_squares()
        row, col = random.choice(empties)
        board.move(row, col, curplayer)

        # check winner, switch player
        winner = board.check_win()
        curplayer = provided.switch_player(curplayer)

        # display board
#        print board			# comment out
#        print				# comment out

def mc_update_scores(scores, board, player):
    '''
    A function which takes:
    scores 	- a matrix of scores/weightings
            the same size as the TTTBoard.
    board 	- a completed TTTBoard (from mc_trial)
    player	- the computer player (X/O)

    This function updates the weighting matrix (scores)
    by assessing whether which player is the winner,
    and adjusting the current weighting with the constants
    SCORE_CURRENT (ai) and SCORE_OTHER (dummy_human).
    AI increases weight of its marks on win, or decreases
    on loss, and does the opposite for the dummy_human moves.
    Empty squares and draws recieve no weighting.
    '''
    # initialize result, machine/opponent mark(X/O) and score
    result = board.check_win()
    size = board.get_dim()
    mc_mark = player							# machine X/O
    op_mark = provided.switch_player(player) 	# opponent X/O
    mc_score = SCORE_CURRENT	# weighting for machine square
    op_score = SCORE_OTHER		# weighting for opponent square

    # modify scoring w.r.t. win, return if draw.
    if result == mc_mark:	# machine win
        op_score *= -1
    elif result == op_mark:	# machine loss
        mc_score *= -1
    else:
        return scores		# draw

    # iterate over board/scores and update scores
    for row in range(size):
        for col in range(size):
            value = board.square(row, col)
            if value == mc_mark:
                scores[row][col] += mc_score
            elif value == op_mark:
                scores[row][col] += op_score

#    print_scores(scores)	# comment out
    return scores

def print_scores(scores):
    """
    print scores all pretty like
    code modeled on TTTBoard __str__ method
    """
    rep = ''
    size = len(scores)
    for row in range(size):
        for col in range(size):
            score = str(scores[row][col])
            while len(score) < 4:
                score = ' ' + score
            rep += score
            if col == size - 1:			# @ right edge
                rep += '\n'
            else:
                rep += ' | '			# col sep
        if row != size - 1:       		# not bottom
            rep += '-' * (7 * size - 3) # row sep
            rep += '\n'
    print rep

def get_best_move(board, scores):
    '''
    A function which takes:
    board	- a current live board (TTTBoard)
    scores	- a grid from a completed battery of ntrial
            executions of mc_trial and mc_update_scores

    This function then returns a random move (row, col)
    with a maximum weighting.
    '''
    # helper lambda functions
    value = lambda pos: scores[pos[0]][pos[1]]
    equals_max = lambda pos: value(pos) == max_score

    # determine possible moves (error if no moves possible)
    candidates = board.get_empty_squares()
    assert len(candidates) > 0, 'Error, game complete, no move'
#    print candidates	# Comment out

    # determine max score and filter candidates
    score_lst = list(map(value, candidates))
    max_score = max(score_lst)
    choices = filter(equals_max, candidates)
#    print choices		# Comment out

    # return random selection from viable choices
    return random.choice(choices)

def mc_move(board, player, trials):
    '''
    A function which takes:
    board 	- the current board state (TTTBoard)
    player	- identity of the machine player (X/O)
    trials	- number of trials to run when determining
            the next move via monte carlo simulation.

    The function returns the move of the machine player,
    as a (row, col) tuple.
    '''
    # initialize score matrix, trial counter
    size = board.get_dim()
    score_matrix = [[0 for dummy_col in range(size)] for
                    dummy_row in range(size)]
    trial = 0

    # run trials
    while trial < trials:
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(score_matrix, board_copy, player)
        trial += 1

    # return move
#    print board			# Comment out
    return get_best_move(board, score_matrix)


#test_board = provided.TTTBoard(3)
#print mc_move(test_board, PLAYERX, NTRIALS)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

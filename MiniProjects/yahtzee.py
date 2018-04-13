#! python2
"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_sorted_seq(outcomes, length):
    """
    Function which returns "sorted" sequences, ie, unique sets of sequences
    """

    all_seqs = gen_all_sequences(outcomes, length)
    sorted_seqs = [tuple(sorted(seq)) for seq in all_seqs]
    return set(sorted_seqs)

def remove_used(full, used):
    """
    helper function for gen_permutations, removes items from full list
    """
    unused = list(full)
    for item in used:
        try:
            unused.remove(item)
        except ValueError:
            pass
    return unused

def gen_permutations(outcomes, length):
    """
    Iterative function modeled on gen_all_sequences,
    which return all permutations of a given length from a
    set of possible outcomes.
    """

    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            used = list(seq)
            unused = remove_used(outcomes, used)
#            print 'used', used, '| unused', unused
            for item in unused:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def gen_combinations(outcomes, length):
    """
    a function which returns all possible combinations
    of a given length for set of possible outcomes
    """

    all_perm = gen_permutations(outcomes, length)
    sorted_perm = [tuple(sorted(perm)) for perm in all_perm]
    return set(sorted_perm)

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand, a tuple

    Returns an integer score
    """
    die_vals = set(hand)
    max_score = 0
    for die in die_vals:
        total_val = die * hand.count(die)
        if total_val > max_score:
            max_score = total_val

    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    new_dice = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    new_hands = list(map(lambda dice: tuple(list(held_dice) + list(dice)), new_dice))
    total_hands_scores = sum(map(score, new_hands))
    tally_hands = float(len(new_hands))
    return total_hands_scores/tally_hands


def gen_all_holds(hand):
    """
    Generate ALL possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    held_dice = set([()])

    for idx in range(1, len(hand) + 1):
        held_dice.update(gen_combinations(hand, idx))

    return held_dice

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    possible_holds = gen_all_holds(hand)
    max_exp_val = 0.0
    keep = set()

    for held_dice in possible_holds:
        free_dice =  len(hand) - len(held_dice)
        exp_val = expected_value(held_dice, num_die_sides, free_dice)
        if exp_val > max_exp_val:
            max_exp_val = exp_val
            keep = held_dice

    return (max_exp_val, keep)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


#run_example()
#
#
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

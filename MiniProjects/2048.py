#! python2
"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
#    print
#    print 'begin merge', line
    final_len = len(line)
    condensed_list = list(filter(lambda num: num > 0, line))
    return_line = squish(condensed_list, 0)
    while len(return_line) < final_len:
        return_line += [0]
    return return_line

def squish(condensed_list, start):
    """
    Function that merges adjacent same numbers from the left.
    """
#    print
#    print 'begin squish with ', condensed_list, ' @ ', start
    squished = list(condensed_list)
    for idx, num in enumerate(condensed_list):
        if idx < start:							# not at start
#            print idx, 'less than', start
            continue
        elif idx >= len(squished) - 1:	# at end
#            print idx, 'is end'
            return squished
        elif num == squished[idx + 1]:	# squish
            squished[idx] += squished.pop(idx + 1)
#            print 'send down', squished, idx + 1
            return squish(squished, idx + 1)
    return squished


# print merge([4, 4, 8, 8]), [8, 16, 0, 0]
# print merge([2, 0, 2, 2]), [4, 2, 0, 0]
# print merge([2, 0, 2, 4]), [4, 4, 0, 0]
# print merge([0, 0, 2, 2]), [4, 0, 0, 0]
# print merge([2, 2, 0, 0]), [4, 0, 0, 0]
# print merge([2, 2, 2, 2, 2]), [4, 4, 2, 0, 0]
# print merge([8, 16, 16, 8]), [8, 32, 8, 0]

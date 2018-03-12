"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    shorter_length = min(len(line1),len(line2))
    # Check for mismatch over length of shorter string
    for index in range(shorter_length):
        if line1[index] != line2[index]:
            return index

    same_length = (len(line1) == len(line2))
    # If no mismatch is found over length of shorter string
    if not same_length:
        return shorter_length
    else:
        return IDENTICAL

# Tests of singleline_diff
# print(singleline_diff('', 'line2'))         #0
# print(singleline_diff('li1', 'line1'))      #2
# print(singleline_diff('line1', 'line2'))    #4
# print(singleline_diff('line1', 'line1'))    #-1

def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index of first difference between the lines
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    shorter_length = min(len(line1),len(line2))
    lines = line1+line2
    # Check for valid input (ie single line & index in range)
    if '\n' in lines or '\r' in lines:
        return ""
    elif idx < 0 or shorter_length < idx:
        return ""
    # create separator and return output
    else:
        separator = '=' * idx + '^'
        return '\n'.join([line1, separator, line2]) + '\n'

# Tests of singleline_diff_format
# print(singleline_diff_format('', 'line2', singleline_diff('', 'line2')))         #0
# print(singleline_diff_format('li1', 'line1', singleline_diff('li1', 'line1')))      #2
# print(singleline_diff_format('line1', 'line1', singleline_diff('line1', 'line1')))    #-1
# print(singleline_diff_format('line1', 'line2', singleline_diff('line1', 'line2')))    #4
# print(singleline_diff_format('line1\rline2', 'line2', singleline_diff('line1', 'line2')))    #4
# print(singleline_diff_format('abc', 'abd', 2))
# print(singleline_diff_format('abc','',0))

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs. (line_num, first_diff)

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    shorter_list = min(len(lines1), len(lines2))
    # Check for difference over length of shorter list
    for line_num in range(shorter_list):
        first_diff = singleline_diff(lines1[line_num],lines2[line_num])
        # first_diff = -1 if identical (continue), else return output tuple
        if first_diff >= 0:
            return(line_num, first_diff)

    same_length = (len(lines1) == len(lines2))

    if not same_length:
        return (shorter_list, 0)
    else:
        return (IDENTICAL, IDENTICAL)


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    with open(filename, 'rt') as infile:
        lines = infile.read()
    return lines.splitlines()

# print(get_file_lines('file8.txt'))
# print(get_file_lines('file9.txt'))

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines1, lines2 = get_file_lines(filename1), get_file_lines(filename2)
    line_num, first_diff = multiline_diff(lines1, lines2)

    if line_num < 0:    # ie files IDENTICAL
        return "No differences\n"
    else:
        header = 'Line {}:\n'.format(line_num)
        # Prevents index error if file is empty
        # (Would have done this at get_file_lines... stupid OwlTest)
        line1 = lines1[line_num] if lines1 != [] else ''
        line2 = lines2[line_num] if lines2 != [] else ''
        body = singleline_diff_format(line1, line2, first_diff)
        return header + body

# print(file_diff_format('cancer_risk05_v4_county.csv','cancer_risk05_v4_county_copy.csv'))
print(file_diff_format('file1.txt', 'file2.txt'))
# print(file_diff_format('file1.txt', 'file1.txt'))
# print(file_diff_format('file8.txt', 'file9.txt'))

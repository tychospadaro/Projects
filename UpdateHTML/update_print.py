"""
Note: the "solution" an instance of print that was preceded by
<pre> rather than <pre class='cm'>. docs_updated_soln was hand corrected.
https://www.coursera.org/learn/python-representation/discussions/weeks/4/threads/T8gF1_ZOEee5uA4X_K2X3A


Week 4 practice project template for Python Data Representation
Update syntax for print in CodeSkulptor Docs
from "print ..." syntax in Python 2 to "print(...)" syntax for Python 3
"""
# import os
# print(os.getcwd())

# HTML tags that bounds example code
PREFIX = "<pre class='cm'>"
POSTFIX = "</pre>"
PRINT = "print"


def update_line(line):
    """
    Takes a string line representing a single line of code
    and returns a string with print updated
    """
    # Strip left white space using built-in string method lstrip()
    new_line = line.lstrip()
    striped_spaces = len(line)-len(new_line)

    # If line is print statement,  use the format() method to add insert parentheses
    if new_line.find('print') == 0:
        new_line = "print("+ new_line[6:] +")"

    # Note that solution does not handle white space/comments after print statememt
    new_line = " " * striped_spaces + new_line
    return new_line

# # Some simple tests
# print(update_line(""))
# print(update_line("foobar()"))
# print(update_line("print 1 + 1"))
# print(update_line("    print 2, 3, 4"))

# Expect output
##
##foobar()
##print(1 + 1)
##    print(2, 3, 4)


def update_pre_block(pre_block):
    """
    Take a string that correspond to a <pre> block in html and parses it into lines.
    Returns string corresponding to updated <pre> block with each line
    updated via process_line()
    """
    lines = pre_block.split('\n')
    updated_block = ""
    for line in lines:
        updated_block += update_line(line) + "\n"
    #removes final "new line"
    return updated_block[:-1]

# # Some simple tests
# print(update_pre_block(""))
# print(update_pre_block("foobar()"))
# print(update_pre_block("if foo():\n    bar()"))
# print(update_pre_block("print\nprint 1+1\nprint 2, 3, 4"))
# print(update_pre_block("    print a + b\n    print 23 * 34\n        print 1234"))

# Expected output
##
##foobar()
##if foo():
##    bar()
##print()
##print(1+1)
##print(2, 3, 4)
##    print(a + b)
##    print(23 * 34)
##        print(1234)

def update_file(input_file_name, output_file_name):
    """
    Open and read the file specified by the string input_file_name
    Proces the <pre> blocks in the loaded text to update print syntax)
    Write the update text to the file specified by the string output_file_name
    """
    # open file and read text in file as a string
    with open(input_file_name, 'rt') as infile,\
         open(output_file_name, 'wt') as outfile:

        py2_html = infile.read()

    # split text in <pre> blocks and update using update_pre_block()
        py2_block_list = py2_html.split('<pre')
        fixed_block_list = list(py2_block_list.pop(0))

        for block in py2_block_list:
            body_start = block.index('>')+1
            body_end = block.index('</pre>')

            front = "<pre"+block[:body_start]
            body = update_pre_block(block[body_start:body_end])
            back = block[body_end:]

            fixed_block_list.append(front + body + back)

    # Write the answer in the specified output file
        outfile.write(''.join(fixed_block_list))


# A couple of test files
update_file("table.html", "table_updated.html")
update_file("docs.html", "docs_updated.html")

# Import some code to check whether the computed files are correct
import file_diff
file_diff.compare_files("table_updated.html", "table_updated_soln.html")
file_diff.compare_files("docs_updated.html", "docs_updated_soln.html")

# Expected output
##table_updated.html and table_updated_solution.html are the same
##docs_updated.html and docs_updated_solution.html are the same

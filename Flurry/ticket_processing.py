"""
Project to process Ticket Purchase Summary CSV file exported
from Flurry Sites database with PayPal data.

Ticket orders will be processed and formatted for printing.
"""

import csv

def read_csv(filename, separator=',', quote='"'):
    """
    Inputs:
        filename    - name of CSV file
        separator   - character that separates fields
        quote       - character used to optionally quote fields
    Output:
        Returns a list. Each item corresponds to a row
        in the CSV file where the transaction was completed.
    """
    list_out = []
    with open(filename, newline='') as csv_in:
        csv_reader = csv.DictReader(csv_in, delimiter=separator, quotechar=quote)
        for row in csv_reader:
            if row['Sales state'] == 'completed':
                details = row['Details Summary'].replace('\n','')
                list_out.append(details)
    return list_out

def clean_data(list_in):
    """
    Inputs:
        list_in - filtered list of ticket orders
    Outputs:
        Return list of tuples, each tuple contains
        (last name, first name, note,[tickets])
    """
    notes_list = []
    data_out = []

    for row in list_in:
        trimmed_row = row[row.index('Purchaser Name: ')+16:]
        name = trimmed_row[:trimmed_row.index('<br/>')].strip().title()
        first_name = name[:name.rindex(' ')]    #get first name
        last_name = name[name.rindex(' '):]     #get last name

        trimmed_row = trimmed_row[len(name+'<br/>')+1:]
        if 'Special Instructions:'  in row:     #get notes
            note = trimmed_row[22:trimmed_row.index('<br/>')]
            trimmed_row = trimmed_row[trimmed_row.index('<br/>')+5:]
            notes_list.append((last_name,first_name,note))
        else:
            note = ''

        orders = trimmed_row.split('<br/>')
        tickets = []
        for order in orders:                    #get ticket orders
            if ('Membership Dues' in order) or ('Donation' in order):
                continue
            else:
                tickets.append(order)

        data_out.append([last_name, first_name, note, tickets])
        # print(last_name, first_name,note,tickets)
        # print()

        data_out.sort(key=lambda item: item[1])     #sort by first name (to break last name ties)
        data_out.sort(key=lambda item: item[0])     #sort by last name

    # for idx, note in enumerate(notes_list):       #optional print of all notes
    #     print(idx,note)

    return data_out

def count_tix(list_in):
    """
    Inputs:
        list_in - cleaned data list
    Output:
        Dictionary with count for each ticket type.
    """

    ticket_dict = {
        'Child': 0,
        'FULL FESTIVAL':0,
        'FRIDAY NIGHT':0,
        'SATURDAY DAY':0,
        'SATURDAY NIGHT':0,
        'ALL SATURDAY':0,
        'ALL SUNDAY':0,
        }

    for order in list_in:
        tickets = order[-1]
        for ticket in tickets:
            quant, sep, session = ticket.partition(' ')
            for ticket_type in ticket_dict:
                if ticket_type in session:
                    ticket_dict[ticket_type] = ticket_dict[ticket_type] + int(quant)
    return ticket_dict

def print_clean_data_to_file(list_in, file_name):
    """
    Inputs:
        list_in     - Sorted cleaned data. Each row is [Last, First, Note, [Tix]]
        file_name   - file to output data to
    Outputs:
        Write to file, text of list
    """
    # longest = [0,0,0,0]                   #used to figure out spacing for formatting
    # for order in list_in:
    #     for idx, current in enumerate(longest):
    #         if len(order[idx]) > current:
    #             longest[idx] = len(order[idx])
    # print(longest)
    rows_out =[]

    for order in list_in:
        last = order[0]
        first = order[1]
        note = order[2]
        tix = order[3]

        rows_out.append(f'{last:<18}{first:<19}\n')
        if note != '':
            rows_out.append(f'     Note: {note}\n')
        for ticket in tix:
            # print(last,ticket)
            rows_out.append(' '*32+ticket+'\n')
        rows_out.append('----------------------------------------------------------------------------\n')

    with open(file_name, 'wt') as file_out:
        for line in rows_out:
            file_out.write(line)
        # file_out.writelines(rows_out)


data = read_csv('TicketPurchaseSummary_scrubbed.csv')
# filtered_data = filter_list(data)

# print(len(data))
cleaned_data = clean_data(data)

# for order in cleaned_data:
#     print(order)

print(count_tix(cleaned_data))

print_clean_data_to_file(cleaned_data,'testoutput_scrubbed.txt')

#
# for row in data:
#     print(row)

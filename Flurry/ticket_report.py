"""
Project to process Ticket Purchase Details CSV file exported
from Flurry Sites database with PayPal data.

Ticket orders will be processed to report out # and kind of tickets ordered.
"""

import csv
import datetime
from collections import OrderedDict

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
                list_out.append(row)
    return list_out

def separate_orders_by_order_method(list_in):
    """
    Inputs:
        list_in -  List containing all ticket orders
    Outputs:
        paypal_full - List containing paypal full price orders
        paypal_discount - List containing paypal discount orders
        paper_discount - List containing paper discount orders
    """
    paypal_full, paypal_discount, paper_discount = [], [], []
    PREORDER_DEADLINE = datetime.datetime(2018, 1, 16)

    for order in list_in:
        order_date = datetime.datetime.strptime(order['Created Date'],'%m/%d/%Y')

        if order['Payment Id'] == 'PaperTicket':
            paper_discount.append(order)
        elif order_date <= PREORDER_DEADLINE:
            paypal_discount.append(order)
        elif order_date > PREORDER_DEADLINE:
            paypal_full.append(order)

    return paypal_full, paypal_discount, paper_discount

TICKET_TYPES = [
    'Adult',
    'Child',
    'Teen',
    'Student',
    'Senior',
    'Military',
    'DFO Member',
    ]

def separate_orders_by_ticket_type(list_in, ticket_types):
    """
    Inputs:
        list_in -  List containing ticket orders
        ticket_types - List of all ticket types
    Outputs:
        dict_out - A dictionary keyed to ticket types, containing a list of
            ticket orders of each type
    """
    dict_out = OrderedDict((ticket_type,[]) for ticket_type in ticket_types)

    for order in list_in:
        ticket_order = order['Item name']
        for ticket_type in dict_out:
            if ticket_type in ticket_order:
                dict_out[ticket_type].append(order)
    return dict_out

SESSIONS = [
    'FRIDAY NIGHT',
    'SATURDAY DAY',
    'SATURDAY NIGHT',
    'ALL SATURDAY',
    'ALL SUNDAY',
    'FULL FESTIVAL',
    ]

def separate_orders_by_session(list_in, sessions):
    """
    Inputs:
        dict_in -  A list of orders
        Sessions - List of all ticket types
    Outputs:
        dict_out - A dictionary keyed to ticket types, containing a dictionary of
            ticket orders keyed to session
    """
    dict_out = OrderedDict((session,[]) for session in sessions)

    for order in list_in:
        ticket_order = order['Item name']
        for session in dict_out:
            if session in ticket_order:
                dict_out[session].append(order)
    return dict_out

def crunch_numbers():
    """
    Use the written methods to print number of tickets for each type/session/payment method
    """
    all_orders = read_csv("TicketPurchaseDetails_scrubbed.csv")
    paypal_full, paypal_discount, paper_discount = separate_orders_by_order_method(all_orders)
    orders_by_method = {
        'paypal_full' : paypal_full,
        'paypal_discount' : paypal_discount,
        'paper_discount' : paper_discount,
        }

    for order_method in orders_by_method:
        print(order_method)
        method_orders = orders_by_method[order_method]
        orders_by_ticket_type = separate_orders_by_ticket_type(method_orders, TICKET_TYPES)
        for ticket_type in orders_by_ticket_type:
            print('    '+ticket_type)
            ticket_orders = orders_by_ticket_type[ticket_type]
            orders_by_session = separate_orders_by_session(ticket_orders, SESSIONS)
            for session in orders_by_session:
                session_tix = 0
                for order in orders_by_session[session]:
                    session_tix += int(order['Quantity'])
                print('        '+str(session_tix)+' '+session)

crunch_numbers()

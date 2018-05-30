
from collections import OrderedDict as o_dict

# pet = ('rabbit', 'rat', 'lion', 'fox', 'frog', 'elephant', 'cat', 'dog')
# sport = ('volley', 'ballet', 'basketb', 'soccer', 'baseb', 'hockey', 'box', 'bowl', 'footb')
# social = ('skype', 'fb', 'youtube', 'ebay', 'linkedin', 'instagram', 'g_plus', 'pint', 'twitter')
# ('Country', ['British', 'German', 'American', 'French', 'Japanese', 'Korean', 'Italian', 'Swede', 'Russian']),
# ('Food', ['Banana', 'Cheese', 'Cherry', 'Corn', 'Mushroom', 'Pasta', 'Pineapple', 'Steak', 'Tomato']),
# ('Hospital', ['Blood_bag', 'Pressure_meter', 'Bandage_cross', 'Thermometer', 'Syringe', 'Scalpel', 'Microscope', 'Pill', 'Orthopedic_cast']),
# tool = ('wbarrow', 'handsaw', 'chainsaw', 'snips', 'drill', 'tablesaw', 'shovel', 'wrench', 'hammer')
# game = ('cpu', 'headph', 'handh', 'mouse', 'joystick', 'wheel', 'wii', 'xbox', 'ps')
# name = ('r', 'f', 'w', 'm', 'j', 'l', 's', 'c', 'p')
# job = ('eng', 'dr', 'sci', 'photo', 'teach', 'police', 'art', 'plane', 'dent')
# hat = ('feather', 'cow', 'cap', 'driver', 'santa', 'wiz', 'detective', 'crown', 'grad')
# cash = ('coin1', 'coin5', 'coin10', 'coin25', 'paper1', 'paper5', 'paper10', 'paper20', 'paper50')
# music = ('violin', 'trumpet', 'tamb', 'xylo', 'flute', 'sax', 'keyboard', 'harp', 'guitar')
# drink = ('coffee', 'lime', 'mshake', 'beer', 'water', 'milk', 'coke', 'wine', 'whiskey')
# costume = ('arab', 'devil', 'judge', 'queen', 'sombrero', 'superman', 'uncle_sam', 'king', 'angel')
# ('Vehicle', ['Car', 'Truck', 'Tank', 'Bike', 'Train', 'Zepplin', 'Helicopter', 'Submarine', 'Ambulance']),

# categories = (pet, hospital, sport, social, tool, flag, game, vehicle, name, job, hat, cash, food, music, drink)

#for each puzzle, [(category, [object, ...]), ...]
cat_info = [
    ('Pet', ['Rabbit', 'Rat', 'Lion', 'Panda', 'Fox', 'Frog', 'Elephant', 'Cat', 'Dog']),
    ('Hospital', ['Blood_bag', 'Pressure_meter', 'Bandage_cross', 'Thermometer', 'Syringe', 'Scalpel', 'Microscope', 'Pill', 'Orthopedic_cast']),
    ('Sport', ['Volleyball', 'Ballet', 'Basketball', 'Soccer', 'Baseball', 'Hockey', 'Boxing', 'Bowling', 'Rugby']),
    ('Social_app', ['Skype', 'Facebook', 'YouTube', 'eBay', 'LinkedIn', 'Instagram', 'Google_plus', 'Pinterest', 'Twitter']),
    ('Tool', ['Wheelbarrow', 'Handsaw', 'Chainsaw', 'Clamp', 'Drill', 'Tablesaw', 'Shovel', 'Adjustable_wrench', 'Hammer']),
    ('Country', ['British', 'German', 'American', 'French', 'Japanese', 'Korean', 'Italian', 'Swede', 'Russian']),
    ('Game', ['Computer', 'Headphone', 'Handheld', 'Mouse', 'Joystick', 'Driving_wheel', 'Wii', 'Xbox', 'Playstation']),
    ('Vehicle', ['Car', 'Truck', 'Tank', 'Bike', 'Train', 'Zepplin', 'Helicopter', 'Submarine', 'Ambulance']),
    ('Name', ['Ryan', 'Fred', 'William', 'Mary', 'Johanne', 'Louis', 'Sarah', 'Claude', 'Peter']),
    ('Profession', ['Engineer', 'Doctor', 'Scientist', 'Photographer', 'Teacher', 'Police_officer', 'Painter', 'Airline_pilot', 'Dentist']),
    ('Hat', ['Feather_hat', 'Cowboy_hat', 'Baseball_cap', 'Helmet', 'Santa_claus_hat', 'Wizard_hat', 'Detective_hat', 'Crown', 'Graduation_hat'])
    ]

hints = [
    (('Driving_wheel', 'Cat'), False, 1),
    (('Joystick', 'Frog'), False, 2),
    (('Zepplin', 'Cat'), False, 3),
    (('Cat', 'Tank'), False, 4),
    (('Mary', 'Cat'), False, 5),
    (('Mary', 'Frog'), False, 6),
    (('Scientist', 'Panda'), False, 7),
    (('Engineer', 'Frog'), False, 8),
    (('Rat', 'Wizard_hat'), False, 9),
    (('eBay', 'Pill'), True, 10),
    (('Syringe', 'Wheelbarrow'), False, 11),
    (('Claude', 'Scalpel'), True, 12),
    (('Ryan', 'Blood_bag'), False, 13),
    (('Graduation_hat', 'Orthopedic_cast'), False, 14),
    (('Blood_bag', 'Feather_hat'), False, 15),
    (('Truck', 'Bowling'), True, 16),
    (('Baseball_cap', 'Baseball'), True, 17),
    (('Detective_hat', 'Boxing'), True, 18),
    (('Rugby', 'Wizard_hat'), False, 19),
    (('Russian', 'Pinterest'), False, 20),
    (('French', 'Facebook'), False, 21),
    (('Wii', 'Twitter'), False, 22),
    (('Mary', 'Google_plus'), False, 23),
    (('Fred', 'YouTube'), False, 24),
    (('Johanne', 'YouTube'), False, 25),
    (('Engineer', 'Instagram'), False, 26),
    (('Detective_hat', 'eBay'), True, 27),
    (('Facebook', 'Crown'), False, 28),
    (('British', 'Handsaw'), True, 29),
    (('Handheld', 'Chainsaw'), True, 30),
    (('Ambulance', 'Handsaw'), True, 31),
    (('Peter', 'Wheelbarrow'), False, 32),
    (('Engineer', 'Clamp'), True, 33),
    (('Crown', 'Wheelbarrow'), False, 34),
    (('Baseball_cap', 'Adjustable_wrench'), False, 35),
    (('German', 'Ryan'), True, 36),
    (('Russian', 'Fred'), True, 37),
    (('French', 'Airline_pilot'), False, 38),
    (('German', 'Graduation_hat'), True, 39),
    (('Swede', 'Detective_hat'), True, 40),
    (('French', 'Crown'), False, 41),
    (('Car', 'Driving_wheel'), True, 42),
    (('Claude', 'Joystick'), True, 43),
    (('Painter', 'Driving_wheel'), True, 44),
    (('Louis', 'Train'), True, 45),
    (('Baseball_cap', 'Submarine'), True, 46),
    (('Feather_hat', 'Tank'), False, 47),
    (('Car', 'Cowboy_hat'), True, 48),
    (('Mary', 'Scientist'), True, 49),
    (('Dentist', 'Detective_hat'), True, 50),
    (('Photographer', 'Helmet'), True, 51),
    (('Fox', 'Headphone'), True, 52),
    (('Cat', 'Ambulance'), False, 53),
    (('Claude', 'Panda'), False, 54),
    (('Doctor', 'Dog'), True, 55),
    (('Lion', 'Wizard_hat'), False, 56),
    (('Headphone', 'Microscope'), True, 57),
    (('Police_officer', 'Bandage_cross'), True, 58),
    (('Xbox', 'Hockey'), True, 59),
    (('Soccer', 'Santa_claus_hat'), True, 60),
    (('German', 'YouTube'), False, 61),
    (('Pinterest', 'Playstation'), True, 62),
    (('Johanne', 'Google_plus'), False, 63),
    (('Mary', 'YouTube'), False, 64),
    (('Feather_hat', 'Instagram'), False, 65),
    (('Japanese', 'Tablesaw'), True, 66),
    (('Shovel', 'Car'), True, 67),
    (('Police_officer', 'Hammer'), False, 68),
    (('French', 'Playstation'), False, 69),
    (('American', 'Airline_pilot'), False, 70),
    (('British', 'Wizard_hat'), True, 71),
    (('Bike', 'Mouse'), True, 72),
    (('Scientist', 'Computer'), True, 73),
    (('Sarah', 'Truck'), False, 74),
    (('Truck', 'Crown'), True, 75),
    (('Police_officer', 'Baseball_cap'), True, 76),
    (('Peter', 'Police_officer'), True, 77),
    (('Tank', 'Frog'), False, 78),
    (('Panda', 'Graduation_hat'), False, 79),
    (('Sarah', 'Orthopedic_cast'), False, 80),
    (('Mary', 'Volleyball'), True, 81),
    (('Japanese', 'LinkedIn'), True, 82),
    (('Fred', 'Google_plus'), False, 83),
    (('Korean', 'Wheelbarrow'), False, 84),
    (('Fred', 'Hammer'), False, 85),
    (('Japanese', 'Louis'), True, 86),
    (('French', 'Feather_hat'), False, 87),
    (('Baseball_cap', 'Wii'), False, 88),
    (('Sarah', 'Airline_pilot'), True, 89),
    (('Submarine', 'Rabbit'), True, 90),
    (('Skype', 'Thermometer'), True, 91),
    (('Helmet', 'Ballet'), True, 92),
    (('Painter', 'Instagram'), False, 93),
    (('Hammer', 'Santa_claus_hat'), False, 94),
    (('William', 'Handheld'), True, 95),
    (('Teacher', 'Wizard_hat'), True, 96),
    (('Blood_bag', 'Santa_claus_hat'), False, 97),
    (('Truck', 'Clamp'), False, 98),
    (('Graduation_hat', 'Zepplin'), True, 99),
    (('YouTube', 'Ambulance'), False, 100),
    (('Scientist', 'Lion'), False, 101),
    (('American', 'Feather_hat'), False, 102),
    (('German', 'William'), False, 103),
    ]

'''
# class Category:
#     """
#     a class to hold all the items of a given category
#     """
#     def __init__(self, cat_info):
#         """
#         name    - name of category
#         """
#         self.name = cat_info[0]
#         self.items = [Item(item) for item in cat_info[1]]
#
# class Item(Category):
#     """
#     subclass of category for each item
#     """
#     def __init__(self):
#         """
#         name
#         """
#         pass

class Group:
    """
    collection of clues
    """
    def __init__(self, cat_info, locked):
        """
        """
        self.collection = o_dict((cat, set(items)) for cat, items in cat_info)
        self.lock_items(locked)

    def __repr__(self):
        """
        representation of group
        """
        title_width = 4
        item_with = 4
        str_out = ''
        for cat in self.collection:
            str_out += f"{cat[:title_width]:<{title_width}}| {', '.join(item for item in self.collection[cat])}\n"
        return str_out

    def all_items(self):
        """
        return a set of all items in the collection
        """
        return set().union(*self.collection.values())

    def lock_items(self, true_items):
        """
        reduce a update a category to contain true items
        """
        to_lock = set(true_items)
        for cat, items in self.collection.items():
            if not to_lock.isdisjoint(items):
                items &= to_lock

    def exclude_items(self, false_items):
        """
        remove any false items from categories
        """
        to_remove = set(false_items).intersection(self.all_items())
        for cat, items in self.collection.items():
            if not to_remove.isdisjoint(items):
                items -= to_remove

    def locked_items(self):
        """
        return items from group which are locked
        """
        return {next(iter(item)) for item in self.collection.values() if len(item) == 1}

# test_grp = Group(cat_info, ['Rabbit', 'Xbox'])
# test_grp.exclude_items(['Ryan', 'Tim'])
# test_grp.exclude_items(['Detective_hat', 'Feather_hat', 'Graduation_hat', 'Baseball_cap', 'Crown', 'Cowboy_hat', 'Santa_claus_hat', 'Helmet'])
# print(test_grp)
# print(test_grp.locked_items())

class Grid:
    """
    solution grid for logic puzzle
    """
    def __init__(self, logic_info, clues):
        """
        baseline info for the puzzleself.
        grid        - nested list, 2d grid
        cat_list    - list of categories, equivalent to rows
        clues       - list of clues [(item1, item2, pos/neg, #),...]
        """
        n_row = len(logic_info)
        n_col = len(logic_info[0][1])
        self.grid = [[None for dummy in range(n_col)] for dummy in range(n_row)]
        self.cat_list = [cat_info[0] for cat_info in logic_info]
        self.all_clues = set().union(*logic_info)
        self.clues = list(clues)
        self.groups = {Group(cat_info, clue) for clue in all_clues}
        self.solution = self.solve()

    def __repr__(self):
        """
        print out of grid
        """
        title_width = 6
        str_width = 3
        str_out = ''

        for idx, row in enumerate(self.grid):
            row_title = self.cat_list[idx][:title_width]
            str_out += f'{row_title:<{title_width}}|'
            for item in row:
                str_out += f' {str(item)[:str_width]}'
            str_out += '\n'
        return str_out

    def solve(self):
        """
        logic puzzle solver
        """
        positive_clues = (clue[0] for clue in self.clues if clue[1] == True)
        negative_clues = (clue[0] for clue in self.clues if clue[1] == False)
        # print (f'+ clues: {len(list(positive_clues))}')
        # print (f'- clues: {len(list(negative_clues))}')

        associations = associate(positive_clues)
        disassociations = condense(negative_clues)
        # for index, group in enumerate(associations):
        #     print(f'{index+1:>2}. {group}')
        # for index, (key, val) in enumerate(disassociations.items()):
        #     print(f'{index+1:>2}. {key} - {val}')

        groups = {Group(cat_info, group_info) for group_info in associations}



def associate(clue_list):
    """
    In: List of paired positive_clues (tuple)
    Out: List of groups (sets) of connections between positive_clues
    idea from https://stackoverflow.com/questions/6144262/need-to-create-a-list-of-sets-from-a-list-of-sets-whose-members-may-be-connecte
    """
    group_list = [set(clue) for clue in clue_list]

    while True:
        merged_a_group = False
        merged_groups = [group_list[0]]

        for group in group_list[1:]:
            merge_with_existing = False
            for big_group in merged_groups:
                if not big_group.isdisjoint(group):
                    big_group |= group
                    merged_a_group = True
                    merge_with_existing = True
                    break

            if not merge_with_existing:
                merged_groups.append(group)

        # print (merged_groups)
        if not merged_a_group:
            break
        group_list = merged_groups

    return merged_groups

def condense(clue_list):
    """
    In: List of paired negative_clues (tuple)
    Out: Dict, keys are clues, values are list of nonassociated clues
    """
    nonassoc_dict = {}
    for clue1, clue2 in clue_list:
        add_pair(clue1, clue2, nonassoc_dict)
        add_pair(clue2, clue1, nonassoc_dict)
    return nonassoc_dict

def add_pair(key_clue, val_clue, nonassoc_dict):
    """
    Add val_clue to key_clue's to nonassoc list
    """
    if key_clue not in nonassoc_dict:
        nonassoc_dict[key_clue] = [val_clue]
    else:
        nonassoc_dict[key_clue].append(val_clue)

def merge_groups(group1, group2):
    """
    merge two groups of clues
    """
    pass

my_grid = Grid(cat_info, hints)
print (my_grid)
'''



class Info_group:
    """
    A class that holds a grouping of solution information
    """

    def __init__(self, category_info, in_members, in_non_members = None):
        """
        category_info   - [(cat_name, [cat_mem1, cat_mem2, ...]), ...]
        in_members     - [member1, ...]
        in_non_members  - [non_member1, ...]
        ---------------------------------------------------------------------
        .column         - o_dict{cat_name:{cat_mem1, cat_mem2,...}, ...}
        .members        - {group_mem1, group_mem2, ...}
        .non_members    - {group_non_mem1, group_non_mem2, ...}
        """
        self.column = o_dict((cat, set(cat_mems)) for cat, cat_mems in category_info)
        self.members = set(in_members)
        if in_non_members == None:
            self.non_members = set()
        else:
            self.non_members = set(in_non_members)
        self.update_col()

    def __repr__(self):
        return '{}: {}'.format(self.__class__.__name__,
                                  self.members)

    def __str__(self):
        """return a string of all group members"""
        return '.'.join(self.members)

    def add_member(self, new_member):
        '''
        new_member  - [new_member, ...]
        '''
        self.members |= set(new_member)
        self.update_col()

    def add_non_member(self, new_non_member):
        """
        new_non_member  - [new_non_member, ...]
        """
        self.non_members |= set(new_non_member)
        self.update_col()

    def update_col(self):
        """
        update column to reflect members/non_members
        """
        for category in self.column:
            if len(self.column[category]) == 1:
                self.members |= self.column[category]
            elif not self.members.isdisjoint(self.column[category]):
                self.column[category] &= self.members
            elif not self.non_members.isdisjoint(self.column[category]):
                self.column[category] -= self.non_members

    def get_members(self):
        """
        return - members
        """
        return self.members

    def get_non_members(self):
        """
        return - non_members
        """
        return self.non_members

    def check_complete(self):
        """
        return True if only one member per category
        """
        return all(len(category)==1 for category in self.column.values())

    def is_locked(self, category):
        """
        return True if category has one member
        """
        return len(self.column[category]) == 1

    def num_locked(self):
        """
        return the number of locked categories
        """
        return sum(self.is_locked(category) for category in self.column.keys())

    def unlocked_members(self):
        """
        return members of unlocked catagories
        """
        str_out = ''
        for category in self.column:
            if not self.is_locked(category):
                str_out += f'{category}, {self.column[category]} '
        return str_out

    def getKey(self):
        """
        sorting key for Info_groups
        """
        return self.num_locked()

# def getKey(info_group):
#     return info_group.getKey()

class Grid:
    """
    contains solution grid and all clues
    """

    def __init__(self, cat_info, hints, locked_row = None):
        """
        cat_info   - [(cat_name, [cat_mem1, cat_mem2, ...]), ...]
        hints      - [((item1, item2), T/F, #), ...]
        locked_row - pre-locked in row
        """
        self.cat_info = cat_info
        self.grid = []
        for row in cat_info:
            category = row[0]
            data = [category]
            if locked_row != None and category in locked_row:
                data += row[1]
            else:
                data += [None for _item_ in range(len(row[1]))]
            self.grid.append(data)

        self.cat_dict = {name:members for (name, members) in cat_info}
        all_items = set().union(*self.cat_dict.values())
        self.groups = {Info_group(cat_info, [item]) for item in all_items}
        print('use hints')
        self.use_hints(hints)
        print(self)
        print('\nuse solve')
        self.solve()
        print(self)
        print ()
        # for group in self.groups:
        #     print (group)
            # print (group.num_locked(),group.column)
        # for group in self.groups:
            # if "Swede" in group.get_members():
                # print (group.column)

    def __str__(self):
        """
        return group on each row
        """
        return '\n'.join(str(group) for group in list(self.groups))

    def use_hints(self, hints):
        """
        merge info_groupings based on hints
        """
        for hint in hints:
            item1, item2 = hint[0]
            associative = hint[1]

            group1 = self.find_group(item1)
            group2 = self.find_group(item2)
            if associative == True and group1 != group2:
                self.merge_info_groups(group1, group2)
            elif associative == False:
                group1.add_non_member(list(group2.get_members()))
                group2.add_non_member(list(group1.get_members()))
            self.check_overlap()

    def check_overlap(self):
        """
        check if any groups have overlaping members, if so, merge them
        """
        while True:
            found_overlap = False
            group_queue = list(self.groups)

            for idx, head_group in enumerate(group_queue):
                head_members = head_group.get_members()
                for test_group in group_queue[idx+1 :]:
                    if not head_members.isdisjoint(test_group.get_members()):
                        found_overlap = True
                        # print(f'found overlap: merge {head_group} AND {test_group}')
                        self.merge_info_groups(head_group, test_group)
                        break
                if found_overlap:
                    break           # restart while
            if not found_overlap:
                break               # break while

    def solve(self):
        """
        finish solution by continuing to merge groups with common items
        """
        groups = sorted(self.groups,
                        key=lambda info_group: info_group.num_locked(),
                        reverse=True)
        print (groups)
        # branch_queue = list(self.groups)
        #
        # while True:
        #     merged_any = False                  # group merged this pass, if False at end, break
        #     root_list = [branch_queue[0]]    # use first group in queue as base/root
        #
        #     for branch_group in branch_queue[1:]:     # all other groups
        #         merge_branch = False                # flag for branch merge on pass
        #         branch_members = branch_group.get_members()
        #         for root_group in root_list:
        #             root_members = root_group.get_members()
        #             if not root_members.isdisjoint(branch_members):
        #                 print()
        #                 print(self)
        #                 print(f"Merge: {root_members} AND {branch_members}")
        #                 self.merge_info_groups(root_group, branch_group)
        #                 merged_any = True
        #                 merge_branch = True
        #                 break
        #
        #         if not merge_branch:                # if no merge on pass, branch is orthogonal to
        #             root_list.append(branch_group)  # current roots, add to root list
        #
        #     # print (root_list)
        #     if not merged_any:                      # no merges on pass, should be solved
        #         break
        #     branch_queue = root_list                # reset loop
        #
        # return root_list

    def find_group(self, item):
        """
        return the group which contains the item
        """
        for group in self.groups:
            if item in group.get_members():
                return group
        else:
            raise Exception(f'{item} not found in any group')

    def merge_info_groups(self, group1, group2):
        """
        from two Info_groups, merge 2 into 1.
        """
        # print(f"Merge: {group1} AND {group2}")
        self.groups.remove(group1)
        self.groups.remove(group2)
        # group1.add_member(list(group2.get_members()))
        # group1.add_non_member(list(group2.get_non_members()))
        # self.scrub(group1.get_members(), group1)
        merge_members = group1.get_members() | group2.get_members()
        merge_non_members = group1.get_non_members() | group2.get_non_members()
        self.scrub(merge_members)
        self.groups.add(Info_group(self.cat_info, merge_members, merge_non_members))

    def scrub(self, merge_members):
        """
        remove merge members from incompatible groups
        """
        member_cats = [self.member_cat(mem) for mem in merge_members]
        # print (f'merge_members: {merge_members}')
        # print (f'member_cats: {member_cats}')
        for group in self.groups:
            for cat in member_cats:
                if group.is_locked(cat):
                    group.add_non_member(merge_members)

    def member_cat(self, member):
        """
        return the category of the member
        """
        for cat, members in self.cat_dict.items():
            if member in members:
                return cat

# test0 = Info_group(cat_info, ['Skype','Car'],['Feather_hat', 'Cowboy_hat', 'Baseball_cap', 'Helmet', 'Santa_claus_hat', 'Wizard_hat', 'Detective_hat', 'Crown'])
# test1 = Info_group(cat_info, ['Rabbit','British'])
# test = merge_info_groups(test0, test1)
# print (test.column)
# out = test.column
# print (out)

testgrid = Grid(cat_info, hints)

cat_info1 = [
    ('Hospital', ['Pressure_meter', 'Bandage_cross', 'Thermometer', 'Syringe']),
    ('Vehicle', ['Helicopter', 'Submarine', 'Ambulance', 'Car']),
    ('Country', ['American', 'French', 'Japanese', 'Korean']),
    ('Food', ['Pasta', 'Pineapple', 'Steak', 'Tomato']),
    ]
hints1 =  [
    (('French', 'Car'), True, 1),
    (('Helicopter', 'Pineapple'), False, 2),
    (('Japanese', 'Steak'), True, 3),
    (('French', 'Steak'), False, 4),
    (('Helicopter', 'Thermometer'), False, 5),
    (('Bandage_cross', 'Pineapple'), True, 6),
    (('Ambulance', 'Tomato'), True, 7),
    (('Korean', 'Tomato'), False, 8),
    (('Pasta', 'Helicopter'), False, 9),
    (('Syringe', 'Tomato'), True, 10),
    (('French', 'Pasta'), False, 11),
    (('American', 'Ambulance'), True, 12),
    (('Bandage_cross', 'Car'), True, 13),
    (('Ambulance', 'Syringe'), True, 14),
    (('Japanese', 'Submarine'), False, 15),
    (('Ambulance', 'Thermometer'), False, 16),
    (('American', 'Pineapple'), False, 17),
    (('Korean', 'Bandage_cross'), False, 18),
    ]

# testgrid1 = Grid(cat_info1, hints1)

"""Zoe Berling henryInterfaceClasses Denver University DU ID 872608482"""

class getAuthor():
    """author details"""
    def __init__(self, auth_id, last_name, first_name):
        self.auth_id = auth_id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_auth_id(self):
        return self.auth_id

class getBook():
    """book details"""
    def __init__(self, book_code=None, title=None,publisher_code=None, book_type=None, price=None, paperback=None):
        self.book_code = book_code
        self.title = title
        self.publisher_code = publisher_code
        self.book_type = book_type
        self.price = price
        self.paperback = paperback

    def __str__(self):
        return self.title

    def get_book_code(self):
        if "X" in self.book_code:
            self.book_code= self.book_code.replace("X","")
        return self.book_code

    def get_price(self):
        return self.price

    def get_publisher_code(self):
        return self.publisher_code

    def get_type(self):
        return self.book_type

    def paperback(self):
        return self.paperback

class getWrote():
    """Wrote details"""
    def __init__(self, book_code, author_num, sequence):
        self.book_code = book_code
        self.author_num = author_num
        self.sequence = sequence

    def __str__(self):
        return f'{self.book_code} {self.author_num}'

    def get_book_code(self):
        return self.book_code

    def get_author_num(self):
        return self.author_num

    def get_sequence(self):
        return self.sequence

class getInventory():
    """Inventory details"""
    def __init__(self, book_code, branch_num, on_hand):
        self.book_code = book_code
        self.branch_num = branch_num
        self.on_hand = on_hand

    def __str__(self):
        return f'{self.on_hand}'

    def get_branch_num(self):
        return self.branch_num

class getBranch():
    """branch details"""
    def __init__(self, branch_num, branch_name, branch_location=None, num_employees=None):
        self.branch_num = branch_num
        self.branch_name = branch_name
        self.branch_location = branch_location
        self.num_employees = num_employees

    def __str__(self):
        return f'{self.branch_name}'

    def get_branch_num(self):
        return self.branch_num

    def get_branch_location(self):
        return self.branch_location


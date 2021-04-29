"""Zoe Berling Denver University DU ID 872608482"""

import tkinter as tk
from tkinter import ttk
import mysql.connector
from HenryDAO import HenryDAO

COMBOBOX_WIDTH = 35
PADX=15

def main():
    db = HenryDAO()
    root = tk.Tk()
    create_GUI(root, db)
    root.mainloop()

class create_GUI:
    """Set up the tabs"""
    def __init__(self, r, db):
        self.window = r
        r.title("Henry Bookstore")
        r.geometry('800x400')
        # style = ttk.Style(r)

        mytab = "blue"
        sometab = "black"
        tabbackground = "white"

        s= ttk.Style(r)
        s.configure("TNotebook", background=tabbackground, borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", mytab)],
                    foreground=[("selected", mytab)])
        s.configure("TNotebook.Tab", background=sometab, foreground=sometab)

        # s.theme_create("stylish", parent="alt", settings={
        #     "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        #     "TNotebook.Tab": {
        #         "configure": {"padding": [5, 1], "background": sometab},
        #         "map": {"background": [("selected", mytab)],
        #                 "expand": [("selected", [1, 1, 1, 0])]}}})
        s.configure("")


        # s.theme_use("stylish")
        print(s.theme_names())


        tabControl = ttk.Notebook(r, height=400, width=735)
        self.tab1 = self.create_tab(tabControl, 'Search by Author', 1)
        self.tab2 = self.create_tab(tabControl, 'Search by Category', 2)
        self.tab3 = self.create_tab(tabControl, 'Search by Publisher', 3)

        HenrySBA(self.tab1, db)
        HenrySBC(self.tab2, db)
        HenrySBP(self.tab3, db)

    def create_tab(self, tabControl, title,c):
        tab = ttk.Frame(tabControl)  # tab1 and tab2 are tab window names
        tabControl.add(tab, text=title)  # Blue and Red are tab titles
        tabControl.grid(column=c, row=0,ipadx=15, padx=15)
        return tab

class HenrySBA():
    """Henry Search By Author"""

    def __init__(self, tab, db):
        self.db = db

        # Author
        self.list1 = self.db.getauthordata()
        _avalue = self.authorcomBox(self.list1, tab)

        # Book
        self.list2 = self.db.getbookdata(author_num=self.list1[_avalue].get_auth_id())
        _bvalue = self.bookcomBox(self.list2, tab)

        # Price
        self.price = self.list2[_bvalue].get_price()
        self.price_label(tab)

        # Inventory
        self.list3 = self.db.getinventorydata(book_code=self.list2[_bvalue].get_book_code())

        # Make tree
        self.tree(self.list3, tab)


    def price_label(self, tab):
        price = ttk.Label(tab)
        price.grid(column=6, columnspan=1, row=3)
        price['text'] = f"${self.price}"

        price_text = ttk.Label(tab)
        price_text.grid(column=5, columnspan=1, row=3, padx=45)
        price_text['text'] = "Price: "


    """ComboBoxes!"""
    def authorcomBox(self, list1, tab):
        """Create author comboBox"""
        lab1 = ttk.Label(tab)
        lab1.grid(column=1, columnspan=4, row=4, padx=PADX)
        lab1['text'] = "Author Selection"
        com1 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com1.grid(column=1, columnspan=4, row=5, padx=PADX)
        com1['values'] = [list1[i] for i in range(len(list1))]
        com1.current(0)
        com1.bind("<<ComboboxSelected>>", lambda e: self.authorcomCallback(e, tab))
        return com1.current()


    def bookcomBox(self,list2,tab):
        """Create book comboBox"""
        lab2 = ttk.Label(tab)
        lab2.grid(column=5, columnspan=3, row=4)
        lab2['text'] = "Book Selection"
        com2 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com2.grid(column=5, columnspan=3, row=5)
        com2['values'] = [list2[i] for i in range(len(list2))]
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", lambda e: self.bookcomCallback(e, tab))
        self.price = self.list2[com2.current()].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[com2.current()].get_book_code())
        self.tree(self.list3, tab)

        return com2.current()


    def tree(self, list3, tab):
        """Tree vie for Branch Name and Copies Available"""
        # Treeview
        tree1 = ttk.Treeview(tab, columns=('Your MOM', 'Copies Available'), show='headings')
        tree1.heading('Your MOM', text='Branch Name')
        tree1.heading('Copies Available', text='Copies Available')
        tree1.grid(column=1, columnspan=4, row=3, pady=5, padx=15)



        for i in tree1.get_children():  # Remove any old values in tree list
            tree1.delete(i)

        for rows in list3:
            branch = self.db.getbranchdata(branch_num=rows.get_branch_num())
            tree1.insert("", "end", values=[branch[0], rows])


    """ComoBox Callback Functions"""

    def authorcomCallback(self, event, tab):
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))
        self.list2 = self.db.getbookdata(author_num=self.list1[selIndex].get_auth_id())
        self.bookcomBox(self.list2, tab)


    def bookcomCallback(self, event, tab):
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))

        self.price = self.list2[selIndex].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[selIndex].get_book_code())
        self.tree(self.list3, tab)


class HenrySBC(): # Category
    """Henry Search By Category Functions start here"""

    def __init__(self, tab, db):
        self.db = db

        # Category
        self.list1 = self.db.getcategorydata()
        _avalue = self.categorycomBox(self.list1, tab)

        # Book from Category
        self.list2 = self.db.getbookcategorydata(type=self.list1[_avalue])
        _bvalue = self.bookcomBox(self.list2, tab)

        # Price from Category
        self.price = self.list2[_bvalue].get_price()
        self.price_label(tab)

        # Inventory
        self.list3 = self.db.getinventorydata(book_code=self.list2[_bvalue].get_book_code())

        # Author from Category
        self.list4 = self.db.getauthorfrombook(self.list2[_bvalue].get_book_code())
        self.authorcomBox(self.list4, tab)

        # Make tree
        self.tree(self.list3, tab)


    def price_label(self, tab=None): # Category
        price = ttk.Label(tab)
        price.grid(column=6, columnspan=1, row=3)
        price['text'] = f"${self.price}"

        price_text = ttk.Label(tab)
        price_text.grid(column=5, columnspan=1, row=3, padx=45)
        price_text['text'] = "Price: "


    """ComboBoxes!"""
    def categorycomBox(self, list1,tab): # Category
        """Create author comboBox"""
        lab1 = ttk.Label(tab)
        lab1.grid(column=1, columnspan=4, row=4)
        lab1['text'] = "Category Selection"
        com1 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com1.grid(column=1, columnspan=4, row=5)
        com1['values'] = [list1[i] for i in range(len(list1))]
        com1.current(0)
        com1.bind("<<ComboboxSelected>>", lambda e: self.categorycomCallback(e, tab))
        return com1.current()


    def bookcomBox(self,list2,tab): # Category
        """Create book comboBox"""
        lab2 = ttk.Label(tab)
        lab2.grid(column=5, columnspan=3, row=4)
        lab2['text'] = "Book Selection"
        com2 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com2.grid(column=5, columnspan=3, row=5)
        com2['values'] = [list2[i] for i in range(len(list2))]
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", lambda e: self.bookcomCallback(e, tab))
        self.price = self.list2[com2.current()].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[com2.current()].get_book_code())
        self.tree(self.list3, tab)

        self.list4 = self.db.getauthorfrombook(self.list2[com2.current()].get_book_code())
        self.authorcomBox(self.list4, tab)

        return com2.current()


    def authorcomBox(self,list4,tab): # Category
        """Create book comboBox"""
        lab3 = ttk.Label(tab)
        lab3.grid(column=5, columnspan=3, row=6)
        lab3['text'] = "Author(s)"
        com3 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com3.grid(column=5, columnspan=3, row=7)
        com3['values'] = [list4[i] for i in range(len(list4))]
        com3.current(0)
        return com3.current()


    def tree(self, list3, tab): # Category
        """Tree vie for Branch Name and Copies Available"""
        # Treeview
        tree1 = ttk.Treeview(tab, columns=('Your MOM', 'Copies Available'), show='headings')
        tree1.heading('Your MOM', text='Branch Name')
        tree1.heading('Copies Available', text='Copies Available')
        tree1.grid(column=1, columnspan=4, row=3, pady=5, padx=PADX)



        for i in tree1.get_children():  # Remove any old values in tree list
            tree1.delete(i)

        for row in list3:
            branch = self.db.getbranchdata(branch_num=row.get_branch_num())
            tree1.insert("", "end", values=[branch[0], row])
                # tree1.insert("", "end", values=[row, "check please"])



    """ComoBox Callback Functions"""

    def categorycomCallback(self, event, tab): # Category
        """ get books where category == text in box"""
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))

        self.list2 = self.db.getbookcategorydata(type=self.list1[selIndex])
        self.bookcomBox(self.list2, tab)



    def bookcomCallback(self, event, tab): # Category
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))

        self.price = self.list2[selIndex].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[selIndex].get_book_code())
        self.tree(self.list3, tab)

        self.list4 = self.db.getauthorfrombook(self.list2[selIndex].get_book_code())
        self.authorcomBox(self.list4, tab)


class HenrySBP(): # By Publisher
    """Henry Search By Publisher"""
    # def __init__(self, create_gui):
    #     super(HenryDAO,self).__init__(create_gui)
    #     self.tab = create_gui.tab1
    def __init__(self, tab, db):
        self.db = db

        # Publisher
        self.list1 = self.db.getpublisherdata()
        _avalue = self.publishercomBox(self.list1, tab)

        print(self.list1[_avalue])

        # Book from Publisher
        self.list2 = self.db.getbookpublisherdata(publisher_name=self.list1[_avalue])
        _bvalue = self.bookcomBox(self.list2, tab)
        print(_bvalue)

        # Price from Category
        self.price = self.list2[_bvalue].get_price()
        self.price_label(tab)
        print(self.list2[_bvalue])

        # Inventory
        self.list3 = self.db.getinventorydata(book_code=self.list2[_bvalue].get_book_code())

        # Author from Category
        self.list4 = self.db.getauthorfrombook(self.list2[_bvalue].get_book_code())
        self.authorcomBox(self.list4, tab)

        # Make tree
        self.tree(self.list3, tab)



    """ComboBoxes!"""
    def publishercomBox(self, list1,tab): # Publisher
        lab1 = ttk.Label(tab)
        lab1.grid(column=1, columnspan=4, row=4)
        lab1['text'] = "Category Selection"
        com1 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com1.grid(column=1, columnspan=4, row=5)
        com1['values'] = [list1[i] for i in range(len(list1))]
        com1.current(0)
        com1.bind("<<ComboboxSelected>>", lambda e: self.publishercomCallback(e, tab))
        return com1.current()


    def bookcomBox(self,list2,tab): # Publisher
        """Create book comboBox"""
        lab2 = ttk.Label(tab)
        lab2.grid(column=5, columnspan=3, row=4)
        lab2['text'] = "Book Selection"
        com2 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com2.grid(column=5, columnspan=3, row=5)
        com2['values'] = [list2[i] for i in range(len(list2))]
        com2.current(0)
        com2.bind("<<ComboboxSelected>>", lambda e: self.bookcomCallback(e, tab))
        self.price = self.list2[com2.current()].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[com2.current()].get_book_code())
        self.tree(self.list3, tab)

        self.list4 = self.db.getauthorfrombook(self.list2[com2.current()].get_book_code())
        self.authorcomBox(self.list4, tab)

        return com2.current()


    def authorcomBox(self,list4,tab): # Publisher
        """Create book comboBox"""
        lab3 = ttk.Label(tab)
        lab3.grid(column=5, columnspan=3, row=6)
        lab3['text'] = "Author(s)"
        com3 = ttk.Combobox(tab, width=COMBOBOX_WIDTH, state="readonly")
        com3.grid(column=5, columnspan=3, row=7)
        com3['values'] = [list4[i] for i in range(len(list4))]
        com3.current(0)
        return com3.current()


    def tree(self, list3, tab): # Publisher
        """Tree vie for Branch Name and Copies Available"""
        # Treeview
        tree1 = ttk.Treeview(tab, columns=('Your MOM', 'Copies Available'), show='headings')
        tree1.heading('Your MOM', text='Branch Name')
        tree1.heading('Copies Available', text='Copies Available')
        tree1.grid(column=1, columnspan=4, row=3, pady=5, padx=PADX)



        for i in tree1.get_children():  # Remove any old values in tree list
            tree1.delete(i)

        for row in list3:
            branch = self.db.getbranchdata(branch_num=row.get_branch_num())
            tree1.insert("", "end", values=[branch[0], row])
                # tree1.insert("", "end", values=[row, "check please"])

    def price_label(self, tab=None): # Category
        price = ttk.Label(tab)
        price.grid(column=6, columnspan=1, row=3)
        price['text'] = f"${self.price}"

        price_text = ttk.Label(tab)
        price_text.grid(column=5, columnspan=1, row=3, padx=45)
        price_text['text'] = "Price: "



    """ComoBox Callback Functions"""

    def publishercomCallback(self, event, tab):  # Publisher
        """ get books where category == text in box"""
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))
        self.list2 = self.db.getbookpublisherdata(publisher_name=self.list1[selIndex])
        _bvalue = self.bookcomBox(self.list2, tab)


    def bookcomCallback(self, event, tab): # Publisher
        selIndex = event.widget.current()
        print(type(selIndex))
        print("Index selected is: " + str(selIndex))

        self.price = self.list2[selIndex].get_price()
        self.price_label(tab)

        self.list3 = self.db.getinventorydata(book_code=self.list2[selIndex].get_book_code())
        self.tree(self.list3, tab)

        self.list4 = self.db.getauthorfrombook(self.list2[selIndex].get_book_code())
        self.authorcomBox(self.list4, tab)




if __name__ == '__main__':
    main()
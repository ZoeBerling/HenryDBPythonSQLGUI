"""Zoe Berling HenryDAO Denver University DU ID 872608482"""

import mysql.connector

from henryInterfaceClasses import getAuthor
from henryInterfaceClasses import getBook
from henryInterfaceClasses import getWrote
from henryInterfaceClasses import getInventory
from henryInterfaceClasses import getBranch
# from my_SQL_root_data import passwd, database, host


class HenryDAO():
    """create database connection. Enter info or import to variables"""
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user='root',
            passwd=passwd,
            database=database,
            host=host)
        self.mycur = self.mydb.cursor()

    def close(self):
        self.mydb.commit()
        self.mydb.close()

    def getauthordata(self):
        """Author information (authors that have books in system)"""
        # perform query
        sql = "SELECT DISTINCT(a.AUTHOR_NUM), a.AUTHOR_LAST, a.AUTHOR_FIRST "\
              "FROM henry_author a "\
              "JOIN henry_wrote w "\
              "ON w.AUTHOR_NUM = a.AUTHOR_NUM " \
              "ORDER BY a.AUTHOR_FIRST"
        self.mycur.execute(sql)
        author_list = []

        for row in self.mycur:
            auth_id = row[0]
            last_name = row[1]
            first_name = row[2]
            author_list.append(getAuthor(auth_id, last_name, first_name))
        return author_list


    def getbookdata(self, author_num):
        """Book Information from author name"""
        sql = "SELECT b.BOOK_CODE, b.TITLE, b.PUBLISHER_CODE, b.TYPE, b.PRICE, b.PAPERBACK, w.AUTHOR_NUM, w.SEQUENCE " \
              "FROM henry_book b " \
              "JOIN henry_wrote w " \
              "ON b.BOOK_CODE = w.BOOK_CODE " \
              f"WHERE w.AUTHOR_NUM = {author_num} "
        self.mycur.execute(sql)
        book_list = []

        for row in self.mycur:
            book_code = row[0]
            title = row[1]
            publisher_code = row[2]
            type = row[3]
            price = row[4]
            paperback = row[5]
            book_list.append(getBook(book_code,title,publisher_code,type,price,paperback))
        return book_list

    def getinventorydata(self, book_code):
        """Inventory Information from book code"""
        # perform query
        sql = "SELECT hi.BOOK_CODE, hi.BRANCH_NUM, hi.ON_HAND " \
              "FROM henry_inventory hi " \
              "JOIN henry_book b " \
              "ON hi.BOOK_CODE = b.BOOK_CODE " \
              f"WHERE hi.BOOK_CODE = {book_code} "
        self.mycur.execute(sql)
        inventory_list = []

        for row in self.mycur:
            book_code = row[0]
            branch_num = row[1]
            on_hand = row[2]
            inventory_list.append(getInventory(book_code, branch_num, on_hand))
        return inventory_list

    def getbranchdata(self,branch_num):
        """Branch Information" from branch number"""
        sql = "SELECT br.BRANCH_NUM, br.BRANCH_NAME " \
              "FROM henry_branch br " \
              "JOIN henry_inventory hi " \
              "ON br.BRANCH_NUM = hi.BRANCH_NUM " \
              f"WHERE br.BRANCH_NUM = {branch_num} "
        self.mycur.execute(sql)
        branch_list = []
        for row in self.mycur:
            branch_num = row[0]
            branch_name = row[1]
            branch_list.append(getBranch(branch_num=branch_num, branch_name=branch_name))
        return branch_list


    def getcategorydata(self):
        """distinct list of categories: not connected to an interface class"""
        sql = "SELECT DISTINCT(b.TYPE) " \
              "FROM henry_book b " \
              "ORDER BY b.TYPE "
        self.mycur.execute(sql)
        category_list = []
        for row in self.mycur:
            book_type = row[0]
            # new = getCategories(book_type)
            # category_list.append(new)
            category_list.append(book_type)
        return category_list

    def getbookcategorydata(self, type):
        """get books in a category"""
        sql = "SELECT BOOK_CODE, TITLE, PRICE " \
              "FROM henry_book " \
              f"WHERE TYPE = '{type}' "

        self.mycur.execute(sql)

        book_titles = []
        for row in self.mycur:
            book_code = row[0]
            book_title = row[1]
            price = row[2]
            book_titles.append(getBook(book_code=book_code, title=book_title, price=price))
        return book_titles

    def getauthorfrombook(self, book_code):
        """not connected to a class because this doesn't need to populate more information"""
        sql = "SELECT CONCAT(a.AUTHOR_FIRST, ' ', a.AUTHOR_LAST) " \
              "FROM henry_book b " \
              "JOIN henry_wrote w " \
              "ON b.BOOK_CODE = w.BOOK_CODE " \
              "JOIN henry_author a " \
              "ON a.AUTHOR_NUM = w.AUTHOR_NUM " \
              f"WHERE b.BOOK_CODE = {book_code} "
        self.mycur.execute(sql)

        author_names = []
        for row in self.mycur:
            author = row[0]
            author_names.append(author)
        return author_names

    def getpublisherdata(self): # Get distinct Publisher list
        """get list of unique publishers (not connected to an interface class)"""
        sql = "SELECT distinct p.PUBLISHER_NAME " \
              "FROM henry_book b " \
              "JOIN henry_publisher p " \
              "ON b.PUBLISHER_CODE = p.PUBLISHER_CODE "
        self.mycur.execute(sql)
        publisher_list = []
        for row in self.mycur:
            publisher = row[0]
            publisher_list.append(publisher)
        return publisher_list

    def getbookpublisherdata(self, publisher_name):
        """get book titles based on publisher"""
        sql = "SELECT b.BOOK_CODE, b.TITLE, b.PRICE " \
              "FROM henry_book b " \
              "JOIN henry_publisher p " \
              "ON b.PUBLISHER_CODE = p.PUBLISHER_CODE " \
              f"WHERE p.PUBLISHER_NAME = '{publisher_name}' "

        self.mycur.execute(sql)

        book_titles = []
        for row in self.mycur:
            book_code = row[0]
            book_title = row[1]
            price = row[2]
            # book_titles.append(getBookPublisher(book_code, book_title, price))
            book_titles.append(getBook(book_code=book_code, title=book_title, price=price))
        return book_titles

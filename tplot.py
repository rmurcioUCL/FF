import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
        return conn
    except Error as e:
        print(e)
 
    return None

def main():
    database = "D:/sqlite-tools-win32-x86-3250200/ff.db"
        # create a database connection
    conn = create_connection(database)

if __name__ == '__main__':  
    main()
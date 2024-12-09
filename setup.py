import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import random 
import numpy as np
from datetime import date

engine = create_engine('sqlite://', echo=False)

books_db = pd.read_csv('longlist.csv')
groups_db = pd.read_csv('groups.csv')
students_db = pd.read_csv('Class_list.csv')

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create books table and insert values
def create_books_table():
    print("Creating Books Table...")    
    cursor.execute("CREATE TABLE IF NOT EXISTS BOOKS(id INTEGER PRIMARY KEY, isbn varchar(14), title varchar(100), author varchar(100), translator varchar(50), format varchar(50), page INTEGER, publisher varchar(50), published varchar(50), year INTEGER, votes float, rating float)")

def create_books_values():
    print("Inserting values into table...")
    for index, row in books_db.iterrows():       
        cursor.execute(f"INSERT INTO BOOKS (id, isbn, title, author, translator, format, page, publisher, published, year, votes, rating) values({index+1}, {row.isbn}, '{row.title}', '{row.author}', '{row.translator}', '{row.format}', {row.pages}, '{row.publisher}', '{row.published}', {row.year}, {row.votes}, {row.rating})")

# Create groups table and insert values
def create_groups_table():
    print("Creating Groups Table...")    
    cursor.execute("CREATE TABLE IF NOT EXISTS GROUPS(id INTEGER PRIMARY KEY, name varchar(50))")

def create_groups_values():
    print("Inserting values into table...")
    for index, row in groups_db.iterrows():       
        cursor.execute(f"INSERT INTO GROUPS (id, name) VALUES({index+1}, '{row.groupname}')")

# Create students table and insert values
def create_students_table():
    print("Creating Student Table...")    
    cursor.execute("CREATE TABLE IF NOT EXISTS STUDENTS(id INTEGER PRIMARY KEY, last varchar(50), first varchar(50), groupname INTEGER, FOREIGN KEY(groupname) REFERENCES GROUPS(id) )")

def create_students_values():
    print("Inserting values into table...")
    for index, row in students_db.iterrows():       
        cursor.execute(f"INSERT INTO STUDENTS (id, last, first) VALUES({index+1}, '{row.Lastname}', '{row.Firstname}')")

# Create library table and insert values
def create_library_table():
    print("Creating Library Table...")    
    cursor.execute("CREATE TABLE IF NOT EXISTS LIBRARY(id INTEGER PRIMARY KEY, title INTEGER, location INTEGER, checkoutdate REAL, returndate REAL, FOREIGN KEY(title) REFERENCES BOOKS(title), FOREIGN KEY(location) REFERENCES STUDENTS(id))")

def create_library_values():
    print("Inserting values into table...")
    for index, row in books_db.iterrows():       
        cursor.execute(f"INSERT INTO LIBRARY (id, title, location) VALUES({index+1}, '{index+1}', 'Library')")

# Checks if a table exists in an SQLite database.
def check_if_table_exists(conn, table_name):
 
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    if cursor.fetchone() is None:
        return True
    else:
        return False        

# ----- Start ----
# Check for table existance 
if check_if_table_exists(conn, 'BOOKS'):
    create_books_table()
    create_books_values()
    conn.commit()

if check_if_table_exists(conn, 'GROUPS'):
    create_groups_table()
    create_groups_values()
    conn.commit()

if check_if_table_exists(conn, 'STUDENTS'):
    create_students_table()
    create_students_values()
    conn.commit()

if check_if_table_exists(conn, 'LIBRARY'):
    create_library_table()
    create_library_values()
    conn.commit()

# Assign Random Groups
groups = ['1', '1', '1', '1', '2', '2', '2', '2', '3', '3', '3', '3', '4', '4', '4', '4']
random.shuffle(groups)
for index in range(len(groups)):
    data=cursor.execute(f"""UPDATE STUDENTS SET groupname = '{groups[index]}' WHERE id = {index}""")
conn.commit()

# Assign Random Books
randombooks = np.arange(1,79)
np.random.shuffle(randombooks)
randombooks = randombooks[:36]

for index, book_id in enumerate(randombooks):
    x = index // 3  # Compute x based on index
    y = index % 3   # Compute y based on index (not used in your query)
    data = cursor.execute(f"""UPDATE LIBRARY SET location = '{x + 1}', checkoutdate = julianday('now'), returndate = julianday('now', '+30 days') WHERE id = {book_id}""")

conn.commit()
# Test code

# Close connection
conn.close()
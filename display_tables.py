import pandas as pd
import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()


def display_table(table_name):
    data=cursor.execute(f'''SELECT * FROM {table_name}''') 
    for row in data: 
        print(row) 
    input()

display_table("BOOKS")
display_table("STUDENTS")
display_table("LIBRARY")
display_table("GROUPS")

conn.close()
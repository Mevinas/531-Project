import pandas as pd
from datetime import date
import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

data=cursor.execute(f'''SELECT count(id) FROM BOOKS''') 
result = data.fetchone()

print(f"Total book count is {result}")
#for index, row in df.iterrows():       
#    print(row.Lastname)

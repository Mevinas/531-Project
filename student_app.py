import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

def main_menu():
    exit = False
    menu = """
--[ Main Menu ]--\n
1: Enter Student ID
2: Enter by name
3: Show Students Per Group
4: Show Class List
Q: Quit Application\n"""

    while(not exit):
        userinput = input(menu).lower()
    # Enter Student ID
        if userinput == '1':
            studentid = input("Enter Student ID: ")

            # Student Name
            data=cursor.execute(f'''SELECT first, groupname FROM STUDENTS WHERE id = '{studentid}';''')
            name = data.fetchone()
            groupid = name[1]
            print(f"Hello {name[0]}")

            # Books from Student
            data=cursor.execute(f'''SELECT BOOKS.title, location, date(julianday(checkoutdate)), date(julianday(returndate)) FROM LIBRARY 
                                INNER JOIN BOOKS on LIBRARY.title = BOOKS.id WHERE location = '{studentid}';''')                                
            print("You have checked out the following: ")             
            for row in data:            
                print(f"Book title: {row[0]}, checked out on {row[2]}, with a returndate of {row[3]}")
                    
            #data=cursor.execute(f'''Select groupname from STUDENTS WERE first LIKE '{studentname}';''')
            #studentid = data.fetchone()
            # Student Group
            data=cursor.execute(f'''SELECT GROUPS.name FROM GROUPS WHERE GROUPS.id = '{groupid}';''') 
            group = data.fetchone()
            if isValid(group):
                print(f"You belong to group {group[0]}")

    # Enter Student Name
        elif userinput == '2':
            studentname = input("Enter Student name: ")

            # Student Name
            try: 
                data=cursor.execute(f'''SELECT first, last, groupname, id FROM STUDENTS WHERE first LIKE '{studentname}';''')
                name = data.fetchone()
                print(f"Hello {name[0]}")

                
                # Books from Student
                data=cursor.execute(f'''SELECT BOOKS.title, location, date(julianday(checkoutdate)), date(julianday(returndate)) FROM LIBRARY 
                                    INNER JOIN BOOKS on LIBRARY.title = BOOKS.id WHERE location = '{name[3]}';''') 
                print("You have checked out the following: ")
                for row in data: 
                    print(f"Book title: {row[0]}, checked out on {row[2]}, with a return date of {row[3]}")
                
                # Student Group
                data=cursor.execute(f'''SELECT GROUPS.name FROM GROUPS WHERE GROUPS.id = '{name[2]}';''')             
                group = data.fetchone()
                print(f"You belong to group {group[0]}")
            except:
                print("Student not found.")
        

    # Show Groups
        elif userinput == '3':
            userinput = input("Group Name: ")
            data=cursor.execute(f'''SELECT STUDENTS.last, STUDENTS.first FROM STUDENTS
                                INNER JOIN GROUPS on GROUPS.id = STUDENTS.groupname                    
                                WHERE GROUPS.name = '{userinput}';''') 
            display(data)

    # Show Students
        elif userinput == '4':
            data=cursor.execute(f'''SELECT first, GROUPS.name FROM STUDENTS 
                                INNER JOIN GROUPS on GROUPS.id = STUDENTS.groupname''') 
            display(data)
        
        elif userinput == 'exit' or userinput == 'q':
            exit = True
    conn.close()

# Check if data is valid
def isValid(data):    
    if data is not None:
        return True
    return False

# Display results
def display(data):    
    for row in data: 
        print(row)

if __name__ == '__main__':
    main_menu()    

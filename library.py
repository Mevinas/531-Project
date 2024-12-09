import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()


def main_menu():    
    menu = """
--[ Main Menu ]--\n
1: Show Books
2: Check in or out books
Q: Quit Application\n
"""

    while(True):
        userinput = input(menu).lower()
        if userinput == '1':
            book_menu()
        if userinput == '2':
            check_menu()
        elif userinput in {'exit', 'q'}:
            break
        else:
            print("Invalid option. Please try again.")
            exit = True
    conn.close()

def book_menu():
    exit = False
    menu = """
--[ Books ]--\n
1: Show All Books
2: Show Books in Library
3: Show Checked Out Books
4: Show highest rated books
5: Show lowest rated books
R: Return\n"""

    while(not exit):
        userinput = input(menu).lower()
        # Show books by user ID
        if userinput == '1':
            print("Showing All Books:\n")
            data=cursor.execute('''SELECT BOOKS.title, location FROM LIBRARY 
                                INNER JOIN BOOKS on LIBRARY.title = BOOKS.id;''') 
            display(data)
        # Show books in Library
        elif userinput == '2':
            print("Showing All Books in Library:\n")
            data=cursor.execute('''SELECT BOOKS.title, location FROM LIBRARY 
                                INNER JOIN BOOKS on LIBRARY.title = BOOKS.id WHERE location = 'Library';''') 
            display(data)
        # Show all checked out books
        elif userinput == '3':
            print("Showing All Books checked out:\n")
            data=cursor.execute('''SELECT BOOKS.title, location, date(julianday(checkoutdate)), date(julianday(returndate)) FROM LIBRARY 
                                INNER JOIN BOOKS on LIBRARY.title = BOOKS.id WHERE location != 'Library';''') 
            display(data)

        # Display Highest Rating Books
        elif userinput == '4':
            print("Showing highest rated books:\n")
            data=cursor.execute('''Select avg(rating) rating FROM BOOKS
                                ''' )
            avgrating = data.fetchone()
            rating = avgrating[0]            
            data=cursor.execute(f'''Select Books.title, rating FROM BOOKS 
                                WHERE rating > {rating}''' )
            display(data)
        # Display Lowest Rating Books
        elif userinput == '5':    
            print("Showing lowest rated books:\n")
            data=cursor.execute('''Select avg(rating) rating FROM BOOKS
                                ''' )
            avgrating = data.fetchone()
            rating = avgrating[0]            
            data=cursor.execute(f'''Select Books.title, rating FROM BOOKS 
                                WHERE rating < {rating}''' )
            display(data)
        # Exit
        elif userinput == 'exit' or userinput == 'r':
            exit = True

def check_menu():
    exit = False
    menu = """
--[ Check in and out ]--\n
1: Check out book to student
2: Check in book
R: Return\n"""
    while(not exit):
        userinput = input(menu).lower()
        if userinput == '1':
            bookid = input("Book ID: ")
            studentid = input("Student ID: ")
            try:
                data=cursor.execute(f"""UPDATE LIBRARY SET location = '{studentid}', checkoutdate = julianday('now'), returndate = julianday('now', '+30 days') WHERE id = '{bookid}'""")                
                print(f'Checked out book: {bookid} to student: {studentid}')    
            except:
                print("Invalid Input")
            conn.commit()
        elif userinput == '2':
            bookid = input("Book ID: ")            
            data=cursor.execute(f"""UPDATE LIBRARY SET location = 'Library', checkoutdate = julianday('now'), returndate = julianday('now', '+30 days') WHERE id = '{bookid}'""")
            print(f'Checked in book: {bookid}')    
            conn.commit()
        
        elif userinput == 'exit' or userinput == 'r':
            exit = True

def display(data):
    for row in data: 
        print(row)

if __name__ == '__main__':
    main_menu()

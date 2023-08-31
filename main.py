from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk
import mysql.connector
from mysql.connector import errorcode
import sys
import re


class Window:
    def __init__(self, root, db_name, conn, cursor):
        self.root = root
        self.db_name = db_name
        self.conn = conn
        self.cursor = cursor

        # Create Window
        self.root.title('Phonebook')
        self.root.iconbitmap('assets/phonebook-9.ico')
        self.root.geometry('700x400')
        self.root.resizable(False, False)

        # Entry Frame
        self.entry_frame = Frame(self.root, bg='gray')
        self.entry_frame.place(x=10, y=10, width=300, height=380)
        self.entry_frame_label = Label(self.entry_frame, text='Contacts', font=('norwester', 30), bg='gray')
        self.entry_frame_label.place(x=65, y=5)

        self.man_icon = ImageTk.PhotoImage(file='assets/man.png')
        self.man_icon_label = Label(self.entry_frame, image=self.man_icon, bg='gray')
        self.man_icon_label.place(x=25, y=110)

        self.phone_icon = ImageTk.PhotoImage(file='assets/phone.png')
        self.phone_icon_label = Label(self.entry_frame, image=self.phone_icon, bg='gray')
        self.phone_icon_label.place(x=25, y=205)

        # Contact Information
        self.firstname_label = Label(self.entry_frame, text='First Name', font=('RobotoCondensed-Light', 12, 'bold'),
                                     bg='gray')
        self.firstname_label.place(x=100, y=70)
        self.user_firstname = Entry(self.entry_frame, font=('RobotoCondensed-Light', 15), bg='white', width=15)
        self.user_firstname.place(x=102, y=95)

        self.lastname_label = Label(self.entry_frame, text='Last Name', font=('RobotoCondensed-Light', 12, 'bold'),
                                    bg='gray')
        self.lastname_label.place(x=100, y=130)
        self.user_lastname = Entry(self.entry_frame, font=('RobotoCondensed-Light', 15), bg='white', width=15)
        self.user_lastname.place(x=102, y=155)

        self.phone_number_label = Label(self.entry_frame, text='Phone Number',
                                        font=('RobotoCondensed-Light', 12, 'bold'), bg='gray')
        self.phone_number_label.place(x=100, y=200)
        self.user_phone_number = Entry(self.entry_frame, font=('RobotoCondensed-Light', 15), bg='white', width=15)
        self.user_phone_number.place(x=102, y=225)

        # Database frame
        self.db_frame = Frame(self.root, bg='lightgray')
        self.db_frame.place(x=320, y=10, width=370, height=380)
        self.db_view = ttk.Treeview(self.db_frame)
        self.db_view['columns'] = ("First Name", "Last Name", "Phone Number")
        self.db_view.column("#0", width=0, stretch=False)
        self.db_view.column("First Name", anchor=W, width=116)
        self.db_view.column("Last Name", anchor=W, width=116)
        self.db_view.column("Phone Number", anchor=CENTER, width=116)

        # Create Headings
        self.db_view.heading("First Name", text="First Name", anchor=W)
        self.db_view.heading("Last Name", text="Last Name", anchor=W)
        self.db_view.heading("Phone Number", text="Phone Number", anchor=CENTER)
        self.db_view.place(x=10, y=10)

        self.cursor.execute('SELECT * FROM contacts')
        for row in self.cursor.fetchall():
            self.db_view.insert("", "end", values=(row[0], row[1], row[2]))

        # Buttons
        self.add_contact_button = Button(self.entry_frame, command=self.add_contact, cursor='hand2', text='Add',
                                         bg='lightgray',
                                         font=('RobotoCondensed-Light', 10, 'bold'), width=10)
        self.add_contact_button.place(x=10, y=300)
        self.update_contact_button = Button(self.entry_frame, cursor='hand2', text='Update', bg='lightgray',
                                            font=('RobotoCondensed-Light', 10, 'bold'), width=10)
        self.update_contact_button.place(x=105, y=300)
        self.delete_contact_button = Button(self.entry_frame, cursor='hand2', text='Delete', bg='lightgray',
                                            font=('RobotoCondensed-Light', 10, 'bold'), width=10)
        self.delete_contact_button.place(x=200, y=300)
        # self.database_data = Button(self.entry_frame, command=self.load_database, cursor='hand2',
        #                                   text='Load Database', bg='lightgray',
        #                                   font=('RobotoCondensed-Light', 8, 'bold'))
        # self.database_data.place(x=10, y=350)

    def get_data(self):
        user_firstname = self.user_firstname.get()
        user_lastname = self.user_lastname.get()
        user_phone_number = self.user_phone_number.get()

        return user_firstname.strip().title(), user_lastname.strip().title(), user_phone_number.strip()

    def clear_entrybox(self):
        self.user_firstname.delete(0, 'end')
        self.user_lastname.delete(0, 'end')
        self.user_phone_number.delete(0, 'end')

    def add_contact(self):
        phone_number_format = r"^(9[0-9]{9})$"
        user_firstname, user_lastname, user_phone_number = self.get_data()
        if user_firstname and user_lastname and user_phone_number != '':
            if re.search(phone_number_format, user_phone_number):
                self.cursor.execute('SELECT * FROM contacts')
                for row in self.cursor.fetchall():
                    first_name, last_name, phone_number = row[0], row[1], row[2]
                    if user_firstname == first_name and user_lastname == last_name and user_phone_number == phone_number:
                        messagebox.showinfo(title='Add Contact', message='Contact Already Added.')
                        break
                else:
                    addcontact = ("INSERT INTO contacts"
                                  "(first_name, last_name, phone_number)"
                                  "VALUES (%s, %s, %s)")
                    datacontact = (user_firstname, user_lastname, user_phone_number)
                    self.cursor.execute(addcontact, datacontact)
                    self.conn.commit()
                    self.db_view.insert("", "end", values=(user_firstname, user_lastname, user_phone_number))
                    messagebox.showinfo(title='Add Contact', message='Contact Added Successfully.')

            else:
                print('Invalid Phone Number')
        else:
            messagebox.showerror(title='Add Contact', message='All fields are Required.', parent=self.root)

        self.clear_entrybox()

    def update_contact(self):
        pass

    def delete_contact(self):
        pass

    def view_database(self):
        pass

    # def load_database(self):
    #
    #     if len(self.current_data) == 0:
    #         for row in self.cursor.fetchall():
    #             self.db_view.insert("", "end", values=(row[0], row[1], row[2]))
    #             self.current_data.append((row[0], row[1], row[2]))
    #     else:
    #         messagebox.showinfo(title='Load Database', message='All data from Database has been loaded.')



def main():
    database = 'phonebook'
    config = {
        'host': 'localhost',
        'port': '3306',
        'user': 'root',
        'password': 'Sarmiento1020',
        'database': database
    }

    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            db = conn.get_server_info()
            # messagebox.showinfo(title='Database Connection', message=f'Connected to MySQL Server {db}')
            cursor = conn.cursor()
            root = Tk()
            window = Window(root, database, conn, cursor)
            root.mainloop()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror(title='Connection Access Denied',
                                 message='Something is wrong with your user name or password.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            messagebox.showerror(title='Database Error', message='Database does not exist.')
        else:
            print(err)
    else:
        conn.close()


if __name__ == '__main__':
    main()

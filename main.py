import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import *
from tkinter import ttk
from PIL import Image
import pyodbc
import re

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

appWidth, appHeight = 600, 300


class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, conn, data_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.data_frame = data_frame

        # Define StringVars
        self.user_firstname = StringVar()
        self.user_lastname = StringVar()
        self.user_phonenumber = StringVar()

        # Frame Title
        self.entryframe_title = ctk.CTkLabel(self, text='INFORMATION', font=('helvetica', 25, 'bold'),
                                             text_color='white')
        self.entryframe_title.grid(row=0, column=0, padx=10, pady=(15, 0), columnspan=2, sticky='nsew')

        # Frame Icon
        self.man_icon = ctk.CTkImage(Image.open('assets/dark_man.png'), size=(64, 64))
        self.man_icon_label = ctk.CTkLabel(self, image=self.man_icon, text='', anchor='center')
        self.man_icon_label.grid(row=1, column=0, padx=8, pady=(10, 0), columnspan=2, sticky='ew')

        # Frame Labels
        self.firstname_label = ctk.CTkLabel(self, text='First Name', font=('helvetica', 15), text_color='white',
                                            anchor='center')
        self.firstname_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.lastname_label = ctk.CTkLabel(self, text='Last Name', font=('helvetica', 15), text_color='white',
                                           anchor='center')
        self.lastname_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.phone_number_label = ctk.CTkLabel(self, text='Phone Number', font=('helvetica', 15), text_color='white',
                                               anchor='w')
        self.phone_number_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky='ew')

        # Frame Entries
        self.firstname_entry = ctk.CTkEntry(self, placeholder_text='Enter First Name', textvariable=self.user_firstname)
        self.firstname_entry.grid(row=2, column=1, padx=10, pady=(10, 0), sticky='ew')

        self.lastname_entry = ctk.CTkEntry(self, placeholder_text='Enter Last Name', textvariable=self.user_lastname)
        self.lastname_entry.grid(row=3, column=1, padx=10, pady=(10, 0), sticky='ew')

        self.phonenumber_entry = ctk.CTkEntry(self, placeholder_text='Enter Phone Number', textvariable=self.user_phonenumber)
        self.phonenumber_entry.grid(row=4, column=1, padx=10, pady=(10, 0), sticky='ew')

        # Frame Buttons
        self.info_button = ctk.CTkButton(self, text='i', font=('times new roman', 15, 'bold'), width=2,
                                         corner_radius=15, fg_color='transparent', border_color='#AEC3AE',
                                         border_width=1, anchor='e')
        self.info_button.grid(row=0, column=1, padx=5, pady=5, sticky='ne')

        self.add_button = ctk.CTkButton(self, text='Add', cursor='hand2', command=self.add_contact, width=80)
        self.add_button.grid(row=5, column=0, padx=10, pady=(15, 10), sticky='w')
        self.add_button.bind('<Return>', self.add_contact)

        self.update_button = ctk.CTkButton(self, text='Update', cursor='hand2', width=80)
        self.update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(15, 10))

        self.delete_button = ctk.CTkButton(self, text='Delete', cursor='hand2', command=self.delete_contact, width=80)
        self.delete_button.grid(row=5, column=1, padx=10, pady=(15, 10), sticky='e')

    def get_entry_data(self):
        return self.user_firstname.get().strip().title(), self.user_lastname.get().strip().title(), self.user_phonenumber.get().strip().title()

    def clear_entrybox(self):
        self.firstname_entry.delete(0, 'end')
        self.lastname_entry.delete(0, 'end')
        self.phonenumber_entry.delete(0, 'end')

    def add_contact(self, event=None):
        phone_number_format = r"^(0?9[0-9]{9})$"
        user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
        if user_firstname and user_lastname and user_phonenumber != '':
            if re.search(phone_number_format, user_phonenumber):
                self.cursor.execute('SELECT * FROM contacts')
                for row in self.cursor.fetchall():
                    first_name, last_name, phone_number = row[0], row[1], row[2]
                    if user_firstname == first_name and user_lastname == last_name and user_phonenumber == phone_number:
                        CTkMessagebox(title='Contact Record', message='Contact already in Record.')
                else:
                    query = ("INSERT INTO contacts"
                             "(FirstName, LastName, PhoneNumber)"
                             "VALUES (?, ?, ?)")
                    datacontact = (user_firstname, user_lastname, user_phonenumber)
                    self.cursor.execute(query, datacontact)
                    self.data_frame.clear()
                    self.conn.commit()
                    CTkMessagebox(title='Add Contact', message='Contact Added Successfully.', icon='check',
                                  option_1='Thanks')
                self.clear_entrybox()
            else:
                CTkMessagebox(title='Error', message='Wrong Phone number format.', icon='cancel', sound=True)
                self.phonenumber_entry.delete(0, 'end')
        else:
            CTkMessagebox(title='Warning', message='All fields are Required.', icon='warning', sound=True)

    def update_contact(self):
        user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
        pass

    def delete_contact(self):
        user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
        response = CTkMessagebox(title='Confirm Delete', message='Are you sure to delete this contact?', icon='question',
                      option_1="No", option_2="Yes")
        if response.get() == 'Yes':
            query = 'DELETE FROM contacts WHERE FirstName = ? AND LastName = ? AND PhoneNumber = ?'
            datacontact = (user_firstname, user_lastname, user_phonenumber)
            self.cursor.execute(query, datacontact)
            self.data_frame.clear()
            self.conn.commit()
        else:
            pass



class DataFrame(ctk.CTkFrame):
    def __init__(self, master, conn, entry_frame, **kwargs):
        super().__init__(master, **kwargs)
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.entry_frame = entry_frame

        # # Define StringVar
        self.to_search = StringVar()
        self.to_search.trace('w', self.search)

        # Frame Title
        self.dataframe_title = ctk.CTkLabel(self, text='RECORD', font=('helvetica', 25, 'bold'), text_color='white')
        self.dataframe_title.grid(row=0, column=0, padx=10, pady=(15, 0), columnspan=3, sticky='ew')

        # Label
        self.search_label = ctk.CTkLabel(self, text='Search:', font=('helvetica', 15), text_color='white')
        self.search_label.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky='w')

        # Frame Entries
        self.to_search_entry = ctk.CTkEntry(self, placeholder_text='Search', textvariable=self.to_search, width=190)
        self.to_search_entry.grid(row=1, column=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky='e')

        # Button
        self.clear_button = ctk.CTkButton(self, text='Clear', cursor='hand2', command=self.clear)
        self.clear_button.grid(row=1, column=2, padx=10, pady=(10, 0), sticky='ew')

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview.Heading", font=('helvetica', 15, 'bold'))
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 15))
        self.db_view = ttk.Treeview(self, columns=("firstname", "lastname", "phonenumber"), show='headings',
                                    style='mystyle.Treeview')

        # Create Headings
        self.db_view.heading("firstname", text="First Name", anchor='w')
        self.db_view.heading("lastname", text="Last Name", anchor='w')
        self.db_view.heading("phonenumber", text="Phone Number", anchor='w')
        self.db_view.grid(row=2, column=0, padx=15, pady=15, columnspan=3, sticky='nsew')

        self.db_view.bind('<Double 1>', self.getrow)

        self.cursor.execute('SELECT * FROM contacts')
        self.rows = self.cursor.fetchall()
        self.update_dataframe(self.rows)

    def getrow(self, event):
        item = self.db_view.item(self.db_view.focus())
        self.entry_frame.user_firstname.set(item['values'][0])
        self.entry_frame.user_lastname.set(item['values'][1])
        self.entry_frame.user_phonenumber.set(item['values'][2])

    def update_dataframe(self, rows):
        self.db_view.delete(*self.db_view.get_children())
        for item in sorted(rows):
            firstname, lastname, phonenumber = item[0], item[1], item[2]
            self.db_view.insert('', 'end', values=(firstname, lastname, phonenumber))

    def search(self, *args):
        to_search = self.to_search.get()
        if to_search != '':
            query = "SELECT FirstName, LastName, PhoneNumber FROM contacts WHERE FirstName Like '%" + to_search + "%' OR LastName LIKE '%" + to_search + "%' OR PhoneNumber LIKE '%" + to_search + "%'"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            self.update_dataframe(rows)
        else:
            self.clear()

    def clear(self):
        self.to_search_entry.delete(0, 'end')
        query = 'SELECT FirstName, LastName, PhoneNumber FROM contacts'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.update_dataframe(rows)

    # def insert_data(self, firstname, lastname, phonenumber):
    #     record = (firstname, lastname, phonenumber)
    #     if record in self.data:
    #         print('Already in Record.')
    #     else:
    #         self.db_view.insert(parent='', index=0, values=record)
    #         # self.data.append(record)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\Users\acer\PycharmProjects\Phonebook\phonebook.accdb'
        )
        self.conn = pyodbc.connect(config)

        # self.cursor = database.cursor()
        # Check Database connection
        # for table_info in self.cursor.tables(tableType='TABLE'):
        #     print(table_info.table_name)

        # Create Window
        self.title('Phonebook')
        self.iconbitmap('assets/telephone-directory.ico')
        # self.geometry(f"{appWidth}x{appHeight}")
        self.minsize(appWidth, appHeight)
        self.resizable(False, False)
        self.configure(fg_color='#040D12')
        self.columnconfigure(0, weight=1)

        self.entry_frame = EntryFrame(master=self, conn=self.conn, data_frame=None, fg_color='#183D3D',
                                      border_color='#AEC3AE', border_width=2,
                                      width=300, height=300)

        self.entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.entry_frame.columnconfigure(0, weight=1)

        self.data_frame = DataFrame(master=self, conn=self.conn, entry_frame=self.entry_frame, fg_color='#5C8374',
                                    border_color='white',
                                    border_width=2, width=300, height=300)
        self.data_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='nsew')
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.rowconfigure(2, weight=1)

        self.entry_frame.data_frame = self.data_frame


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()

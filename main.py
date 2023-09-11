import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import *
from tkinter import ttk
from PIL import Image
import pyodbc
import re
import os

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

appWidth, appHeight = 900, 500


class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, conn, data_frame, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize class instance variables
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.data_frame = data_frame

        # Define StringVars
        self.user_firstname = StringVar()
        self.user_lastname = StringVar()
        self.user_phonenumber = StringVar()

        # Configure Frame Columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Configure Frame Rows
        self.rowconfigure(6, weight=1)

        # Frame Title
        self.entryframe_title = ctk.CTkLabel(self, text='INFORMATION', font=('helvetica', 25, 'bold'),
                                             text_color='white')
        self.entryframe_title.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')

        # Frame Icon
        self.man_icon = ctk.CTkImage(Image.open('assets/dark_man.png'), size=(64, 64))
        self.man_icon_label = ctk.CTkLabel(self, image=self.man_icon, text='', anchor='center')
        self.man_icon_label.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')

        # Frame Labels
        self.firstname_label = ctk.CTkLabel(self, text='First Name', font=('helvetica', 15), text_color='white')
        self.firstname_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.lastname_label = ctk.CTkLabel(self, text='Last Name', font=('helvetica', 15), text_color='white')
        self.lastname_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.phone_number_label = ctk.CTkLabel(self, text='Phone Number', font=('helvetica', 15), text_color='white', )
        self.phone_number_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky='ew')

        # Frame Entries
        self.firstname_entry = ctk.CTkEntry(self, placeholder_text='Enter First Name', textvariable=self.user_firstname,
                                            validatecommand=self.firstname_has_input)
        self.firstname_entry.grid(row=2, column=1, padx=(10, 25), pady=(10, 0), columnspan=2, sticky='ew')
        self.firstname_entry.bind('<KeyRelease>', self.firstname_has_input)

        self.lastname_entry = ctk.CTkEntry(self, placeholder_text='Enter Last Name', textvariable=self.user_lastname,
                                           validatecommand=self.lastname_has_input)
        self.lastname_entry.grid(row=3, column=1, padx=(10, 25), pady=(10, 0), columnspan=2, sticky='ew')
        self.lastname_entry.bind('<KeyRelease>', self.lastname_has_input)

        self.phonenumber_entry = ctk.CTkEntry(self, placeholder_text='Enter Phone Number',
                                              textvariable=self.user_phonenumber,  validatecommand=self.phonenumber_has_input,)
        self.phonenumber_entry.grid(row=4, column=1, padx=(10, 25), pady=(10, 0), columnspan=2, sticky='ew')
        self.phonenumber_entry.bind('<KeyRelease>', self.phonenumber_has_input)

        # Entry Labels
        self.firstname_entry_required = ctk.CTkLabel(self, text='*', text_color='#C63D2F', fg_color='transparent')
        self.firstname_entry_required.grid(row=2, column=2, padx=15, pady=(10, 0), sticky='e')

        self.lastname_entry_required = ctk.CTkLabel(self, text='*', text_color='#C63D2F')
        self.lastname_entry_required.grid(row=3, column=2, padx=15, pady=(10, 0), sticky='e')

        self.phonenumber_entry_required = ctk.CTkLabel(self, text='*', text_color='#C63D2F')
        self.phonenumber_entry_required.grid(row=4, column=2, padx=15, pady=(10, 0), sticky='e')

        # Frame Buttons
        self.add_contact_icon = ctk.CTkImage(Image.open('assets/add_contact.png'), size=(32, 32))
        self.add_button = ctk.CTkButton(self, image=self.add_contact_icon, compound='right', text='Add', cursor='hand2',
                                        command=self.add_contact, anchor='center')
        self.add_button.grid(row=5, column=0, padx=(10, 0), pady=(10, 0), sticky='ew')

        self.update_contact_icon = ctk.CTkImage(Image.open('assets/update.png'), size=(32, 32))
        self.update_button = ctk.CTkButton(self, image=self.update_contact_icon, compound='right', text='Update',
                                           cursor='hand2', command=self.update_contact, anchor='center')
        self.update_button.grid(row=5, column=1, padx=10, pady=(10, 0), sticky='ew')

        self.delete_contact_icon = ctk.CTkImage(Image.open('assets/delete_contact.png'), size=(32, 32))
        self.delete_button = ctk.CTkButton(self, image=self.delete_contact_icon, compound='right', text='Delete',
                                           cursor='hand2', command=self.delete_contact, anchor='center')
        self.delete_button.grid(row=5, column=2, padx=(0, 10), pady=(10, 0), sticky='ew')

        self.clear_statusbox_button = ctk.CTkButton(self, text='Clear', cursor='hand2', command=self.clear_statusbox)
        self.clear_statusbox_button.grid(row=7, column=2, padx=10, pady=10, sticky='ew')

        # Status Text Box
        self.statusbox = ctk.CTkTextbox(self, corner_radius=10, fg_color='#040D12', font=('consolas', 12), text_color='white')
        self.statusbox.grid(row=6, column=0, padx=10, pady=(10, 0), columnspan=3, sticky='nsew')

        # Frame Mark
        self.framemark_label = ctk.CTkLabel(self, text='C.Sarmiento 2023 Version 1.1', font=('helvetica', 10))
        self.framemark_label.grid(row=7, column=0, padx=10, pady=(0, 2), sticky='sw')

    def firstname_has_input(self, event):
        if len(self.get_entry_data()[0]) != 0:
            self.firstname_entry_required.configure(text_color='#A6FF96')
            return True
        else:
            self.firstname_entry_required.configure(text_color='#C63D2F')
            return False

    def lastname_has_input(self, event):
        if len(self.get_entry_data()[1]) != 0:
            self.lastname_entry_required.configure(text_color='#A6FF96')
            return True
        else:
            self.lastname_entry_required.configure(text_color='#C63D2F')
            return False

    def phonenumber_has_input(self, event):
        if len(self.get_entry_data()[2]) != 0:
            self.phonenumber_entry_required.configure(text_color='#A6FF96')
            return True
        else:
            self.phonenumber_entry_required.configure(text_color='#C63D2F')
            return False

    def add_status(self, text):
        status = f"$ {text}\n"
        self.statusbox.configure(state='normal')
        self.statusbox.insert("end", status)
        self.statusbox.configure(state='disable')

    def clear_statusbox(self):
        self.statusbox.configure(state='normal')
        self.statusbox.delete('0.0', 'end')
        self.statusbox.configure(state='disable')

    def get_entry_data(self):
        return self.user_firstname.get().strip().title(), self.user_lastname.get().strip().title(), self.user_phonenumber.get().lstrip(
            '0')

    def clear_entrybox(self):
        self.firstname_entry.delete(0, 'end')
        self.firstname_entry_required.configure(text_color='#C63D2F')
        self.lastname_entry.delete(0, 'end')
        self.lastname_entry_required.configure(text_color='#C63D2F')
        self.phonenumber_entry.delete(0, 'end')
        self.phonenumber_entry_required.configure(text_color='#C63D2F')

    def add_contact(self):
        phone_number_format = r"^(0?9[0-9]{9})$"
        if self.firstname_has_input(None) and self.lastname_has_input(None) and self.phonenumber_has_input(None):
            user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
            if re.search(phone_number_format, user_phonenumber):
                # Check if the data already exists in the database
                query = 'SELECT * FROM contacts WHERE PhoneNumber = ?'
                self.cursor.execute(query, user_phonenumber)
                existing_contact = self.cursor.fetchone()

                if existing_contact is None:
                    # Data doesn't exist, so add it to the database
                    query = "INSERT INTO contacts (FirstName, LastName, PhoneNumber) VALUES (?, ?, ?)"
                    datacontact = (user_firstname, user_lastname, user_phonenumber)
                    self.cursor.execute(query, datacontact)
                    self.data_frame.clear()
                    self.conn.commit()
                    self.add_status(f'New Contact Added Successfully.')
                else:
                    CTkMessagebox(title='Contact Record', message='Phone number already in Record.')
                self.clear_entrybox()
            else:
                CTkMessagebox(title='Error', message='Wrong Phone number format.', icon='cancel', sound=True)
                self.phonenumber_entry.delete(0, 'end')
                self.phonenumber_entry_required.configure(text_color='#C63D2F')
        else:
            CTkMessagebox(title='Warning', message='All fields are Required.', icon='warning', sound=True)

    def update_contact(self):
        if self.firstname_has_input(None) and self.lastname_has_input(None) and self.phonenumber_has_input(None):
            user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
            response = CTkMessagebox(title='Confirm Update', message='Are you sure to update this contact?',
                                     icon='question', option_1="No", option_2="Yes")
            if response.get() == 'Yes':
                query = 'UPDATE contacts SET FirstName = ?, LastName = ? WHERE PhoneNumber = ?'
                datacontact = (user_firstname, user_lastname, user_phonenumber)
                self.cursor.execute(query, datacontact)
                self.conn.commit()
                self.data_frame.clear()
                self.clear_entrybox()
                self.add_status('Contact Updated Successfully.')
            else:
                pass
        else:
            CTkMessagebox(title='Warning', message='No Contact selected to update.', icon='warning', sound=True)

    def delete_contact(self):
        if self.firstname_has_input(None) and self.lastname_has_input(None) and self.phonenumber_has_input(None):
            user_firstname, user_lastname, user_phonenumber = self.get_entry_data()
            response = CTkMessagebox(title='Confirm Delete', message='Are you sure to delete this contact?',
                                     icon='question',
                                     option_1="No", option_2="Yes")
            if response.get() == 'Yes':
                query = 'DELETE FROM contacts WHERE FirstName = ? AND LastName = ? AND PhoneNumber = ?'
                datacontact = (user_firstname, user_lastname, user_phonenumber)
                self.cursor.execute(query, datacontact)
                self.conn.commit()
                self.data_frame.clear()
                self.clear_entrybox()
                self.add_status('Contact Deleted Successfully.')
            else:
                pass
        else:
            CTkMessagebox(title='Warning', message='No Contact selected to delete.', icon='warning', sound=True)


class DataFrame(ctk.CTkFrame):
    def __init__(self, master, conn, entry_frame, **kwargs):
        super().__init__(master, **kwargs)
        # Initialize class instance variables
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.entry_frame = entry_frame

        # Define StringVar
        self.to_search = StringVar()
        self.to_search.trace('w', self.search)

        self.data_count = IntVar()

        # Configure Frame Columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Configure Frame Rows
        self.rowconfigure(2, weight=1)

        # Frame Title
        self.dataframe_title = ctk.CTkLabel(self, text='RECORD', font=('helvetica', 25, 'bold'), text_color='white')
        self.dataframe_title.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky='nsew')

        # Label
        self.search_label = ctk.CTkLabel(self, text='Search:', font=('helvetica', 15), text_color='white')
        self.search_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        # Frame Entries
        self.to_search_entry = ctk.CTkEntry(self, placeholder_text='Search', textvariable=self.to_search)
        self.to_search_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Button
        self.clear_button = ctk.CTkButton(self, text='Clear', cursor='hand2', command=self.clear)
        self.clear_button.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

        # Show number of Data
        self.show_datacount = ctk.CTkLabel(self, text_color='white')
        self.show_datacount.grid(row=3, column=0, padx=10, pady=(0, 5), columnspan=2, sticky='w')

        # Treeview Customisation (based on CTk Theme)
        # self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme['CTkFrame']['fg_color'])
        # self.text_color = self._apply_appearance_mode(ctk.ThemeManager.theme['CTkLabel']['text_color'])
        # self.selected_color = self._apply_appearance_mode(ctk.ThemeManager.theme['CTkButton']['fg_color'])

        # Configure Treeview Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview.Heading", font=('Verdana', 15, 'bold'))
        self.style.configure("Treeview", rowheight=30, font=('Verdana', 15), borderwidth=5)
        # self.style.configure("Treeview", rowheight=30, font=('Calibri', 15), background=self.bg_color,
        #                      foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=5)
        self.style.map('Treeview', background=[('selected', '#183D3D')], foreground=[('selected', 'white')])

        # Create Treeview
        self.db_view = ttk.Treeview(self, columns=("firstname", "lastname", "phonenumber"), show='headings')

        # Place Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self, orientation='vertical', command=self.db_view.yview)
        self.scrollbar.grid(row=2, column=3, padx=(0, 5), pady=(30, 0), sticky='ns')

        self.db_view.configure(yscrollcommand=self.scrollbar.set)

        # Create Headings
        self.db_view.heading("firstname", text="First Name", anchor='w')
        self.db_view.heading("lastname", text="Last Name", anchor='w')
        self.db_view.heading("phonenumber", text="Phone Number", anchor='w')
        self.db_view.grid(row=2, column=0, padx=(15, 0), pady=(15, 0), columnspan=3, sticky='nsew')

        # Bind Double Left Click
        self.db_view.bind('<Double 1>', self.getrow)

        # Fetch all data from contacts and display on DataFrame
        self.cursor.execute('SELECT * FROM contacts')
        self.rows = self.cursor.fetchall()
        self.update_dataframe(self.rows)

    def getrow(self, event):
        item = self.db_view.item(self.db_view.focus())
        self.entry_frame.user_firstname.set(item['values'][0])
        self.entry_frame.user_lastname.set(item['values'][1])
        self.entry_frame.user_phonenumber.set(item['values'][2])

    def update_dataframe(self, rows):
        counter = 0
        self.db_view.delete(*self.db_view.get_children())
        for item in sorted(rows):
            firstname, lastname, phonenumber = item[0], item[1], item[2]
            self.db_view.insert('', 'end', values=(firstname, lastname, phonenumber))
            counter += 1
        self.show_datacount.configure(text=f'Showing {counter} of contact record.')

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


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get Access Database Directory
        current_directory = os.getcwd()
        db_file_path = f'{current_directory}\\Phonebook.accdb'

        # Set Connection Configurations
        self.config = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            f'DBQ={db_file_path}'
        )

        # Create connection
        self.conn = pyodbc.connect(self.config)

        # Create a cursor to execute SQL commands
        self.cursor = self.conn.cursor()

        table_exists = False

        # Create a Window
        self.title('Phonebook')
        self.iconbitmap('assets/telephone-directory.ico')
        self.minsize(appWidth, appHeight)
        self.configure(fg_color='#040D12')

        # Configure Window Column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Configure Window Row
        self.rowconfigure(0, weight=1)

        # Initialize EntryFrame
        self.entry_frame = EntryFrame(master=self, conn=self.conn, data_frame=None, fg_color='#183D3D',
                                      border_color='#AEC3AE', border_width=2,
                                      width=300, height=300)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Initialize DataFrame
        self.data_frame = DataFrame(master=self, conn=self.conn, entry_frame=self.entry_frame, fg_color='#5C8374',
                                    border_color='white', border_width=2,
                                    width=300, height=300)
        self.data_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='nsew')

        self.entry_frame.data_frame = self.data_frame

        try:
            # Attempt to fetch data from the 'Contacts' table
            self.cursor.execute("SELECT TOP 1 * FROM Contacts")
            self.cursor.fetchone()
            table_exists = True
        except pyodbc.Error as e:
            # Handle the exception (e.g., print a message)
            self.entry_frame.add_status(f"Table 'Contacts' does not exist or cannot be accessed: {e}")

        if not table_exists:
            # Create the 'Contacts' table if it doesn't exist
            create_table_sql = """
            CREATE TABLE Contacts (
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                PhoneNumber TEXT NOT NULL
            )
            """
            self.cursor.execute(create_table_sql)
            self.conn.commit()
            self.entry_frame.add_status("Table 'Contacts' created.")
        else:
            self.entry_frame.add_status("Table 'Contacts' accessed.")


if __name__ == '__main__':
    app = App()
    app.mainloop()
    app.cursor.close()
    app.conn.close()

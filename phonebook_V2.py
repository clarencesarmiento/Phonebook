import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import *
from tkinter import ttk
from PIL import Image
import sqlite3
import re
import os

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('dark-blue')

appWidth, appHeight = 850, 450

# Define database path
current_directory = os.getcwd()
db_file_path = f'{current_directory}\\phonebook.db'
# Connect to Database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS record (name TEXT NOT NULL, phonenumber TEXT NOT NULL, email TEXT, tag TEXT)")


# Create Window
class Window(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry(f'{appWidth}x{appHeight}')
        self.minsize(appWidth, appHeight)
        self.title('Phonebook Version 2.0')
        self.iconbitmap('assets/telephone-directory.ico')

        # Configure Window Column
        self.columnconfigure(0, weight=1)

        # Configure Window Row
        self.rowconfigure(0, weight=1)

        # Create Window Frame Object
        self.window_frame = WindowFrame(self)
        self.window_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.mainloop()


# Create a Window Frame
class WindowFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.optionmenu_var = StringVar(value='All')
        self.to_search = StringVar()
        self.to_search.trace('w', self.search)
        self.toplevel_window = None
        self.data = []

        # Configure Window Frame Column
        self.columnconfigure(0, weight=1)

        # Configure Window Frame Row
        self.rowconfigure(1, weight=1)

        # Add Window Label
        self.window_label = ctk.CTkLabel(self, text='Phonebook', text_color='#068FFF', font=('helvetica', 30, 'bold'))
        self.window_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Create Search Entry Widget
        self.search_entry = ctk.CTkEntry(self, textvariable=self.to_search, width=300)
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        # Create OptionMenu for Tag
        self.tag_optionmenu = ctk.CTkOptionMenu(self,
                                                values=['All', 'Family', 'Friend', 'Classmate', 'Workmate', 'No Tag'],
                                                variable=self.optionmenu_var, command=self.show_tag)
        self.tag_optionmenu.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # Create Clear Button
        self.clear_button = ctk.CTkButton(self, text='Clear', cursor='hand2', corner_radius=50, command=self.clear)
        self.clear_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

        # Configure TreeView Style
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure("Treeview.Heading", font=('Verdana', 18, 'bold'), foreground='#F5F5F5',
                             background='#27374D')
        self.style.configure("Treeview", rowheight=45, font=('Verdana', 14), foreground='#272829', borderwidth=5)

        # Create Treeview Table
        self.db_view = ttk.Treeview(self, columns=('name', 'phonenumber', 'email'), show='headings')

        # Create Headings
        self.db_view.heading("name", text="Name", anchor='w')
        self.db_view.heading("phonenumber", text="Phone Number", anchor='w')
        self.db_view.heading("email", text="Email", anchor='w')

        self.db_view.grid(row=1, column=0, columnspan=3, padx=10, sticky='nsew')

        # Create Contact Count
        self.contact_count = ctk.CTkLabel(self, text='')
        self.contact_count.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Create Add Button
        self.add_button = ctk.CTkButton(self, text='Add', cursor='hand2', corner_radius=50, command=self.open_toplevel)
        self.add_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

        # Create Delete Button
        self.delete_button = ctk.CTkButton(self, text='Delete', cursor='hand2', corner_radius=50, fg_color='#D80032',
                                           hover_color='#A73121', command=self.delete)
        self.delete_button.grid(row=2, column=2, padx=10, pady=10, sticky='w')

        # Bind Double Left Click to the Treeview
        self.db_view.bind('<Double 1>', self.insert_data)

        # Fetch all the data
        cursor.execute('SELECT * FROM record ORDER BY name ASC')
        self.rows = cursor.fetchall()
        self.update_treeview(self.rows)

    # Create Add Button Callback
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = TopLevelWindow(self, WindowFrame(self))
            self.toplevel_window.attributes('-topmost', 'true')
        else:
            self.toplevel_window.focus()

    # Create Delete Button Callback
    def delete(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            if self.get_row():
                name, phonenumber, email, tag = self.get_row()
                response = CTkMessagebox(title='Confirm Delete', message='Are you sure to delete this contact?',
                                         icon='question', option_1='No', option_2='Yes')
                if response.get() == 'Yes':
                    query = 'DELETE FROM record WHERE name = ? AND phonenumber = ? AND (email = ? or email IS NULL) AND tag = ?'
                    data = (name, phonenumber, email, tag)
                    cursor.execute(query, data)
                    conn.commit()
                    self.clear()
                else:
                    return
            else:
                CTkMessagebox(title='Delete Contact', message='No contact selected to delete.', icon='warning', sound=True)
        else:
            return

    # Create Clear Button Callback
    def clear(self):
        self.search_entry.delete(0, 'end')
        tag = self.optionmenu_var.get()
        if tag == 'All':
            cursor.execute('SELECT * FROM record ORDER BY name ASC')
        else:
            cursor.execute('SELECT * FROM record WHERE tag = ? ORDER BY name ASC ', (tag,))
        rows = cursor.fetchall()
        self.update_treeview(rows)

    # Create Function to show all data based on tags
    def show_tag(self, choice):
        if choice == 'All':
            cursor.execute('SELECT * FROM record ORDER BY name ASC')
        else:
            cursor.execute('SELECT * FROM record WHERE tag = ? ORDER BY name ASC', (choice,))

        rows = cursor.fetchall()
        self.update_treeview(rows)

    # Create Search Bar Function
    def search(self, *args):
        to_search = self.to_search.get()
        tag = self.optionmenu_var.get()
        if len(to_search) != 0:
            if tag == 'All':
                cursor.execute("SELECT * FROM record WHERE name Like '%" + to_search + "%' ORDER BY name ASC")
            else:
                cursor.execute(
                    "SELECT * FROM record WHERE tag = ? AND name Like '%" + to_search + "%' ORDER BY name ASC", (tag,))
            rows = cursor.fetchall()
            self.update_treeview(rows)
        else:
            self.clear()

    # Create function to update treeview table
    def update_treeview(self, rows):
        counter = 0
        self.db_view.delete(*self.db_view.get_children())
        for item in rows:
            name, phonenumber, email, tag = item[0], item[1], item[2], item[3]
            self.db_view.insert('', 'end', values=(name, phonenumber, email), tags=str(tag))
            self.db_view.tag_configure('No Tag', background='#ffffff')
            self.db_view.tag_configure('Family', background='#B0D9B1')
            self.db_view.tag_configure('Friend', background='#FAF2D3')
            self.db_view.tag_configure('Classmate', background='#F5FCCD')
            self.db_view.tag_configure('Workmate', background='#8DDFCB')
            counter += 1

        if counter > 1:
            self.contact_count.configure(text=f'You have {counter} contacts in the phonebook')
        else:
            self.contact_count.configure(text=f'You have {counter} contact in the phonebook')

    # Create Function to get all the row data
    def get_row(self):
        item = self.db_view.item(self.db_view.focus())
        if len(item['values']) != 0:
            return item['values'][0], str(item['values'][1]), item['values'][2], ' '.join(item['tags'])
        else:
            return

    # Create Function to insert data got from get_row Function to the entry widgets of TopLevelWindow
    # when double-clicked
    def insert_data(self, event):
        self.data.clear()
        region_clicked = self.db_view.identify_region(event.x, event.y)
        if region_clicked == 'cell':
            row_id = self.db_view.identify_row(event.y)
            self.db_view.selection_set(row_id)
            item = self.db_view.item(row_id)
            name, phonenumber, email, tag = item['values'][0], str(item['values'][1]), item['values'][2], ' '.join(
                item['tags'])
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = TopLevelWindow(self, WindowFrame(self))
                self.toplevel_window.attributes('-topmost', 'true')
                self.toplevel_window.title('Edit')
                self.toplevel_window.top_level_label.configure(text='Edit Contact')
                self.toplevel_window.name_entry.insert(0, name)
                self.toplevel_window.phonenumber_entry.insert(0, phonenumber)
                self.toplevel_window.email_entry.insert(0, email)
                self.toplevel_window.optionmenu_var.set(tag)
                self.toplevel_window.save_button.configure(command=self.save_edit)
                self.data.append([name, phonenumber, email, tag])
            else:
                self.toplevel_window.destroy()
                self.insert_data(event)
        else:
            return

    def save_edit(self):
        row_name, row_phonenumber, row_email, row_tag = self.data[0]
        if self.toplevel_window.name_has_input() and self.toplevel_window.phone_has_input_and_valid():
            new_name, new_phonenumber, new_email, new_tag = self.toplevel_window.get_data()

            # Data in entry widgets has changed, update it in the database
            if (row_name != new_name) or (row_phonenumber != new_phonenumber) or (row_email != new_email) or (
                    row_tag != new_tag):
                # The phonenumber has changed
                if row_phonenumber != new_phonenumber:
                    # check if the new number exists in the database
                    cursor.execute('SELECT COUNT(*) FROM record WHERE phonenumber = ?', (new_phonenumber,))
                    count = cursor.fetchone()[0]

                    # if the number do exist, no updates will be done
                    if count > 0:
                        CTkMessagebox(title='Edit Contact', message='Number already exist. Update not allowed.',
                                      icon='cancel', sound=True)
                        return

                response = CTkMessagebox(title='Confirm Edit', message='Are you sure to update this contact?',
                                         icon='question', option_1="No", option_2="Yes", sound=True)
                if response.get() == 'Yes':
                    query = ("UPDATE record SET name = ?, phonenumber = ?, email = ?, tag = ? "
                             "WHERE name = ? AND phonenumber = ? AND (email = ? or email IS NULL) AND tag = ?")
                    data = (
                        new_name, new_phonenumber, new_email, new_tag, row_name, row_phonenumber, row_email,
                        row_tag)
                    cursor.execute(query, data)
                    conn.commit()
                    self.clear()
                    self.toplevel_window.destroy()
            else:
                self.toplevel_window.destroy()


# Create Top Level Window
class TopLevelWindow(ctk.CTkToplevel):
    def __init__(self, window_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optionmenu_var = StringVar(value='No Tag')
        self.window_frame = window_frame

        # self.geometry('300x285')
        self.resizable(False, False)
        self.title('Add')
        self.iconbitmap('assets/telephone-directory.ico')

        # Configure Top Level Window Column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Define Top Level Window Icons
        self.name_icon = ctk.CTkImage(Image.open('assets/profile.png'), size=(24, 24))
        self.phone_icon = ctk.CTkImage(Image.open('assets/phone.png'), size=(24, 24))
        self.email_icon = ctk.CTkImage(Image.open('assets/email.png'), size=(24, 24))

        # Create Top Level Window Labels
        self.top_level_label = ctk.CTkLabel(self, text='New Contact', text_color='#068FFF',
                                            font=('helvetica', 18, 'bold'))
        self.top_level_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky='ew')

        self.name_label = ctk.CTkLabel(self, image=self.name_icon, text=' Name', text_color='#272829',
                                       font=('roboto', 15, 'bold'), compound='left')
        self.name_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky='w')

        self.error_name_label = ctk.CTkLabel(self, text='', text_color='#FE0000', font=('roboto', 10))
        self.error_name_label.grid(row=1, column=1, padx=10, pady=(10, 0), sticky='e')

        self.phonenumber_label = ctk.CTkLabel(self, image=self.phone_icon, text=' Phone Number', text_color='#272829',
                                              font=('roboto', 15, 'bold'), compound='left')
        self.phonenumber_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky='w')

        self.error_phonenumber_label = ctk.CTkLabel(self, text='', text_color='#FE0000', font=('roboto', 10))
        self.error_phonenumber_label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky='e')

        self.email_label = ctk.CTkLabel(self, image=self.email_icon, text=' Email', text_color='#272829',
                                        font=('roboto', 15, 'bold'), compound='left')
        self.email_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky='w')

        self.error_email_label = ctk.CTkLabel(self, text='', text_color='#FE0000', font=('roboto', 10))
        self.error_email_label.grid(row=5, column=1, padx=10, pady=(10, 0), sticky='e')

        # Create Top Level Window Entry
        self.name_entry = ctk.CTkEntry(self, placeholder_text='Ex. Juan Dela Cruz', validatecommand=self.name_has_input,
                                       validate='focus')
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=10, sticky='ew')

        self.phonenumber_entry = ctk.CTkEntry(self, placeholder_text='Ex. 09XXXXXXXXX',
                                              validatecommand=self.phone_has_input_and_valid,
                                              validate='focus')
        self.phonenumber_entry.bind('<KeyRelease>', self.phone_has_input_and_valid)
        self.phonenumber_entry.grid(row=4, column=0, columnspan=2, padx=10, sticky='ew')

        self.email_entry = ctk.CTkEntry(self, placeholder_text='Ex. juandelacruz@email.com',
                                        validatecommand=self.email_has_input,
                                        validate='focus')
        self.email_entry.bind('<KeyRelease>', self.email_is_valid)
        self.email_entry.grid(row=6, column=0, columnspan=2, padx=10, sticky='ew')

        # Create OptionMenu for Tag
        self.top_optionmenu = ctk.CTkOptionMenu(self, values=['No Tag', 'Family', 'Friend', 'Classmate', 'Workmate'],
                                                variable=self.optionmenu_var)
        self.top_optionmenu.grid(row=7, column=0, padx=10, pady=10)

        # Create Save Button
        self.save_button = ctk.CTkButton(self, text='Save', cursor='hand2', corner_radius=50, command=self.save)
        self.save_button.grid(row=7, column=1, padx=10, pady=10)

    # Create Entry Widgets Validations
    def name_has_input(self):
        name = self.name_entry.get()
        if len(name) != 0:
            self.error_name_label.configure(text='')
            return True
        else:
            self.error_name_label.configure(text='Required')
            return False

    def phone_has_input_and_valid(self, event=None):
        phone_number_format = r"^(0?9[0-9]{9})$"
        phonenumber = self.phonenumber_entry.get()
        if len(phonenumber) != 0:
            if re.search(phone_number_format, phonenumber):
                self.error_phonenumber_label.configure(text='')
                return True
            else:
                self.error_phonenumber_label.configure(text='Invalid Number')
                return False
        else:
            self.error_phonenumber_label.configure(text='Required')
            return False

    def email_has_input(self):
        email = self.email_entry.get()
        if len(email) != 0:
            return True
        else:
            self.error_email_label.configure(text='')
            return False

    def email_is_valid(self, event=None):
        email_format = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b$"
        email = self.email_entry.get()
        if self.email_has_input():
            if re.search(email_format, email):
                self.error_email_label.configure(text='')
                return True
            else:
                self.error_email_label.configure(text='Invalid Email')
                return False

    # Function to get all entry data
    def get_data(self):
        return self.name_entry.get().strip().title(), self.phonenumber_entry.get().lstrip(
            '0'), self.email_entry.get().strip(), self.optionmenu_var.get()

    # Create Save Button Callback
    def save(self):
        if self.name_has_input() and self.phone_has_input_and_valid():
            name, phonenumber, tag = self.get_data()[0], self.get_data()[1], self.get_data()[3]
            if self.email_has_input():
                if self.email_is_valid():
                    email = self.get_data()[2]
                    data = (name, phonenumber, email, tag)
                else:
                    return
            else:
                data = (name, phonenumber, None, tag)

            # Check first if the data already exist in the database
            cursor.execute('SELECT * FROM record WHERE phonenumber = ?', (phonenumber,))
            existing_contact = cursor.fetchone()

            if existing_contact is None:
                # Data doesn't exist, add it to the database
                query = 'INSERT INTO record (name, phonenumber, email, tag) VALUES (?, ?, ?, ?)'
                cursor.execute(query, data)
                conn.commit()
                self.window_frame.clear()
                self.destroy()
            else:
                CTkMessagebox(title='Add Contact', message='Phone number already in Table.', sound=True)
        else:
            return


if __name__ == '__main__':
    Window()
    cursor.close()
    conn.close()

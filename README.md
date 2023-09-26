# Phonebook ☎️
![interface](https://github.com/clarencesarmiento/Phonebook/blob/b554be0dfc04a66fe53d2d765fdc6ad545d715f0/Images/V2%20Interface.png)
## DESCRIPTION:
A python program with Graphic User Interface that lets the user to
- Add Contact
- Edit Contact
- Delete Contact
- Search Contact
### How the Program Works?
To create the modern graphic user interface look, the program utilizes a library `customtkinter`[^1]. For the data table, the program utilizes `ttk.treeview`[^2].
For data storage and manipulation, the program utilizes `sqlite3`[^3] that connects the program to the program database which is a SQLite Database.

Add Contact
- Adds the contact details to the database.

Edit Contact
- Edit contact.

Delete Contact
- Deletes contact record.

Search Contact
- Search contact details in database.

## TODO:
### Download
Download the Repository through Clone Repository using [Git](https://git-scm.com/downloads) or Download Zip.
```
git clone https://github.com/clarencesarmiento/Phonebook.git
```
### Installation
After downloading, go to `cmd` and navigate to the folder directory.
```
cd Phonebook
```
Use [pip](https://pip.pypa.io/en/stable/) to install needed libraries inside
the `requirements.txt`.
```
pip install -r requirements.txt
```
### Usage
Run the `phonebook.py` using [python](https://www.python.org/).
```
python phonebook.py
```
## REFERENCES:
[^1]: [Customtkinter](https://github.com/tomschimansky/customtkinter)
[^2]: [ttk.Treeview](http://tkdocs.com/shipman/ttk-Treeview.html)
[^3]: [sqlite3](https://docs.python.org/3/library/sqlite3.html)

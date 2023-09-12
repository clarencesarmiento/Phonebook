# Phonebook ☎️
![image](https://github.com/clarencesarmiento/Phonebook/blob/e046dc137862196b2ff27964bba9d9ef1aea7f74/phonebook_interface.png)
## [.exe](https://www.mediafire.com/file/7mal7egoio7e8t5/Phonebook_V1.1_%2528.exe%2529.rar/file)
## DESCRIPTION:
A python program with Graphic User Interface that lets the user to
- Add Contact
- Update Contact's Name
- Delele Contact
- Search Contact
### How the Program Works?
To create the modern graphic user interface look, the program utilizes a library `customtkinter`[^1]. For the data table, the program utilizes `ttk.treeview`[^2].
For data storage and manipulation, the program utilizes `pyodbc`[^3] that connects the program to the program database which is a Microsoft Access Database.

Add Contact
- Adds the contact details to the database.

Update Contact
- Updates contact.

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
The Program needs a `Microsoft Access Driver (*.mdb, *.accdb)`. To check, run the following command in python.
```
import pyodbc
pyodbc.drivers()
```
If the Driver is not present, you have to download `Microsoft Access Database Engine`. 
Download the appropriate version (32-bit or 64-bit) from the Microsoft Website and install it.
### Usage
Run the `main.py` using [python](https://www.python.org/).
```
python main.py
```
## REFERENCES:
[^1]: [Customtkinter](https://github.com/tomschimansky/customtkinter)
[^2]: [ttk.Treeview](http://tkdocs.com/shipman/ttk-Treeview.html)
[^3]: [pyodbc](https://pypi.org/project/pyodbc/)

# Phonebook ☎️
![interface](https://github.com/clarencesarmiento/Phonebook/blob/b554be0dfc04a66fe53d2d765fdc6ad545d715f0/Images/V2%20Interface.png)

## DESCRIPTION:
A python program with Graphic User Interface that lets the user to
- Add Contact
- Edit Contact
- Delete Contact
- Search Contact

### How the Program Works?
Before saving a contact, the details goes through a validity check, where it checks if the phone number and the email address given by the user if valid and follows the required format of the program. It also checks if the phone number to be added is existing in the database. Once done, the details are stored to an SQLite database. The same flow for updating the contact details. 

### Built With
- [python](https://www.python.org/) - Backend
- [customtkinter](https://github.com/tomschimansky/customtkinter) - Frontend
- [sqlite3](https://docs.python.org/3/library/sqlite3.html) - Database

## TODO:
### Download
Download the Repository through Clone Repository using [Git](https://git-scm.com/downloads) or Download Zip.
```
git clone https://github.com/clarencesarmiento/Phonebook.git
```
### Installation
After downloading, go to `cmd` and navigate to the folder directory.
```
cd \folder_directory\Phonebook
```
Use [pip](https://pip.pypa.io/en/stable/) to install required packages inside
the `requirements.txt`.
```
pip install -r requirements.txt
```
### Usage
Run the `phonebook.py` using [python](https://www.python.org/).
```
python phonebook.py
```
## LICENSE:
Distributed under the MIT License. See `LICENSE` for more information.

# Phonebook ☎️
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/clarencesarmiento/Youtube-Downloader/blob/638e7266043379c67f927dbfcdccc1972c17c990/LICENSE.md)
[![Moodboard](https://img.shields.io/badge/Behance-Moodboard-blue.svg)](https://www.behance.net/gallery/181131141/Window-Desktop-Phonebook-Application)

![interface](https://github.com/clarencesarmiento/Phonebook/blob/b554be0dfc04a66fe53d2d765fdc6ad545d715f0/Images/V2%20Interface.png)

## [Video Demo](https://youtu.be/rF7C11wcsC0)

## [.exe](https://www.mediafire.com/file/g1bkc0tk256ztod/Phonebook_V2.0.zip/file)

## DESCRIPTION:
A python program with Graphic User Interface that lets the user to
- Add Contact
- Edit Contact
- Delete Contact
- Search Contact by Name

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

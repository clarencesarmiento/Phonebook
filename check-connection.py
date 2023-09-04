import mysql.connector
from mysql.connector import errorcode

try:
    conn = mysql.connector.connect(
        host='localhost',
        port= '3306',
        user= 'root',
        password= 'Sarmiento1020',
        database= 'phonebook'
    )
    if conn.is_connected():
        db = conn.get_server_info()
        print('Connected to MySQL Server', db)
        cursor = conn.cursor()
        cursor.execute('SELECT DATABASE();')
        record = cursor.fetchone()
        print('Connected to ', record)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    conn.close()
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'laptop'

TABLE = {}
TABLE['laptop'] = (
    "CREATE TABLE laptop ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `brand` varchar(30) NOT NULL,"
    "   `model` varchar(30) NOT NULL,"
    "   `cpu_brand` varchar(20),"
    "   `cpu_bm` varchar(30),"
    "   `cpu_model` varchar(30),"
    "   `sd_ram` varchar(10),"
    "   `ram_capacity` varchar(5),"
    "   `display` varchar(45),"
    "   `graphic_card` varchar(30),"
    "   `graphic_card_rs` varchar(5),"
    "   `hdd` varchar(15),"
    "   `ssd` varchar(15),"
    "   `description` varchar(80),"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['user'] = (
    "CREATE TABLE `user` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `fullname` varchar(80) NOT NULL,"
    "   `email` varchar(45) NOT NULL,"
    "   `password` varchar(45) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

db = mysql.connector.connect(host='127.0.0.1', user='root', password="@615$011m9841k@")
cursor = db.cursor()


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed Creating Database : {}".format(err))
        exit(1)


try:
    cursor.execute(" USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} Create Successfully.".format(DB_NAME))
        db.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLE:
    table_description = TABLE[table_name]
    try:
        print("Creating Table {}".format(table_name), end=' ')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already Exist!")
        else:
            print(err.msg)
    else:
        print("Ok")

cursor.close()
db.close()

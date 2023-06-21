from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
#Creating a MySQL database
DB_NAME = 'KIG'
TABLES = {}
TABLES['Users'] = (
    "CREATE TABLE `Users` ("
    "  `User_ID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `Name` varchar(15) NOT NULL,"
    "  `Password` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`User_ID`)"
    ") ENGINE=InnoDB")

TABLES['Plants'] = (
    "CREATE TABLE `Plants` ("
    "  `ID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `Name` varchar(40) NOT NULL,"
    "  `Watering_time` int(11) NOT NULL DEFAULT '1',"
    "  `Watering_date` varchar(40) NOT NULL,"
    "  `User_ID` int(11) NOT NULL,"
    "  PRIMARY KEY (`ID`), KEY `User_ID` (`User_ID`),"
    "  CONSTRAINT `plants_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='Dy03&2628',
                              host='127.0.0.1')

cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()
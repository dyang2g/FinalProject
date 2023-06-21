from __future__ import print_function
import mysql.connector
#testing
try:
    cnx = mysql.connector.connect(user='root', password='Dy03&2628',
                              host='127.0.0.1',
                              database='KIG')
    cursor = cnx.cursor()

    # Insert new user
    #add_user = ("INSERT INTO Users "
    #           "(Name, Password) "
    #           "VALUES (%s, %s)")
    #data_user = ('Leo', '11111')
    #cursor.execute(add_user, data_user)
    #user_id = cursor.lastrowid

    # Insert new plant
    add_plant = ("INSERT INTO Plants "
               "(Name, Watering_time, Watering_date, User_ID) "
               "VALUES (%s, %s, %s, %s)")
    data_plant = ('Tree', 3, '2023-06-20', 1)
    cursor.execute(add_plant, data_plant)

    # Make sure data is committed to the database
    cnx.commit()
    print("The new records are successfully added to Users table and Plants table!")

except mysql.connector.Error as error:
    print("Adding records to tables failed {}".format(error))

finally:
    if cnx.is_connected():
        cursor.close()
        cnx.close()
        print("MySQL connection is closed")

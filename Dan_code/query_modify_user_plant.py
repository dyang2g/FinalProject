import mysql.connector

cnx = mysql.connector.connect(user='root', password='Dy03&2628',
                              host='127.0.0.1',
                              database='plants')
cursor = cnx.cursor()

# find the number of plants for a specific user
uid = 1
query = "SELECT * FROM Plants WHERE User_ID in (%s, %s)"
data = (uid, uid)
cursor.execute(query, data)
# get all records
records = cursor.fetchall()
print("Total number of plants: ", cursor.rowcount)

#testing
# list plant information for a specific user
for row in records:
        print("ID = ", row[0], )
        print("Name = ", row[1])
        print("Watering_time  = ", row[2])
        print("User_ID  = ", row[3], "\n")


# Modify plant watering time for a specific plant and user
uid = 1
new_watering_time = 3
plant_name = "Rose"
update_query = "UPDATE Plants SET Watering_time = %(Watering_time)s WHERE User_ID = %(User_ID)s AND Name = %(Name)s"
update_data = {
    'Name': plant_name,
    'Watering_time': new_watering_time,
    'User_ID': uid,
}
cursor.execute(update_query, update_data)
cnx.commit()

# Insert a plant for a specific user
uid = 1
watering_time = 6
name = "Lily"
insert_query = ("INSERT INTO Plants "
               "(Name, Watering_time, User_ID) "
               "VALUES (%(Name)s, %(Watering_time)s, %(User_ID)s)")
insert_data = {
    'Name': name,
    'Watering_time': watering_time,
    'User_ID': uid,
}
cursor.execute(insert_query, insert_data)
cnx.commit()

# Delete a plant for a specific user
uid = 1
delete_name = "Rose"
delete_query = "DELETE FROM Plants WHERE Name = %(Name)s AND User_ID = %(User_ID)s"
delete_data = {
    'Name': delete_name,
    'User_ID': uid,
}
cursor.execute(delete_query, delete_data)
cnx.commit()

cursor.close()
cnx.close()
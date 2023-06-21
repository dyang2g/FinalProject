from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import mysql.connector
from datetime import date, datetime, timedelta

#connecting to MySQL
cnx = mysql.connector.connect(user='root', password='Dy03&2628',
                                host='127.0.0.1',
                                database='KIG')

#function return to index
def home(request):
    return render(request, "index.html")

#sign up fuction
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Users")

        records = cursor.fetchall()

        #Check if username aready exist
        for row in records:
            if row[1] == username:
                return render(request, "error.html", {'fName': "null",'message': "Username already exist. Please try a different username."}) #Send to error page

        # Insert new user into database
        add_user = ("INSERT INTO Users "
                "(Name, Password) "
                "VALUES (%s, %s)")
        data_user = (username, password)
        cursor.execute(add_user, data_user)
        user_id = cursor.lastrowid
        cnx.commit()
        return redirect('signin') #Send to sign in page

    return render(request, "signup.html")

#sign in function
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Users")

        records = cursor.fetchall()
        uID = 0

        #Find user in database
        for row in records:
            if row[1] == username and row[2] == password:
                
                today0, today1, today2, today3, today4, later0, later1, later2, later3, later4, over0, over1, over2, over3, over4 = sort(username)
                #Send to home page
                return render(request, "homepage.html", {'fname': username, 'today0': today0, 'today1': today1, 'today2': today2, 'today3': today3, 'today4': today4, 'later0': later0, 'later1': later1, 'later2': later2, 'later3': later3, 'later4': later4, 'over0': over0, 'over1': over1, 'over2': over2, 'over3': over3, 'over4': over4})

    return render(request, "signin.html")

#home page function
def homepage(request):
    if request.method == "POST":
        try: #Plant button clicked
            pName = request.POST['pName']
            fName = request.POST['fName']

            u1 = User(fName)
            wateringTime, wateringDate = u1.getPlantInfo(pName)

            return render(request, "plantinfo.html", {'pName': pName, 'wateringTime': wateringTime, 'wateringDate': wateringDate, 'fName': fName}) #Send to plant info page
        except: #Add plant button clicked
            fName = request.POST['fName']
            return render(request, "createplant.html", {'fName': fName}) #Send to add plant page
    
    return render(request, "homepage.html")

def plantinfo(request):
    if request.method == "POST":
        fName = request.POST['fName']
        pName = request.POST['pName']
        try: #I have watered the plant button clicked
            wateringtime = request.POST['iswatered']
            nextDate = str(date.today() + timedelta(days = int(wateringtime))) #Set next watering date
            u1 = User(fName)
            u1.uptatePlantWateringDate(pName, nextDate)

        except:
            var1 = 0
        
        try: #Edit button clicked
            newName = request.POST['newName']
            newTime = request.POST['newTime']

            u1 = User(fName)

            cursor = cnx.cursor()

            cursor.execute("SELECT * FROM Plants")

            records = cursor.fetchall()

            for row in records: #Check if user already has a repeating plant name
                if newName == pName:
                    break
                if row[1] == newName and row[4] == u1.uID:
                    return render(request, "error.html", {'fName': fName, 'message': "Plant name aready in use. Please choose a different name."})

            u1.editPlant(pName, newName, newTime)
        
        except:
            var1 = 0

        try: #Delete button clicked
            delete = request.POST['del']
            cursor = cnx.cursor()

            u1 = User(fName)
            u1.deletePlant(pName)

        except:
            var1 = 0

        today0, today1, today2, today3, today4, later0, later1, later2, later3, later4, over0, over1, over2, over3, over4 = sort(fName)
        #Send to home page
        return render(request, "homepage.html", {'fname': fName, 'today0': today0, 'today1': today1, 'today2': today2, 'today3': today3, 'today4': today4, 'later0': later0, 'later1': later1, 'later2': later2, 'later3': later3, 'later4': later4, 'over0': over0, 'over1': over1, 'over2': over2, 'over3': over3, 'over4': over4})

#Add plant function
def createplant(request):
    if request.method == "POST":
        fName = request.POST['fName']
        pName = request.POST['pName']
        wTime = request.POST['wTime']
        wDate = str(date.today() + timedelta(days = int(wTime)))
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Users")

        records = cursor.fetchall()
        uID = 0

        for row in records:
            if row[1] == fName:
                uID = row[0]

        cursor.execute("SELECT * FROM Plants")

        records = cursor.fetchall()

        for row in records: #Check if user already has a repeating plant name
            if row[1] == pName and row[4] == uID:
                return render(request, "error.html", {'fName': fName, 'message': "Plant name aready in use. Please choose a different name."}) #Send to error page

        u1 = User(fName)
        u1.addPlant(pName, wTime, wDate)

        today0, today1, today2, today3, today4, later0, later1, later2, later3, later4, over0, over1, over2, over3, over4 = sort(fName)
        #Send to home page
        return render(request, "homepage.html", {'fname': fName, 'today0': today0, 'today1': today1, 'today2': today2, 'today3': today3, 'today4': today4, 'later0': later0, 'later1': later1, 'later2': later2, 'later3': later3, 'later4': later4, 'over0': over0, 'over1': over1, 'over2': over2, 'over3': over3, 'over4': over4})

        
    return render(request, "createplant.html")

#Error function
def error(request):
    if request.method == "POST":
        try:
            fName = request.POST['fName']
            if fName == "null":
                return redirect('home')
            
            today0, today1, today2, today3, today4, later0, later1, later2, later3, later4, over0, over1, over2, over3, over4 = sort(fName)
            #Send to home page
            return render(request, "homepage.html", {'fname': fName, 'today0': today0, 'today1': today1, 'today2': today2, 'today3': today3, 'today4': today4, 'later0': later0, 'later1': later1, 'later2': later2, 'later3': later3, 'later4': later4, 'over0': over0, 'over1': over1, 'over2': over2, 'over3': over3, 'over4': over4})


        except:
            return redirect('home') #Send to index
    
    return render(request, "error.html")

#Sorting function by watering date
def sort(fName):
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM Users")

    records = cursor.fetchall()
    uID = 0

    for row in records: #Identify user
        if row[1] == fName:
            uID = row[0]
            cursor.execute("SELECT * FROM Plants")
            pRecords = cursor.fetchall()
            plantNamesToday = []
            plantNamesLater = []
            plantNamesOverdue = []
            for i in pRecords: #Categorize plants based on watering date
                if i[4] == uID:
                    diff = datetime.strptime(i[3], "%Y-%m-%d") - datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
                    if str(date.today()) == i[3]:
                        plantNamesToday.append(i[1])
                    elif diff.days > 0:
                        plantNamesLater.append(i[1])
                    else:
                        plantNamesOverdue.append(i[1])

            try:
                today0 = plantNamesToday[0]
            except:
                today0 = ""
            try:
                today1 = plantNamesToday[1]
            except:
                today1 = ""
            try:
                today2 = plantNamesToday[2]
            except:
                today2 = ""
            try:
                today3 = plantNamesToday[3]
            except:
                today3 = ""
            try:
                today4 = plantNamesToday[4]
            except:
                today4 = ""
            try:
                later0 = plantNamesLater[0]
            except:
                later0 = ""
            try:
                later1 = plantNamesLater[1]
            except:
                later1 = ""
            try:
                later2 = plantNamesLater[2]
            except:
                later2 = ""
            try:
                later3 = plantNamesLater[3]
            except:
                later3 = ""
            try:
                later4 = plantNamesLater[4]
            except:
                later4 = ""
            try:
                over0 = plantNamesOverdue[0]
            except:
                over0 = ""
            try:
                over1 = plantNamesOverdue[1]
            except:
                over1 = ""
            try:
                over2 = plantNamesOverdue[2]
            except:
                over2 = ""
            try:
                over3 = plantNamesOverdue[3]
            except:
                over3 = ""
            try:
                over4 = plantNamesOverdue[4]
            except:
                over4 = ""
            return(today0, today1, today2, today3, today4, later0, later1, later2, later3, later4, over0, over1, over2, over3, over4) #Return list of sorted plants
        
#User class
class User:
    def __init__(self, username):
        self.username = username
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM Users")
        records = cursor.fetchall()
        self.password = ""
        self.uID = 0
        for row in records: #Identify user
            if row[1] == username:
                self.password = row[2]
                self.uID = row[0]
            
    def getPlantInfo(self, pName):
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Plants")

        records = cursor.fetchall()
        wateringTime = ""
        wateringDate = ""

        for i in records: #Get plant information from database
            if i[1] == pName and i[4] == self.uID:
                wateringTime = i[2]
                wateringDate = i[3]
        return(wateringTime, wateringDate)
        
    def uptatePlantWateringDate(self, pName, nextDate):
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Plants")

        records = cursor.fetchall()

        for i in records: #Uptate database
            if i[1] == pName:
                update_query = "UPDATE Plants SET Watering_date = %(Watering_date)s WHERE User_ID = %(User_ID)s AND Name = %(Name)s"
                update_data = {
                    'Name': i[1],
                    'Watering_date': nextDate,
                    'User_ID': self.uID,
                }
                cursor.execute(update_query, update_data)
                cnx.commit()

    def editPlant(self, pName, newName, newTime):
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM Plants")

        records = cursor.fetchall()

        for i in records: #Uptate database
            if i[1] == pName:
                update_query = "UPDATE Plants SET Watering_time = %(Watering_time)s WHERE User_ID = %(User_ID)s AND Name = %(Name)s"
                update_data = {
                    'Name': i[1],
                    'Watering_time': newTime,
                    'User_ID': self.uID,
                }
                cursor.execute(update_query, update_data)
                cnx.commit()
                update_query = "UPDATE Plants SET Name = %(newName)s WHERE User_ID = %(User_ID)s AND Name = %(Name)s"
                update_data = {
                    'Name': i[1],
                    'newName': newName,
                    'User_ID': self.uID,
                }
                cursor.execute(update_query, update_data)
                cnx.commit()

    def deletePlant(self, pName):
        cursor = cnx.cursor()

        #Delete plant from database
        delete_query = "DELETE FROM Plants WHERE Name = %(Name)s AND User_ID = %(User_ID)s"
        delete_data = {
            'Name': pName,
            'User_ID': self.uID,
        }
        cursor.execute(delete_query, delete_data)
        cnx.commit()

    def addPlant(self, pName, wTime, wDate):
        cursor = cnx.cursor()

        #Add plant to database
        add_plant = ("INSERT INTO Plants "
               "(Name, Watering_time, Watering_date, User_ID) "
               "VALUES (%s, %s, %s, %s)")
        data_plant = (pName, wTime, wDate, self.uID)
        cursor.execute(add_plant, data_plant)

        cnx.commit()
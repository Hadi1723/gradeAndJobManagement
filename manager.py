import pandas as pd
import csv, sqlite3
from datetime import datetime

#establishing connection to database
conn = sqlite3.connect('usersList.db')

#creating a cursor
cursor = conn.cursor()

class CoopManager:
    def __init__(self, user):
        self.user = user
    
    def logIn(self):
        getAccess = True
        while getAccess:        
            data = cursor.execute("SELECT * FROM customers").fetchall()
        
            conn.commit()

            print(data[0][1])
            for d in range(len(data)):
                if data[d][0] == self.user:
                    checkPassword = input("Please enter password")
                    if checkPassword == data[d][1]:
                        getAccess = False
                        break
        
        return True
    
    def createPassword(self, user):
        user_password = input("Input password please")
        dateNow = datetime.now()
    
        grade_file = self.user + "grades" + ".csv"
        gradeHeaders = [['Course Code', 'Course Name', 'Grade']]
        with open(grade_file, "w") as fh:
            gradeNames = csv.writer(fh)
            gradeNames.writerows(gradeHeaders)
        
        job_file = self.user + "jobs" + ".csv"
        jobHeaders = [['Company Name', 'Length', 'Salary in $']]
        with open(job_file, "w") as fh:
            jobNames = csv.writer(fh)
            jobNames.writerows(jobHeaders)
          
        #executing many rows
        many = [(user, user_password, grade_file, job_file, dateNow)]

        #the "?" is placeholder and must always be used
        cursor.executemany("INSERT INTO customers VALUES (?,?,?,?,?)", many)
        
        conn.commit()
        
        return True
    
    def updateFiles(self, file):
        self.file = file
        correctGrades = True
        correctJobs = True
        
        update_values = []
                      
        data = cursor.execute("SELECT * FROM customers").fetchall()
                    
        conn.commit()
        
        for d in range(len(data)):
            if data[d][0] == self.user:
                if self.file == 'g' or self.file == 'G':
                    marksFile = data[d][2]
                    
                    while correctGrades:
                        code = input("what is the course code?")
                        cName = input("what is your course name?")  
                        mark = input("what was your mark?")
                        
                        update_values.append([code,cName,mark])
                        
                        stillAsk = input("do you still want to add more subjects? press 1 for no and anything else for yes")
                        
                        if stillAsk == "1":
                            with open(marksFile, 'a') as gh:
                                grades = csv.writer(gh)
                                grades.writerows(update_values)
                            return 
                            
                else:
                    marksFile = data[d][3]

                    while correctJobs:
                        job = input("what was the name of the company?")
                        length = input("how long did you work for?")  
                        salary = input("please indicate your salary in $")
            
                        update_values.append([job,length, salary])
                        
                        stillAsk = input("do you still want to add more subjects? press 1 for no and anything else for yes")
                        
                        if stillAsk == "1":
                            with open(marksFile, 'a') as gh:
                                grades = csv.writer(gh)
                                grades.writerows(update_values)   
                            return        
                    
    def readFiles(self, file_path):       
        data = cursor.execute("SELECT * FROM customers").fetchall()
        
        for d in range(len(data)):
            if data[d][0] == self.user:
                if file_path == 'g' or file_path == 'G':
                    self.file_path = data[d][2]
                elif file_path == 'j' or file_path == "J":
                    self.file_path = data[d][3]
                
        wantSort = input("do you want your data to be sorted? Press 1 for yes and anything else for no")
        
        df = pd.read_csv(self.file_path)
        
        if wantSort == "1":
            if self.file_path[len(self.file_path)-8:len(self.file_path):] != 'jobs.csv':
                whichSort = input("what do you want to be sorted? press 1 for the course code, 2 for the course name, and 3 for grades. if you press neither, grades will automatically be sorted")
                
                isAssending = True
                userAssending = input("do you want your data to be in assending order? press 1 for yes and anything else for no.")
                
                if userAssending != "1":
                    isAssending = False
                      
                if whichSort == "1":
                   print(df.sort_values('Course Code', ascending = isAssending))                 
                elif whichSort == "2":
                    print(df.sort_values('Course Name', ascending = isAssending))
                else:
                    print(df.sort_values('Grade', ascending = isAssending))
            else:
                whichSort = input("what do you want to be sorted? press 1 for the company name, 2 for the length of job, and 3 for salary. if you press neither, salary will automatically be sorted")
                
                isAssending = True
                userAssending = input("do you want your data to be in assending order? press 1 for yes and anything else for no.")
                
                if userAssending != "1":
                    isAssending = False
                      
                if whichSort == "1":
                   print(df.sort_values('Company Name', ascending = isAssending))                       
                elif whichSort == "2":
                    print(df.sort_values('Length', ascending = isAssending))
                else:
                    print(df.sort_values('Salary in $', ascending = isAssending))
        else:
            print(df)
        
        return

            
operate = True

while operate:
    print("Welcome to Program!! \n")
    
    user = input("What is your name?")
    
    coop = CoopManager(user)
    
    access = False
    
    while not access:
        accountExist = input("Do you already have an account? Type \"y\" for yes, \"n\" for no, and \"q\" to quit program")
    
        if accountExist == "y" or accountExist == "Y":
            access = coop.logIn()
        elif accountExist == "n" or accountExist == "N":
            access = coop.createPassword(user)
        elif accountExist == "q" or accountExist == "Q":
            operate = False
    
    wantUpdate = True
    while wantUpdate:
        fileChoose = input("which file do you want to read? type \"g\" for grades, \"j\" for jobs, and \"q\" to quit program")
        
        if fileChoose == 'g' or fileChoose == "G" or fileChoose == 'j' or fileChoose == 'J':
            actionFile = input("Do you want to read or update file? Type \"r\" for read, \"u\" for update, or \"q\" to quit program")

            appropiateFile = False
        
            while not appropiateFile:
                if actionFile == "r" or actionFile == "R":
                    coop.readFiles(fileChoose)
                    appropiateFile = True
                elif actionFile == 'u' or actionFile == "U":
                    coop.updateFiles(fileChoose)
                    appropiateFile = True
                elif actionFile == 'q' or actionFile == "Q":
                    wantUpdate = False
                    operate = False
        elif fileChoose == 'q' or fileChoose == "Q":
            wantUpdate = False
            operate = False
            
#cursor.execute("INSERT INTO customers VALUES (str(user),str(user_password),str(user_file),datenow)")
conn.close()
    


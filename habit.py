import sys
import os
from sys import argv, exit
import datetime
from datetime import date
from datetime import time
from datetime import datetime
import sqlite3
import functools
import operator
from collections import Counter
import unittest
import subprocess
import habtest
#from habtest import habitTest
#import cs50


def main():
    ''' This is the main function where details are acquired before class is called
    for creating,
    checking in/off
    analysing, 
    deleting, and
    testing habits take place '''
    print("habit program")
    print()
    print("Welcome to the habit program, you can create new habits, check in or off habits, analyse test existing habits, test habit data, and delete habits")
    print()
    new_oper = input("What would you like to do? create, check, analyse, delete an habit or test habits?  ")
    print()
    if new_oper == 'create':    #if input is 'create' then a periodicity will be asked
        
        period = period_quest(new_oper)     #for taking in periodicity and checking if it is correct by calling a function
        hab_name = input("Please input name of habit you want to create?  ")
        print()
        name_check = hab_check(hab_name, period)    #checks if name of habit already exists in selected peiodicity
        if name_check == False:
            #habit(hab_name, period, new_oper)
            cre_hab = habit(hab_name, period)
            cre_hab.create()
        else:
            comerror(5)

    elif new_oper == 'check':   #if check is chosen then a list is printed and request for input
        
        period = period_quest(new_oper)     #asks for periodicity
        pri_hab(period)     #prints all habit in selected peiodicity
        chab_name = input(f"Which of the above listed {period} would you like to check in or off?  ")
        print()
        habname_check = hab_check(chab_name, period)    #check if input name actually exists by calling a function
        if habname_check == True:
            check_hab = habit(chab_name, period)    #if it exists, then the check method in class is called
            check_hab.check()
        else:
            comerror(6)     #if it does not exist then an error will be printed
            exit(0)
        #print(period)

    elif new_oper == 'analyse':     #if analyse is chosen then a question about periodicity will pop up after which the analyse method in habit class will be called
        
        period = period_quest(new_oper)
        hab_anal = habit(None, period)
        hab_anal.analyse()

    elif new_oper == 'delete':      #if delete is chosen then a question about periodicity will also pop up 
        period = period_quest(new_oper)
        pri_hab(period)     #prints all habit in selected periodicity
        delhab_name = input(f"Which of the above listed {period} habits would you like to delete?  ")   #asks for input of habit that needs to be deleted
        print()
        delname_check = hab_check(delhab_name, period)      #checks if input actually exists in database
        if delname_check == True:
            confirm = input(f"Are you sure you want to delete the {delhab_name} habit?  ")      #asks for confirmation  for habit deletion
            print()
            if confirm == "yes":    #if yes is selected, then the delete method in habit class will be called
                print(f"Deleting the {delhab_name} {period} habit")
                del_hab = habit(delhab_name, period)
                del_hab.delete()
            elif confirm == "no":   #if no is selected then habit will not be deleted
                print(f"{delhab_name} habit not deleted")
            else:
                print("Invalid command: Please type yes or no")
            
        else:
            comerror(6)
            exit(0)
    
    elif new_oper == "test":    #if input is test, test method will be called for sampling of predefined habits
        test_hab = habit()
        test_hab.hab_test()
       
    else:
        comerror(1)


class habit:
    '''class with two attributes namely: name and period,
    five methods namely: create, check, delete, analyse and test '''
    def __init__(self, name = None, period = None):     #constructor function with null as default values
        self.name = name
        self.period = period
        #self.hab_oper = hab_oper
        
    def create(self):   #create method for creating habits
        name = self.name
        period = self.period
        day = ftime(period)
        db = sqlite3.connect("../habit/habit.db")
        cur = db.cursor()
    
        #query to incert input name to create habit in database of selected pereiod
        cur.execute(f"INSERT INTO {period} ('name', 'first') VALUES ('{name}',{day})")

        db.commit()     #makes changes to database permanent
        cur.close()     #closes connection to database
        db.close()
    
        print(f"{name} {period} habit created")
    
    def check(self):    #check method for checking in/off habits
        name = self.name
        period = self.period
        in_or_off = input(f"Would you like to check in or off the {name} habit? please type in or off:-   ")
        if in_or_off == "in":    #this checks if input is in or off
            habit_checkin(period, name)
        elif in_or_off == "off":
            habit_checkoff(period, name)
        else:
            comerror(4)
            exit(0)
            
    def analyse(self):      #analyse method for analysing habits in selected periodicity
        period = self.period
        print(f"Below is an analysis of {period} habits")
        print("To succesfully make a daily and weekly habit, it needs to be checked in six times daily or weekly after creation\n")
        print("To successfully make a monthly habit, it needs to be checked in 5 times monthly after creation\n")
        anal_hab(period)  
    
    def delete(self):       #delete method for deleting habits
        name = self.name
        period = self.period
        db = sqlite3.connect("../habit/habit.db")
        cur = db.cursor()
    
        #query to delete row given name and period in database
        cur.execute(f"DELETE FROM {period} WHERE name = '{name}'")
    
        db.commit()
        cur.close()
        db.close()
    
    def hab_test(self):     #test method for analysis with predefined habits
        #print("test habit")
        #test_en = unittest.TestLoader().loadTestsFromModule(habtest)
        #unittest.TextTestRunner(verbosity=2).run(test_en)
        
        test_en = unittest.TestLoader().loadTestsFromModule(habtest)
        unittest.TextTestRunner(verbosity=1).run(test_en)
        
           
def period_quest(oper):     #
    ''' function that asks question about periodicity and checks
    if input corresponds to periodicity and returns period '''
    per_list = ["daily", "weekly", "monthly"]
    if oper == 'check':
        period = input("Which period would you like to check in or off? daily, weekly or monthly?   ")
    else:
        period  = input(f"Which period would you like to {oper}? daily, weekly or monthly?  ")

    if period in per_list:
        return period
    else:
        comerror(3)
        exit(0)

def hab_check(in_name, period):  
    '''function that checks if a selected habit exists
    and return boolean true or false '''
    #db = sqlite3.connect("../habit/habit.db")   #connects to  database file using sqlite3 connector
    db = sqlite3.connect("../habit/habit.db")   #connects to  database file using sqlite3 connector
    cur = db.cursor()
    data = []   #empty list to accomodate database query for habit names in selected period

    cur.execute(f"SELECT name FROM {period}")   #database query for names in selected period
    for row in cur:     #for loop to append names from database to list
        rowe = functools.reduce(operator.add, (row))    #converts tuple from database to string
        data.append(f"{rowe}")
        #print(rowe)

    if in_name in data:     #checks if name already exists in database
        return True
    else:
        return False

    cur.close()     #closes connection to database
    db.close()

def pri_hab(period): 
    ''' function that prints all habits in selected periodicity
    before checking in/off or deleting of habits takes place '''
    db = sqlite3.connect("../habit/habit.db")   #establishing connection with database
    cur = db.cursor()
    
    cur.execute(f"SELECT name FROM {period}")   #query to get names in selected period from database
    i = 1
    for row in cur:
        
        names = functools.reduce(operator.add, (row))   #converts tuple from database to string
        print(f"{i}.) {names}")
        i+=1
        #print(names)
    
    cur.close()     #closes connection to database
    db.close()
 
 
def habit_checkin(period, name):      
    '''function for checking in habits which is called from
    the class'''
    
    chevalue = ftime(period)    #takes value from time function, either day, week or month
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    data =[]
    
    cur.execute(f"SELECT comp FROM {period} WHERE name = '{name}'")     #query to check if selected habit is already checked off
    
    for row in cur:     #for loop to extract if yes already inserted
        data = row
        choff = functools.reduce(operator.add, (row))   #
        conf = choff
        #print(data)
    
    if conf == 'yes':  #if habit is already markede as complete, checkoff not possible
        print(f"{name} habit already checked off")
        
        
        
    else:   #if it is not marked as complete
        cur.execute(f"SELECT first FROM {period} WHERE name = '{name}'")
    
        for row in cur:
            rowe = functools.reduce(operator.add, (row))
            first_date = rowe
        #print(first_date)  
    
        currdate = chevalue - first_date    #for computing check-in days
    
        if period == 'monthly': 
            chinsertmon(period, currdate, chevalue, name)
        elif period == 'weekly':
            chinsert(period, currdate, chevalue, name)
        else:
            chinsert(period, currdate, chevalue, name)
        #cur.execute(f"INSERT INTO {period} ('first') VALUES ({day})")
    
    
    db.commit()
    cur.close()
    db.close()

def habit_checkoff(period, name):   
    '''function for checkin off habits by checking if it was already checked off
    and checks it off if not already checked off '''
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    cur.execute(f"SELECT comp FROM {period} WHERE name = '{name}'")     #for checking off in database
    
    for row in cur:     #for loop for checking if habit was checked off earlier
        rowe = functools.reduce(operator.add, (row))
        con = rowe
    
    if con == 'yes':    #if selected habit is already checked off, print and error and terminate checkoff
        print(f"{name} habit already checked off")
        
    else:
        cur.execute(f"UPDATE {period} SET comp = 'yes' WHERE name = '{name}'")
    
    
    db.commit()
    cur.close()
    db.close()


def chinsertmon(period, cdate, invalue, name):
    '''Function for inserting monthly check-ins into
    monthly table in database'''
    chevalue = ftime(period)    #takes value from time function, either day, week or month
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    if cdate == 0:
        print("Check in not possible. Already checked in")
    elif cdate == 1:
        cur.execute(f"UPDATE {period} SET second = {invalue} WHERE name = '{name}'")
    elif cdate == 2:
        cur.execute(f"UPDATE {period} SET third = {invalue} WHERE name = '{name}'")
    elif cdate == 3:
        cur.execute(f"UPDATE {period} SET forth = {invalue} WHERE name = '{name}'")
    elif cdate == 4:
        cur.execute(f"UPDATE {period} SET fifth = {invalue} WHERE name = '{name}'")
    elif cdate == 5:
        cur.execute(f"UPDATE {period} SET sixth = {invalue} WHERE name = '{name}'")
    else:
        print("Incorrect Check-in: Check-in beyond recommended time -> This means that if checkin is not complete at this time then this habit is not a success ")
        
    db.commit()
    cur.close()
    db.close()
    
def chinsert(period, cdate, invalue, name):
    '''Function for inserting daily and weekly check-ins into
    daily and weekly tables in database'''
    chevalue = ftime(period)    #takes value from time function, either day, week or month
    db = sqlite3.connect("../habit/habit.db")
    cur = db.cursor()
    
    if cdate == 0:
        print("Check in not possible. Already checked in")
    elif cdate == 1:
        cur.execute(f"UPDATE {period} SET second = {invalue} WHERE name = '{name}'")
    elif cdate == 2:
        cur.execute(f"UPDATE {period} SET third = {invalue} WHERE name = '{name}'")
    elif cdate == 3:
        cur.execute(f"UPDATE {period} SET forth = {invalue} WHERE name = '{name}'")
    elif cdate == 4:
        cur.execute(f"UPDATE {period} SET fifth = {invalue} WHERE name = '{name}'")
    elif cdate == 5:
        cur.execute(f"UPDATE {period} SET sixth = {invalue} WHERE name = '{name}'")
    elif cdate == 6:
        cur.execute(f"UPDATE {period} SET seventh = {invalue} WHERE name = '{name}'")
    else:
        print("Incorrect Check-in: Check-in beyond recommended time -> This means that if checkin is not complete at this time then this habit is not a success ")
        
    db.commit()
    cur.close()
    db.close()
 
 
def anal_hab(period):    
    '''function for analyzing habits in selected period
    by calculating total amounts of correct check-ins and
    checking if habits are already checked off'''
    db = sqlite3.connect("../habit/habit.db")   #establishing connection to database
    cur = db.cursor()
    #data = []   #empty list for data insertion
    ana_dict = {}
    
    cur.execute(f"SELECT * FROM {period}")
    k = 1
    for row in cur:
        #print(row)  #this line can be uncommented to confirm that actual date values are being inserted into the database
        data = row
        name = row[1]
        #print(name)
        count = 0
        
        for i in row:   #this counts all non-empty cells in the row
            if i is not None:
                count = count + 0
            else:
                count = count + 1
        
        
        if period == 'monthly':
            comp = row[8]
            #global counts
            counts = anal_count(period, comp, count)    
            if counts == 6:
                print(f"{k}.) {name} {period} habit checked in completly {counts - 1} times consecutively after creation, {name} is successfully made an habit")
                
            elif counts != 6 and comp == 'yes':
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")
            
            else:
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")
                
        else:
            comp = row[9]
            #global counts
            counts = anal_count(period, comp, count)       
            if counts == 7:
                print(f"{k}.) {name} {period} habit checked in completly {counts - 1} times consequtively after creation, {name} is successfully made an habit")
            elif counts != 7 and comp == 'yes':
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")
                
            else:
                print(f"{k}.) {name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")
        
        k+=1        
        #print(sum(x is not None for x in data))
        
        
        
    cur.close()
    db.close()

def anal_count(period, comp, count):
    if period == 'monthly':     #if period to be analysed is monthly, calculate amount of check-in's
        
            
        counts = 7 - count
        if comp == 'yes':
            counts = counts - 1
            return counts    
        else:
            counts = counts
            return counts
    
    else:
        
        counts = 8 - count
        if comp == 'yes':
            counts = counts - 1
            return counts
        else:
            counts = counts
            return counts
    
def comerror(val):  #used to print errors
    if val == 1:
        print("Invalid Entry: Please type create, check, analyse, delete or test")
    elif val == 2:
        print("command line error, methods are: create, check, analyse and delete")
    elif val == 3:
        print("Invalid entry: Please input daily, weekly or monthly")
    elif val == 4:
        print("Invalid Entry: Please input in or off")
    elif val == 5:
        print("Habit already exists")
    elif val == 6:
        print("Habit doesn't exist")


def ftime(period):  #function that returns day, week or month number of selected periodicity
    
    t = date.today()    #stores today's date
    day = t.day     #stores day
    week = t.isocalendar()[1]   #this stores the nth week
    mon = t.month       #stores month
    if period == "daily":
        return day
    elif period == "weekly":
        return week
    else:
        return mon


    #process2 = subprocess.Popen(['python', 'habtest.py'], cwd=os.getcwd(), preexec_fn=os.setsid)
    #process2.wait()

main()
#print(habit)
#test = habitTest()
#test.test_period()



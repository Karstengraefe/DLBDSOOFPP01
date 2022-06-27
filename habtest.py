import unittest
import sqlite3


class habit_Test(unittest.TestCase):

    def test_comp_dailyhab(self):
        '''method for testing analysis function and
        complete daily habits in the database'''

    #hab_list = ['reading']
        i = 'reading'

        check_count = anal_hab('daily', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 7, message)

    def test_incomp_dailyhab(self):
        '''method for testing analysis function and
        incomplete daily habits in the database'''

    #hab_list = ['reading']
        i = 'swimming'

        check_count = anal_hab('daily', i)
        message = "Habit is complete"
        self.assertNotEqual(check_count, 7, message)

    def test_comp_weeklyhab(self):
        '''method for testing analysis function and
        complete weekly habits in the database'''

    #hab_list = ['reading']
        i = 'jogging'

        check_count = anal_hab('weekly', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 7, message)

    def test_incomp_weeklyhab(self):
        '''method for testing analysis function and
        incomplete weekly habits in the database'''

    #hab_list = ['reading']
        i = 'hiking'

        check_count = anal_hab('weekly', i)
        message = "Habit is complete"
        self.assertNotEqual(check_count, 7, message)

    def test_comp_monthlyhab(self):
        '''method for testing analysis function and
        complete monthly habits in the database'''

    #hab_list = ['reading']
        i = 'gaming'

        check_count = anal_hab('monthly', i)
        message = "Habit is not complete"
        self.assertEqual(check_count, 6, message)

    def test_dailyperiod_quest(self):
        

        per = 'daily'

        check_per = period_quest('daily')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)

    def test_weeklylyperiod_quest(self):


        per = 'weekly'

        check_per = period_quest('weekly')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)

    def test_monthlyperiod_quest(self):


        per = 'monthly'

        check_per = period_quest('monthly')
        message = "Period is not correct"
        self.assertEqual(check_per, per, message)


def anal_hab(period, name):    #function for analyzing habits in selected period
    db = sqlite3.connect("../habit/habittest.db")   #establishing connection to database
    cur = db.cursor()
    #data = []   #empty list for data insertion
    ana_dict = {}


    cur.execute(f"SELECT * FROM {period} WHERE name = '{name}'")
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
            counts = anal_count(period, comp, count)
            if counts == 6:
                print(f"{name} {period} habit checked in completly {counts - 1} times consecutively after creation, {name} is successfully made an habit")

            elif counts != 6 and comp == 'yes':
                print(f"{name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")

            else:
                print(f"{name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")

        else:
            comp = row[9]
            #global counts
            counts = anal_count(period, comp, count)
            if counts == 7:
                print(f"{name} {period} habit checked in completly {counts - 1} times consequtively after creation, {name} is successfully made an habit")
            elif counts != 7 and comp == 'yes':
                print(f"{name} {period} habit checked in {counts - 1} times after creation, but already marked as complete")

            else:
                print(f"{name} {period} habit checked in {counts - 1} times after creation, {name} habit not made yet")



    cur.close()
    db.close()
    return counts

def anal_count(period, comp, count):
    if period == 'monthly':     #if period to be analysed is monthly, calculate amount of check-in's


        count_hab = 7 - count
        if comp == 'yes':
            count_hab = count_hab - 1
            return count_hab
        else:
            count_hab = count_hab
            return count_hab

    else:

        count_hab = 8 - count
        if comp == 'yes':
            count_hab = count_hab - 1
            return count_hab
        else:
            count_hab = count_hab
            return count_hab


def period_quest(oper):     #function that asks question about periodicity and checks if input corresponds to periodicity
    per_list = ["daily", "weekly", "monthly"]

    if oper in per_list:
        return oper
    else:
        exit(0)

#if __name__ == '__main__':
#unittest.main()
#test = habitTest()
#test.test_period()
'''
Created on Oct 17, 2014

@author: Adrian
'''
import unittest
import datetime
from datetime import date
import jac.mydate


class Test(unittest.TestCase):


    def testName(self):
#         d = date(2014, 10, 3)
#         next_day = 2 # wed
#         n = (next_day - d.weekday()) % 7 # mod-7 ensures we don't go backward in time
#         next_run_date = d + timedelta(days=n)
#         print('next wed: ' + str(next_run_date))
        #print('next thur: ' + next_run_date)
        print(jac.mydate.get_next_weekday(date.today(), 2).strftime("%A %d. %B %Y"))# wed
        print(jac.mydate.get_next_weekday(date.today(), 3).strftime("%A %d. %B %Y"))# thu

    def testNextDates(self):
        print(jac.mydate.get_next_dates(date(2014, 10, 11)))
        ret = jac.mydate.get_next_dates(date(2014, 10, 17))
        self.assertEqual(ret[0], datetime.date(2014, 10, 22))
        self.assertEqual(ret[1], datetime.date(2014, 10, 23))

        ret = jac.mydate.get_next_dates(date(2014, 10, 21))
        self.assertEqual(ret[0], datetime.date(2014, 10, 22))
        self.assertEqual(ret[1], datetime.date(2014, 10, 23))




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
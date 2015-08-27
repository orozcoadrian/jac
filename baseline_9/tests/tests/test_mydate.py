'''
Created on Oct 17, 2014

@author: Adrian
'''
import unittest
import datetime
from datetime import date
import jac.mydate
import pprint


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
        d = date(2015, 8, 9)
        print('get_next_dates: input: ' + str(d))
        ret = jac.mydate.get_next_dates(d)
        pprint.pprint(ret)
        mystr = pprint.pformat(ret)
        self.assertEqual('''[datetime.date(2015, 8, 12),
 datetime.date(2015, 8, 19),
 datetime.date(2015, 8, 26),
 datetime.date(2015, 9, 2),
 datetime.date(2015, 9, 9),
 datetime.date(2015, 9, 16)]''', mystr)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
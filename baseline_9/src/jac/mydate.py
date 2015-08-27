'''
Created on Oct 3, 2014

@author: Adrian
'''
import unittest

from datetime import date, timedelta

def get_next_weekday(from_date, next_weekday):
    n = (next_weekday - from_date.weekday()) % 7 # mod-7 ensures we don't go backward in time
    return from_date + timedelta(days=n)

def get_next_wed():
    return get_next_weekday(date.today(), 2)
def get_next_thu():
    return get_next_weekday(date.today(), 3)

def get_next_wed_offset(adate):
    return get_next_weekday(adate, 2)
def get_next_thu_offset(adate):
    return get_next_weekday(adate, 3)

def get_next_dates(from_date):
    ret= []
    weeks_num=6
    ret.extend([get_next_wed_offset(from_date+ timedelta(weeks=x)) for x in range(0,weeks_num)])
    # ret.extend([get_next_thu_offset(from_date+ timedelta(weeks=x)) for x in range(0,weeks_num)])
    ret.sort()
    return ret




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.record.MyRecordSet import MyRecordSet
from jac.filters.FilterCancelled import FilterCancelled

class Test(unittest.TestCase):


    def test1(self):
        mrs = MyRecordSet()
        item={'comment': 'CANCELLED'}
        mrs.set_items([item])
        instance = FilterCancelled(None)
        instance.apply(mrs)
    def test2(self):
        mrs = MyRecordSet()
        item={'comment': ''}
        mrs.set_items([item])
        instance = FilterCancelled(None)
        instance.apply(mrs)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
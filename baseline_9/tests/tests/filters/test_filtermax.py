'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.record.MyRecordSet import MyRecordSet
from jac.filters.FilterMax import FilterMax

class TestArgs(object):
#     def max(self):
#         return 2
    def __init__(self):
        self.__dict__['max'] = 2

class Test(unittest.TestCase):


    def test1(self):
        mrs = MyRecordSet()
        item={'comment': 'CANCELLED'}
        mrs.set_items([item,item,item])
        args=TestArgs()
        instance = FilterMax(args)
        v=instance.get_limit()
        self.assertEqual(2, v)
        instance.apply(mrs)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
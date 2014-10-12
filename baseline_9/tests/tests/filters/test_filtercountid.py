'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.record.MyRecordSet import MyRecordSet
from jac.filters.FilterCountId import FilterCountId

class TestArgs(object):
#     def max(self):
#         return 2
    def __init__(self):
        self.__dict__['count_id'] = [2,3]

class Test(unittest.TestCase):


    def test1(self):
        mrs = MyRecordSet()
        item={'count': 3}
        mrs.set_items([item,item,item])
        args=TestArgs()
        instance = FilterCountId(args)
        instance.get_count_id()
        instance.get_count_id_ints()
        instance.apply(mrs)

    def test2(self):
        class TestArgs2(object):
            def __init__(self):
                self.__dict__['count_id'] = None
        mrs = MyRecordSet()
        item={'count': 3}
        mrs.set_items([item,item,item])
        args=TestArgs2()
        instance = FilterCountId(args)
        instance.get_count_id()
#         instance.get_count_id_ints()
        instance.apply(mrs)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
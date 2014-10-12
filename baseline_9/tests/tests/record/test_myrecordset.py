'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.record.MyRecord import MyRecord
from jac.record.MyRecordSet import MyRecordSet

class Test(unittest.TestCase):


    def test1(self):
        instance = MyRecordSet()
        print(instance)

        item={'bcpao_acc': '2733237',
                  'bcpao_item': {'address': '2243  ROYAL POINCIANA BLVD , MELBOURNE 32935',
                                 'frame code': '03',
                                 'latest market value total': '$108,250',
                                 'total base area': u'1,812',
                                 'use code': {'use_code': '110', 'use_code_str': None},
                                 'year built': '1995',
                                 'zip_code': '32935'},
                  'case_number': u'05-2008-CA-013830-XXXX-XX',
                  'case_title': u'COUNTRYWIDE VS NOEL C GABBERT',
                  'comment': '',
                  'count': 1,
                  'foreclosure_sale_date': u'06/18/2014',
                  'legal': {'blk': u'D',
                            'lt': u'60',
                            'pb': u'38',
                            'pg': u'19',
                            'subd': u'LANSING RIDGE SUBD PHASE TWO',
                            'subid': u'12'}}
        instance.set_items([MyRecord(item)])
        instance.pprint()
        instance.get_size()
        instance.get_records()
        instance.set_records(instance.get_records())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.record.MyRecord import MyRecord


class Test(unittest.TestCase):


    def test1(self):
        instance = MyRecord('hi')
        instance.__repr__()
        print(instance)
        instance.pprint()
        instance.get_item()
    def test2(self):
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
        instance = MyRecord(MyRecord(item))
        self.assertEqual(108250.0, instance.get_latest_market_value_total())
    def test3(self):
        item={'bcpao_acc': '2733237',
                  'latest_amount_due':'$50,000',
                  'bcpao_item': {'address': '2243  ROYAL POINCIANA BLVD , MELBOURNE 32935',
                                 'frame code': '03',
                                 'total base area': u'1,812',
                                 'use code': {'use_code': '110', 'use_code_str': None},
                                 'year built': '1995',
                                 'zip_code': '32935',
                                 'latest market value total': '$100,000'},
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
        instance = MyRecord(MyRecord(item))
        self.assertEqual(-50000.0, instance.owed_minus_ass())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
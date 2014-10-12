'''
Created on Jul 27, 2014

@author: Adrian
'''
import unittest
from jac.cfm import cfm

class Test(unittest.TestCase):


    def test1(self):
#         out_dir='hi'
        year='1950'
        court_type='hj'
        seq_number='56'
        cfid='99'
        cftoken='66'
        self.assertEqual('https://vweb1.brevardclerk.us/facts/d_caseno.cfm', cfm.get_url())
        expected_headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'CFID=99; CFTOKEN=66'}
        self.assertEqual(expected_headers, cfm.get_headers(cfid, cftoken))
        expected_data='CaseNumber1=05&CaseNumber2=1950&CaseNumber3=hj&CaseNumber4=56&CaseNumber5=&CaseNumber6=&submit=Submit'
        self.assertEqual(expected_data, cfm.get_data(year, court_type, seq_number))
#         cfm.cfm.case_info(out_dir, year, court_type, seq_number, cfid, cftoken)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()
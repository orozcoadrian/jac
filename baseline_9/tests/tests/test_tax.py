'''
Created on Nov 17, 2014

@author: Adrian
'''
import unittest
import requests
from bs4 import BeautifulSoup
import re
import jac.tax



class Test(unittest.TestCase):

    def test0(self):
        tax_id = '2002300'
        pay_all = jac.tax.get_pay_all_from_taxid(tax_id)
        print(pay_all)
#         soup = BeautifulSoup(r.text.encode('utf-8'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
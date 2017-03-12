'''
Created on Jul 27, 2014

@author: Adrian
'''
import sys,os
# sys.path.append(os.path.realpath(__file__)+"/../../../")
# print(str(sys.path))
import pprint
import re

# from jac import bcpao
from jac.cfm import cfm
# from jac import bclerk, bcpao, bcpao_radius

class MyRecord(object):
    '''
    classdocs
    '''

    def __init__(self, item):
        '''
        Constructor
        '''
        self.item=item
    def __str__(self):
        return 'MyRecord(%s)'%self.item
    def __repr__(self):
        return self.__str__()
    def pprint(self):
        pprint.pprint(self.item)
    def get_item(self):
        return self.item
    def get_latest_market_value_total(self):
        i=self.item.get_item()
        # print(i
        if 'bcpao_item' in i and 'latest market value total' in i['bcpao_item']:
            latest_market_value_total_str=i['bcpao_item']['latest market value total']
            # print('%r' % latest_market_value_total_str)
            latest_market_value_total_str_float=float(latest_market_value_total_str.replace('$','').replace(',',''))
            # print('%r' % latest_market_value_total_str_float)
            return latest_market_value_total_str_float
    def owed_minus_ass(self):
        i=self.item.get_item()
        if 'bcpao_item' in i and 'latest market value total' in i['bcpao_item'] and 'latest_amount_due' in i:
            latest_amount_due_str=i['latest_amount_due']
            latest_market_value_total_str=i['bcpao_item']['latest market value total']
            print('%r' % latest_amount_due_str)
            print('%r' % latest_market_value_total_str)
            latest_amount_due_float=float(latest_amount_due_str.replace('$','').replace(',',''))
            latest_market_value_total_str_float=float(latest_market_value_total_str.replace('$','').replace(',',''))
            print('%r' % latest_amount_due_float)
            print('%r' % latest_market_value_total_str_float)
            # if (latest_amount_due_float - latest_market_value_total_str_float) > 0:
            return latest_amount_due_float - latest_market_value_total_str_float
    def fetch_cfm(self, out_dir_htm):
        m = re.search('(.*)-(.*)-(.*)-(.*)-.*-.*', self.item['case_number'])
        print('MyRecord.fetch_cfm():'+str(self.item['case_number']))
        if m:
            # print(m.group(1)+','+m.group(2))
            # print(m.groups())
            year = m.group(2)
            court_type = m.group(3)
            seq_number = m.group(4)
            cfid = '1550556'
            cftoken = '74317641'
            values = cfm.do(out_dir_htm, year, court_type, seq_number, cfid, cftoken)
            if 'latest_amount_due' in values:
                self.item['latest_amount_due'] = values['latest_amount_due']
    def fetch_legal(self):
        legal=bclerk.get_legal_by_case(self.item['case_number'])
        self.item['legal'] = legal
    def fetch_bcpao(self):
        legal=self.item['legal']
        if 'subd' in legal:
            acc=bcpao.get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg']))
            # print(acc)
            self.item['bcpao_acc']=acc
            self.item['bcpao_item'] = bcpao.get_bcpaco_item(acc)
            self.item['bcpao_radius'] = bcpao_radius.get_average_from_radius(self.item['bcpao_acc'])
    def get_name_combos(self):
        i=self.item
        if 'name_combos' in i:
            return i['name_combos']
        m = re.search('V[S]? (.*)', i['case_title'])
        if m:
            # print(m.group(1))
            raw_full_name = m.group(1)
            i['raw_full_name'] = raw_full_name
            i['name_combos'] = []
            # print(raw_full_name)
            # os.system('c:/Python27/python.exe mech3.py "'+raw_full_name+'"')
            names = raw_full_name.split()
            # do_name_and_link(raw_full_name)
            # print('<html>')
            if len(names) == 2:
                i['name_combos'].append(names[1]+', '+names[0])
                # do_name_and_link(names[1]+', '+names[0])
            if len(names) == 3:
                i['name_combos'].append(names[2]+', '+names[0]+' '+names[1])
                i['name_combos'].append(names[2]+', '+names[0])
            return i['name_combos']

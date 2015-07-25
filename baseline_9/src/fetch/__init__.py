import re
from jac.cfm import cfm
from jac import bclerk, bcpao, bcpao_radius,tax
# import db
import pprint
import logging

class Fetcher(object):
    def get_name(self):
        return 'Fetcher'
class Cfm(Fetcher):
    def __init__(self, out_dir_htm):
        self.out_dir_htm=out_dir_htm
    def get_name(self):
        return 'Cfm'
    def fetch(self, mr):
        m = re.search('(.*)-(.*)-(.*)-(.*)-.*-.*', mr.item['case_number'])
        print('MyRecord.fetch_cfm():'+str(mr.item['case_number']))
        if m:
            # print(m.group(1)+','+m.group(2))
            # print(m.groups())
            year = m.group(2)
            court_type = m.group(3)
            seq_number = m.group(4)
            cfid = '1550556'
            cftoken = '74317641'
            values = cfm.do(self.out_dir_htm, year, court_type, seq_number, cfid, cftoken)
            if 'latest_amount_due' in values:
                mr.item['latest_amount_due'] = values['latest_amount_due']
            if 'orig_mtg_link' in values:
                mr.item['orig_mtg_link'] = values['orig_mtg_link']
#             mr.item['orig_mtg_link']=cfm.get_orig_mortgage_url_by_cn(mr.item['case_number'])

class Legal(Fetcher):
    def get_name(self):
        return 'Legal'
    def fetch(self, mr):
        legal=bclerk.get_legal_by_case(mr.item['case_number'])
        mr.item['legal'] = legal
        legals=bclerk.get_legals_by_case(mr.item['case_number'])
        mr.item['legals'] = legals
        # logging.debug('asdfasd 111 '+pprint.pformat(mr.item))

class Bcpao(Fetcher):
    def get_name(self):
        return 'Bcpao'

    def fetch(self, mr):
        bcpao.fill_bcpao_from_legal(mr)

class Bcpao_db(Fetcher):
    def get_name(self):
        return 'Bcpao_db'
    def fetch(self, mr):
        legal=mr.item['legal']
        if 'subd' in legal:
            db_item=db.fetch_item_by_parcel_id(legal['t'], legal['r'], legal['s'], legal['subid'],legal['blk'],legal['lt'])
            # print(acc)
            if db_item:
                mr.item['bcpao_db_acc']=db_item['TaxAcct']
                mr.item['bcpao_db_item'] = db_item
            #mr.item['bcpao_radius'] = bcpao_radius.get_average_from_radius(mr.item['bcpao_acc'])

class Taxes(Fetcher):
    def get_name(self):
        return 'Taxes'
    def fetch(self, mr):
        the_str = None
        value_to_use = None
        url_to_use = None
        if 'bcpao_acc' in mr.item and len(mr.item['bcpao_acc']) > 0:
            the_str = mr.item['bcpao_acc']
        if the_str is None:
            value_to_use = None#jac.xl3.Cell.from_display('')
        else:
            ###### move get pay all to a new fetcher
            display_str = tax.get_pay_all_from_taxid(the_str)
            if display_str:
                display_str = display_str.replace('$', '').replace(',', '')
                value_to_use = display_str
                url_to_use = tax.get_tax_url_from_taxid(the_str)

        mr.item['taxes_value'] = value_to_use
        mr.item['taxes_url'] = url_to_use
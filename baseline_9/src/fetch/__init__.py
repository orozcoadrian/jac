import re
from jac.cfm import cfm
from jac import bclerk, bcpao, bcpao_radius,db
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

class Bcpao(Fetcher):
    def get_name(self):
        return 'Bcpao'
    def fetch(self, mr):
        legal=mr.item['legal']
        if 'subd' in legal:
            acc=bcpao.get_acct_by_legal((legal['subd'],legal['lt'],legal['blk'],legal['pb'],legal['pg'], legal['s'], legal['t'], legal['r'], legal['subid']))
            # print(acc)
            mr.item['bcpao_acc']=acc
            mr.item['bcpao_item'] = bcpao.get_bcpaco_item(acc)
            #mr.item['bcpao_radius'] = bcpao_radius.get_average_from_radius(mr.item['bcpao_acc'])

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
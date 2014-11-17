'''
this module has logic related to creating spreadsheets
'''
import jac.xl3
import jac.record.MyRecord
import jac.bcpao
import re
import urllib
import jac.columns
from jac.cfm import cfm

class MainSheetBuilder(object):
    '''
    base class
    '''
    def __init__(self, sheet_name='all'):
        self.sheet_name = sheet_name
        self.args = None
        self.column_handlers = {}
        headers = []
        headers.append(jac.columns.ClassicMapColumnHandler('Classic Map'))
        headers.append(jac.columns.Avg250ColumnHandler('avg 250'))
        headers.append(jac.columns.Avg500ColumnHandler('avg 500'))
        headers.append(jac.columns.Avg750ColumnHandler('avg 750'))
        headers.append(jac.columns.Avg1000ColumnHandler('avg 1000'))
        for header in headers:
            self.column_handlers[header.get_col_header_display()] = header
    @staticmethod
    def get_name():
        '''
        gets the name of the builder
        '''
        return 'MainSheetBuilder'
    def set_args(self, args):
        self.args = args
    @staticmethod
    def get_bclerk_name_url(name):  # TODO: move this to xl3
        return 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2014&n=' + urllib.quote(name) + '&bt=OR&d=5%2F31%2F2014&pt=-1&cn=&dt=ALL%20DOCUMENT%20TYPES&st=fullname&ss=ALL%20DOCUMENT%20TYPES'
    @staticmethod
    def get_case_number_url(cn):
        return 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2015&n=&bt=OR&d=5%2F31%2F2014&pt=-1&cn='+cn+'&dt=ALL%20DOCUMENT%20TYPES&st=casenumber&ss=ALL%20DOCUMENT%20TYPES'
    def get_items_to_use(self, all_items):
        return all_items  # no filtering here
    def get_headers(self):
        headers = []
        headers.append(jac.xl3.Cell.from_display("high", width=3000))
        headers.append(jac.xl3.Cell.from_display("win", width=3000))
        headers.append(jac.xl3.Cell.from_link("case_number", 'http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html', width=5000))
        headers.append(jac.xl3.Cell.from_display("case_title", width=10000))
        headers.append(jac.xl3.Cell.from_display("fc._sale_date", width=3000))
        headers.append(jac.xl3.Cell.from_link("case_info", 'https://vweb1.brevardclerk.us/facts/caseno.cfm'))
        headers.append(jac.xl3.Cell.from_link("reg_actions", 'https://vweb1.brevardclerk.us/facts/caseno.cfm'))
        headers.append(jac.xl3.Cell.from_display("count"))
        headers.append(jac.xl3.Cell.from_display("address", width=10000))
        headers.append(jac.xl3.Cell.from_display("zip"))
        headers.append(jac.xl3.Cell.from_link("liens-name", 'http://web1.brevardclerk.us/oncoreweb/search.aspx', width=5000))
#         headers.append(jac.xl3.Cell.from_display("legal"))
#         headers.append(jac.xl3.Cell.from_display("Pb", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Pg", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Twp", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Rng", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Sec", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Sub", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Blk", width=1500))
#         headers.append(jac.xl3.Cell.from_display("Lot", width=1500))
        headers.append(jac.xl3.Cell.from_link("bcpao", 'https://www.bcpao.us/asp/real_search.asp'))
        headers.append(jac.xl3.Cell.from_display("f_code"))
        headers.append(jac.xl3.Cell.from_display("owed", width=4000))
        headers.append(jac.xl3.Cell.from_display("assessed"))
        headers.append(jac.xl3.Cell.from_display("base_area"))
        headers.append(jac.xl3.Cell.from_display("year built"))
        headers.append(jac.xl3.Cell.from_display("owed - ass"))
#         headers.append(jac.xl3.Cell.from_display("db-addr"))
#         headers.append(jac.xl3.Cell.from_display("db-taxid"))
#         headers.append(jac.xl3.Cell.from_display("db-area"))
#         headers.append(jac.xl3.Cell.from_display("db-year"))
#         headers.append(jac.xl3.Cell.from_display("db-ass"))
#         headers.append(jac.xl3.Cell.from_display("db-fcode"))
        headers.append(jac.xl3.Cell.from_display("orig_mtg"))
        return headers
    def get_display_case_number(self, case_number):
        return case_number.replace('XXXX-XX', '')
    def try_get(self, i, one, two):
        if one in i and two in i[one]:
            return i[one][two]
        return ''
    def add_to_row(self, row, r, row_index):
        i = r.get_item()
        for col_index, h in enumerate(self.get_headers()):
            str(col_index)
            if 'high' in h.get_display():
                row.append(jac.xl3.Cell.from_display(''))
            if 'win' in h.get_display():
                row.append(jac.xl3.Cell.from_display(''))
            if 'case_number' in h.get_display():
                row.append(jac.xl3.Cell.from_link(self.get_display_case_number(i['case_number']), self.get_case_number_url(i['case_number'])))
            if 'case_title' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['case_title']))
            if 'fc._sale_date' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['foreclosure_sale_date']))
            if 'count' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['count']))
            if 'address' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'address' in i['bcpao_item']:
                    the_str = i['bcpao_item']['address']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'zip' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                zip_str = self.try_get(i, 'bcpao_item', 'zip_code')
                if zip_str:
                    value_to_use = jac.xl3.Cell.from_display(int(zip_str))
                row.append(value_to_use)
            if 'owed' == h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if 'latest_amount_due' in i and i['latest_amount_due']:
                    a_str = i['latest_amount_due'].replace('$', '').replace(',', '')
                    if a_str:
                        try:
                            value_to_use = jac.xl3.Cell.from_display(float(a_str))
                        except:
                            value_to_use = jac.xl3.Cell.from_display(a_str)
                row.append(value_to_use)
            if 'case_info' in h.get_display():
                link_str = ''
                m = re.search('(.*)-(.*)-(.*)-(.*)-.*-.*', i['case_number'])  # todo: remove this duplication with record.fetch_cfm
                if m:
                    # print(m.group(1)+','+m.group(2))
                    # print(m.groups())
                    year = m.group(2)
                    court_type = m.group(3)
                    seq_number = m.group(4)
                    id2 = year + '_' + court_type + '_' + seq_number
                    link_str = self.get_sheet_name()+'/html_files/' + id2 + '_case_info.htm'
                # row_data.append(Formula('HYPERLINK("http://www.google.com";"Python")'))
                # row.append(self.get_formula_hyperlink(link_str, link_str))
                row.append(jac.xl3.Cell.from_link('link', link_str))
            if 'reg_actions' in h.get_display():
                link_str = ''
                m = re.search('(.*)-(.*)-(.*)-(.*)-.*-.*', i['case_number'])  # todo: remove this duplication with record.fetch_cfm
                if m:
                    # print(m.group(1)+','+m.group(2))
                    # print(m.groups())
                    year = m.group(2)
                    court_type = m.group(3)
                    seq_number = m.group(4)
                    id2 = year + '_' + court_type + '_' + seq_number
                    link_str = self.get_sheet_name()+'/html_files/' + id2 + '_reg_actions.htm'
                # row_data.append(Formula('HYPERLINK("http://www.google.com";"Python")'))
                # row.append(self.get_formula_hyperlink(link_str, link_str))
                row.append(jac.xl3.Cell.from_link('link', link_str))
            if 'liens-name' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if r.get_name_combos() is not None and len(r.get_name_combos()) > 0:
                    value_to_use = jac.xl3.Cell.from_link(r.get_name_combos()[0], self.get_bclerk_name_url(r.get_name_combos()[0]))
                row.append(value_to_use)
            if 'legal' in h.get_display():
                the_str = ''
                if 'legal' in i and 'legal_description' in i['legal']:
                    the_str = i['legal']['legal_description']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Pb' in h.get_display():
                the_str = ''
                if 'legal' in i and 'pb' in i['legal']:
                    the_str = i['legal']['pb']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Pg' in h.get_display():
                the_str = ''
                if 'legal' in i and 'pg' in i['legal']:
                    the_str = i['legal']['pg']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Twp' in h.get_display():
                the_str = ''
                if 'legal' in i and 't' in i['legal']:
                    the_str = i['legal']['t']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Rng' in h.get_display():
                the_str = ''
                if 'legal' in i and 'r' in i['legal']:
                    the_str = i['legal']['r']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Sec' in h.get_display():
                the_str = ''
                if 'legal' in i and 's' in i['legal']:
                    the_str = i['legal']['s']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Sub' in h.get_display():
                the_str = ''
                if 'legal' in i and 'subid' in i['legal']:
                    the_str = i['legal']['subid']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Lot' in h.get_display():
                the_str = ''
                if 'legal' in i and 'lt' in i['legal']:
                    the_str = i['legal']['lt']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'Blk' in h.get_display():
                the_str = ''
                if 'legal' in i and 'blk' in i['legal']:
                    the_str = i['legal']['blk']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'bcpao' in h.get_display():
                the_str = None
                if 'bcpao_acc' in i and len(i['bcpao_acc']) > 0:
                    the_str = i['bcpao_acc']
                if the_str is None:
                    row.append(jac.xl3.Cell.from_display(''))
                else:
                    row.append(jac.xl3.Cell.from_link(the_str, jac.bcpao.get_bcpao_query_url_by_acct(the_str)))
            if 'f_code' in h.get_display():
                fc_str = ''
                if 'bcpao_item' in i and 'frame code' in i['bcpao_item']:
                    fc_str = i['bcpao_item']['frame code']
                row.append(jac.xl3.Cell.from_display(fc_str))
            if 'assessed' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                a_str = self.try_get(i, 'bcpao_item', 'latest market value total').replace('$', '').replace(',', '')
                if a_str:
                    try:
                        value_to_use = jac.xl3.Cell.from_display(float(a_str))
                    except:
                        value_to_use = jac.xl3.Cell.from_display(a_str)
                row.append(value_to_use)
            if 'base_area' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'total base area' in i['bcpao_item']:
                    the_str = float(i['bcpao_item']['total base area'].replace(',', ''))
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'year built' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'year built' in i['bcpao_item']:
                    try:
                        the_str = int(i['bcpao_item']['year built'])
                    except:
                        print("error parsing i['bcpao_item']['year built']='"+i['bcpao_item']['year built']+"' as an int")
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'owed - ass' in h.get_display():
                row_str = str(row_index + 2)
                owed_column = 'N' # latest_amount_due
                ass_column = 'O' # latest market value total
                f_str = 'IF(AND(NOT(ISBLANK('+owed_column + row_str + ')),NOT(ISBLANK('+ass_column + row_str + '))),'+owed_column + row_str + '-'+ass_column + row_str + ',"")'
                row.append(jac.xl3.Cell.from_formula(f_str))
            if 'db-addr' == h.get_display():
                the_str = ''
                if 'bcpao_db_item' in i and 'address' in i['bcpao_db_item']:
                    try:
                        the_str = str(i['bcpao_db_item']['address'])
                    except:
                        raise
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'db-taxid' == h.get_display():
                the_int = None
                if 'bcpao_db_item' in i and 'TaxAcct' in i['bcpao_db_item']:
                    the_int = i['bcpao_db_item']['TaxAcct']
                if the_int is None:
                    row.append(jac.xl3.Cell.from_display(''))
                else:
                    row.append(jac.xl3.Cell.from_link(str(the_int), jac.bcpao.get_bcpao_query_url_by_acct(str(the_int))))
            if 'db-area' == h.get_display():
                the_str = ''
                if 'bcpao_db_item' in i and 'BaseArea' in i['bcpao_db_item']:
                    try:
                        the_str = int(i['bcpao_db_item']['BaseArea'])
                    except:
                        raise
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'db-year' == h.get_display():
                the_str = ''
                if 'bcpao_db_item' in i and 'YearBuilt' in i['bcpao_db_item']:
                    try:
                        the_str = int(i['bcpao_db_item']['YearBuilt'])
                    except:
                        raise
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'db-ass' == h.get_display():
                the_str = ''
                if 'bcpao_db_item' in i and 'MarketValueCurr' in i['bcpao_db_item']:
                    try:
                        the_str = float(i['bcpao_db_item']['MarketValueCurr'])
                    except:
                        raise
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'db-fcode' == h.get_display():
                the_str = ''
                if 'bcpao_db_item' in i and 'FrameCode' in i['bcpao_db_item']:
                    try:
                        the_str = str(i['bcpao_db_item']['FrameCode'])
                    except:
                        raise
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'orig_mtg' == h.get_display():
                the_str = None
                if 'orig_mtg_link' in i:
                    if i['orig_mtg_link'] and len(i['orig_mtg_link']) > 0:
                        row.append(jac.xl3.Cell.from_link('link', i['orig_mtg_link']))
                    else:
                        row.append(jac.xl3.Cell.from_display(''))
    def get_sheet_name(self):
        return self.sheet_name
    def add_sheet(self, items):
        rows = []
        # row=[]


        # row.append(jac.xl3.Cell.from_display('oneb'))
        # row.extend()
        headers = self.get_headers()
        rows.append(headers)


        for index, i in enumerate(self.get_items_to_use(items)):
            row = []
            self.add_to_row(row, i, index)
            rows.append(row)

        ret = jac.xl3.DataSet(self.get_sheet_name(), rows)
        return ret

class LuxurySheetBuilder(MainSheetBuilder):
    def get_name(self):
        return 'LuxurySheetBuilder'
    def get_headers(self):
        headers = []
        headers.extend(super(LuxurySheetBuilder, self).get_headers())
        del headers[0:2]
        return headers
    def get_items_to_use(self, all_items):
        ret = []
        for i in all_items:
            r = jac.record.MyRecord.MyRecord(i)
            if r.get_latest_market_value_total() > 150000:
                ret.append(i)
        # pprint.pprint(ret)
        return ret

    def get_sheet_name(self):
        return 'luxury'


class DiffSheetBuilder(MainSheetBuilder):
    def get_name(self):
        return 'DiffSheetBuilder'
    def get_items_to_use(self, all_items):
        ret = []
        for i in all_items:
            r = jac.record.MyRecord.MyRecord(i)
            if r.owed_minus_ass() is not None:
                ret.append(i)
        # pprint.pprint(ret)
        return ret

    def get_headers(self):
        headers = []
        headers.extend(super(DiffSheetBuilder, self).get_headers())
        del headers[0:2]
        headers.append(jac.xl3.Cell.from_display("owed - ass"))
        return headers

    def get_sheet_name(self):
        return 'diff'

    def add_to_row(self, row, i, row_index):
        super(DiffSheetBuilder, self).add_to_row(row, i, row_index)
        for h in self.get_headers():
            if 'owed - ass' in h.get_display():
                r = jac.record.MyRecord.MyRecord(i)
                row.append(jac.xl3.Cell.from_display(r.owed_minus_ass()))

class ZipsSheetBuilder(MainSheetBuilder):
    def get_name(self):
        return 'ZipsSheetBuilder'
    def get_sheet_name(self):
        return 'zip codes'
    def get_headers(self):
        headers = []
        headers.extend(super(ZipsSheetBuilder, self).get_headers())
        del headers[0:2]
        return headers
    def get_items_to_use(self, all_items):
        ret = []
        # pprint.pprint(self.args.zip_code)
        for i in all_items:
            # r=record.MyRecord(i)
            if self.args.zip_code:
                # if i.get_item()['bcpao_item']['zip_code'] in self.args.zip_code:
                it = i.get_item()
                if 'bcpao_item' in it and 'zip_code' in it['bcpao_item'] and it['bcpao_item']['zip_code'] in self.args.zip_code:
                # if i.get_item()['bcpao_item']['zip_code'] in self.args.zip_code:
                    ret.append(i)
        # pprint.pprint(ret)
        return ret

def is_cheap(item):
    lad_str = item['latest_amount_due']
    m = re.search('([\d,.]*)', lad_str)
    if m:
        dollar_string = m.group(1)
        due_float = float(dollar_string.replace(',', ''))
        return due_float < 150000.00
    return False
class CheapSheetBuilder(MainSheetBuilder):
    def get_name(self):
        return 'CheapSheetBuilder'
    def get_sheet_name(self):
        return 'cheap'
    def get_items_to_use(self, all_items):
        ret = []
        for i in all_items:
            # r=record.MyRecord(i)
            try:
                if is_cheap(i.get_item()):
                    ret.append(i)
            except Exception as e:
                print('ignoring exception(asodkfj09823)' + str(e))
        # pprint.pprint(ret)
        return ret

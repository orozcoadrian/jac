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
    def get_items_to_use(self, all_items):
        return all_items  # no filtering here
    def get_headers(self):
        headers = []
        headers.append(jac.xl3.Cell.from_display("high", width=3000))
        headers.append(jac.xl3.Cell.from_display("win", width=3000))
        headers.append(jac.xl3.Cell.from_link("case_number", 'http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html', width=5000))
        headers.append(jac.xl3.Cell.from_display("case_title", width=10000))
        headers.append(jac.xl3.Cell.from_display("foreclosure_sale_date", width=3000))
        headers.append(jac.xl3.Cell.from_link("case_info", 'https://vweb1.brevardclerk.us/facts/caseno.cfm'))
        headers.append(jac.xl3.Cell.from_link("reg_actions", 'https://vweb1.brevardclerk.us/facts/caseno.cfm'))
        headers.append(jac.xl3.Cell.from_display("count"))
        headers.append(jac.xl3.Cell.from_display("address", width=10000))
        headers.append(jac.xl3.Cell.from_display("zip"))
        headers.append(jac.xl3.Cell.from_display("latest_amount_due", width=4000))
        headers.append(jac.xl3.Cell.from_link("liens-case", 'http://web1.brevardclerk.us/oncoreweb/search.aspx', width=5000))
        headers.append(jac.xl3.Cell.from_link("liens-name", 'http://web1.brevardclerk.us/oncoreweb/search.aspx', width=5000))
        headers.append(jac.xl3.Cell.from_link("bcpao", 'https://www.bcpao.us/asp/real_search.asp'))
        headers.append(jac.xl3.Cell.from_display("frame code"))
        headers.append(jac.xl3.Cell.from_display("latest market value total"))
        headers.append(jac.xl3.Cell.from_display("total base area"))
        headers.append(jac.xl3.Cell.from_display("year built"))
        headers.append(jac.xl3.Cell.from_display("owed - ass"))
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
                row.append(jac.xl3.Cell.from_display(self.get_display_case_number(i['case_number'])))
            if 'case_title' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['case_title']))
            if 'foreclosure_sale_date' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['foreclosure_sale_date']))
            if 'count' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['count']))
            if 'address' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'address' in i['bcpao_item']:
                    the_str = i['bcpao_item']['address']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'zip' in h.get_display():
                row.append(jac.xl3.Cell.from_display(self.try_get(i, 'bcpao_item', 'zip_code')))
            if 'latest_amount_due' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if 'latest_amount_due' in i:
                    value_to_use = jac.xl3.Cell.from_display(i['latest_amount_due'])
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
            if 'liens-case' in h.get_display():
                row.append(jac.xl3.Cell.from_link(self.get_display_case_number(i['case_number']), cfm.get_case_number_url(i['case_number'])))
            if 'liens-name' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if r.get_name_combos() is not None and len(r.get_name_combos()) > 0:
                    value_to_use = jac.xl3.Cell.from_link(r.get_name_combos()[0], self.get_bclerk_name_url(r.get_name_combos()[0]))
                row.append(value_to_use)
            if 'bcpao' in h.get_display():
                bcpao_acc_str = None
                if 'bcpao_acc' in i and len(i['bcpao_acc']) > 0:
                    bcpao_acc_str = i['bcpao_acc']
                if bcpao_acc_str is None:
                    row.append(jac.xl3.Cell.from_display(''))
                else:
                    row.append(jac.xl3.Cell.from_link(bcpao_acc_str, jac.bcpao.get_bcpao_query_url_by_acct(bcpao_acc_str)))
            if 'frame code' in h.get_display():
                fc_str = ''
                if 'bcpao_item' in i and 'frame code' in i['bcpao_item']:
                    fc_str = i['bcpao_item']['frame code']
                row.append(jac.xl3.Cell.from_display(fc_str))
            if 'latest market value total' in h.get_display():
                row.append(jac.xl3.Cell.from_display(self.try_get(i, 'bcpao_item', 'latest market value total')))
            if 'total base area' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'total base area' in i['bcpao_item']:
                    the_str = i['bcpao_item']['total base area']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'year built' in h.get_display():
                the_str = ''
                if 'bcpao_item' in i and 'year built' in i['bcpao_item']:
                    the_str = i['bcpao_item']['year built']
                row.append(jac.xl3.Cell.from_display(the_str))
            if 'owed - ass' in h.get_display():
                row_str = str(row_index + 2)
                owed_column = 'K' # latest_amount_due
                ass_column = 'P' # latest market value total
                f_str = 'IF(AND(NOT(ISBLANK('+owed_column + row_str + ')),NOT(ISBLANK('+ass_column + row_str + '))),'+owed_column + row_str + '-'+ass_column + row_str + ',"")'
                row.append(jac.xl3.Cell.from_formula(f_str))
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
class RadiusSheetBuilder(MainSheetBuilder):
    def get_name(self):
        return 'RadiusSheetBuilder'
    def get_sheet_name(self):
        return 'radius'
    def get_headers(self):
        headers = []
        headers.extend(super(RadiusSheetBuilder, self).get_headers())
        del headers[0:2]
        # headers.append(jac.xl3.Cell.from_display("Classic Map"))
        self.column_handlers['Classic Map'].handle_add(headers)
        self.column_handlers['avg 250'].handle_add(headers)
        self.column_handlers['avg 500'].handle_add(headers)
        self.column_handlers['avg 750'].handle_add(headers)
        self.column_handlers['avg 1000'].handle_add(headers)
        return headers
    def add_to_row(self, row, i, row_index):
        super(RadiusSheetBuilder, self).add_to_row(row, i, row_index)
        self.column_handlers['Classic Map'].handle_add_to_row(row, i)
        self.column_handlers['avg 250'].handle_add_to_row(row, i)
        self.column_handlers['avg 500'].handle_add_to_row(row, i)
        self.column_handlers['avg 750'].handle_add_to_row(row, i)
        self.column_handlers['avg 1000'].handle_add_to_row(row, i)
import sys
from mechanize import ParseResponse, urlopen
import requests
import json
from bs4 import BeautifulSoup
import pprint
import jac.columns
import urllib
import re
from xlwt import Workbook
import os
import jac.bcpao

# uri = 'https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE=10/23/2014'
uri = 'https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=C&PageDir=0'


def main():
    r = requests.get(uri)
    print(r.status_code)
    print(r.text)

def do_tax_sheet(date_str):
    maps=[]

    do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE='+date_str, False, maps)
    first = True
    currentPageDir = 0
    while True:
        ret = do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=W&PageDir='+str(currentPageDir), True, maps)
        if first:
            currentPageDir = 1
            first = False
        if not ret:
            break
    print('+'*100)
    print(str(len(maps))+' records')

    sheetBuilder = TaxSheetBuilder(date_str, date_str.replace('/2014', '').replace('/', '_'))
    #sheetBuilder.set_args(args)
    dataset = sheetBuilder.add_sheet(maps)
    return dataset

def do_tax(date_strs):

    datasets = []
    for date_str in date_strs:
        datasets.append(do_tax_sheet(date_str))

    book = Workbook()
    for dataset in datasets:
        jac.xl3.add_data_set_sheet(dataset, book)
    date0 = date_strs[0].replace('/2014', '').replace('/', '_')
    date1 = date_strs[1].replace('/2014', '').replace('/', '_')
    abc = '-'.join([date0, date1])
    out_file = 'tax_deeds_' + abc+'.xls'
    book.save(out_file)
    print(out_file)
    return out_file

def main3():

    out_file = do_tax(['10/23/2014', '10/24/2014'])

    if True:
        os.system('start "" "C:/Program Files/Microsoft Office/Office12/Excel.exe" /e '+out_file)
    #pprint.pprint(maps)

def main2():
    print('hi')

#     do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE=10/23/2014', False)
#     #do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=C&PageDir=0', True)
#     do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=W&PageDir=0', True)
#     do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=W&PageDir=1', True)
#     do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=W&PageDir=1', True)
#     do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=W&PageDir=1', True)
    #do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=N&PageDir=0', True)
    #do('https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=UPDATE&FNC=LOAD&AREA=R&PageDir=0', True)

#     s1='https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&ZMETHOD=UPDATE&FNC=UPDATE&ref=806287,806289,806290,806292,806294,806297,806298,806300,806301,806302,806288,806291,806293,806295,806296,806299,806304,806305,806306,806307,&tx=1413861110975&_=1413861110976'
#     s2='https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&ZMETHOD=UPDATE&FNC=UPDATE&ref=806287'
#     response = urlopen(s2)
#     myr = response.read()
#     #print(response.read())
#     data = json.loads(myr)
#     pprint.pprint(data)

    print('DONE')

def do(uri2, do_print, maps):

    #print((('*1'*100)+'\n')*5)
    print(uri2)
    print('-'*100)
    response = urlopen(uri2)
    if do_print:
        myr = response.read()
        #print(myr)
        #print(myr[0])
        data = json.loads(myr)
        html = data['retHTML']
        #print(html)
        rH=html.replace('@D', '<div>')
        #print(rH)
        rH = rH.replace('@A','<div class="')
        rH = rH.replace('@B','</div>')
        rH = rH.replace('@C','class="')
        rH = rH.replace('@D','<div>')
        rH = rH.replace('@E','AUCTION')
        rH = rH.replace('@F','</td><td')
        rH = rH.replace('@G','</td></tr>')
        rH = rH.replace('@H','<tr><td ')
        rH = rH.replace('@I','table')
        rH = rH.replace('@J','p_back="NextCheck=')
        rH = rH.replace('@K','style="Display:none"')
        rH = rH.replace('@L','/index.cfm?zaction=auction&zmethod=details&AID=')
        #print(rH)
        soup = BeautifulSoup(rH)
        #print(soup.get_text())

        ts=soup.find_all("table")
        new_maps=[]
        for t in ts:
            rows = t.find_all("tr")

            amap={}
            for row in rows:
                cells = row.find_all("td")
                #print(row.contents)
                key=cells[0].get_text().replace(':','')
                if not key:
                    key = '_Property Address_2'
                amap[key] = cells[1].get_text()
                #print(cells[0].get_text() + '  ' + cells[1].get_text())

            new_maps.append(amap)

        print(str(len(maps))+' records')

        maps.extend(new_maps)
        pprint.pprint(maps[-1])
        if len(new_maps) == 10:
            return True
        else:
            return False
    return False

#         stats = soup.find_all('div', class_='AUCTION_STATS')
#         print(stats)
        #for stat in stats:
        #    print(stat.find('div', class_='ASTAT_MSGA ASTAT_LBL').get_text())
        #    print(stat.find('div', class_='ASTAT_MSGB Astat_DATA').get_text())


    #forms = ParseResponse(response)
    #print(forms)

    #print((('*2'*100)+'\n')*5)
    #r = requests.get(uri2)
    #print(r.status_code)
    #print(r.text)
#     form = forms[0]
#     print form


class TaxSheetBuilder(object):
    '''
    base class
    '''
    def __init__(self, date_str, sheet_name='all'):
        self.sheet_name = sheet_name
        self.args = None
        self.date_str = date_str
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
        headers.append(jac.xl3.Cell.from_display("Auction Type", width=3000))
        headers.append(jac.xl3.Cell.from_display("Case #", width=3000))
        headers.append(jac.xl3.Cell.from_display("Certificate #", width=4000))
        headers.append(jac.xl3.Cell.from_display("Opening Bid", width=4000))
        headers.append(jac.xl3.Cell.from_link("Parcel ID", 'https://www.brevard.realforeclose.com/index.cfm?zaction=AUCTION&Zmethod=PREVIEW&AUCTIONDATE='+self.date_str, width=3000))
        headers.append(jac.xl3.Cell.from_display("Property Address", width=10000))
        headers.append(jac.xl3.Cell.from_display("_zip"))
        headers.append(jac.xl3.Cell.from_display("Assessed Value", width=4000))
        return headers
    def get_display_case_number(self, case_number):
        return case_number.replace('XXXX-XX', '')
    def try_get(self, i, one, two):
        if one in i and two in i[one]:
            return i[one][two]
        return ''
    def add_to_row(self, row, r, row_index):
        #i = r.get_item()
        i=r
        for col_index, h in enumerate(self.get_headers()):
            str(col_index)
            if 'Auction Type' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['Auction Type']))
            if 'Case #' in h.get_display():
                row.append(jac.xl3.Cell.from_display(int(i['Case #'])))
            if 'Certificate #' in h.get_display():
                row.append(jac.xl3.Cell.from_display(int(i['Certificate #'])))
            if 'case_title' in h.get_display():
                row.append(jac.xl3.Cell.from_display(i['Property Address']))
            if 'Opening Bid' in h.get_display():
                row.append(jac.xl3.Cell.from_display(float(i['Opening Bid'].replace('$', '').replace(',', ''))))
            if 'Assessed Value' in h.get_display():
                row.append(jac.xl3.Cell.from_display(float(i['Assessed Value'].replace('$', '').replace(',', ''))))
            if 'Parcel ID' in h.get_display():
#                 row.append(jac.xl3.Cell.from_display(int(i['Parcel ID'])))
                row.append(jac.xl3.Cell.from_link(i['Parcel ID'], jac.bcpao.get_bcpao_query_url_by_acct(i['Parcel ID'])))
            if 'Property Address' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if 'Property Address' in i:
                    value_to_use = jac.xl3.Cell.from_display(i['Property Address'] + " " + i['_Property Address_2'])
                row.append(value_to_use)
            if '_zip' in h.get_display():
                value_to_use = jac.xl3.Cell.from_display('')
                if 'Property Address' in i:
                    value_to_use = jac.xl3.Cell.from_display(int(i['_Property Address_2'].split(',')[1]))
                row.append(value_to_use)

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


def get_pay_all_from_tax_text(r_text):
    ret = None
#     lines = r_text.split('\n')
#     for l in lines:
    # print(l)
    # if 'AMOUNT DUE' in l:
#     print(l)
    # m = re.search('<font color="Blue">(.* VS .*)<', l)
    # if m:
    # print(indent+m.group(1))
    m = re.search('.*Pay All: \$([\d,.]*).*', r_text)
    if m:
    # print(m.groups())
        ret = m.group(1)
        # print(l)
        # if '<font color="Blue">' in l:
        # print(l)
    return ret

def get_tax_url_from_taxid(tax_id):
        url = 'https://brevard.county-taxes.com/public/real_estate/parcels/' + tax_id
        return url


def get_tax_text_from_taxid(tax_id):
    url = get_tax_url_from_taxid(tax_id)
#         cfid = '1550556'
#         cftoken = '74317641'
    headers = '' #get_headers(cfid, cftoken)
    data = '' #get_data(year, court_type, seq_number)
    #     r = requests.post(url, data, headers=headers, stream=True)
    r = requests.post(url, data, headers=headers, stream=True)
    return r

def get_pay_all_from_taxid(tax_id):
    ret = '0'
    r = get_tax_text_from_taxid(tax_id)
#         print(r.text)
    pay_all = get_pay_all_from_tax_text(r.text)
    if pay_all:
        ret = pay_all
    return ret

if __name__ == '__main__':
    sys.exit(main3())
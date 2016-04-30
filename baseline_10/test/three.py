# http://askubuntu.com/questions/116020/python-https-requests-urllib2-to-some-sites-fail-on-ubuntu-12-04-without-proxy
import ssl

ssl.PROTOCOL_SSLv23 = ssl.PROTOCOL_TLSv1

import logging
import re
import unittest

import itertools
import urllib

import requests
from bs4 import BeautifulSoup
from mechanize import ParseResponse, urlopen

from HTMLParser import HTMLParser

from jac.record.MyRecord import MyRecord


class ForeclosuresList(object):
    def get_first(self):
        r = requests.get('http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html')
        return self.get_rows(r.content)[0]

    def get_rows(self, the_html):
        rows = []
        soup = BeautifulSoup(the_html)
        # print(soup.prettify())
        trs = soup.find_all("tr")
        for tr in trs:
            # print(tr)
            current_row = {}
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            # print(tds)
            current_row['case_number'] = tds[0].string
            current_row['case_title'] = tds[1].string
            current_row['comment'] = tds[2].string.replace(u'\xa0', u'').encode('utf-8')
            current_row['foreclosure_sale_date'] = tds[3].string
            current_row['count'] = len(rows) + 1
            rows.append(ForeclusreListItem(current_row))
        # pprint.pprint(rows)
        return rows

class ForeclusreListItem(object):
    def __init__(self, row):
        self._row = row
    def get(self, id):
        return self._row[id]

class BrevardClerk(object):
    def get_legal_description(self, case):
        print('get_legal_description("' + case + '")')
        ret = {}

        #     soup = get_bclerk_results_soup(case)
        #     print soup.renderContents()


        # bi_cell = soup.find(text="                                                                                                LT 22 BLK 10 PB 5 PG 20 EAU GALLIE SHORES S 35 T 26 R 37 SUBID 02")
        #     bi_cell = soup.findAll(text=re.compile('.* S \d+ T [0-9a-zA-Z]+ R \d+ .*'))#"td", { "class" : "stdFontResults" })
        rows = self.get_records_grid_for_case_number(case)
        lds = []
        for row in rows:
            if row['First Legal'] and len(row['First Legal']) > 0:
                lds.append(row['First Legal'])
        ret['legal_description'] = '; '.join(lds).strip()
        #     print('ret[legal_description]: ' + ret['legal_description'])
        if len(lds) > 0:
            ret['oncoreweb_by_legal_url'] = self.oncoreweb_by_legal(lds[0])
            print(ret['oncoreweb_by_legal_url'])
        for i, ld in enumerate(lds):
            # print(b.strip())
            legal_desc = ld.strip()
            temp = self.get_legal_from_str(legal_desc)
            if temp:
                ret = dict(itertools.chain(ret.items(), temp.items()))
                if i < (len(lds) - 1):
                    the_str = 'choosing a legal description (index='
                    the_str += str(i)
                    the_str += ':' + legal_desc
                    the_str += ') before going through all of them(total='
                    the_str += str(len(lds))
                    the_str += '): '
                    # logging.info(the_str)
                    # pprint.pprint(lds)
                break
                #     print(ret)
        return LegalDescription(ret)

    def oncoreweb_by_legal(self, leg_desc_in):
        ret = ''
        l = self.get_legal_from_str(leg_desc_in)
        try:
            # lot = l['lt']  # ''7'
            # lot_s=urllib.quote('Lot,'+lot+'|Block'+',H'+'|Land_Lot'+','+l['pb'],'|District')
            theblk = ''
            thelt = ''
            thepb = ''
            thepg = ''
            if 'blk' in l and l['blk']:
                theblk = '|Block' + ',' + l['blk']
            if 'lt' in l and l['lt']:
                thelt = l['lt']
            if 'pb' in l and l['pb']:
                thepb = l['pb']
            if 'pg' in l and l['pg']:
                thepg = l['pg']
            lot_s = urllib.quote('Lot,' + thelt + theblk + '|Land_Lot' + ',' + thepb
                                 + '|District' + ',' + thepg + '|PropSection' + ',' + l['s'] + '|Building' + ',' + l[
                                     't'] + '|Range' + ',' + l['r']
                                 + '|Phase' + ',' + l['subid'])
            # 2c ,
            # 7c |
            mys = 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=01%2F01%2F1981&ed=4%2F19%2F2016&bt=OR&d=4%2F19%2F2016&pt=-1&lf='
            mys += lot_s
            # mys += '&cn=05-2015-CA-026652-XXXX-XX&dt=ALL%20DOCUMENT%20TYPES&st=legal&ld='
            mys += '&cn=&dt=&st=legal&ld='
            mys2 = 'Lot ' + thelt + ' Block ' + theblk + ' Plat' + ' ' + 'BK' + ' ' + thepb + ' ' + 'Plat' + ' ' + 'Pg' + ' ' + thepg \
                   + ' ' + 'Section' + ' ' + l['s'] + ' ' + 'Township' + ' ' + l['t'] + ' ' + 'Range' + ' ' + l[
                       'r'] + ' ' + 'SUBID' + ' ' + l['subid'] + ' '
            mys2 = urllib.quote(mys2)
            # mys += mys2
            ret = mys
        except Exception as e:
            print(' ** error in oncoreweb_by_legal ' + str(e))

        return ret

    def get_records_grid_for_case_number(self, case_number):
        soup = self.get_bclerk_results_soup(case_number)  # ('05-2014-CA-024535-XXXX-XX')
        #         print(soup)
        #         results_node = soup.find('table', id='dgResults')
        #         print('1')
        #         print(soup.table)
        #         print('12')
        adr = soup.find('table', id='dgResults')
        #     print adr
        #     print '1' * 50
        #         print(adr.parent)
        # bs4.BeautifulSoup uses findAll() whereas BeautifulSoup.BeautifulSoup uses find_all(). bs4 is newer
        items = []
        col_names = []
        trs = adr.findAll("tr")
        for r, a in enumerate(trs):
            if r != 0 and r != len(trs) - 1:
                #             print 'r' + str(r) + '===' + str(a).replace("\n", "").replace("\r", "").replace("\t", "")
                current_item = {}
                for c, d in enumerate(a.findAll("td")):
                    #                 print ' c' + str(c) + '===' + str(d).replace("\n", "").replace("\r", "").replace("\t", "")
                    key = None
                    if r == 1:
                        col_names.append(d.get_text(strip=True))
                    else:
                        current_item[col_names[c]] = d.get_text(strip=True)
                if r > 1:
                    items.append(current_item)

        return items

    def get_legal_from_str(self, the_str):
        legal_desc = the_str.replace(u'\xc2', u'')
        logging.info('get_legal_from_str(' + legal_desc + ')')
        ret = {}

        m = re.search(
            '(LT (?P<lt>[0-9a-zA-Z]+) )?(BLK (?P<blk>[0-9a-zA-Z]+) )?(PB (?P<pb>\d+) PG (?P<pg>\d+))?(?P<subd>.*) S (?P<s>\d+) T (?P<t>\d+G?) R (?P<r>\d+)( SUBID (?P<subid>[0-9a-zA-Z]+))?',
            the_str)
        if m:
            # pprint.pprint(m)
            # pprint.pprint(m.groups())
            # print(m.group('blk'))
            # return m.groupdict()
            ret = dict(itertools.chain(ret.items(), m.groupdict().items()))

            # print(m.group(1)+','+m.group(2)+','+m.group(3))
            # ret['lt']=m.group(1)
            # ret['blk']=m.group(2)
            # ret['subd']=m.group(3)
            # ret['subid']=m.group(4)
        elif 'condo'.upper() in the_str.upper():
            ret['condo'] = True
            #     print('ret='+str(ret))
        ret['legal_desc'] = legal_desc
        return ret

    def get_bclerk_results_soup(self, case):
        bclerk_results_text = self.get_bclerk_results_text(case)
        soup = BeautifulSoup(bclerk_results_text, "lxml")
        return soup

    def get_bclerk_results_text(self, case):
        uri = 'http://web1.brevardclerk.us/oncoreweb/search.aspx'
        response = urllib.urlopen(uri)
        forms = ParseResponse(response, backwards_compat=False)
        form = forms[0]
        #     print form
        form["txtCaseNumber"] = case  # "orozco"
        form["SearchType"] = 'casenumber'  # "orozco"
        form["txtDocTypes"] = ''  # 'JRP, J' #"orozco"
        # form["txtName"] = "orozco"
        #     time.sleep(1)
        bclerk_results_text = urlopen(form.click()).read()
        return bclerk_results_text

class LegalDescription(object):
    def __init__(self, bc_dict):
        self._bc_dict = bc_dict

    def get_leg_desc_string(self):
        return self._bc_dict['legal_desc']

    def get_bc_dict(self):
        return self._bc_dict

class Bcpao(object):
    def get_bcpao_info(self, legal_description):
        item={}
        mr = MyRecord(item)
        mr.get_item()['legal']=legal_description.get_bc_dict()
        mr.get_item()['legals']=[mr.get_item()['legal']]
        self.fill_bcpao_from_legal(mr)
        return BcpaoItem(mr)

    def fill_bcpao_from_legal(self, mr):
        legal = mr.item['legal']
        if 'subd' in legal:
            acc = self.get_acct_by_legal((legal['subd'], legal['lt'], legal['blk'], legal['pb'], legal['pg'], legal['s'],
                                     legal['t'], legal['r'], legal['subid']))
            # logging.debug('a: ' + (str(acc) if acc else 'None'))
            mr.item['bcpao_acc'] = acc
            mr.item['bcpao_item'] = self.get_bcpaco_item(acc)
        # mr.item['bcpao_radius'] = bcpao_radius.get_average_from_radius(mr.item['bcpao_acc'])
        # logging.debug('asdfasd 1.5 ' + pprint.pformat(mr.item))
        legals = mr.item['legals']
        # logging.debug('legals: ' + pprint.pformat(legals))
        # logging.debug('** * * ****   4563456')
        mr.item['bcpao_accs'] = []
        for i, l in enumerate(legals):
            # logging.debug(pprint.pformat(l))
            acc = None
            if 't' in l:
                acc = self.get_acct_by_legal(
                    (l['subd'], l['lt'], l['blk'], l['pb'], l['pg'], l['s'], l['t'], l['r'], l['subid']))
                mr.item['bcpao_accs'].append(acc)
                if 'bcpao_acc' not in mr.item:
                    mr.item['bcpao_acc'] = acc
                    mr.item['bcpao_item'] = self.get_bcpaco_item(acc)
                    # logging.debug('choosing a secondary legal description because it gave a bcpao_acc')
                    # logging.debug(str(i) + ': ' + ('None' if not acc else str(acc)))

                    # logging.debug('asdfasd 222 ' + pprint.pformat(mr.item))

    def get_acct_by_legal(self, legal):
        use_local_logging_config = False
        if use_local_logging_config:
            logging.basicConfig(format='%(asctime)s %(module)-15s %(levelname)s %(message)s', level=logging.DEBUG)
            #     logging.getLogger().setLevel(logging.DEBUG)
            logger = logging.getLogger(__name__)
            logger.info('START')
        sub, lot, block, pb, pg, s, t, r, subid = legal
        sub = sub.replace(u'\xc2', u'').encode('utf-8')
        logging.info('get_acct_by_legal(sub="' + sub + '", lot=' + str(lot) + ', block=' + str(block) + ', pb=' + str(
            pb) + ', pg=' + str(pg) + ', s=' + str(s) + ', t=' + str(t) + ', r=' + str(r) + ', subid=' + str(
            subid) + ')')
        ret = ''

        # url = 'https://legacy.bcpao.us/asp/find_property.asp'
        url = 'https://legacy.bcpao.us/asp/find_property.asp'
        headers = {
            # 'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
            'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if not ret:
            data = None
            offset = 82
            #         if pb is not None and pg is not None and lot is not None and block is not None:
            #             data='SearchBy=Plat&book='+str(pb)+'&page='+str(pg)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
            #             offset=86
            if sub is not None and pg is not None and lot is not None and block is not None:
                data = 'SearchBy=Sub&sub=' + urllib.quote(sub) + '&blk=' + str(block) + '&lot=' + str(
                    lot) + '&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
                #         elif pb is not None and pg is not None and lot is not None:
                #             data='SearchBy=Plat&book='+str(pb)+'&page='+str(pg)+'&blk=&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
                #             offset=86
                #         elif t and r and s and subid and lot:
                #             data='SearchBy=Sub&sub='+urllib.quote(sub)+'&blk=&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'

            elif pg is not None:
                data = 'SearchBy=Sub&sub=' + urllib.quote(sub) + '&pg=' + str(pg) + '&lot=' + str(
                    lot) + '&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
            # r = requests.post(url, data, stream=True)
            # time.sleep(1)
            req = requests.post(url, headers=headers, data=data, verify=False)
            # the_url="https://legacy.bcpao.us/asp/find_property.asp?"+'SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
            # print(the_url)
            soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
            # print_headers(the_url, 'html.parser')
            rers_cell = soup.find(text="Real Estate Records Search")

            #         for a in soup.find_all('a'):
            #             pprint.pprint(a)
            aerials = soup.find_all('a', text="Aerial")
            if aerials and len(aerials) > 1:
                # need to ignore this whole page if we have more than one result. can search for how many "Aerial" there are
                print('ignoring this whole page because we have more than one result (tax ids)')
                rers_cell = None
            # print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants), max=50)
            # print_headers(soup, 'Real Estate Records Search')
            if rers_cell is not None:
                # print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants))
                # print(bi_cell.parent.parent.parent.parent)
                # # print(list(bi_cell.parent.parent.parent.parent.descendants))
                # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
                # try:
                # print('list(bi_cell.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item).decode('utf-8').replace(u'\xa0', u''))
                # except:
                # pass
                # ret=str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[82])
                ret = str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[offset])

        if not ret:
            print('trying condo')

            data = None
            offset = 82
            blk_str = self.convertBlock(block)
            if not blk_str:
                blk_str = ''
            lot_str = self.convertLot(lot)
            data = 'SearchBy=PID&twp=' + str(t) + '&rng=' + str(r) + '&sec=' + str(s) + '&subn=' + str(
                subid) + '&blk=' + str(blk_str) + '&lot=' + str(lot_str) + '&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
            req = requests.post(url, headers=headers, data=data)
            # the_url="https://legacy.bcpao.us/asp/find_property.asp?"+'SearchBy=Sub&sub='+urllib.quote(sub)+'&blk='+str(block)+'&lot='+str(lot)+'&gen=T&tax=T&bld=T&oth=T&lnd=T&sal=T&leg=T'
            print(data)
            soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
            #         print(soup.prettify())
            #         print_headers(the_url, 'html.parser')
            rers_cell = soup.find(text="Real Estate Records Search")
            # print_small_texts(list(rers_cell.parent.parent.parent.parent.parent.descendants), max=50)
            aerials = soup.find_all('a', text="Aerial")
            if aerials and len(aerials) > 1:
                # need to ignore this whole page if we have more than one result. can search for how many "Aerial" there are
                print('ignoring this whole page because we have more than one result (tax ids)')
                rers_cell = None
            if rers_cell is not None:
                ret = str(list(rers_cell.parent.parent.parent.parent.parent.descendants)[offset])

        if not ret:
            print('no bcpao acct, no address')

        return ret

    def get_bcpaco_item(self, acct):
        print("get_bcpaco_item('" + acct + "')")
        # don't do anything if acct is blank (same in bcpao_radius
        ret = {}
        if acct is None or len(acct) == 0:
            return ret
            # https://legacy.bcpao.us/asp/Show_parcel.asp?acct=2713420&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address
            # url = 'https://legacy.bcpao.us/asp/Show_parcel.asp'
            # headers = {
            # 'Cookie': 'ASPSESSIONIDQABRBBSS=ELGLAMBAELLCGOLCONGKOFHE',
            # 'Content-Type': 'application/x-www-form-urlencoded'
            # }
            # data='acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address'
            # r = requests.post(url, headers=headers, data=data)

            # with closing(urlopen("https://legacy.bcpao.us/asp/Show_parcel.asp?"+'acct='+acct+'&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address')) as f:
            # document = html5lib.parse(f, encoding=f.info().getparam("charset"))
            # print(document)

        # print(str(r.text.encode('utf-8'))[8000:9000])
        # print(str(r.text))
        the_url = "http://legacy.bcpao.us/asp/Show_parcel.asp?" + 'acct=' + acct + '&gen=T&tax=T&bld=T&oth=T&sal=T&lnd=T&leg=T&GoWhere=real_search.asp&SearchBy=Address'

        print(the_url)
        f = urlopen(the_url)
        html = f.read().replace(u'\xa0', u'').encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        try:
            # time.sleep(1)

            # print(soup.prettify())
            # gpc = soup.find(text="General Parcel Information")
            # print_small_texts(list(soup.descendants), max=500)
            sa = soup.find(text="Site Address:")
            if sa is not None:
                # print_small_texts(list(sa.parent.parent.descendants), max=50)
                # # for index,item in enumerate(list(gpc.parent.parent.parent.descendants)):
                # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # # if str(item).startswith('7667'):
                # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                ret['address'] = str(list(sa.parent.parent.descendants)[5].replace('\\r\\n', '').strip())
                ret['zip_code'] = ret['address'][-5:]
        except:
            raise

        try:
            # time.sleep(1)
            # with closing(urlopen(the_url)) as f:
            html = f.read().replace(u'\xa0', u'').encode('utf-8')
            filtered = []
            for l in html.split('\n'):
                if 'javascript:void(0);' not in l and 'px;"' not in l and '&nbsp;' not in l:
                    to_append = l.replace(u'\xa0', u'').encode('utf-8')
                    filtered.append(to_append)
                    # print(to_append)
                    # else:
                    # print('filtering: '+l)
            data = ''.join(filtered)
            # soup = BeautifulSoup(html, 'lxml')
            # soup = BeautifulSoup(urlopen(the_url))
            #     print('test test test adrian ' + data)
            #     print(soup.prettify())
            # print('one two three')
            vs_cell = soup.find(text="Value Summary")
            # print_small_texts(list(soup.descendants), max=50)
            # print_headers(the_url, 'html.parser')
            # print_headers(the_url, 'html5lib')
            # print(str(soup.find(text='110')))
            # print(BeautifulSoup(urlopen(the_url)).prettify())
            # sa = soup.find(text="Site Address:")
            if vs_cell is not None:
                # print_small_texts(list(vs_cell.parent.parent.parent.parent.descendants))
                # # # for index,item in enumerate(list(gpc.parent.parent.parent.descendants)):
                # # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # # # if str(item).startswith('7667'):
                # # # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                ret['latest market value total'] = str(list(vs_cell.parent.parent.parent.parent.descendants)[38])
            # ret['zip_code']=ret['address'][-5:]

            bi_cell = soup.find(text="Building Information")
            # print(bi_cell)
            if bi_cell is not None:
                # print_small_texts(list(bi_cell.parent.parent.parent.parent.parent.descendants))
                use_code = list(bi_cell.parent.parent.parent.parent.parent.descendants)[52].encode('utf-8')
                ret['use code'] = dict(use_code=use_code, use_code_str=self.get_use_code_str(use_code))
                ret['year built'] = str(list(bi_cell.parent.parent.parent.parent.parent.descendants)[56])
                ret['frame code'] = str(list(bi_cell.parent.parent.parent.parent.parent.descendants)[65])

            bai_cell = soup.find(text="Building Area Information")
            if bai_cell is not None:
                # print_small_texts(list(bai_cell.parent.parent.parent.parent.descendants))
                ret['total base area'] = str(list(bai_cell.parent.parent.parent.parent.descendants)[93])
        except:
            raise

        # print(ret)

        try:
            if 'latest market value total' not in ret:
                # with closing(urlopen(the_url)) as f:
                soup = BeautifulSoup(html, "html.parser")
                mvt = soup.find(text="Market Value Total:")
                # for index,item in enumerate(list(mvt.parent.parent.descendants)):
                # print('list(gpc.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                if mvt:
                    ret['latest market value total'] = str(list(mvt.parent.parent.descendants)[13])

            if 'latest market value total' not in ret:
                # with closing(urlopen(the_url)) as f:
                #     html = f.read().replace(u'\xa0', u'').encode('utf-8')
                filtered = []
                for l in html.split('\n'):
                    if 'Homestead' not in l and 'tdHeader_Row_1_Col_1' not in l:
                        filtered.append(l.replace(u'\xa0', u'').encode('utf-8'))
                        # else:
                        # print('filtering: '+l)
                soup = BeautifulSoup(''.join(filtered), "lxml")
                mvt = soup.find(text="Market Value Total:")
                # print(soup.find(text="General Parcel Information"))
                # print(soup.find(text="Owner Information"))
                # print(soup.find(text="Owner Name:"))
                # print(soup.find(text="Second  Name:"))
                # print(soup.find(text="Mailing Address:"))
                # print(soup.find(text="City, State, Zipcode:"))
                # print(soup.find(text="Taxable Value School:"))
                # print(soup.find(text="Roll Year:"))
                # print(soup.find(text="Sale Information"))
                # print(soup.find(text="Sale Date"))
                # print(soup.find(text="Land Information"))
                # print(soup.find(text="Acres"))
                # print(soup.find(text="Millage Code:"))
                # print(soup.find(text="Exemption:"))
                # print(soup.find(text="Use Code:"))
                # print(soup.find(text="Site Address:"))
                # print(soup.find(text="Tax ID:"))
                # pi = soup.find(text="Tax ID:")
                # print(pi)
                # print(soup.find(text="Owner Name:"))
                # print(soup.find(text="Roll Year:"))
                # print(soup.find(text="Assessed Value School:"))
                # for index,item in enumerate(list(pi.parent.parent.parent.parent.parent.descendants)):
                # print('list(pi.parent.parent.parent.parent.parent.descendants)['+str(index)+']: '+str(item))
                # for index,item in enumerate(list(soup.descendants)):
                # print('\n\n\n\n\n\n\n\n\nlist(soup.descendants)['+str(index)+']: '+str(item))
                # b=list(soup.descendants)[26]
                # c=list(b.descendants)[9]
                # for index,item in enumerate(list(b.descendants)):
                # print('list(\n\n\n\n\n\n\n b.descendants)['+str(index)+']: '+str(item))
                # if '$' in str(item):
                # print('['+str(index)+']: '+str(item))
                # if str(item).startswith('$'):
                # print('list(pi.parent.parent.descendants)['+str(index)+']: '+str(item))
                # if mvt:
                # ret['latest market value total']=str(list(mvt.parent.parent.descendants)[13])

            class MyHTMLParser(HTMLParser):
                def handle_starttag(self, tag, attrs):
                    print('handle_starttag: ' + tag)
                    if 'tr' in tag:
                        self.in_tr = True

                def handle_endtag(self, tag):
                    if 'tr' in tag:
                        self.in_tr = False
                        self.in_mvt = False

                def handle_data(self, data):
                    # print('handle_data: ' + data)
                    if 'Market Value Total:' in data:
                        self.in_mvt = True
                    if self.in_mvt and '\\n' not in data:
                        self.mvt = data
                        print('handle_data: ' + data)

            parser = MyHTMLParser()
            parser.limit_tables = 20
            parser.limit = 5000
            parser.rows = []
            parser.current_row = None
            parser.in_tr = False
            parser.tables = []
            parser.table_count = 0
            parser.td_count = 0
            parser.in_table = False
            parser.current_table = None
            parser.in_mvt = False
            # print(r.text)
            # print(r.json())
            # f = urlopen(the_url)
            # html = f.read()
            # parser.feed(html)
            # parser.feed(urlopen(the_url).encode('utf-8'))
            # parser.feed(str(r.text))
            # pprint.pprint(parser.tables)
            # print(parser.mvt)
            # return parser.mvt
            # ret['latest market value total']=parser.mvt
        except:
            raise  # print('123 ex: '+str(e))

        try:
            # year built - Condo Unit Detail
            # time.sleep(1)
            soup = BeautifulSoup(html, 'html.parser')
            bi_cell = soup.find(text="Building Information")
            if bi_cell is not None:
                # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
                # if str(item).startswith('1,173'):
                # break
                ret['year built'] = list(bi_cell.parent.parent.parent.parent.parent.descendants)[56]

                bai_cell = soup.find(text="Building Area Information")
                # for index, item in enumerate(list(bai_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
                # if str(item).startswith('1,173'):
                # break
                ret['total base area'] = list(bai_cell.parent.parent.parent.parent.parent.descendants)[59]

            cud_cell = soup.find(text="Condo Unit Detail")
            if cud_cell is not None:
                # for index, item in enumerate(list(cud_cell.parent.parent.parent.parent.parent.descendants)):
                # if len(item.encode('utf-8').strip()) > 0 and len(item.encode('utf-8')) < 20:
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + item.encode('utf-8'))
                # if item.encode('utf-8').startswith('1990'):
                # break
                ret['year built'] = list(cud_cell.parent.parent.parent.parent.parent.descendants)[198].encode('utf-8')
                ret['sq feet'] = list(cud_cell.parent.parent.parent.parent.parent.descendants)[112].encode('utf-8')

        except Exception as e:
            str(e)
            raise  # print('345 ex: '+str(e))

        try:
            # print_headers2(the_url)
            # the_html=urlopen(the_url)
            # time.sleep(1)
            soup = BeautifulSoup(html, 'html.parser')
            bi_cell = soup.find(text="Building Information")
            if bi_cell is not None:
                # print_headers(the_url, 'html.parser')
                # print_headers(the_url, 'html5lib')
                # print(fc_cell.parent.parent.parent.parent.parent)
                # print(fc_cell.parent.parent.parent.parent.parent)
                # print(list(fc_cell.parent.parent.parent.parent.parent.descendants))
                # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
                # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
                use_code = list(bi_cell.parent.parent.parent.parent.parent.descendants)[52].encode('utf-8')
                ret['use code'] = dict(use_code=use_code, use_code_str=self.get_use_code_str(use_code))
                ret['year built'] = list(bi_cell.parent.parent.parent.parent.parent.descendants)[56].encode('utf-8')
                ret['frame code'] = list(bi_cell.parent.parent.parent.parent.parent.descendants)[
                    65].parent.parent.get_text().encode('utf-8')
        except:
            raise  # print('sdf ex: '+str(e))

            # try:
            # bai_cell = soup.find(text="Building Area Information")
            # # print(list(fc_cell.parent.parent.parent.parent.parent.descendants))
            # # for index, item in enumerate(list(bi_cell.parent.parent.parent.parent.parent.descendants)):
            # # print('list(fc_cell.parent.parent.parent.parent.parent.descendants)['+str(index)+']: ' + str(item))
            # ret['total base area']=list(bai_cell.parent.parent.parent.parent.parent.descendants)[95].encode('utf-8')
            # except:
            # pass#print('sdf ex: '+str(e))

        manuf_codes = ['212', '213', '214']
        if 'use code' in ret and ret['use code']['use_code'] in manuf_codes:
            ret['manuf'] = True

        return ret

    def convertBlock(self, block):
        blk_str = block
        if block:
            m = re.search('^(?P<num>[\0-9]+)(?P<letter>[A-Z])$', block)
            if m:
                block = m.group('num') + '.' + m.group('letter')
                #     if block and block.endswith('S'):
                #         block = block[:-1] + '.S'
                #     elif block and block.endswith('F'):
                #         block = block[:-1] + '.F'
                #     elif block and block.endswith('J'):
                #         block = block[:-1] + '.J'
                #     elif block and block.endswith('L'):
                #         block = block[:-1] + '.L'
                #     elif block and block.endswith('U'):
                #         block = block[:-1] + '.U'
                #     elif block and block.endswith('K'):
                #         block = block[:-1] + '.K'


                #     if block and len(block) == 4 and '.' not in block:
                #         print 'block is length 4'
                #         block = block[0:3] + '.' + block[3:4]
            if block:
                blk_str = block
        return blk_str

    def convertLot(self, lot):
        lot_str = ''
        if lot and len(lot) == 4 and '.' not in lot:
            print 'lot is length 4'
            lot = lot[0:2] + '.' + lot[2:4]
        if lot:
            lot_str = lot
        return lot_str

    def get_use_code_str(self, use_code):
        # https://legacy.bcpao.us/asp/Show_code.asp?numeric=t&table=UseCodes&ValColName=UseCode&DescColName=UseDesc&value=110
        the_map = {}
        the_map['110'] = 'R-SINGLE FAMILY RESIDENCE'
        the_map['212'] = 'M-MANUFACTURED HOUSING - SINGLE WIDE'
        the_map['213'] = 'M-MANUFACTURED HOUSING - DOUBLE WIDE'
        the_map['214'] = 'M-MANUFACTURED HOUSING - TRIPLE WIDE'
        if use_code in the_map:
            return the_map[use_code]

class BcpaoItem(object):
    def __init__(self, mr):
        self._mr = mr

    def get_account(self):
        return self._mr.get_item()['bcpao_acc']

    def get_address(self):
        return self._mr.get_item()['bcpao_item']['address']

class MyTestCase(unittest.TestCase):
    def test_something(self):
        fl = ForeclosuresList()
        first_fli = fl.get_first()
        print(first_fli.get('case_number'))
        # self.assertEqual('05-2009-CA-029039-XXXX-XX', first_fli.get('case_number'))
        bc = BrevardClerk()
        ld = bc.get_legal_description(first_fli.get('case_number'))
        print(ld.get_leg_desc_string())
        # self.assertEqual('LT 25 BLK D PB 44 PG 76 CHELSEA PARK UNIT 3 S 22 T 25 R 36 SUBID 28', ld.get_leg_desc_string())
        bcpao = Bcpao()
        bi = bcpao.get_bcpao_info(ld)
        print(bi.get_account())
        # self.assertEqual('2530331', bi.get_account())
        print(bi.get_address())
        # self.assertEqual('405  STONEHENGE CIR , ROCKLEDGE 32955', bi.get_address())


if __name__ == '__main__':
    unittest.main()

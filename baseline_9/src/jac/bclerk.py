from bs4 import BeautifulSoup
from mechanize import ParseResponse, urlopen
import re
import itertools
import logging
import pprint



def get_bclerk_results_text(case):
    uri = 'http://web1.brevardclerk.us/oncoreweb/search.aspx'
    response = urlopen(uri)
    forms = ParseResponse(response, backwards_compat=False)
    form = forms[0]
#     print form
    form["txtCaseNumber"] = case #"orozco"
    form["SearchType"] = 'casenumber' #"orozco"
    form["txtDocTypes"] = ''#'JRP, J' #"orozco"
# form["txtName"] = "orozco"
    bclerk_results_text = urlopen(form.click()).read()
    return bclerk_results_text

def get_bclerk_results_soup(case):
    bclerk_results_text = get_bclerk_results_text(case)
    soup = BeautifulSoup(bclerk_results_text, "lxml")
    return soup

def get_legal_by_case(case):
    print('get_legal_by_case("'+case+'")')
    ret={}

#     soup = get_bclerk_results_soup(case)
#     print soup.renderContents()


    # bi_cell = soup.find(text="                                                                                                LT 22 BLK 10 PB 5 PG 20 EAU GALLIE SHORES S 35 T 26 R 37 SUBID 02")
#     bi_cell = soup.findAll(text=re.compile('.* S \d+ T [0-9a-zA-Z]+ R \d+ .*'))#"td", { "class" : "stdFontResults" })
    rows = get_records_grid_for_case_number(case)
    lds = []
    for row in rows:
        if row['First Legal'] and len(row['First Legal']) > 0:
            lds.append(row['First Legal'])
    ret['legal_description']='; '.join(lds).strip()
#     print('ret[legal_description]: ' + ret['legal_description'])
    for i,ld in enumerate(lds):
        # print(b.strip())
        legal_desc = ld.strip()
        temp = get_legal_from_str(legal_desc)
        if temp:
            ret = dict(itertools.chain(ret.items(), temp.items()))
            if i < (len(lds) - 1):
                the_str = 'choosing a legal description (index='
                the_str += str(i)
                the_str += ':'+legal_desc
                the_str += ') before going through all of them(total='
                the_str += str(len(lds))
                the_str += '): '
                # logging.info(the_str)
                # pprint.pprint(lds)
            break
#     print(ret)
    return ret


def get_legals_by_case(case):
    print('get_legals_by_case("'+case+'")')
    rets=[]


    rows = get_records_grid_for_case_number(case)
    lds = []
    for row in rows:
        if row['First Legal'] and len(row['First Legal']) > 0:
            lds.append(row['First Legal'])
    #ret['legal_description']='; '.join(lds).strip()
    for i,ld in enumerate(lds):
        # print(b.strip())
        legal_desc = ld.strip()
        temp = get_legal_from_str(legal_desc)
        if temp:
            rets.append(dict(temp.items()))
#     print(ret)
    return rets

def get_legal_from_str(the_str):
    legal_desc = the_str.replace(u'\xc2',u'')
    logging.info('get_legal_from_str('+legal_desc+')')
    ret={}

    m = re.search('(LT (?P<lt>[0-9a-zA-Z]+) )?(BLK (?P<blk>[0-9a-zA-Z]+) )?(PB (?P<pb>\d+) PG (?P<pg>\d+))?(?P<subd>.*) S (?P<s>\d+) T (?P<t>\d+G?) R (?P<r>\d+)( SUBID (?P<subid>[0-9a-zA-Z]+))?', the_str)
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
        ret['condo']=True
#     print('ret='+str(ret))
    ret['legal_desc']=legal_desc
    return ret

def get_records_grid_for_case_number(case_number):
    soup = get_bclerk_results_soup(case_number) #('05-2014-CA-024535-XXXX-XX')
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
import itertools


import time
from bs4 import BeautifulSoup
import pprint
import logging
import sys

from jac import bclerk

import urllib
import urllib2

import requests
import re


def get_url():
    return 'https://vweb1.brevardclerk.us/facts/d_caseno.cfm'


def get_data(year, court_type, seq_number):
    return 'CaseNumber1=05&CaseNumber2=' + year + '&CaseNumber3=' + court_type + '&CaseNumber4=' + seq_number + '&CaseNumber5=&CaseNumber6=&submit=Submit'


def get_headers(cfid, cftoken):
    return {
        'Cookie':'CFID=' + cfid + '; CFTOKEN=' + cftoken,
        'Content-Type':'application/x-www-form-urlencoded'}

def case_info(out_dir, year, court_type, seq_number, cfid, cftoken):
    id2 = year+'_'+court_type+'_'+seq_number
    # print('case_info('+id+')')
    url = get_url()
    headers=get_headers(cfid, cftoken)
    data=get_data(year, court_type, seq_number)
#     r = requests.post(url, data, headers=headers, stream=True)
    r = requests.post(url, data, headers=headers, stream=True, timeout=5)
    #print(r.url)
    # print(r.cookies)
    # print(r.cookies['CFID'])
    # print(r.cookies['CFTOKEN'])
    # print(r.text)
    #lines = r.text.split('\n')
    #for l in lines:
        # print(l)
        #m = re.search('b>(.* VS .*)</b', l)
        # if m:
            # print(''+m.group(1))
    ret = {}
    # ret['defs']=get_defendant_item(r.text)
    if out_dir:
        with open(out_dir+'/'+id2+'_case_info.htm', 'wb') as handle:
            for block in r.iter_content(1024):
                if not block:
                    break
                handle.write(block)
    return ret

def get_case_number_url(cn):
    adate=time.strftime("%m/%d/%Y")#'5/31/2014'
    # thedate=urllib2.quote(adate) why is this not escaping the fwd slash to %2F ?
    thedate=adate.replace('/','%2F')
    print(thedate)
    # print(urllib.quote('/~connolly/'))
    # print (time.strftime("%m/%d/%Y"))
    return get_case_number_url(thedate, cn)


def get_case_number_url(date_str, cn):
    return 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2015&n=&bt=OR&d=' + date_str + '&pt=-1&cn=' + cn + '&dt=ALL%20DOCUMENT%20TYPES&st=casenumber&ss=ALL%20DOCUMENT%20TYPES'

def do(out_dir, year, court_type, seq_number, cfid, cftoken):
    ret1 = case_info(out_dir, year, court_type, seq_number, cfid, cftoken)
    ret2 = reg(out_dir, year, court_type, seq_number, cfid, cftoken)
    ret = dict(itertools.chain(ret1.items(), ret2.items()))

    return ret


def get_lad_from_reg_text(r_text):
    lad = None
    lines = r_text.split('\n')
    for l in lines:
        # print(l)
        # if 'AMOUNT DUE' in l:
        # print(l)
        # m = re.search('<font color="Blue">(.* VS .*)<', l)
        # if m:
        # print(indent+m.group(1))
        m = re.search('.*AMOUNT DUE: \$ ?([\d,.]*).*', l)
        if m:
        # print(m.groups())
            lad = m.group(1)

        # print(l)
        # if '<font color="Blue">' in l:
        # print(l)
    return lad

def get_lad_from_reg_text2(g):
    ret = None
    valid_patterns_for_original_mortgage = ['ER: F/J FCL']
#     for i in g['items']:
# #         pprint.pprint(i)
# #         if 'Description' in i and ('OR MTG' in i['Description'] or 'MTG & ORIG' in i['Description'] or 'COPY OF MTG' in i['Description']):
#         if 'Description' in i and any(x in i['Description'] for x in valid_patterns_for_original_mortgage):
#             if i['Img']:
#                 ret = i['Img']
    for x in valid_patterns_for_original_mortgage:
        ret = get_lad_url_from_grid2(g, x)
        if ret:
            print('getting by: '+x)
            break

    return ret

def get_lad_url_from_grid2(g, a_pattern):
    ret = None
    for i in g['items']:
#         pprint.pprint(i)
#         if 'Description' in i and ('OR MTG' in i['Description'] or 'MTG & ORIG' in i['Description'] or 'COPY OF MTG' in i['Description']):
        if 'Description' in i and a_pattern in i['Description']:
            if i['Img']:
                ret = i['Img']
                break
    return ret

def get_lad_url_from_rtext(r_text):
    grid = get_reg_actions_dataset(r_text)
    return get_lad_from_reg_text2(grid)

def reg(out_dir, year, court_type, seq_number, cfid, cftoken):
    ret = {}
    #indent = '                                                        '
    id2 = year+'_'+court_type+'_'+seq_number
    r_text = get_reg_actions_text(year, court_type, seq_number)
    lad = get_lad_url_from_rtext(r_text)
    ret['latest_amount_due'] = lad
    ret['orig_mtg_link'] = get_orig_mortgage_url_from_rtext(r_text)

    if out_dir:
        with open(out_dir+'/'+id2+'_reg_actions.htm', 'wb') as handle:
            handle.write(r_text)
                # print(block)
    return ret


def get_reg_actions_dataset(r_text):
#     print(r_text[0:len(r_text)/2])
#     soup = BeautifulSoup(r_text)
#     soup = BeautifulSoup(r_text.encode('utf-8'), 'html.parser')
    soup = BeautifulSoup(r_text.encode('utf-8'), 'lxml')
#     print soup.prettify()
#     print('case number: ' + soup.title.text)
#     print('case title: ' + soup.find_all('font', color='Blue')[0].text)
    ret = {}
    ret['case number'] = soup.title.text
    ret['case title'] = soup.find_all('font', color='Blue')[0].text
#     print(soup.find_all('table')[1].find_all('tr'))
    items = []
    col_names = []
    trs = soup.find_all('table')[1].findAll("tr")
    for row, a in enumerate(trs):
#         print 'r' + str(row) + '===' + str(a).replace("\n", "").replace("\r", "").replace("\t", "")
        current_item = {}
        for h_index, h_text in enumerate(a.findAll("th")):
#             print ' h_index' + str(h_index) + '===' + str(h_text).replace("\n", "").replace("\r", "").replace("\t", "")
            col_names.append(h_text.text)

        for c, d in enumerate(a.findAll("td")):
#             print ' c' + str(c) + '===' + str(d).replace("\n", "").replace("\r", "").replace("\t", "")
            the_a = None
            try:
                current_item[col_names[c]] = d.text
                the_a = d.find('a')
                if the_a:
                    current_item[col_names[c]] = the_a['href']
            except (IndexError, KeyError) as error:
                logging.debug(' '.join(['********exception******', str(error), str(sys.exc_info()[0]), str(col_names), str(d)]))
#                 logging.exception(error)

        if row >= 1:
            items.append(current_item)

#     pprint.pprint(items)
    ret['items'] = items
    return ret


def get_reg_actions_text(year, court_type, seq_number):
    url = 'https://vweb1.brevardclerk.us/facts/d_reg_actions.cfm'
    cfid = '1550556'
    cftoken = '74317641'
    headers = get_headers(cfid, cftoken)
    data = get_data(year, court_type, seq_number)
#     r = requests.post(url, data, headers=headers, stream=True)
    r = requests.post(url, data, headers=headers, stream=True)
    r_text = r.text
    return r_text

def reg_actions_grid(year, court_type, seq_number):

    case_info_grid(year, court_type, seq_number) # have only been able to make reg work after case_info

    r_text = get_reg_actions_text(year, court_type, seq_number)
    ret = get_reg_actions_dataset(r_text)
    return ret

def get_orig_mortgage_url_from_rtext(r_text):
    grid = get_reg_actions_dataset(r_text)
    return get_orig_mortgage_url_from_grid(grid)

def case_info_grid(year, court_type, seq_number):
    cfid = '1550556'
    cftoken = '74317641'
    id2 = year+'_'+court_type+'_'+seq_number
    # print('case_info('+id+')')
    url = get_url()
    headers=get_headers(cfid, cftoken)
    data=get_data(year, court_type, seq_number)
#     r = requests.post(url, data, headers=headers, stream=True)
    r = requests.post(url, data, headers=headers, stream=True)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'html.parser')
#     print(soup.prettify())

def reg_actions_grid_by_cn(cn):
    cn_fields = get_case_number_fields(cn)
    return reg_actions_grid(cn_fields['year'], cn_fields['court_type'], cn_fields['seq_number'])

def get_case_number_fields(case_number):
    m = re.search('(.*)-(.*)-(.*)-(.*)', case_number.replace('-XXXX-XX',''))
    if m:
        # print(m.group(1)+','+m.group(2))
        print(m.groups())
        ret = {}
        ret['year'] = m.group(2)
        ret['court_type'] = m.group(3)
        ret['seq_number'] = m.group(4)
        return ret


def get_orig_mortgage_url_from_grid(g):
    ret = None
    valid_patterns_for_original_mortgage = ['NOTICE FILING ORIG NOTE & MTG', 'OR MTG', 'MTG & ORIG', 'COPY OF MTG', 'ORIGINAL NOTE & MORTGAGE DEED']
#     for i in g['items']:
# #         pprint.pprint(i)
# #         if 'Description' in i and ('OR MTG' in i['Description'] or 'MTG & ORIG' in i['Description'] or 'COPY OF MTG' in i['Description']):
#         if 'Description' in i and any(x in i['Description'] for x in valid_patterns_for_original_mortgage):
#             if i['Img']:
#                 ret = i['Img']
    for x in valid_patterns_for_original_mortgage:
        ret = get_orig_mortgage_url_from_grid2(g, x)
        if ret:
            print('getting by: '+x)
            break

    return ret

def get_orig_mortgage_url_from_grid2(g, a_pattern):
    ret = None
    for i in g['items']:
#         pprint.pprint(i)
#         if 'Description' in i and ('OR MTG' in i['Description'] or 'MTG & ORIG' in i['Description'] or 'COPY OF MTG' in i['Description']):
        if 'Description' in i and a_pattern in i['Description']:
            if i['Img']:
                ret = i['Img']
                break
    return ret

def get_orig_mortgage_url_by_yts(year, court_type, seq_number):
    g = reg_actions_grid(year, court_type, seq_number)
    return get_orig_mortgage_url_from_grid(g)

def get_orig_mortgage_url_by_cn(cn):
    ######## try to get both latest amount due as well as orig mtg from a single fetch of reg of actions
    g = reg_actions_grid_by_cn(cn)
#     print('='*80)
    ret = get_orig_mortgage_url_from_grid(g)
    return ret

def get_amount_due_by_cn(cn):
    ######## try to get both latest amount due as well as orig mtg from a single fetch of reg of actions
    g = reg_actions_grid_by_cn(cn)
    cn_fields = get_case_number_fields(cn)
    r_text = get_reg_actions_text(cn_fields['year'], cn_fields['court_type'], cn_fields['seq_number'])
#     print('='*80)
    ret = get_lad_from_reg_text(r_text)
    return ret



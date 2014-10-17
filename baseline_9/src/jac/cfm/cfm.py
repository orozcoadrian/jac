import itertools
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
    r = requests.post(url, data, headers=headers, stream=True)
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
    return 'http://web1.brevardclerk.us/oncoreweb/search.aspx?bd=1%2F1%2F1981&ed=5%2F31%2F2014&n=&bt=OR&d=5%2F31%2F2014&pt=-1&cn='+cn+'&dt=ALL%20DOCUMENT%20TYPES&st=casenumber&ss=ALL%20DOCUMENT%20TYPES'

def do(out_dir, year, court_type, seq_number, cfid, cftoken):
    ret1 = case_info(out_dir, year, court_type, seq_number, cfid, cftoken)
    ret2 = reg(out_dir, year, court_type, seq_number, cfid, cftoken)
    ret = dict(itertools.chain(ret1.items(), ret2.items()))

    return ret

def reg(out_dir, year, court_type, seq_number, cfid, cftoken):
    ret = {}
    #indent = '                                                        '
    id2 = year+'_'+court_type+'_'+seq_number
    # print(indent+'reg('+id+')')
    url = 'https://vweb1.brevardclerk.us/facts/d_reg_actions.cfm'
    # cookies = {}
    # cookies['cfid'] = '1554122'
    # cookies['cftoken'] = '49155602'
    # cookies['cfid'] = '1550556'
    # cookies['cftoken'] = '74317641'
    # print(indent+str(cookies))
    headers = {
        'Cookie': 'CFID='+cfid+'; CFTOKEN='+cftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Referer': 'https://vweb1.brevardclerk.us/facts/d_caseno.cfm'
        }
    data='RequestTimeout=500'
    # print('pre asdfasdf')
    r = requests.post(url, data, headers=headers, stream=True)
    # print('post asdfasdf')
    # print(r.text)
    lines = r.text.split('\n')
    for l in lines:
        # print(l)
        # if 'AMOUNT DUE' in l:
            # print(l)
        # m = re.search('<font color="Blue">(.* VS .*)<', l)
        # if m:
            # print(indent+m.group(1))
        m = re.search('.*AMOUNT DUE: \$([\d,.]*).*', l)
        if m:
            # print(m.groups())
            ret['latest_amount_due'] = m.group(1)
            # print(l)
        # if '<font color="Blue">' in l:
            # print(l)

    if out_dir:
        with open(out_dir+'/'+id2+'_reg_actions.htm', 'wb') as handle:
            for block in r.iter_content(1024):
                if not block:
                    break
                if 'You were brought to this page because search information has not been provided' in str(block):
                    print('no data')
                handle.write(block)
                # print(block)
    return ret
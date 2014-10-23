'''
Created on Oct 21, 2014

@author: Adrian



'''
import requests
from bs4 import BeautifulSoup
import pprint

def add_address(i):
    r = requests.get(i['case_link'])
#print(r.encoding)
#r.encoding = 'utf-8'
#print(r.raw.read(3000))
    soup = BeautifulSoup(r.text)
    tb = soup.find("table", id='fcDetail')
    if tb is None:
        return
    #print('0::')
    #print(tb.find_all("tr"))
    #print('1::')
    #print(tb.find_all("tr")[0].find_all('td')[1])
    first = 0;
    the_tr = tb.find_all("tr")[first]
    #print(the_tr.string)
    i['cancelled'] = False
    if the_tr.string and 'cancelled' in the_tr.string:
        #print('skipping')
        first += 1
        the_tr = tb.find_all("tr")[first]
        i['cancelled'] = True
    #print(the_tr)
    addr = the_tr.find_all('td')[1].string.replace(u'\xa0', u'').replace(u'\r\n', u', ').replace(u'  ', u', ')
#pprint.pprint(addr)
    i['address'] = addr
    street_addr=addr.split(',')[0]
    print(street_addr)
    ss=street_addr.split()
    print(ss)
    try:
        print(ss.pop(0))
        print(ss.pop(len(ss)-1))
        print(ss)
        print(ss.join(' '))
        print(ss)
    except:
        pass
#     print(ss.pop(len(ss)-1))
#     print(ss)

    desc_tr = tb.find_all("tr")[first+7]
    #print(desc_tr)
    desc = desc_tr.find_all('td')[0].string.replace(u'\xa0', u'').replace(u'\r\n', u', ').replace(u'  ', u', ')
    #print(desc)
    i['description'] = desc

    pprint.pprint(i)

def get_rows(the_html):
    rows = []
    soup = BeautifulSoup(the_html)
    #print(soup.prettify())
    tb = soup.find("table", id='fcResults')
    #print(tb)
    trs = tb.find_all("tr")
    for tr in trs:
        #print(tr)
        current_row = {}
        tds = tr.find_all('td')
        if len(tds) == 0:
            continue

        #print(tds)
        current_row['date'] = tds[0].string
        current_row['case'] = tds[1].string
        current_row['case_link'] = 'http://www.seminoleclerk.org/Foreclosures/'+tds[1].a['href']
        current_row['detail'] = tds[2].string.replace(u'\xa0', u'').encode('utf-8').replace('\n\n','')
#         current_row['foreclosure_sale_date'] = tds[3].string
        current_row['count'] = len(rows) + 1
        add_address(current_row)
        rows.append(current_row)
        if len(rows) > 5:
            break
        #break
    # pprint.pprint(rows)
    return rows

def get_items():
    r = requests.get('http://www.seminoleclerk.org/Foreclosures/default.jsp')
    return get_rows(r.content)

def foreclosures_list():
    items = get_items()


def add_pa(amap, street_name, street_number, street_suffix):
    r = requests.get('http://www.scpafl.org/RunQuery.aspx?Which=ADDRESS&What='+street_name+'&Addr='+street_number+'&Suffix='+street_suffix+'&Dir=')
    print r.url
#print(r.content)
    soup = BeautifulSoup(r.content)
#print(soup.prettify())
    tb = soup.find("table", class_='dxgvTable')
#print(tb)
    ass_cell = soup.find(text="Assessed Value")
    print ass_cell
    print str(list(ass_cell.parent.parent.parent.descendants))
    amap['ass'] = str(list(ass_cell.parent.parent.parent.descendants)[6])
    amap['prop_appr_url'] = r.url

def prop():
    #http://www.scpafl.org/RunQuery.aspx?Which=ADDRESS&What=Rantoul&Addr=749&Suffix=LN&Dir=
#     street_name = 'Rantoul'
#     street_number = '749'
#     street_suffix = 'LN'
    street_name = '13TH'
    street_number = '148'
    street_suffix = 'AVE'
    amap={}
    add_pa(amap, street_name, street_number, street_suffix)
    pprint.pprint(amap)

if __name__ == '__main__':
    #prop()
    foreclosures_list()
    #pprint.pprint(items)
    #for i in items:
    #i = items[2]
    #pprint.pprint(i)
    print('DONE')

    #http://www.seminoleclerk.org/Foreclosures/default.jsp
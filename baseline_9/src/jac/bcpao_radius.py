#import sys
#import os
#import requests
#from time import strftime
import re
import pprint
#import urllib
# from urllib import parse
# from html.parser import HTMLParser
#from HTMLParser import HTMLParser
# import html.parser
from bs4 import BeautifulSoup
import time

#from contextlib import closing
#from urllib2 import urlopen
#import html5lib
import unittest
from mechanize import ParseResponse, urlopen
#from StringIO import StringIO

class TestUM(unittest.TestCase):
    def test_radius(self):
        #i=get_radius_data('2807459')
        pass
    def test_radius2(self):
        # i=get_to_map('2424844')
        i=get_average_from_radius('2423244')
        pprint.pprint(i)
        

def print_small_texts(the_list,max2=20):
    for index, item in enumerate(the_list):
        # print('the_list['+str(index)+']: ' + item.encode('utf-8'))
        if len(item.encode('utf-8').strip()) > 0 and len(item.encode('utf-8')) < max2:
            print('the_list['+str(index)+']: ' + item.encode('utf-8'))
            
def get_nearby_table(the_url):
    # print('get_nearby_table(%s)'%the_url)
    soup2 = BeautifulSoup(urlopen(the_url))
    # print(soup2.prettify())
    # print_small_texts(list(soup2.descendants))
    trs=soup2.find_all("tr")
    parsed_rows=[]
    #header_row={}
    headers=[]
    for i,t in enumerate(trs):
        # print('trs['+str(i)+']: '+str(t))
        new_row={}
        if i == 0:
            for h_i,header_cell in enumerate(t.find_all('th')):
                # print('header_cell: '+str(header_cell))
                # print(header_cell.font.string)
                new_h=None
                if header_cell.font.string is None:
                    new_h='null_column_'+str(h_i)
                else:
                    new_h=header_cell.font.string
                headers.append(new_h)
            # print(headers)
        else:
            # print(' * * * ** * * ** * * ** * * ** * * ** * * ** * * *  find th')
            hi=t.find('th')
            # print('hi: '+str(hi))
            offset=0
            if hi is not None:
                # print('hi '+hi.font.string)
                new_row[headers[0]]=hi.font.string
                offset=1
            # print(' * * * ** * * ** * * ** * * ** * * ** * * ** * * *  find_all td')
            # print('offset: '+str(offset))
            for c_i,row_cell in enumerate(t.find_all('td')):
                
                # if row_cell.br is not None:
                    #this is a blank first column
                    # new_row[headers[0]]=None
                    
                # print('row_cell.br:')
                # print(row_cell.br)
                
                # print('row_cell '+headers[c_i+offset]+' <--- '+str(row_cell.font.string))
                new_row[headers[c_i+offset]]=row_cell.font.string
                # if c_i ==3:
                    # break
            parsed_rows.append(new_row)
    return parsed_rows
                
def get_radius_data(acct):
    # print('get_radius_data('+acct+')')
    ret={}
    if acct is None or len(acct) == 0:
        return ret
    # https://www.bcpao.us/scripts/esrimap.dll?name=Brevard1&id=201406081615007073&cmd=mapclick&Parcels=1&RoadNames=1&Water=1&Left=737379.85076&Right=739190.28624&Top=1456972.55954&Bottom=1455711.95166&locate=&lSel=MAPCLICK&lTab=tabFrame201406081616027932.html&thmvis=10000000000001000111101111&thmavl=00000000000001111010010010&x=738670.263874576&y=1456523.04774181&zlev=12&view=Map&select=Sales&radius=250&click.x=359&click.y=202
    the_domain='https://www.bcpao.us'
    the_app='/scripts/esrimap.dll'
    the_url=the_domain+the_app+'?name=Brevard1&id=201406081615007073&cmd=mapclick&Parcels=1&RoadNames=1&Water=1&Left=737379.85076&Right=739190.28624&Top=1456972.55954&Bottom=1455711.95166&locate=&lSel=MAPCLICK&lTab=tabFrame201406081616027932.html&thmvis=10000000000001000111101111&thmavl=00000000000001111010010010&x=738670.263874576&y=1456523.04774181&zlev=12&view=Map&select=Sales&radius=250&click.x=359&click.y=202'
    print(the_url)
    
    try:
        soup = BeautifulSoup(urlopen(the_url))
        p=soup.prettify()
        print(p.replace(u'\xa9', u'').encode('utf-8'))
        # gpc = soup.find(text="General Parcel Information")
        # print_small_texts(list(soup.descendants))
        # for index, item in enumerate(list(soup.descendants)):
            # print('the_list['+str(index)+']: ' + item.encode('utf-8'))
            # if 'tabFrame' in str(item):
                # print('found: '+str(item))
        fr_url=the_domain+soup.find(src=re.compile("tabFrame"))['src']
        # print(fr_url)
        rows=get_nearby_table(fr_url)
        pprint.pprint(rows)
            # if i ==3:
                # break
        # pprint.pprint(parsed_rows)
        # print(headers)
            # if len(header_row)==0:
                # for cell in t.find_all('td'):
                    # header_row
    except:
        raise
        
    return ret
                

def print_headers(the_url, parser_name=None):
    # print('print_headers(the_html, '+parser_name+')')
    soup=None
    if parser_name is None:
        print('print_headers(the_url)')
        soup = BeautifulSoup(urlopen(the_url))
    else:
        print('print_headers(the_url, '+parser_name+')')
        soup = BeautifulSoup(urlopen(the_url), parser_name)
    
    texts=[]
    texts.append("BCPAO - Property Details")
    texts.append("New Search")
    texts.append("General Parcel Information")
    texts.append("Millage Code:")
    texts.append("Exemption:")
    texts.append("Use Code:")
    texts.append("Site Address:")
    texts.append("Tax ID:")
    texts.append("Owner Information")
    texts.append("Abbreviated Description")
    texts.append("Owner Name:")
    texts.append("Second  Name:")
    texts.append("Mailing Address:")
    texts.append("City, State, Zipcode:")
    texts.append("Value Summary")
    texts.append("Land Information")
    texts.append("Taxable Value School:")
    texts.append("Roll Year:")
    texts.append("Sale Information")
    texts.append("Building Information")
    texts.append("Building Area Information")
    texts.append("Extra Feature Information")
    texts.append("Sale Date")
    texts.append("Acres")
    
    
    
    
    # print(texts)
    for t in texts:
        print(t.ljust(28)+': '+str(soup.find(text=t)))
  
def get_nearby_from_input(the_input):
    rr2=the_input.read()
    # print(rr2)
    for l2 in rr2.split('\\n'):
        mt=re.search('/temp/tabFrame[0-9]+\.html',l2)
        if mt:
            # print(mt.group())
            the_domain='https://www.bcpao.us'
            fr_url=the_domain+mt.group()
            rows=get_nearby_table(fr_url)
            # print('***********************dsssss*************************')
            # pprint.pprint(rows)
            return rows
            
def get_nearby_from_parent(the_url):
    # print('get_nearby_from_parent: '+the_url)
    
    r2 = urlopen(the_url)
    return get_nearby_from_input(r2)
    
def get_info_from_graframe_rows(the_rows):
    ret={}
    ret['dollar_strs']=get_dollar_strings_from_graframe_rows(the_rows)
    dollar_ints=[]
    for ds in ret['dollar_strs']:
        dollar_ints.append(int(ds.replace('$','').replace(',','')))
    ret['rows_num']=len(ret['dollar_strs'])
    #"{:3.0f}%".format(100.0*index/len(items2[:limit]))
    ret['average']="{:.0f}".format(float(sum(dollar_ints))/len(dollar_ints)) if len(dollar_ints) > 0 else ''#float('nan')
    return ret
    
def get_dollar_strings_from_graframe_rows(the_rows):
    ret=[]
    for r in the_rows:
        if 'Deed Type' in r and 'WD' in r['Deed Type'] and 'Sale Date' in r and '2014' in r['Sale Date'] and 'Sale Amount' in r and not '$100' == r['Sale Amount']:
            ret.append(r['Sale Amount'])
    return ret

def get_rows_from_graframe_url(url3, radius):
    # print('get_rows_from_graframe_url(%s, %s)' % (url3, radius))
    r3 = urlopen(url3)
    forms = ParseResponse( r3, backwards_compat=False)
    # for f in forms:
        # print f
    form = forms[0]
    # print(form)
    form["select"] = ['Sales']
    form["radius"] = [radius]
    # print(form)
    rows=get_nearby_from_input(urlopen(form.click()))
    # pprint.pprint(rows)
    return rows
                    
def get_average_from_radius(tax_id):
    # print('sdfs:'+str(tax_id))
    tax_id_str='None' if tax_id is None else str(tax_id)
    print("get_average_from_radius('"+tax_id_str+"')")
    ret={}
    
    the_domain='https://www.bcpao.us'
    # the_id='20140624' ### this seems to be the date and seems to need to be udpated each day?? adrian
    the_id=time.strftime("%Y%m%d")
    uri = the_domain+'/scripts/esrimap.dll?name=Brevard1&Cmd=TID&id='+the_id+'&tid='+tax_id
    # print(uri)
    ret['map_url']=uri
    response = urlopen(uri)
    # html = response.read()
    # s = StringIO(html)
    # print(response)
    # print(response.info())
    # print(response.read())
    rr=response.read()
    # print(rr)
    for l in rr.split('\\n'):
        # print(l)
        m=re.search('/temp/disFrame[0-9]+\.html',l)
        # print(m)
        if m:
            # print(m.group())
            url2=the_domain+m.group()
            get_nearby_from_parent(url2)
            # print(url2)
            r2 = urlopen(url2)
            rr2=r2.read()
            # print(rr2)
            for l2 in rr2.split('\\n'):
                m2=re.search('/temp/graFrame[0-9]+\.html',l2)
                if m2:
                    # print(m2.group())
                    url3=the_domain+m2.group()
                    # print(url3)
                    # r3 = urlopen(url3)
                    # rr3=r3.read()
                    # print(rr3)
                    rads=['250','500','750','1000']
                    res=[]
                    for rad in rads:
                        try:
                            # print('%s, %s'%(url3, rad))
                            rows=get_rows_from_graframe_url(url3, rad)
                            # pprint.pprint(rows)
                            if rows:
                                my_ret=get_info_from_graframe_rows(rows)
                                my_ret['radius']=rad
                                res.append(my_ret)
                        except:
                            print('ignoring exception (asdf34)')
                    # for myres in res:
                        # pprint.pprint(myres)
                    ret['entries']=res
                    # pprint.pprint(get_info_from_graframe_rows(get_rows_from_graframe_url(url3, '500')))
                    # soup = BeautifulSoup(urlopen(form.click()).read())
                    # print(soup.prettify())
    # soup = BeautifulSoup(response.read())
    # fr_url=the_domain+soup.find(SRC=re.compile("disFrame"))
    # print(soup.find("title"))
    # fr_url=the_domain+soup.find("Frame")
    # print(fr_url)
    # forms = ParseResponse(s, backwards_compat=False)
    # print(forms)
    # form = forms[0]
    # print form
    return ret
    
def main():
    
    pprint.pprint(get_radius_data('get_radius_data')) 
    
    
if __name__ == '__main__':
    # sys.exit(main())
    unittest.main()
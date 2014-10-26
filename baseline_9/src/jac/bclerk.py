from BeautifulSoup import BeautifulSoup
from mechanize import ParseResponse, urlopen
import re
import itertools

def get_legal_by_case(case):
    print('get_legal_by_case("'+case+')"')
    ret={}
    
    uri = 'http://web1.brevardclerk.us/oncoreweb/search.aspx'
    response = urlopen(uri)
        
    forms = ParseResponse(response, backwards_compat=False)
    form = forms[0]
    # print form
    
    form["txtCaseNumber"] = case #"orozco"
    form["SearchType"] = 'casenumber' #"orozco"
    # form["txtName"] = "orozco"
    soup = BeautifulSoup(urlopen(form.click()).read())
    # print soup.renderContents()
    
    
    # bi_cell = soup.find(text="                                                                                                LT 22 BLK 10 PB 5 PG 20 EAU GALLIE SHORES S 35 T 26 R 37 SUBID 02")
    bi_cell = soup.findAll(text=re.compile('.*SUBID.*'))#"td", { "class" : "stdFontResults" })
    # print(bi_cell)
    for b in bi_cell:
        # print(b.strip())
        temp = get_legal_from_str(b.strip())
        if temp:
            ret = dict(itertools.chain(ret.items(), temp.items()))
            break
    print(ret)
    return ret
    
def get_legal_from_str(the_str):
    print('get_legal_from_str('+the_str+')')
    ret={}
    m = re.search('(LT (?P<lt>[0-9a-zA-Z]+) (BLK (?P<blk>[0-9a-zA-Z]+) )?)?PB (?P<pb>\d+) PG (?P<pg>\d+) (?P<subd>.*) S \d+ T \d+ R \d+ SUBID (?P<subid>[0-9a-zA-Z]+)', the_str)
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
    return ret
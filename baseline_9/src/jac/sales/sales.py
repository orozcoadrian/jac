import requests
from bs4 import BeautifulSoup

def get_rows(the_html):
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
        rows.append(current_row)
    # pprint.pprint(rows)
    return rows

def get_items():
    r = requests.get('http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html')
    return get_rows(r.content)

def add_foreclosures(mrs, limit=None):
    all2 = get_items()
    print('all:' + str(len(all2)))
    to_set = all2
    if limit is not None:
        to_set = all2[:limit]
    print('to_set:' + str(len(to_set)))
    mrs.set_items(to_set)

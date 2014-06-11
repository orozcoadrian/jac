import requests
print("hello")
r = requests.get('http://vweb2.brevardclerk.us/Foreclosures/foreclosure_sales.html')
lines = r.text.split('\n')
print(lines)
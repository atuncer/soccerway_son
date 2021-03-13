import requests
from bs4 import BeautifulSoup

def getsite(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return result

def getDetails(soup):
    details = soup.find('div', {'class', 'details'})
    details2 = ''
    detail = ''
    for item in details.findChildren(recursive=False):
        if item.text != '':
            details2 += (item.text + ',')
    for item in details2.split('\n'):
        detail += item

    x = detail.split(',')
    arrr = x[0].split('/')
    crct = arrr[2] + '/' + arrr[1] + '/' + arrr[0]
    res = crct + ',' + x[1] + ',' + x[3] + ',' + x[5] + ',' + x[7]
    return res

result = getsite('https://uk.soccerway.com/matches/2021/03/06/turkey/super-lig/denizlispor/malatya-belediyespor/3353047/')
soup = BeautifulSoup(result.text, 'lxml')
details = getDetails(soup)
print(details)


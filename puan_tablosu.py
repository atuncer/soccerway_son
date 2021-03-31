import requests
import csv
from lxml import html
from bs4 import BeautifulSoup
import psycopg2 as psy
con = psy.connect(
    host = "db-bahispesinde1.cwln7t9ajzcz.eu-central-1.rds.amazonaws.com",
    database = "postgres",
    user = "Adminov",
    password = "amdin2323",
    port = "5435"
)

url = ['/england/premier-league/20202021/regular-season/r59136/', '/italy/serie-a/20202021/regular-season/r59286/', '/france/ligue-1/20202021/regular-season/r58178/', '/germany/bundesliga/20202021/regular-season/r58871/', '/spain/primera-division/20202021/regular-season/r59097/', '/turkey/super-lig/20202021/regular-season/r59187/']
puan = ["puan_premier", "puan_seriea", "puan_ligue1", "puan_bundesliga", "puan_laliga", "puan_superlig"]

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

def https(x,xxx=0):
    if xxx != 0:
        return  f"https://uk.soccerway.com{x}"
    return f"https://uk.soccerway.com/national{x}tables"


def gettable():
    '''
       premierlig/tables tarzı linkle çalışır
    '''
    for z in range(6):
        result = requests.get(https(url[z]), headers=headers)
        soup = BeautifulSoup(result.text, 'lxml')
        x = soup.find(lambda tag: tag.has_attr('id') and tag['id'] == "page_competition_1_block_competition_tables_10_block_competition_league_table_1_table")
        x = soup.find('tbody')

        inner(x, z)
        #logos(x, z)


def logos(x,z):
        tr = x.find_all('tr')
        for j in tr:
            href = j.find('a',href=True)
            print(href['title'],end=', ')
            reslt = requests.get(https(href['href'],1), headers=headers)
            soup = BeautifulSoup(reslt.text, 'lxml')
            img=soup.find('div',{"class","logo"}).find('img')
            print(img['src'])


def inner(x, z):
    result11 = ''
    for i in range(0, 30):
        tr = x.find_all('tr')
        result11 += f"insert into {puan[z]} values("
        for j in range(0, 12):

            try:
                td = tr[i].find_all('td')
            except IndexError:
                return

            if j == 2:
                result11 += "$$" + td[j].find('a').get('title') + "$$" + ','
            elif j == 11:
                result11 += "$$"
                for item in td[j].text:
                    if item != '\n':
                        result11 += item + ','
                result11 += "$$"
            elif j != 1:

                result11 += td[j].text + ','
        result11 += ")"
        with con.cursor() as cur:
            cur.execute(result11)
            con.commit()
        print(result11)
        result11 = ''


def getLiveGames():
    '''
    premierlig/matches tarzı linkle çalışır
    '''
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    x = soup.find("table")

    y = x.find("td", {"class": "date"})
    checkIfLive = (True if y.text.strip() == 'Live' else False)

    if checkIfLive is True:

        z = x.find_all("tr", {"data-status": "Playing"})
        for j in range(len(z)):
            for i in range(len(z[j].find_all('td'))):

                td = z[j].find_all('td')
                if i == 2:
                    href = td[i].find("a", href=True)
                    print(href['href'])
                    getEvents(href['href'])

    # print(z.prettify())


def getEvents(URL):
    url = "https://uk.soccerway.com" + URL

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')

    z = soup.find("ul", {"class": "scorer-info"})
    if z is not None:
        for li in z.find_all('li'):
            for i in range(4):
                span = li.find_all('span', recursive=False)
                if i == 0:
                    try:
                        print('goal: ' + span[0].find('a').text.strip() + ' ' + str(
                            span[0].find('a').next_sibling).strip())
                    except AttributeError:
                        print('goal: ' + span[2].find('a').text.strip() + ' ' + str(
                            span[2].find('a').next_sibling).strip())

                    try:
                        print('minute: ' + span[0].find("span", {"class": "minute"}).text.strip())
                    except AttributeError:
                        print('minute: ' + span[2].find("span", {"class": "minute"}).text.strip())

                    try:
                        print('assist by: ' + span[0].find("span", {"class": "assist"}).find('a').text.strip())
                    except AttributeError:
                        try:
                            print('assist by: ' + span[2].find("span", {"class": "assist"}).find('a').text.strip())
                        except AttributeError:
                            continue

                if i == 1:
                    print('score: ' + span[i].text)
                    print()
    else:
        print('Gol Yok')



gettable()

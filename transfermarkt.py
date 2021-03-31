import psycopg2
import requests
from bs4 import BeautifulSoup
import psycopg2 as psy
import scheduled

#sites = ['/super-lig/startseite/wettbewerb/TR1','/1-bundesliga/startseite/wettbewerb/L1','/premier-league/startseite/wettbewerb/GB1','/primera-division/startseite/wettbewerb/ES1','/serie-a/startseite/wettbewerb/IT1','/ligue-1/startseite/wettbewerb/FR1']
sites = ['/super-lig/startseite/wettbewerb/TR1']
def https(item): return f"https://www.transfermarkt.com.tr{item}"


def outerloop():

    for site in sites:
        html = scheduled.getsite(https(site))
        soup = BeautifulSoup(html.text, 'lxml')
        item: BeautifulSoup

        for item in soup.find("table",{'class','items'}).find('tbody').find_all('tr'):
            innerloop1(item.find('a')['href'])

def innerloop1(link):

    html = scheduled.getsite(https(link))
    soup = BeautifulSoup(html.text, 'lxml')
    item: BeautifulSoup


    for item in soup.find("table",{'class','items'}).find('tbody').find_all('tr',recursive=False):
        print(item.find('a',{'class','spielprofil_tooltip'}).text,end=', ')
        print(item.find('td',{'class','rechts hauptlink'}).text)




if __name__ == '__main__':
    outerloop()
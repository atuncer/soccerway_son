import psycopg2
import requests
from bs4 import BeautifulSoup
import psycopg2 as psy
con = psy.connect(
    host = "db-bahispesinde1.cwln7t9ajzcz.eu-central-1.rds.amazonaws.com",
    database = "postgres",
    user = "Adminov",
    password = "amdin2323",
    port = "5435"
)

leagues = ['https://uk.soccerway.com/national/england/premier-league/','https://uk.soccerway.com/national/italy/serie-a/','https://uk.soccerway.com/national/spain/primera-division/','https://uk.soccerway.com/national/germany/bundesliga/','https://uk.soccerway.com/national/france/ligue-1/','https://uk.soccerway.com/national/turkey/super-lig/']
leagues_sql = ['lig_premier','lig_seriea','lig_laliga','lig_bundesliga','lig_ligue1','lig_superlig']
fikstur_sql = ['fikstur_premier','fikstur_seriea','fikstur_laliga','fikstur_bundesliga','fikstur_ligue1','fikstur_superlig']
league_names = ['Premier League','Serie A ','La Liga,','La Liga','Ligue 1','Süper Lig']



def getsite(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return result


def outermain():

    for inx in range(len(leagues)):
        oldurl = f"https://uk.soccerway.com/a/block_competition_matches_summary?block_id=page_competition_1_block_competition_matches_summary_10&callback_params=%7B%22page%22%3A%2217%22%2C%22block_service_id%22%3A%22competition_summary_block_competitionmatchessummary%22%2C%22round_id%22%3A%2258178%22%2C%22outgroup%22%3A%22%22%2C%22view%22%3A%221%22%2C%22competition_id%22%3A%2216%22%7D&action=changePage&params=%7B%22page%22%3A0%7D"
        yr = 20 #2020-2021

        year = getYear(yr)
        code = getCode(year,inx)

        url = urlChangerYearly(oldurl, code)

        # try:
        mainloop(url,inx)
        # except :  #IMPORTANT ÇOK TEHLİKELİ ÇOKKKK, HATA ALAMIYORSAN BUNU SİL
        #     continue



def urlchanger_week(url, index):
    y = []
    for i in range(50):
        if url[-i] == '%':
            y.append(-i)
            if len(y)==2:
                return url[:y[1]] + (url[y[1]:y[1]+3]) + str(index) + url[y[0]:] #TODO eksiyi çıkar


def getall(url,index):
    flag1 = True

    result = getsite(url)
    soup = BeautifulSoup(result.text, 'lxml')
    team1, team2 = getTeams(soup)  # DONE
    try:
        halftime, fulltime = getScores(soup)  # DONE
    except AttributeError:
        return
    details = getDetails(soup)
    goalstats = getGoals(soup)
    coach1, coach2 = getCoaches(soup)
    referee = getRef(soup)
    d = details.split(',')
    arrAsText = f"{team1}, {halftime}, {team2}, {fulltime}, {details},{goalstats}, {coach1}, {coach2}, {referee}, {str(goalstats).strip()})"
    dct = {'takim1':team1, 'ms':fulltime, 'takim2':team2, 'iy':fulltime, 'tarih':d[0], 'lig':d[1], 'hafta':d[2], 'saat':d[3], 'stadyum':d[4], 'goller':goalstats, 'tekadam1':coach1, 'tekadam2':coach2, 'hakem':referee, 'link':url}
    arr = arrAsText.split(',')
    if len(fulltime) < 2 or fulltime is None:
        return
    with con.cursor() as cur:
        lig = leagues_sql[index]
        fix = fikstur_sql[index]

        if flag1:
            cmd2 = f'Insert into {lig} values($${dct["takim1"]}$$,$${dct["ms"]}$$,$${dct["takim2"]}$$,$${dct["iy"]}$$,\'{dct["tarih"]}\',$${dct["lig"]}$$,\'{dct["hafta"]}\',$${dct["saat"]}$$,$${dct["stadyum"]}$$,$${dct["goller"]}$$,$${dct["tekadam1"]}$$,$${dct["tekadam2"]}$$,$${dct["hakem"]}$$,\'{dct["link"]}\')'
            cmd3 = f'DELETE FROM {fix} where link = $${dct["link"]}$$'
            try:
                cur.execute(cmd2)
            except psycopg2.errors.UniqueViolation:
                pass
            cur.execute(cmd3)
        con.commit()

def prettylink(semiurl):
    urltolist = (semiurl.split('\\'))
    resultsemiurl = ''
    for item in urltolist:
        resultsemiurl += item
    return resultsemiurl


def getTeams(soup):
    teams = soup.find_all('a', {'class', 'team-title'})
    return teams[0].text, teams[1].text


def getScores(soup):
    scores = soup.find('h3', {'class', 'thick scoretime'})
    spans = scores.find_all('span')
    try:
        ht1 = spans[1].text
    except IndexError:
        pass

    ht = ""
    for ch in ht1:
        if ((48 <= ord(ch) <= 57) or ord(ch) == 45) and (ord(ch) != 38):  # sadece '-' ve sayı almak için
            ht += ch

    ft = str(spans[0].next_sibling).strip()
    return ht, ft


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
    res = crct + ',' + x[1] + ',' + x[3] + ',' + x[5][:5] + ',' + x[7]
    return res


def getGoals(soup):
    z = soup.find("ul", {"class": "scorer-info"})
    goals = ""
    if z is not None:
        for li in z.find_all('li'):

            span = li.find_all('span', recursive=False)
            try:
                goals += ('Gol: ' + span[0].find('a').text.strip() + ' ' + str(
                    span[0].find('a').next_sibling).strip() + ',')

            except AttributeError:
                goals += ('Gol: ' + span[2].find('a').text.strip() + ' ' + str(
                    span[2].find('a').next_sibling).strip() + ',')

            try:
                goals += ('Dakika: ' + span[0].find("span", {"class": "minute"}).text.strip() + ',')
            except AttributeError:
                goals += ('Dakika: ' + span[2].find("span", {"class": "minute"}).text.strip() + ',')

            try:
                goals += ('(Asist: ' + span[0].find("span", {"class": "assist"}).find(
                    'a').text.strip() + ')' + ',')
            except AttributeError:
                try:
                    goals += ('(Asist: ' + span[2].find("span", {"class": "assist"}).find(
                        'a').text.strip() + ')' + ',')
                except AttributeError:
                    pass

            goals += ('Skor: ' + span[1].text + ',')
    return goals[:-1]


def getCoaches(soup):
    coach1, coach2 = '', ''
    try:
        coach1 = soup.find('div', {'class', 'combined-lineups-container'}).find_all('tbody')[0].find_all('tr', recursive=False)[-1].find('a').text
    except:
        pass
    try:
        coach2 = soup.find('div', {'class', 'combined-lineups-container'}).find_all('tbody')[1].find_all('tr', recursive=False)[-1].find('a').text
    except:
        pass
    return coach1, coach2


def getRef(soup):
    try:
        ref = soup.find(text='Referee:').parent.parent.find_all('td')[-1].text
        return ref
    except AttributeError:
        return ""


def getYear(year):
    if year >= 12:
        return "20"+str(year)+"20"+str(year+1)
    else:
        if (len(str(year)) == 1) and (len(str(year+1)) == 1):
            return "200"+str(year)+"-200"+str(year+1)
        elif (len(str(year)) == 1) and (len(str(year+1)) == 2):
            return "200" + str(year) + "-20" + str(year + 1)
        else:
            return "20" + str(year) + "-20" + str(year + 1)


def getCode(year,index):  # TODO liglerin linkini değiştir
    reulst = getsite(leagues[index]+str(year))
    return reulst.url.split('/')[-2][1:]


def urlChangerYearly(url, code):
    a = (url.split('round_id')[1].split('%')[3])
    b = a[:2]
    b += code
    newurl = url.replace(a, b)
    return newurl


def getLastWeek(index):
    fix = fikstur_sql[index]
    cmd = f"select distinct(hafta) from {fix} where (tarih + saat)< (now() - interval '3 hours') and lig = '{league_names[index]}' order by hafta asc"
    with con.cursor() as cur:
        cur.execute(cmd)
        return cur.fetchall()


def mainloop(url,index):
    try:
        glw = getLastWeek(index)
        ignored = glw[0]  # glw[0]ın varlığını kontrol etmek için bu satır
    except IndexError:
        return
    for week in glw:
        urlnew = urlchanger_week(url, week[0]-1)

        result = getsite(urlnew)
        if result.status_code == 404:
            return urlchanger_week(urlnew, 0)

        soup = BeautifulSoup(result.text, 'lxml')
        tbody = soup.find('tbody')
        divs = tbody.find_all("div")

        print("week " + str(week[0]))

        for div in divs:
            links = div.find_all('a')[1]['href']
            link = ("https://uk.soccerway.com" + prettylink(links[2:-1]))
            print(link)
            getall(link, index)


if __name__ == "__main__":
    outermain()

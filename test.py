import requests

a = []

def getsite(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    result = requests.get(url, headers=headers)
    return result


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


def getCode(year):  # TODO liglerin linkini değiştir
    result = getsite('https://uk.soccerway.com/national/england/premier-league/'+str(year))

    return result.url.split('/')[-2][1:]


if __name__ == '__main__':
    for i in range(20, -1, -1):
        a.append(getCode(getYear(i)))
    print(a)

import requests
import re

def createTiles():
    url = "https://www.reddit.com/r/DotA2/wiki/config/stylesheet"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'}

    response = requests.get(url, headers)
    response.connection.close()

    pattern = "(hero|org|pennant|custom)-?(?P<hero_name>\w+)&quot;]:after[ ]+\{background-position: 0 -??(?P<amount>\d+)px}"


    patternMatches = re.findall(pattern, response.text, re.I)
    #p = re.compile('(hero|org|pennant|custom)-?(?P<hero_name>\w+)&quot;]:after[ ]+\{background-position: 0 -??(?P<amount>\d+)px}', re.IGNORECASE)
    #patternMatches = re.findall(p, response.text)

    flairs = {}
    categories = ['hero', 'org', 'pennant', 'custom']
    for category in categories:
        flairs[category] = {}

    for patternMatch in patternMatches:
        pcategory = patternMatch[0]
        pname = patternMatch[1]
        pposition = patternMatch[2]

        wflair = '[](/%s-%s)' %(pcategory, pname)

        flairs[pcategory][wflair] = {'category': pcategory,
                                    'name': pname,
                                    'position': pposition,
                                    'self': wflair}


    finalString = ''

    for org in flairs:
        for flair in flairs[org]:
            finalString += flair

    print(finalString)



    #print(response.text)
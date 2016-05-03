import requests
import re

from PIL import Image


def test():
    image_folder = 'mosaic/tilesorigin/'
    categories = ['hero', 'org', 'pennant', 'custom']

    for category in categories:
        image_path = image_folder + category + '.png'

        img = Image.open(image_path)
        width, height = img.size

        print('width: %s, height: %s' %(width, height))

        left = 0
        upper = 28
        width = 50
        lower = upper + 28

        bbox = (left, upper, width, lower)

        cropped_image = img.crop(bbox)

        cropped_image.save('mosaic/tiles/firsttest.png')

        return



    return


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
        filename = '%s-%s' %(pcategory, pname)

        flairs[pcategory][wflair] = {'category': pcategory,
                                    'name': pname,
                                    'position': pposition,
                                    'self': wflair,
                                    'filename': filename}

    if True:                           #test
        finalString = ''
        for org in flairs:
            for flair in flairs[org]:
                finalString += flair
        print(finalString)


    image_folder = 'mosaic/tilesorigin/'

    for org in flairs:
        image_path = image_folder + org + '.png'

        img = Image.open(image_path)
        width, height = img.size

        print('width: %s, height: %s' %(width, height))

        for flair in flairs[org]:
            left = 0
            upper = int(flairs[org][flair]['position'])
            width = 50
            lower = upper + 28

            bbox = (left, upper, width, lower)

            cropped_image = img.crop(bbox)

            cropped_image.save('mosaic/tiles/' + flairs[org][flair]['filename'] + '.png')

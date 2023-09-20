import requests
from bs4 import BeautifulSoup


def getNames(url):
    try:
        response = requests.get(url)
    except Exception:
        return None, None, None

    if response.status_code != 200:
        return None, None, None
    htmlContent = response.text
    soup = BeautifulSoup(htmlContent, 'html.parser')

    yearDiv = soup.find('div', class_='year-label')
    year = None
    if yearDiv:
        year = yearDiv.decode_contents()

    namesBox = soup.find('table', class_='employees table--small')
    names = []
    missingNames = False
    # can put in title if wanted
    if namesBox:
        shortListNames = namesBox.find_all(
            'tr', class_='employee-row shortlist')
        rowNames = namesBox.find_all('tr', class_='employee-row')
        if shortListNames:
            for name in shortListNames:
                paddedName = name.find('td', class_='padded-right')
                if paddedName is not None:
                    names.append(paddedName.contents[0].strip())
                else:
                    missingNames = True
        if rowNames:
            for name in rowNames:
                paddedName = name.find('td', class_='padded-right')
                if paddedName is not None:
                    names.append(paddedName.contents[0].strip())
                else:
                    missingNames = True
    else:
        return None, None, None
    return names, year, missingNames

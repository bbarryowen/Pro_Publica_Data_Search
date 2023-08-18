import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def searchByClass(webURL):
    response = requests.get(webURL)
    if response.status_code != 200:
        print(f"failed to get url, status: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    a_element = soup.find('a', class_='action xml')
    if a_element is None:
        return None, None
    href = a_element.get('href')
    formType = a_element.text
    return href, formType


def getNames(url):
    pageURL = url

    href, formType = searchByClass(pageURL)

    if href is None:
        print(f"could not find button for {url}")
        return None
    if formType != str(990):
        print("program not yet capable of handling non 990 forms")
        return None

    xmlURL = f'https://projects.propublica.org{href}'
    response = requests.get(xmlURL, allow_redirects=True)
    if response.status_code == 200:
        xmlContent = response.content
        # print(xmlContent)
    else:
        print(f"failed to fetch xml file {response.status_code}")
        return
    root = ET.fromstring(xmlContent)

    namespace = {'irs': 'http://www.irs.gov/efile'}

    elements = root.findall(
        './/irs:Form990PartVIISectionAGrp', namespaces=namespace)
    count = 0
    names = []
    for element in elements:
        person = element.find('irs:PersonNm', namespaces=namespace)
        if person is None:
            count += 1
        else:
            names.append(person.text)

    if count > 0:
        print(f"{count} board members were not recorded for url: {url}")

    return names


def getBoardMemebers(names: str):
    return {"A": names, "B": None, "C": None, "D": None, "E": None}


def organizationSearch():
    params = "AHEPA 23 II, Inc."
    searchURL = f"https://projects.propublica.org/nonprofits/api/v2/search.json?q=AHEPA%2023%20II%2C%20Inc."

    response = requests.get(searchURL)
    print(response.json())

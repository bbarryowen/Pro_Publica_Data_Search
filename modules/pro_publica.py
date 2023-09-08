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
        return None, None, None, None, None

    xmlURL = f'https://projects.propublica.org{href}'
    response = requests.get(xmlURL, allow_redirects=True)
    if response.status_code == 200:
        xmlContent = response.content
    else:
        print(f"failed to fetch xml file {response.status_code}")
        return None, None, None, None, None
    if formType == str(990):
        return get990Info(xmlContent)
    else:
        return get990ezInfo(xmlContent)


def get990ezInfo(xmlContent):
    # <OfficerDirectorTrusteeEmplGrp>
    root = ET.fromstring(xmlContent)

    namespace = {'irs': 'http://www.irs.gov/efile'}

    nameElements = root.findall(
        './/irs:OfficerDirectorTrusteeEmplGrp', namespaces=namespace)
    count = 0
    names = []
    for element in nameElements:
        person = element.find('irs:PersonNm', namespaces=namespace)
        if person is None:
            count += 1
        else:
            names.append(person.text)

    yearElement: str = root.find(
        './/irs:TaxPeriodBeginDt', namespaces=namespace)
    year = yearElement.text[0:4]

    return names, year, count, None, None


def get990Info(xmlContent):
    root = ET.fromstring(xmlContent)

    namespace = {'irs': 'http://www.irs.gov/efile'}

    nameElements = root.findall(
        './/irs:Form990PartVIISectionAGrp', namespaces=namespace)
    count = 0
    names = []
    for element in nameElements:
        person = element.find('irs:PersonNm', namespaces=namespace)
        if person is None:
            count += 1
        else:
            names.append(person.text)

    yearElement: str = root.find(
        './/irs:TaxPeriodBeginDt', namespaces=namespace)
    year = yearElement.text[0:4]

    irs990_element = root.find(".//irs:IRS990", namespaces=namespace)

    if irs990_element is not None:
        prevRevenueElement = irs990_element.find(
            ".//irs:PYTotalRevenueAmt", namespaces=namespace)
        currRevenueElement = irs990_element.find(
            ".//irs:CYTotalRevenueAmt", namespaces=namespace)
        if prevRevenueElement is not None:
            prevRevenue = prevRevenueElement.text
        else:
            prevRevenue = None
        if currRevenueElement is not None:
            currRevenue = currRevenueElement.text
        else:
            currRevenue = None
    else:
        prevRevenue = None
        currRevenue = None

    return names, year, count, prevRevenue, currRevenue


def getBoardMemebers(names: str):
    return {"A": names, "B": None, "C": None, "D": None, "E": None}

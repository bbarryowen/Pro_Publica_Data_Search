import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def searchByClass(webURL, className):
    response = requests.get(webURL)
    if response.status_code != 200:
        print(f"failed to get url, status: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    a_element = soup.find('a', class_='action xml')
    href = a_element.get('href')
    return href

def getNames(url):
    pageURL = url
    className = "action xml"

    href = searchByClass(pageURL, className)

    if href is None:
        exit()
    
    xmlURL = f'https://projects.propublica.org{href}'
    response = requests.get(xmlURL, allow_redirects=True)
    if response.status_code == 200:
        xmlContent = response.content
        #print(xmlContent)
    else:
        print(f"failed to fetch xml file {response.status_code}")
        exit()
    root = ET.fromstring(xmlContent)

    namespace = {'irs': 'http://www.irs.gov/efile'}

    elements = root.findall('.//irs:Form990PartVIISectionAGrp', namespaces=namespace)
    names = [[element.find('irs:PersonNm', namespaces=namespace).text] for element in elements]
    return names



    
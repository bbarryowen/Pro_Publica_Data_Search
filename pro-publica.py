import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def searchByClass(webURL, className):
    response = requests.get(webURL)
    if response.status_code != 200:
        print("failed to get url")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    a_element = soup.find('a', class_='action xml')
    href = a_element.get('href')
    return href

def getNames(href):
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
    names = [element.find('irs:PersonNm', namespaces=namespace).text for element in elements]
    return names



myURL = "https://projects.propublica.org/nonprofits/organizations/430240455"
className = "action xml"

href = searchByClass(myURL, className)
if href:
    print(getNames(href))
else:
    print("could not find 990 button")

















"""
ein = 430240455
baseURL = "https://projects.propublica.org/nonprofits/api/v2"
url = f'{baseURL}/organizations/:{ein}.json'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Process and use the data
    print(data['filings_without_data'][0])
else:
    print(f"API request failed. Status code: {response.status_code}")
"""
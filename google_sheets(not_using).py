from excel import getCompanyInfo
import gspread
from pro_publica import getNames

sa = gspread.service_account(
    "pro-publica-data-pull-30c8ab839726.json")
sh = sa.open("pro publica test sheet")
wks = sh.worksheet("Sheet1")


def insertNames(url):
    ein = str(url[-9:])
    foundRecord = wks.find(ein, in_column=2)
    insertPayload = getNames(url)
    insertPayload.append([""])

    if foundRecord:
        currentRow = foundRecord.row
        allRows = wks.get_all_values()
        allRows[currentRow - 1: currentRow + len(insertPayload)] = []
        wks.clear()
        wks.insert_rows(allRows, 1)
        insertData(insertPayload, ein)

    else:
        # nextRow = len(wks.get_all_values()) + 1 for insert at end instead of beginning
        insertData(insertPayload, ein)


def insertData(payload, ein):
    wks.insert_rows(payload, 2)
    wks.update_cell(2, 2, ein)


def addOrganization(propertyName, url):
    payload = getCompanyInfo(propertyName)
    companyID = payload[0][0]
    foundRecord = wks.find(str(companyID), in_column=1)
    if foundRecord:
        row = foundRecord.row + 2
        print("company already present, need to update")
        exit()
    else:
        payload.append(
            ["Board memeber name", "Phone number", "Email", "Adress"])
        for name in getNames(url):
            payload.append([name])
        wks.insert_rows(payload, 1)


def pullNames(startRow):
    pulledNames = []
    # doesnt deal with issue of no white space
    while isinstance(wks.cell(startRow, 1).value, str):
        pulledNames.append(wks.cell(startRow, 1).value)
    print(pulledNames)
    return pulledNames

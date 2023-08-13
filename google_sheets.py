import gspread
from pro_publica import getNames

sa = gspread.service_account(
    "/opt/anaconda3/lib/python3.7/site-packages/gspread/pro-publica-data-pull-1b44d9f07737.json")
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

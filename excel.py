from math import isnan
import pandas as pd
import openpyxl

from pro_publica import getBoardMemebers, getNames

filename = 'properties_output.xlsx'
workbook = openpyxl.load_workbook(filename)
worksheet = workbook.active

df1 = pd.read_excel('properties_sample_partial.xlsx')
df2 = pd.read_excel('properties_output.xlsx')


def getCompanyInfo(propertyName: str):
    index = getIndex(df1, "Property Name", propertyName)
    if isinstance(index, str):
        print(f"error: property: {propertyName} is not in file")
        return
    companyInfo = {"A": ["#", df1.loc[index, "#"]],
                   "B": ["Owner Organization Name", df1.loc[index, "Owner Organization Name"]],
                   "C": ["Property Name", df1.loc[index, "Property Name"]],
                   "D": ["Project Category", df1.loc[index, "Project Category"]],
                   "E": ["Owner Company Type", df1.loc[index, "Owner Company Type"]],
                   "F": ["Projects Units", df1.loc[index, "Projects Units"]],
                   "G": ["(Address) Line 1", df1.loc[index, "(Address) Line 1"]],
                   "H": ["(Address) City", df1.loc[index, "(Address) City"]],
                   "I": ["(Address) State", df1.loc[index, "(Address) State"]],
                   "J": ["(Address) Postal Code", df1.loc[index, "(Address) Postal Code"]],
                   "K": ["ProPublica Link", df1.loc[index, "ProPublica Link"]]}

    if not isinstance(companyInfo["K"][1], str):
        print(f"property: {propertyName} does not have link")
        return None, None, None
    names = getNames(companyInfo["K"][1])
    if names is None:
        return companyInfo, None
    boardMembersInfo = getBoardMemebers(names)
    return companyInfo, boardMembersInfo


def getIndex(dataFrame, searchColumn: str, searchValue):
    condition = dataFrame[searchColumn] == searchValue
    filteredDF = dataFrame[condition]
    if filteredDF.empty:
        return f"{searchValue} not in file"
    else:
        index = int(filteredDF.index[0])
        return index


def getFullData(propertyName):
    blankDict = {"A": [""], "B": [""], "C": [""], "D": [""], "E": [""],
                 "F": [""], "G": [""], "H": [""], "I": [""], "J": [""], "K": [""]}
    boardHeaderDict = {"A": ["Contact Name"], "B": [
        "Phone"], "C": ["Email"], "D": ["Adress"], "E": ["Notes"]}
    boardHeadDF = pd.DataFrame(boardHeaderDict)
    blankDF = pd.DataFrame(blankDict)
    companyDict, boardMembersDict = getCompanyInfo(propertyName)
    companyDF = pd.DataFrame(companyDict)

    propertyLocation = getIndex(df2, "A", companyDict["A"][1])

    # will be an issue if last property is updated
    if isinstance(propertyLocation, int):
        prevNames = []
        endRow = None
        for idx, name in enumerate(df2["A"][propertyLocation + 2:], start=propertyLocation + 2):
            if name == "#":
                endRow = idx
                break
            prevNames.append(name)

        df2Edited = df2.drop(df2.index[propertyLocation: endRow + 1])
        """if isnan(prevNames[-1]):
            prevNames.pop()"""
        if boardMembersDict is not None:
            currNames = boardMembersDict["A"]
        else:
            currNames = []
        deletedNames = list(set(prevNames) - set(currNames))
        addedNames = list(set(currNames) - set(prevNames))

        currDict = {"A": currNames}
        addedDict = {"A": addedNames}
        deletedDict = {"A": deletedNames}

        currDF = pd.DataFrame(currDict)
        deletedDF = pd.DataFrame(deletedDict)

        print("trying update")
        return pd.concat([companyDF, boardHeadDF, currDF, deletedDF, df2Edited], ignore_index=True)

    if boardMembersDict is None:
        return pd.concat([companyDF, boardHeadDF, blankDF, df2])

    boardDF = pd.DataFrame(boardMembersDict)
    return pd.concat([companyDF, boardHeadDF, boardDF, blankDF, df2], ignore_index=True)


def getFullDataFromList(propertyList):
    dfList = []
    for property in propertyList:
        print(property)
        fullData = getFullData(property)
        if fullData is not None:
            dfList.append(fullData)
    if len(dfList) != 0:
        combinedDFs = pd.concat(dfList, ignore_index=True)
        try:
            combinedDFs.to_excel('properties_output.xlsx', index=False)
            print("Excel file saved successfully.")
        except Exception as e:
            print("Error while saving Excel file:", e)


def getPropertyNames():
    return df1["Property Name"]

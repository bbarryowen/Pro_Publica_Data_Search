import os
import pandas as pd
from pro_publica import getBoardMemebers, getNames


def getCompanyInfo(propertyName: str):
    index = getIndex(df1, "Property Name", propertyName)
    if isinstance(index, str):
        return None, None

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
        errorProperties.append(f"{propertyName}: no link")
        return None, None
    names, year, notAdded, prevRevenue, currRevenue = getNames(
        companyInfo["K"][1])

    if names is None:
        errorProperties.append(f"{propertyName}: no button")
        return companyInfo, None
    if notAdded > 0:
        errorProperties.append(f"{propertyName}: {notAdded} names not added")
        return companyInfo, None

    companyInfo["L"] = ["Year", year]
    companyInfo["M"] = ["Revenue(previous year)", prevRevenue]
    companyInfo["N"] = ["Revenue(current year)", currRevenue]
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
    blankDF = pd.DataFrame(
        blankDict)
    companyDict, boardMembersDict = getCompanyInfo(propertyName)
    companyDF = pd.DataFrame(companyDict)

    if boardMembersDict is None:
        return pd.concat([companyDF, boardHeadDF, blankDF])

    boardDF = pd.DataFrame(boardMembersDict)
    return pd.concat([companyDF, boardHeadDF, boardDF, blankDF], ignore_index=True)


def getFullDataFromFile(inFilePath, outFileName, state, callback):
    if not os.path.exists(inFilePath):
        return 8, None, None
    if not inFilePath.lower().endswith((".xlsx")):
        return 3, None, None
    expandedPath = os.path.expanduser(outFileName)
    if not os.path.exists(os.path.dirname(expandedPath)):
        return 4, None, None
    if not outFileName.lower().endswith((".xlsx")):
        return 5, None, None

    global df1
    df1 = pd.read_excel(inFilePath)

    if state != "(all states)":
        df1 = df1[df1["(Address) State"] == state]
    # needs function to check this
    numProps, columns = df1.shape
    propertyList = getPropertyNames(df1)
    if isinstance(propertyList, int):
        return 6, None, None

    global errorProperties
    errorProperties = ["Properties with errors:"]
    dfList = []
    count = 0
    percent = 0
    for property in propertyList:
        count += 1
        percent = count / numProps * 100
        callback(int(percent))
        fullData = getFullData(property)
        if fullData is not None:
            dfList.append(fullData)
    if len(dfList) != 0:
        dfList.append(pd.DataFrame({"A": errorProperties}))
        combinedDFs = pd.concat(dfList, ignore_index=True)
        try:
            combinedDFs.to_excel(outFileName, index=False, header=False)
            return 0, len(propertyList), len(errorProperties) - 1
        except Exception as e:
            return 7, None, None


def getPropertyNames(inDF):
    try:
        propertyNameList = inDF["Property Name"]
        return propertyNameList
    except KeyError:
        return 4

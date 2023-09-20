import os
import pandas as pd
from pro_publica import getNames


def getCompanyInfo(propertyName: str, df1):
    index = getIndex(df1, "Property Name", propertyName)
    if isinstance(index, str):
        return None, None, None, None

    companyInfo = {"A": ["Property Number", df1.loc[index, "#"]],
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

    errorProperty = None
    missingProperty = None

    if not isinstance(companyInfo["K"][1], str):
        errorProperty = f"{propertyName}: no link"
        return companyInfo, None, errorProperty, None

    names, year, missing = getNames(
        companyInfo["K"][1])

    if names is None and year is None and missing is None:
        errorProperty = f"{propertyName}: invalid link"
        return companyInfo, None, errorProperty, None
    if missing:
        missingProperty = f"{propertyName}: unlisted names"
    if names == []:
        errorProperty = f"{propertyName}: no names"

    companyInfo["L"] = ["Fiscal year", year]
    boardMembersInfo = getBoardMemebers(names)

    return companyInfo, boardMembersInfo, errorProperty, missingProperty


def getIndex(dataFrame, searchColumn: str, searchValue):
    condition = dataFrame[searchColumn] == searchValue
    filteredDF = dataFrame[condition]
    if filteredDF.empty:
        return f"{searchValue} not in file"
    else:
        index = int(filteredDF.index[0])
        return index


def getFullData(propertyName, df1):
    blankDict = {"A": [""], "B": [""], "C": [""], "D": [""], "E": [""],
                 "F": [""], "G": [""], "H": [""], "I": [""], "J": [""], "K": [""]}
    boardHeaderDict = {"A": ["Contact Name"], "B": [
        "Phone"], "C": ["Email"], "D": ["Adress"], "E": ["Notes"]}
    boardHeadDF = pd.DataFrame(boardHeaderDict)
    blankDF = pd.DataFrame(
        blankDict)
    companyDict, boardMembersDict, erroredProp, missingNamesProp = getCompanyInfo(
        propertyName, df1)
    companyDF = pd.DataFrame(companyDict)

    if boardMembersDict is None:
        return pd.concat([companyDF, boardHeadDF, blankDF]), erroredProp, missingNamesProp

    boardDF = pd.DataFrame(boardMembersDict)
    return pd.concat([companyDF, boardHeadDF, boardDF, blankDF], ignore_index=True), erroredProp, missingNamesProp


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

    df1 = pd.read_excel(inFilePath)
    if "Property Number" in df1.columns or "#" not in df1.columns or "Owner Organization Name" not in df1.columns or "Property Name" not in df1.columns or "Project Category" not in df1.columns or "Owner Company Type" not in df1.columns or "Projects Units" not in df1.columns or "(Address) Line 1" not in df1.columns or "(Address) City" not in df1.columns or "(Address) State" not in df1.columns or "(Address) Postal Code" not in df1.columns or "ProPublica Link" not in df1.columns:
        return 6, None, None

    if state != "(all states)":
        df1 = df1[df1["(Address) State"] == state]

    propertyList = getPropertyNames(df1)

    numProps, columns = df1.shape

    errorProperties = []
    missingProperties = []

    dfList = []
    count = 0
    percent = 0
    for property in propertyList:
        count += 1
        percent = count / numProps * 100
        fullData, errorProp, missedNamesProp = getFullData(property, df1)
        if errorProp is not None:
            errorProperties.append(errorProp)
        if missedNamesProp is not None:
            missingProperties.append(missedNamesProp)
        if fullData is not None:
            dfList.append(fullData)
        callback(int(percent))

    if len(dfList) != 0:
        endMessage = ['Properties with errors:'] + errorProperties + \
            [""] + ['Properties with un-listed names:'] + missingProperties
        dfList.append(pd.DataFrame({"A": endMessage}))
        combinedDFs = pd.concat(dfList, ignore_index=True)
        try:
            combinedDFs.to_excel(outFileName, index=False, header=False)
            return 0, len(propertyList), len(errorProperties)
        except Exception as e:
            return 7, None, None


def getPropertyNames(inDF):
    try:
        propertyNameList = inDF["Property Name"]
        return propertyNameList
    except KeyError:
        return 4


def getBoardMemebers(names: str):
    return {"A": names, "B": None, "C": None, "D": None, "E": None}

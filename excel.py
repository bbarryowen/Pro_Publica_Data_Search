import pandas as pd
from pro_publica import getBoardMemebers, getNames


def getCompanyInfo(propertyName: str):
    index = getIndex(df1, "Property Name", propertyName)
    if isinstance(index, str):
        print(f"error: property: {propertyName} is not in file")
        return None, None

    try:
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
    except KeyError:
        print("error: specified columns defined in documentation do not exist; please review documentation.")
        exit(1)

    if not isinstance(companyInfo["K"][1], str):
        print(f"property: {propertyName} does not have link")
        errorProperties.append(propertyName)
        return None, None, None
    names, year, notAdded = getNames(companyInfo["K"][1])

    if names is None or not isinstance(notAdded, int):
        errorProperties.append(propertyName)
        return companyInfo, None

    companyInfo["L"] = ["Year", year]
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

    if boardMembersDict is None:
        return pd.concat([companyDF, boardHeadDF, blankDF])

    boardDF = pd.DataFrame(boardMembersDict)
    return pd.concat([companyDF, boardHeadDF, boardDF, blankDF], ignore_index=True)


def getFullDataFromFile(filePath, fileName):
    global df1
    df1 = pd.read_excel(filePath)
    global errorProperties
    errorProperties = ["Properties with errors:"]

    propertyList = getPropertyNames(df1)
    dfList = []
    for property in propertyList:
        print(f"adding: {property}")
        fullData = getFullData(property)
        if fullData is not None:
            dfList.append(fullData)
    if len(dfList) != 0:
        dfList.append(pd.DataFrame({"A": errorProperties}))
        combinedDFs = pd.concat(dfList, ignore_index=True)
        try:
            combinedDFs.to_excel(fileName, index=False)
            print(f"Excel file saved successfully: {fileName}")
            exit(0)
        except Exception as e:
            print("Error while saving Excel file:", e)
            exit(2)


def getPropertyNames(inDF):
    try:
        propertyNameList = inDF["Property Name"]
    except KeyError:
        print(f"error: inputed file does not have column: 'Property Name' please review documentation.")
        exit(1)
    return propertyNameList

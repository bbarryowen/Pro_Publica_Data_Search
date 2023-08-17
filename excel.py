import pandas as pd
import openpyxl

from pro_publica import getBoardMemebers, getNames

filename = 'properties_output.xlsx'
workbook = openpyxl.load_workbook(filename)
worksheet = workbook.active

df1 = pd.read_excel('properties_sample.xlsx')
df2 = pd.read_excel('properties_output.xlsx')


def getCompanyInfo(propertyName: str):
    index = getIndex(propertyName)
    if isinstance(index, str):
        print(f"error: property: {propertyName} is not in file")
        exit()
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
    names = getNames(companyInfo["K"][1])
    boardMembersInfo, boardHeader = getBoardMemebers(names)
    return companyInfo, boardMembersInfo, boardHeader


def getIndex(propertyName: str):
    condition = df1['Property Name'] == propertyName
    filteredDF = df1[condition]
    index = int(filteredDF.index[0]) + 2
    if filteredDF.empty:
        return f"{propertyName} not in file"
    else:
        return index


companyDict, boardMembersDict, boardHeader = getCompanyInfo("GRUENING PARK")
companyDF = pd.DataFrame(companyDict)
boardDF = pd.DataFrame(boardMembersDict)
boardHeadDF = pd.DataFrame(boardHeader)

combinedDF = pd.concat(
    [companyDF, boardHeadDF, boardDF, df2], ignore_index=True)

try:
    combinedDF.to_excel('properties_output.xlsx', index=False)
    print("Excel file saved successfully.")
except Exception as e:
    print("Error while saving Excel file:", e)

import pandas as pd

df = pd.read_excel('properties_sample.xlsx')


def getCompanyName(propertyName):
    index = getIndex(propertyName)
    if isinstance(index, str):
        print(f"error: property: {propertyName} is not in file")
        exit()
    companyName = df.loc[index, 'owner_organization_name']
    print(companyName)


def getIndex(propertyName: str):
    for index, row in df.iterrows():
        if row['property_name_text'].lower().strip() == propertyName.lower().strip():
            return index
    return f"{propertyName} not in file"


getCompanyName('Parkway Pl')

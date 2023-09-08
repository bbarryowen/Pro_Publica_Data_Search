import PySimpleGUI as sg
from excel import getFullDataFromFile


def updateCount(newCount):
    window["count"].update(value=f"{newCount}%")
    window.refresh()


layout = [
    [sg.Text("Select a file:")],
    [sg.InputText(key="file_path"), sg.FileBrowse()],
    [sg.Text("Select a state:\n(optional)"),
     sg.DropDown(values=['(all states)', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                         'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                         'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                         'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                         'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'], default_value='(all states)', key="state_drop_down")],
    [sg.Button("Load"), sg.Button("Exit")],
    [sg.Text("Enter Output File Name:\n(full file path)"), sg.InputText(
        key="default_file", default_text="~/downloads/output.xlsx")],
    [sg.Text("Percent complete:", key="prop_message", visible=False),
     sg.Text("", key="count", visible=False)]
]

window = sg.Window("ProPublica Name Search", layout)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Load":
        filePath = values["file_path"]
        fileName = values["default_file"]
        stateCode = values["state_drop_down"]

        window["prop_message"].update(visible=True)
        window["count"].update(visible=True)
        window.refresh()

        completionCode, numProps, numErrors = getFullDataFromFile(
            filePath, fileName, stateCode, updateCount)

        window["prop_message"].update(visible=False)
        window["count"].update(visible=False)
        window.refresh()

        if completionCode == 0:
            sg.popup(
                f"run complete: names found for {numProps - numErrors} out of {numProps} given properties")
        elif (completionCode == 3):
            sg.popup("Inputted file must be an excel file")
        elif (completionCode == 4):
            sg.popup("Please provide valid output file path")
        elif (completionCode == 5):
            sg.popup(
                "out put file path must be an excel file (ending in .xlsx)")
        elif (completionCode == 6):
            sg.popup(
                "Excel file must have specified column names, please review documentation")
        elif (completionCode == 7):
            sg.popup("Error while saving excel file")
        elif (completionCode == 8):
            sg.popup("inputted file does not exist")

window.close()

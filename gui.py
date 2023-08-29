import PySimpleGUI as sg
import subprocess

layout = [
    [sg.Text("Select a file:")],
    [sg.InputText(key="file_path"), sg.FileBrowse()],
    [sg.Button("Load"), sg.Button("Exit")],
    [sg.Text("Enter Output File Name:"), sg.InputText(
        key="default_file", default_text="output.xlsx")]
]

window = sg.Window("File Loader", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Load":
        file_path = values["file_path"]
        file_name = values["default_file"]
        sg.popup(f"Selected file: {file_path}")
        subprocess.run(["python", "main.py", file_path, file_name])

window.close()

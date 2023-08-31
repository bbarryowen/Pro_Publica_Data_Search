import traceback
import PySimpleGUI as sg
import subprocess
import os

try:
    layout = [
        [sg.Text("Select a file:")],
        [sg.InputText(key="file_path"), sg.FileBrowse()],
        [sg.Button("Load"), sg.Button("Exit")],
        [sg.Text("Enter Output File Name:\n(full file path)"), sg.InputText(
            key="default_file", default_text="~/downloads/output.xlsx")],
        [sg.Text("running...", key="running_message",
                 visible=False)]
    ]

    window = sg.Window("ProPublica Name Search", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Load":
            filePath = values["file_path"]
            fileName = values["default_file"]
            sg.popup(f"Selected file: {filePath}")

            window["running_message"].update(visible=True)
            window.refresh()

            subprocessResult = subprocess.run(
                ["python", "main.py", filePath, fileName], text=True, capture_output=True)

            window["running_message"].update(visible=False)
            window.refresh()

            subprocessOutput = subprocessResult.stdout.strip()
            completionCode = subprocessResult.returncode
            sg.popup(
                f"run complete. completion code: {completionCode}.")

    window.close()
except Exception as e:
    print("An error occurred:", str(e))
    traceback.print_exc()

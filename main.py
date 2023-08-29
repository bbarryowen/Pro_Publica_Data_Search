import sys
from excel import getFullDataFromFile, getPropertyNames


def main():
    if len(sys.argv) != 3:
        print("Usage: main_script.py <file_path>")
        return
    filePath = sys.argv[1]
    outputFileName = sys.argv[2]
    print(f"running main for file: {filePath}")
    getFullDataFromFile(filePath, outputFileName)


if __name__ == "__main__":
    main()

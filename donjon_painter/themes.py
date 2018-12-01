from pathlib import Path

# Retrieve list of theme directories
def getThemes():
    themeList = []

    imgLoc = Path(__file__).parent.resolve()
    imgLoc = Path(imgLoc, 'theme')

    for item in imgLoc.iterdir():
            if item.is_dir():
                themeList.append(item)

    themeList = sorted(themeList)
    return themeList


# Display all builtin themes
def printThemes():
    curList = getThemes()
    print("===Theme List===")
    for index, item in enumerate(curList):
        themeName = item.parts
        print("\t[" + str(index) + "]: " + themeName[-1])


# Return desired theme folder
def getFolder(curTile):
    themes = getThemes()
    themeIndex = list(str(item) for item in options)
    selection = input()

    if selection in themeIndex:
        curTile = themes[int(sel)]
    else:
        print("Invalid selection!")
    return curTile

import os
import sys
import csv
from pathlib import Path

# Get dungeon tile set (or pick from preinstalled ones)
def getTheme(tileset):
    if not tileset:
        themeList = []
        
        imgLoc = Path(__file__).parent.resolve()
        imgLoc = Path(imgLoc, 'themes')
        
        for item in imgLoc.iterdir():
            if item.is_dir():
                themeList.append(item)
        
        themeList = sorted(themeList)
        
        print("Theme folder not specified! Select one of the pre-built themes below or type in your folder location now:")
        for index, item in enumerate(themeList):
            themeName = item.parts
            
            print("\t[" + str(index) + "]: " + themeName[-1])
        
        options = range(0, len(themeList))
        validSel = list(str(item) for item in options)
        selection = input()
        
        if selection in validSel:
            return themeList[int(selection)]
        elif Path(selection).is_dir():
            return Path(selection)
        else:
            print("Invalid theme selection! Exiting...")
            sys.exit()
    else:
        return tileset

# Reads in Donjon's TSV file
def createMapArray(tsvMap):
    tmpArray = []
    if Path(tsvMap).is_file():
        with open(tsvMap) as fd:
            rd = csv.reader(fd, delimiter="\t")
            for row in rd:
                tmpArray.append(row)

    else:
        print("Map file not found! Exiting...")
        sys.exit()
            
    return tmpArray

# Checks for the presence of image directory, then returns it
def createImageDirectory(tileLoc):
    tempPath = Path.cwd()
    if Path(tileLoc).exists():
        tempPath = Path(tileLoc)
    return tempPath

import themes
import imgmap
import time


# ==================== List of menu option functions ==================== #
def setTSV(args):
    print("Current TSV file:", args.MAPFILE)
    print("Enter in the location + name of your TSV file.")
    args.MAPFILE = input()
    return args


def setTheme(args):
    print("Current theme:", args.tileset)
    print("Get inbuilt theme? (y/N)")

    getNative = input()
    if getNative == 'y' or getNative == 'Y':
        themes.printThemes()
        args.tileset = themes.selTheme(args.tileset)
    else:
        print("Enter in your theme directory.")
        args.tileset = input()

    return args


def setSave(args):
    print("Current save directory:", args.savetiles)
    print("Enter name/location/location + name to save your map image.")
    args.savetiles = input()
    return args


def setSize(args):
    print("Current tile size:", args.pixels)
    print("Enter in the new size of your tiles.")

    newSize = input()
    if newSize.isdigit():
        args.pixels = int(newSize)
        print("Size set to", newSize)
    else:
        print("Invalid input!")

    return args


def togMetric(args):
    args.measure ^= True
    return args


def togRandom(args):
    args.randomise ^= True
    return args


def genTheme(args):
    print("Attempting theme generation at", args.tileset)
    start = time.time()
    if themes.writeTheme(args.tileset) is False:
        print("Insufficient resources to generate theme.")
    else:
        if args.measure:
            end = time.time()
            print("Done in", end - start, "seconds.")


def genMap(args):
    print("Attempting map generation to", args.output)
    start = time.time()
    if imgmap.writeMap(args) is False:
        print("Insufficient resources to generate map.")
    else:
        if args.measure:
            end = time.time()
            print("Done in", end - start, "seconds.")


def progExit():
    print("Exiting menu...")


choices = {
        "Select TSV File": setTSV,
        "Select Theme": setTheme,
        "Set Save Location": setSave,
        "Set Tile Size": setSize,
        "Toggle Savetime Metrics": togMetric,
        "Toggle Floor Shuffling": togRandom,
        "Generate Theme": genTheme,
        "Generate Map Image": genMap,
        "Exit Generator": progExit
    }
# ==================== End of map menu options ==================== #


def getSettings(args):
    optList = {
        "TSV Map File": args.MAPFILE,
        "Tile Theme Folder": args.tileset,
        "Save Location": args.output,
        "Tile Size (Pixels)": args.pixels,
        "Measure Save Time": args.measure,
        "Shuffle Floor": args.randomise,
        "Generate Theme": args.savetiles
    }
    for i, val in optList.items():
        print(i + ':\t', val)


def getOptions():
    for i, (key, val) in enumerate(choices.items()):
        print('[' + i + ']', key)


def mainmenu(args):
    option = None
    while option != (len(choices) - 1):
        getSettings(args)
        print()
        getOptions()
        print("Select option: ", end='')

        tmpOpt = input()
        # Execute linked option
        if input().isdigit():
            option = int(tmpOpt)
            keyOpt = list(choices)[option]

            # No arguments for exiting
            if keyOpt < len((choices) - 2):
                args = choices[keyOpt](args)
            else:
                choices[keyOpt]
        else:
            print("Invalid option!")
    print("Exiting...")

# List of menu option functions
def setTSV(args):
    print("Current TSV file:", args.MAPFILE)
    print("Enter in the location + name of your TSV file.")


def setTheme(args):
    print("Current theme:", args.tileset)
    print("Get inbuilt theme? (y/N)")


def setSave(args):
    print("Current save directory:", args.savetiles)
    print("Enter in the location to save your map image.")


def setSize(args):
    print("Current tile size:", args.pixels)
    print("Enter in the new size of your tiles.")

    newSize = input()
    if newSize.isdigit():
        args.pixels = int(newSize)
        print("Size set to", newSize)
        return args
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
    print("Attempting theme creation at", args.tileset)


def genMap(args):
    print("Attempting map generation to", args.output)


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
# End of map menu options


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

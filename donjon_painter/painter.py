import sys
import argparse
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))
import menu
import themes
import txtmap
import imgmap


# Handle arguments
def getArgs(showHelp=0):
    parser = argparse.ArgumentParser(
        prog="donjon-painter",
        description="A tool to create dungeon maps from TSV files \
        (Donjon's Random Dungeon Generator)"
    )
    parser.add_argument(
        "MAPFILE", help="specify TSV file to parse", nargs='?')
    parser.add_argument(
        "-t", "--tileset",
        help="select the tileset folder to use (interactive mode if not)")
    parser.add_argument(
        "-m", "--measure",
        help="get the time it takes to execute the script",
        action="store_true")
    parser.add_argument(
        "-o", "--output",
        help="declare name and/or location of map to save",
        default=str(Path(Path.home(), 'Map.png')))
    parser.add_argument(
        "-p", "--pixels",
        help="specify the size of your map tile assets (default 70)",
        default=70)
    parser.add_argument(
        "-r", "--randomise",
        help="rotate the floor tile asset for some variation to the map",
        action="store_true")
    parser.add_argument(
        "-s", "--savetiles",
        help="generate a theme from a partial one (good for making themes)",
        action="store_true")

    if not showHelp:
        return parser.parse_args()
    else:
        return parser.print_help()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = getArgs()

    # Execution Redux (Interactive Mode vs. Single Command Mode)
    if args.MAPFILE is None:
        menu.mainmenu(args)
    else:
        if args.tileset is None:
            themes.printThemes()
            args.tileset = themes.selTheme(args.tileset)
        if args.savetiles:
            start = time.time()
            if themes.writeTheme(args.tileset) is False:
                print("Theme cannot be saved - insufficient resources.")
            else:
                if args.measure:
                    end = time.time()
                    print("Theme generation done in", end - start, "seconds.")
        if args.measure:
            start = time.time()

        tmpMap = txtmap.readMap(args.MAPFILE)
        tmpMap = txtmap.parseMap(tmpMap)
        tmpMap = imgmap.generateMap(args, tmpMap)

        if imgmap.writeMap(args, tmpMap) is False:
            print("Map cannot be saved - insufficient resources.")
        else:
            if args.measure:
                end = time.time()
                print("Map generation done in", end - start, "seconds.")
            print("Finished!")


if __name__ == "__main__":
    main()

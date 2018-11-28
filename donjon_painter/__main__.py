import sys
import argparse
import time
from pathlib import Path

# Handle arguments
def getArgs(showHelp = 0):
    parser = argparse.ArgumentParser(
        prog="donjon-painter",
        description="A tool to create dungeon maps from TSV files (Donjon's Random Dungeon Generator)"
    )
    parser.add_argument("MAPFILE", help="specify TSV file to parse", nargs='?', default=0)
    parser.add_argument("-t", "--tileset", help="select the tileset folder to use (inbuilt theme picker if not used)")
    parser.add_argument("-m", "--measure", help="get the time it takes to execute the script", action="store_true")
    parser.add_argument("-o", "--output", help="declare name and/or location of map to save")
    parser.add_argument("-p", "--pixels", help="specify the size of the squares to scale your image to (default 70)")
    parser.add_argument("-r", "--randomise", help="rotate the floor tile asset for some variation to the map", action="store_true")
    parser.add_argument("-s", "--savetiles", help="save any tile assets you created through this script (good for making themes)", action="store_true")
    
    if not showHelp:
        return parser.parse_args()
    else:
        return parser.print_help()

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    
    args = getArgs()
    if args.MAPFILE == 0:
        print(getArgs(1))
        print("Map file not specified! Read the above contents to learn how to use this. Press Enter to continue.")
        input()
        sys.exit()
    
    sys.path.insert(0, str(Path(__file__).parent.resolve()))
    
    # Module Files
    import reader
    import writer
    import loader
    import painter
    
    # Execution
    themeLoc    = reader.getTheme(args.tileset)
    imagePath   = reader.createImageDirectory(themeLoc)
    mapArray    = reader.createMapArray(args.MAPFILE)
    saveDir     = writer.createSaveDirectory(args.output)
    
    mapRes = loader.createImagePath(imagePath)
    mapRes = loader.generateRes(args.savetiles, mapRes)
    
    if loader.resourcesPresent(mapRes) and mapArray != []:
        start = time.time()
        
        print("Generating rows...")
        mapRes  = painter.normaliseImages(mapRes, args.pixels)
        mapRes  = painter.writeRows(mapArray, mapRes, args)
        print("Merging rows...")
        mapRes  = painter.mergeRows(mapRes)
        
        print("Saving image...")
        writer.saveMap(mapRes, saveDir)
        
        end = time.time()
        
        if args.measure:
            print("Done in", end - start, "seconds.")
        else:
            print("Done!")
    
if __name__ == "__main__":
    main()

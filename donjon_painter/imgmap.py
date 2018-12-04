from pathlib import Path
from PIL import Image
from random import choice
import themes
import txtmap


# Actually create the map in question
def generateMap(args):
    rawFile = txtmap.readMap(args.MAPFILE)
    resFile = txtmap.parseMap(rawFile)

    # Theme map
    mapBlocks = themes.generateTheme(args.tileset)

    if mapBlocks is not False and resFile != []:
        # Scale theme tiles to desired size
        for supKey, category in mapBlocks.items():
            for key, img in category.items():
                mapBlocks[supKey][key] = mapBlocks[supKey][key].resize(
                    (args.pixels, args.pixels),
                    resample=Image.LANCZOS)

        # Convert all tiles to RGBA mode
        for supKey, category in mapBlocks.items():
            for key, img in category.items():
                if mapBlocks[supKey][key].mode != 'RGBA':
                    mapBlocks[supKey][key] = mapBlocks[supKey][key].convert(
                        'RGBA'
                    )

        # Get width & height of image
        width = len(rawFile[0]) * args.pixels
        height = len(rawFile) * args.pixels

        # Paste images onto blank canvas
        tmpImage = Image.new('RGBA', (width, height))
        if mapBlocks is not False:
            for row, tileMap in enumerate(resFile):
                yPos = row * args.pixels
                # Loop through tile resources in single tile
                for col, tileArray in enumerate(tileMap):
                    xPos = col * args.pixels
                    # Merge resources if there's more than one
                    if len(tileArray) > 1:
                        tileImage = Image.new(
                            'RGBA', (args.pixels, args.pixels)
                        )
                        for pos, imgCur in enumerate(tileArray):
                            if pos == (len(tileArray) - 1):
                                break
                            imgNext = tileArray[pos+1]
                            bg = mapBlocks[imgCur[0]][imgCur[1]]
                            fg = mapBlocks[imgNext[0]][imgNext[1]]
                            tileImage = Image.alpha_composite(
                                tileImage, bg)
                            tileImage = Image.alpha_composite(
                                tileImage, fg)
                        tmpImage.paste(im=tileImage, box=(xPos, yPos))
                    else:
                        # Floor tile randomising
                        tileCat = tileArray[0][0]
                        tileNam = tileArray[0][1]
                        if args.randomise and tileNam == 'floor':
                            floorImg = mapBlocks[tileCat][tileNam]
                            floorImg = choice([
                                floorImg,
                                floorImg.transpose(Image.ROTATE_90),
                                floorImg.transpose(Image.ROTATE_180),
                                floorImg.transpose(Image.ROTATE_270)
                            ])
                            tmpImage.paste(im=floorImg, box=(xPos, yPos))
                        else:
                            tmpImage.paste(
                                im=mapBlocks[tileCat][tileNam],
                                box=(xPos, yPos)
                            )
        return tmpImage
    else:
        return False


# Save map to a specific directory
def writeMap(args):

    tmpMap = generateMap(args)
    if tmpMap is not False:
        defName = 'Map.png'
        defLocs = Path.home()
        saveLoc = args.output
        fileTypes = ['.png', '.jpg', '.jpeg']

        if Path(args.output).is_dir():
            saveLoc = Path(args.output, defName)
            tmpMap.save(saveLoc)
        elif Path(args.output).parent.is_dir():
            if Path(args.output).suffix in fileTypes:
                tmpMap.save(saveLoc)
            else:
                saveLoc = args.output + '.png'
                tmpMap.save(saveLoc)
        else:
            saveLoc = str(Path(defLocs, defName))
            tmpMap.save(saveLoc)
    else:
        return False

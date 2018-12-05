from pathlib import Path
from PIL import Image
import copy


# Retrieve list of theme directories
def getThemes():
    themeList = []

    imgLoc = Path(__file__).parent.resolve()
    imgLoc = Path(imgLoc, 'themes')

    for item in imgLoc.iterdir():
            if item.is_dir():
                themeList.append(item)

    themeList = sorted(themeList)
    return themeList


# Display all builtin themes
def printThemes():
    curList = getThemes()
    print("===Theme List===")
    for key, item in enumerate(curList):
        themeName = item.parts
        print("[" + str(key) + "]: " + themeName[-1])


# Return desired theme folder
def selTheme(curTile):
    themes = getThemes()
    options = range(0, len(themes))
    themeIndex = list(str(item) for item in options)
    selection = input()

    if selection in themeIndex:
        curTile = themes[int(selection)]
    else:
        curTile = False
    return curTile


# ==================== Theme Generation Functions ====================
resources = {
    'floorAssets': {
        'floor':                '0-Floor'
    },
    'spaceAssets': {
        'dungeonSpace':         '1-Space'
    },
    'wallAssets': {
        'wallTop':              '2-T_Wall',
        'wallBottom':           '2-B_Wall',
        'wallLeft':             '2-L_Wall',
        'wallRight':            '2-R_Wall'
    },
    'inCorners': {
        'topLeftCornerI':       '3-TL_Corner_I',
        'bottomRightCornerI':   '3-BR_Corner_I',
        'bottomLeftCornerI':    '3-BL_Corner_I',
        'topRightCornerI':      '3-TR_Corner_I'
    },
    'outCorners': {
        'topLeftCornerO':       '4-TL_Corner_O',
        'bottomRightCornerO':   '4-BR_Corner_O',
        'bottomLeftCornerO':    '4-BL_Corner_O',
        'topRightCornerO':      '4-TR_Corner_O'
    },
    'doorAssets': {
        'doorTop':              '5-T_Door',
        'doorBottom':           '5-B_Door',
        'doorLeft':             '5-L_Door',
        'doorRight':            '5-R_Door'
    },
    'doorSAssets': {
        'doorSecretTop':        '6-T_Door_Secret',
        'doorSecretBottom':     '6-B_Door_Secret',
        'doorSecretLeft':       '6-L_Door_Secret',
        'doorSecretRight':      '6-R_Door_Secret'
    },
    'doorPAssets': {
        'doorPortTop':          '7-T_Door_Portcullis',
        'doorPortBottom':       '7-B_Door_Portcullis',
        'doorPortLeft':         '7-L_Door_Portcullis',
        'doorPortRight':        '7-R_Door_Portcullis'
    },
    'stairUAssets': {
        'topStairU':            '8-T_Stair_U',
        'bottomStairU':         '8-B_Stair_U',
        'leftStairU':           '8-L_Stair_U',
        'rightStairU':          '8-R_Stair_U'
    },
    'stairUUAssets': {
        'topStairUU':           '9-T_Stair_UU',
        'bottomStairUU':        '9-B_Stair_UU',
        'leftStairUU':          '9-L_Stair_UU',
        'rightStairUU':         '9-R_Stair_UU'
    },
    'stairDAssets': {
        'topStairD':            '10-T_Stair_D',
        'bottomStairD':         '10-B_Stair_D',
        'leftStairD':           '10-L_Stair_D',
        'rightStairD':          '10-R_Stair_D'
    },
    'stairDDAssets': {
        'topStairDD':           '11-T_Stair_DD',
        'bottomStairDD':        '11-B_Stair_DD',
        'leftStairDD':          '11-L_Stair_DD',
        'rightStairDD':         '11-R_Stair_DD'
    }
}


# Check if resource generation is possible
def canGenerate(mapPath, openImages=False):
    tmpRes = copy.deepcopy(resources)
    mapPath = str(Path(mapPath).expanduser().resolve())

    if Path(mapPath).is_dir:
        sufficient = []
        fileTypes = ['.png', '.jpg', '.jpeg']
        # Different asset types
        for superKey, val in tmpRes.items():
            # Asset type members
            state = False
            for assetKey, fileName in val.items():
                for suffix in fileTypes:
                    tmpName = fileName + suffix
                    if Path(mapPath, tmpName).is_file():
                        if openImages:
                            tmpRes[superKey][assetKey] = Image.open(
                                Path(mapPath, tmpName)
                            )
                        state = True
            sufficient.append(state)

        if openImages:
            return [all(sufficient), tmpRes]
        else:
            return all(sufficient)
    else:
        return False


# Supply a fully made theme if possible
def generateTheme(mapPath):

    tmpRes = canGenerate(mapPath, True)

    if tmpRes[0] is not False:
        # Dictionary with some open images
        tmpRes = tmpRes[1]

        def rotateNone(im):
            return im

        def rotateLeft(im):
            tmpImage = im.transpose(Image.ROTATE_90)
            tmpImage.format = im.format
            return tmpImage

        def rotateFlip(im):
            tmpImage = im.transpose(Image.ROTATE_180)
            tmpImage.format = im.format
            return tmpImage

        def rotateRight(im):
            tmpImage = im.transpose(Image.ROTATE_270)
            tmpImage.format = im.format
            return tmpImage

        rotate = {
            0: {
                0: rotateNone,
                1: rotateFlip,
                2: rotateLeft,
                3: rotateRight
            },
            1: {
                0: rotateFlip,
                1: rotateNone,
                2: rotateRight,
                3: rotateLeft
            },
            2: {
                0: rotateRight,
                1: rotateLeft,
                2: rotateNone,
                3: rotateFlip
            },
            3: {
                0: rotateLeft,
                1: rotateRight,
                2: rotateFlip,
                3: rotateNone
            }
        }

        # Different asset types -> asset permutations
        for key, val in tmpRes.items():
            # Get asset to transpose to others
            imgIndex = ''
            transposee = ''
            for i, (assetKey, img) in enumerate(val.items()):
                if img is isinstance(img, Image.Image):
                    imgIndex = i
                    transposee = img
                    break
            # Create other assets from found one
            for i, (assetKey, img) in enumerate(val.items()):
                if not isinstance(img, Image.Image):
                    tmpRes[key][assetKey] = rotate[imgIndex][i](transposee)

        return tmpRes
    else:
        return False


# Create a theme at the specified path
def writeTheme(mapPath):
    themeRes = generateTheme(mapPath)
    if themeRes is not False:
        for itemGroup, category in themeRes.items():
            for item, asset in category.items():
                imgName = resources[itemGroup][item]
                imgName = imgName + '.' + asset.format.lower()
                saveLoc = Path(mapPath, imgName)
                if not saveLoc.is_file():
                    asset.save(saveLoc)
        print("Theme saved!")
    else:
        return False

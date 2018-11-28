from PIL import Image
from pathlib import Path

Image.MAX_IMAGE_PIXELS = None

# Create direct paths to image resources
def createImagePath(path):
    mapRes = {
        'floor':                '0-Floor',
        'dungeonSpace':         '1-Space',
        
        'wallTop':              '2-T_Wall',
        'wallBottom':           '2-B_Wall',
        'wallLeft':             '2-L_Wall',
        'wallRight':            '2-R_Wall',
        
        'topLeftCornerI':       '3-TL_Corner_I',
        'topRightCornerI':      '3-TR_Corner_I',
        'bottomLeftCornerI':    '3-BL_Corner_I',
        'bottomRightCornerI':   '3-BR_Corner_I',
        
        'topLeftCornerO':       '4-TL_Corner_O',
        'topRightCornerO':      '4-TR_Corner_O',
        'bottomLeftCornerO':    '4-BL_Corner_O',
        'bottomRightCornerO':   '4-BR_Corner_O',
        
        'doorTop':              '5-T_Door',
        'doorBottom':           '5-B_Door',
        'doorLeft':             '5-L_Door',
        'doorRight':            '5-R_Door',
        
        'doorSecretTop':        '6-T_Door_Secret',
        'doorSecretBottom':     '6-B_Door_Secret',
        'doorSecretLeft':       '6-L_Door_Secret',
        'doorSecretRight':      '6-R_Door_Secret',
        
        'doorPortTop':          '7-T_Door_Portcullis',
        'doorPortBottom':       '7-B_Door_Portcullis',
        'doorPortLeft':         '7-L_Door_Portcullis',
        'doorPortRight':        '7-R_Door_Portcullis',
        
        'topStairU':            '8-T_Stair_U',
        'bottomStairU':         '8-B_Stair_U',
        'leftStairU':           '8-L_Stair_U',
        'rightStairU':          '8-R_Stair_U',
        
        'topStairUU':           '9-T_Stair_UU',
        'bottomStairUU':        '9-B_Stair_UU',
        'leftStairUU':          '9-L_Stair_UU',
        'rightStairUU':         '9-R_Stair_UU',
        
        'topStairD':            '10-T_Stair_D',
        'bottomStairD':         '10-B_Stair_D',
        'leftStairD':           '10-L_Stair_D',
        'rightStairD':          '10-R_Stair_D',
        
        'topStairDD':           '11-T_Stair_DD',
        'bottomStairDD':        '11-B_Stair_DD',
        'leftStairDD':          '11-L_Stair_DD',
        'rightStairDD':         '11-R_Stair_DD'
    }
    
    suffixes = ['.jpg', '.jpeg', '.png']
    curFile = path
    
    # Check for image extension type
    def getFileSuffix(sufList, fileName):
        result = ''
        for fileType in sufList:
            curFile = Path(str(path), fileName).with_suffix(fileType)
            if curFile.is_file():
                result = fileType
        return result
    
    for key, value in mapRes.items():
        curFileSuffix = getFileSuffix(suffixes, value)
        curFile = Path(str(path), value).with_suffix(curFileSuffix)
        if curFile.is_file():
            mapRes[key] = curFile
    
    return mapRes

# Checks if resources are present
def resourcesPresent(mapRes):
    imagesPresent = True
    
    for key, value in mapRes.items():
        if value is Image:
            imagesPresent = False
    
    return imagesPresent

# Creates additional resources from existing ones
def generateRes(savetiles, mapRes):
    def genDict(curKeys):
        resDict = dict((i, mapRes[i]) for i in curKeys)
        return resDict
    
    def checkPresent(curKeys):
        isPresent = False
        curDict = genDict(curKeys)
        for key, val in curDict.items():
            if Path(val).is_file():
                isPresent = True
        return isPresent
    
    floorKeys = ['floor']
    spaceKeys = ['dungeonSpace']
    wallKeys = ['wallTop', 'wallBottom', 'wallLeft', 'wallRight']
    cornerOKeys = ['topLeftCornerO', 'bottomRightCornerO', 'bottomLeftCornerO', 'topRightCornerO']
    cornerIKeys = ['topLeftCornerI', 'bottomRightCornerI', 'bottomLeftCornerI', 'topRightCornerI']
    doorKeys = ['doorTop', 'doorBottom', 'doorLeft', 'doorRight']
    sDoorKeys = ['doorSecretTop', 'doorSecretBottom', 'doorSecretLeft', 'doorSecretRight']
    pDoorKeys = ['doorPortTop', 'doorPortBottom', 'doorPortLeft', 'doorPortRight']
    stairUKeys = ['topStairU', 'bottomStairU', 'leftStairU', 'rightStairU']
    stairUUKeys = ['topStairUU', 'bottomStairUU', 'leftStairUU', 'rightStairUU']
    stairDKeys = ['topStairD', 'bottomStairD', 'leftStairD', 'rightStairD']
    stairDDKeys = ['topStairDD', 'bottomStairDD', 'leftStairDD', 'rightStairDD']
    
    floorPresent    = checkPresent(floorKeys)
    spacePresent    = checkPresent(spaceKeys)
    wallPresent     = checkPresent(wallKeys)
    cornerPresent   = (checkPresent(cornerOKeys) and checkPresent(cornerIKeys))
    doorPresent     = checkPresent(doorKeys)
    doorSPresent    = checkPresent(sDoorKeys)
    doorPPresent    = checkPresent(pDoorKeys)
    stairUPresent   = checkPresent(stairUKeys)
    stairUUPresent  = checkPresent(stairUUKeys)
    stairDPresent   = checkPresent(stairDKeys)
    stairDDPresent  = checkPresent(stairDDKeys)
    
    # Actually generate the images
    if (floorPresent and spacePresent and
            wallPresent and cornerPresent and
            doorPresent and doorSPresent and doorPPresent and
            stairUPresent and stairUUPresent and
            stairDPresent and stairDDPresent):
        def resGen(items):
            # Generate dictionary
            curDict = genDict(items)
            # Get image (key) to manipulate
            keyName = ''
            # Temporary filename value
            fileName = ''
            for key, val in curDict.items():
                if Path(val).is_file():
                    keyName = key
                    fileName = keyName
                    mapRes[keyName] = Image.open(mapRes[keyName])
            for key, val in curDict.items():
                # Exclude entries that have an image
                if not Path(val).is_file():
                    tmpImage = mapRes[keyName]
                    if keyName == items[0]:
                        if key == items[1]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_180)
                        if key == items[2]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_90)
                        if key == items[3]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_270)
                    if keyName == items[1]:
                        if key == items[0]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_180)
                        if key == items[2]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_270)
                        if key == items[3]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_90)
                    if keyName == items[2]:
                        if key == items[0]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_270)
                        if key == items[1]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_90)
                        if key == items[3]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_180)
                    if keyName == items[3]:
                        if key == items[0]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_90)
                        if key == items[1]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_270)
                        if key == items[2]:
                            tmpImage = tmpImage.transpose(Image.ROTATE_180)
                    
                    if (savetiles):
                        suffix = '.' + mapRes[keyName].format.lower()
                        curFile = Path(path, val).with_suffix(suffix)
                        
                        tmpImage.save(curFile)
                        mapRes[key] = Image.open(curFile)
                    else:
                        mapRes[key] = tmpImage
                    
                else:
                    keyName = key
        
        # Load space and floor resources to memory
        resGen(floorKeys)
        resGen(spaceKeys)
        
        # Generate new wall resources
        resGen(wallKeys)
        
        # Generate new outwards corner resources
        resGen(cornerOKeys)
        
        # Generate new inwards corner resources
        resGen(cornerIKeys)
        
        # Generate new door resources
        resGen(doorKeys)
        
        # Generate new secret door resources
        resGen(sDoorKeys)
        
        # Generate new portcullis door resources
        resGen(pDoorKeys)
        
        # Generate new U stair resources
        resGen(stairUKeys)
        
        # Generate new UU stair resources
        resGen(stairUUKeys)
        
        # Generate new D stair resources
        resGen(stairDKeys)
        
        # Generate new DD stair resources
        resGen(stairDDKeys)
        
        return mapRes

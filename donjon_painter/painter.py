from PIL import Image
from random import choice

import multiprocessing
import os

Image.MAX_IMAGE_PIXELS = None

# Determine image to use for current position
def setImage(mapArray, size, xPos, yPos, mapRes, args):
    
    keyMap = {
        'F':    'floor',
        
        'DT':   'doorTop',
        'DB':   'doorBottom',
        'DL':   'doorLeft',
        'DR':   'doorRight',
        
        'DST':  'doorSecretTop',
        'DSB':  'doorSecretBottom',
        'DSL':  'doorSecretLeft',
        'DSR':  'doorSecretRight',
        
        'DPT':  'doorPortTop',
        'DPB':  'doorPortBottom',
        'DPL':  'doorPortLeft',
        'DPR':  'doorPortRight',
        
        'STR': {
            'N': {
                'SUU':  'bottomStairU',
                'SU':   'topStairUU',
                'SDD':  'bottomStairD',
                'SD':   'topStairDD'
            },
            'E': {
                'SUU':  'leftStairU',
                'SU':   'rightStairUU',
                'SDD':  'leftStairD',
                'SD':   'rightStairDD'
            },
            'S': {
                'SUU':  'topStairU',
                'SU':   'bottomStairUU',
                'SDD':  'topStairD',
                'SD':   'bottomStairDD'
            },
            'W': {
                'SUU':  'rightStairU',
                'SU':   'leftStairUU',
                'SDD':  'rightStairD',
                'SD':   'leftStairDD'
            }
        }
    }
    
    coord = {
        'NW': '',   'N': '',    'NE': '',
        'W': '',    'M': '',    'E': '',
        'SW': '',   'S': '',    'SE': ''
    }
    
    coord['M'] = mapArray[yPos][xPos]
    
    targetImage = None
    
    # Get cardinal attributes
    def setCardinal(loc, attr, cond, yAdj, xAdj):
        if attr != cond:
            coord[loc] = mapArray[yPos + yAdj][xPos + xAdj]
        else:
            coord[loc] = 'void'

    # Get intermediate attributes
    def setInterCard(targetCoord, cond1, cond2, yAdj, xAdj):
        if coord[cond1] != 'void' and coord[cond2] != 'void':
            coord[targetCoord] = mapArray[yPos + yAdj][xPos + xAdj]
        else:
            coord[targetCoord] = 'void'
    
    setCardinal('N', yPos, 0, -1, 0)
    setCardinal('E', xPos, (size['width'] - 1), 0, 1)
    setCardinal('S', yPos, (size['height'] - 1), 1, 0)
    setCardinal('W', xPos, 0, 0, -1)
    
    setInterCard('NE', 'N', 'E', -1, 1)
    setInterCard('SE', 'S', 'E', 1, 1)
    setInterCard('SW', 'S', 'W', 1, -1)
    setInterCard('NW', 'N', 'W', -1, -1)
    
    # Use space resource
    isEmpty = True
    for key, value in coord.items():
        if value != '' and value != 'void':
            isEmpty = False
            
            # Get rid of void entries
            for key, val in coord.items():
                if val == 'void':
                    coord[key] = ''
    
    if isEmpty:
        targetImage = mapRes['dungeonSpace']
    else:
        if coord['M'] != '':
            if coord['M'][0] != 'S':
                tileName = keyMap[coord['M']]
                targetImage = mapRes[tileName]
                
                if args.randomise and tileName == 'floor':
                    targetImage = choice([
                            targetImage,
                            targetImage.transpose(Image.ROTATE_90),
                            targetImage.transpose(Image.ROTATE_180),
                            targetImage.transpose(Image.ROTATE_270)
                    ])
            else:
                
                for stair, tile in keyMap['STR']['N'].items():
                    if coord['N'] == stair:
                        targetImage = mapRes[tile]
                
                for stair, tile in keyMap['STR']['E'].items():
                    if coord['E'] == stair:
                        targetImage = mapRes[tile]
                        
                for stair, tile in keyMap['STR']['S'].items():
                    if coord['S'] == stair:
                        targetImage = mapRes[tile]
                
                for stair, tile, in keyMap['STR']['W'].items():
                    if coord['W'] == stair:
                        targetImage = mapRes[tile]
                
            if coord['M'][0] == 'S' or coord['M'][0] == 'D':
                bgImage = mapRes['floor'].convert('RGBA')
                targetImage = Image.alpha_composite(bgImage, targetImage)
        else:
            # Use wall resources
            walls = []
            
            def cardinalWall(wallDir, mapItem):
                if wallDir != '':
                    walls.append(mapItem)
            
            def intermedWallOut(wallDir, mapItem, coord1, coord2):
                if wallDir != '':
                    if coord1 == '' and coord2 == '':
                        walls.append(mapItem)
            
            def intermedWallIn(wallDir, mapItem, coord1, coord2):
                if wallDir != '':
                    if coord1 != '' and coord2 != '':
                        walls.append(mapItem)
            
            cardinalWall(coord['N'], mapRes['wallTop'])
            cardinalWall(coord['E'], mapRes['wallRight'])
            cardinalWall(coord['S'], mapRes['wallBottom'])
            cardinalWall(coord['W'], mapRes['wallLeft'])
            
            intermedWallOut(coord['NE'], mapRes['topRightCornerO'], coord['N'], coord['E'])
            intermedWallOut(coord['SE'], mapRes['bottomRightCornerO'], coord['S'], coord['E'])
            intermedWallOut(coord['SW'], mapRes['bottomLeftCornerO'], coord['S'], coord['W'])
            intermedWallOut(coord['NW'], mapRes['topLeftCornerO'], coord['N'], coord['W'])
            
            intermedWallIn(coord['NE'], mapRes['topRightCornerI'], coord['N'], coord['E'])
            intermedWallIn(coord['SE'], mapRes['bottomRightCornerI'], coord['S'], coord['E'])
            intermedWallIn(coord['SW'], mapRes['bottomLeftCornerI'], coord['S'], coord['W'])
            intermedWallIn(coord['NW'], mapRes['topLeftCornerI'], coord['N'], coord['W'])
            
            if len(walls) == 1:
                targetImage = walls[0]
            else:
                targetImage = walls[0]
                
                curPos = 0
                for items in walls:
                    if curPos != len(walls) and curPos != 0:
                        targetImage = Image.alpha_composite(targetImage, walls[curPos])
                    curPos += 1
    return targetImage

# Resize images to get them in a consistent shape and size
def normaliseImages(imgFolder, imgSize):
    if imgSize:
        if imgSize.isnumeric():
            imgSize = abs(int(imgSize))
    else:
        imgSize = 70

    for key, value in imgFolder.items():
        imgFolder[key] = value.resize((imgSize, imgSize), Image.LANCZOS)
    
    return imgFolder

# Create an array of image rows from the specified map
def writeRows(mapFile, mapRes, args):
    # Get the dimensions of the map
    def getSize(mapFile):
        xPos = 0
        yPos = 0
        
        for row in mapFile:
            xPos = 0
            for element in row:
                xPos += 1
            yPos += 1
        
        return {'width': xPos, 'height': yPos}

    outputArray = []
    size = getSize(mapFile)
    
    for yPos, row in enumerate(mapFile):
        images = []
        
        for xPos, element in enumerate(row):
            curEntry = setImage(mapFile, size, xPos, yPos, mapRes, args)
            images.append(curEntry)
        
        widths, heights = zip(*(i.size for i in images))
        totalWidth = sum(widths)
        maxHeight = max(heights)
        
        rowImage = Image.new('RGBA', (totalWidth, maxHeight))
        
        xOffset = 0
        for item in images:
            rowImage.paste(item, (xOffset, 0))
            xOffset += item.size[0]
        
        outputArray.append(rowImage)
    
    return outputArray

# Coalesce an array of images into a single file
def mergeRows(imgArray):
    def getMetrics(inArray):
        width, height = inArray[0].size
        return [width, (height * len(inArray))]
    
    measure = getMetrics(imgArray)
    resImage = Image.new('RGBA', (measure[0], measure[1]))
    
    curHeight = 0
    while imgArray:
        width, height = imgArray[0].size
        resImage.paste(im=imgArray[0], box=(0, curHeight))
        
        curHeight += height
        imgArray.pop(0)
    
    return resImage

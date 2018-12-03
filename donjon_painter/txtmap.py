import csv
from pathlib import Path


# Creates a 2D list from a TSV file
def readMap(mapfile):
    tmpArray = []
    if Path(mapfile).is_file():
        with open(mapfile) as fd:
            rd = csv.reader(fd, delimiter="\t")
            for row in rd:
                tmpArray.append(row)
    return tmpArray

# Translating TSV map -> image map:
#   Link symbols to a list of nested dictionary key/values
#   E.g. [[tileCategory, tileType], [tileCategory, tileType]]


# Return a readable list of tile references from a 2D array
def parseMap(arrMap):
    # Symbols that need more parsing (multiple outcomes)
    nameList = {
        'S':        ['spaceAssets', 'dungeonSpace'],
        'WT':       ['wallAssets', 'wallTop'],
        'WB':       ['wallAssets', 'wallBottom'],
        'WL':       ['wallAssets', 'wallLeft'],
        'WR':       ['wallAssets', 'wallRight'],
        'ITL':      ['inCorners', 'topLeftCornerI'],
        'IBR':      ['inCorners', 'bottomRightCornerI'],
        'IBL':      ['inCorners', 'bottomLeftCornerI'],
        'ITR':      ['inCorners', 'topRightCornerI'],
        'OTL':      ['outCorners', 'topLeftCornerO'],
        'OBR':      ['outCorners', 'bottomRightCornerO'],
        'OBL':      ['outCorners', 'bottomLeftCornerO'],
        'OTR':      ['outCorners', 'topRightCornerO'],
        'SUT':      ['stairUAssets', 'topStairU'],
        'SUB':      ['stairUAssets', 'bottomStairU'],
        'SUL':      ['stairUAssets', 'leftStairU'],
        'SUR':      ['stairUAssets', 'rightStairU'],
        'SUUT':     ['stairUUAssets', 'topStairUU'],
        'SUUB':     ['stairUUAssets', 'bottomStairUU'],
        'SUUL':     ['stairUUAssets', 'leftStairUU'],
        'SUUR':     ['stairUUAssets', 'rightStairUU'],
        'SDT':      ['stairDAssets', 'topStairD'],
        'SDB':      ['stairDAssets', 'bottomStairD'],
        'SDL':      ['stairDAssets', 'leftStairD'],
        'SDR':      ['stairDAssets', 'rightStairD'],
        'SDDT':     ['stairDDAssets', 'topStairDD'],
        'SDDB':     ['stairDDAssets', 'bottomStairDD'],
        'SDDL':     ['stairDDAssets', 'leftStairDD'],
        'SDDR':     ['stairDDAssets', 'rightStairDD']
    }

    # One to one symbols (no function needed)
    txtSymbols = {
        'F':    ['floorAssets', 'floor'],
        'DT':   ['doorAssets', 'doorTop'],
        'DB':   ['doorAssets', 'doorBottom'],
        'DL':   ['doorAssets', 'doorLeft'],
        'DR':   ['doorAssets', 'doorRight'],
        'DST':  ['doorSAssets', 'doorSecretTop'],
        'DSB':  ['doorSAssets', 'doorSecretBottom'],
        'DSL':  ['doorSAssets', 'doorSecretLeft'],
        'DSR':  ['doorSAssets', 'doorSecretRight'],
        'DPT':  ['doorPAssets', 'doorPortTop'],
        'DPB':  ['doorPAssets', 'doorPortBottom'],
        'DPL':  ['doorPAssets', 'doorPortLeft'],
        'DPR':  ['doorPAssets', 'doorPortRight']
    }

    # Return dictionary of items + adjacent letters (mapfile, position)
    def getCoordinates(m, y, x):
        maxY = len(m) - 1
        maxX = len(m[y]) - 1

        minimap = {
            'NW':   m[y-1][x-1],    'N': m[y-1][x], 'NE': m[y-1][x+1],
            'W':    m[y][x-1],      'M': m[y][x],   'E': m[y][x+1],
            'SW':   m[y+1][x-1],    'S': m[y+1][x], 'SE': m[y+1][x+1]
        }

        # N, E, S, W, NE, SE, SW, NW
        checks = [[y, 0],
                  [x, maxX],
                  [y, maxY],
                  [x, 0],
                  [y, 0, x, maxX],
                  [y, maxY, x, maxX],
                  [y, maxY, x, 0],
                  [y, 0, x, 0]]

        for i, (key, val) in enumerate(minimap.items()):
            curCheck = checks[i]
            if len(curCheck) == 2:
                if curCheck[0] == curCheck[1]:
                    minimap[key] = None
            else:
                if curCheck[0] == curCheck[1] and curCheck[2] == curCheck[3]:
                    minimap[key] = None
        return minimap

    # Wall/space tiles needed
    def getWall(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        edges = [mapPart['N'], mapPart['E'], mapPart['S'], mapPart['W']]
        corners = [(mapPart['NE'], mapPart['N'], mapPart['E']),
                   (mapPart['SE'], mapPart['S'], mapPart['E']),
                   (mapPart['SW'], mapPart['S'], mapPart['W']),
                   (mapPart['NW'], mapPart['N'], mapPart['W'])]
        space = [mapPart['NW'], mapPart['N'],   mapPart['NE'],
                 mapPart['W'],  mapPart['M'],   mapPart['E'],
                 mapPart['SW'], mapPart['S'],   mapPart['SE']]

        wallArray = []

        # Empty space if everything blank
        if space == ['', '', '', '', '', '', '', '', '']:
            wallArray.append(nameList['S'])

        # Inwards corner walls
        cornerTypeI = ['ITR', 'IBR', 'IBL', 'ITL']
        for i, corner in enumerate(corners):
            if corner == ['F', 'F', 'F']:
                wallArray.append(nameList[cornerTypeI[i]])

        # Outwards corner walls
        cornerTypeO = ['OTR', 'OBR', 'OBL', 'OTL']
        for i, corner in enumerate(corners):
            if corner == ['F', '', '']:
                wallArray.append(nameList[cornerTypeO[i]])

        # Straight walls
        wallType = ['WT', 'WB', 'WL', 'WR']
        for i, edge in enumerate(edges):
            if edge == ['F']:
                wallArray.append(nameList[wallType[i]])

        return wallArray

    # Stair tiles needed
    def getStair(loc, stairType, stairKey):
        stairArray = []
        stairArray.append(txtSymbols['F'])

        for i, loc in enumerate(loc):
            if loc == stairKey:
                stairArray.append(nameList[stairType[i]])

    def getUStair(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        stairs = [mapPart['N'], mapPart['E'], mapPart['S'], mapPart['W']]
        stairType = ['SUB', 'SUL', 'SUT', 'SUR']

        return getStair(stairs, stairType, 'SUU')

    def getUUStair(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        stairs = [mapPart['N'], mapPart['E'], mapPart['S'], mapPart['W']]
        stairType = ['SUUT', 'SUUR', 'SUUB', 'SUUL']

        return getStair(stairs, stairType, 'SU')

    def getDStair(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        stairs = [mapPart['N'], mapPart['E'], mapPart['S'], mapPart['W']]
        stairType = ['SDB', 'SDL', 'SDT', 'SDR']

        return getStair(stairs, stairType, 'SDD')

    def getDDStair(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        stairs = [mapPart['N'], mapPart['E'], mapPart['S'], mapPart['W']]
        stairType = ['SDDT', 'SDDR', 'SDDB', 'SDDL']

        return getStair(stairs, stairType, 'SD')

    funcSymbols = {
        '':     getWall,
        'SU':   getUStair,
        'SUU':  getUUStair,
        'SD':   getDStair,
        'SDD':  getDDStair
    }

    parsedList = []
    for row, col in enumerate(arrMap):
        rowList = []
        for col, tile in enumerate(col):
            if tile in funcSymbols:
                rowList.append(funcSymbols[tile](arrMap, row, col))
            else:
                rowList.append(txtSymbols[tile])
        parsedList.append(rowList)
    return parsedList

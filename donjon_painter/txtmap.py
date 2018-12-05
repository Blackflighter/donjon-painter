import csv
from pathlib import Path


# Creates a 2D list from a TSV file
def readMap(mapfile):
    tmpArray = []
    if Path(mapfile).suffix != '.txt':
        mapfile = mapfile + '.txt'
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
        'F':    [['floorAssets', 'floor']],
        'DT':   [['floorAssets', 'floor'],
                 ['doorAssets', 'doorTop']],
        'DB':   [['floorAssets', 'floor'],
                 ['doorAssets', 'doorBottom']],
        'DL':   [['floorAssets', 'floor'],
                 ['doorAssets', 'doorLeft']],
        'DR':   [['floorAssets', 'floor'],
                 ['doorAssets', 'doorRight']],
        'DST':  [['floorAssets', 'floor'],
                 ['doorSAssets', 'doorSecretTop']],
        'DSB':  [['floorAssets', 'floor'],
                 ['doorSAssets', 'doorSecretBottom']],
        'DSL':  [['floorAssets', 'floor'],
                 ['doorSAssets', 'doorSecretLeft']],
        'DSR':  [['floorAssets', 'floor'],
                 ['doorSAssets', 'doorSecretRight']],
        'DPT':  [['floorAssets', 'floor'],
                 ['doorPAssets', 'doorPortTop']],
        'DPB':  [['floorAssets', 'floor'],
                 ['doorPAssets', 'doorPortBottom']],
        'DPL':  [['floorAssets', 'floor'],
                 ['doorPAssets', 'doorPortLeft']],
        'DPR':  [['floorAssets', 'floor'],
                 ['doorPAssets', 'doorPortRight']]
    }

    # Return dictionary of items + adjacent letters (mapfile, position)
    def getCoordinates(m, y, x):
        maxY = len(m) - 1
        maxX = len(m[y]) - 1

        minimap = {
            'NW':   '_',   'N': '_',      'NE': '_',
            'W':    '_',   'M': m[y][x],   'E': '_',
            'SW':   '_',   'S': '_',      'SE': '_'
        }

        def setCardinal(mapfile, coord, pos, cond, yAdj, xAdj):
            if pos != cond:
                mapfile[coord] = m[y + yAdj][x + xAdj]
            return mapfile

        def setInterCard(mapfile, coord, pos, cond1, cond2, yAdj, xAdj):
            if pos[0] != cond1 and pos[1] != cond2:
                mapfile[coord] = m[y + yAdj][x + xAdj]
            return mapfile

        minimap = setCardinal(minimap, 'N', y, 0, -1, 0)
        minimap = setCardinal(minimap, 'E', x, maxX, 0, 1)
        minimap = setCardinal(minimap, 'S', y, maxY, 1, 0)
        minimap = setCardinal(minimap, 'W', x, 0, 0, -1)
        minimap = setInterCard(minimap, 'NE', (y, x), 0, maxX, -1, 1)
        minimap = setInterCard(minimap, 'SE', (y, x), maxY, maxX, 1, 1)
        minimap = setInterCard(minimap, 'SW', (y, x), maxY, 0, 1, -1)
        minimap = setInterCard(minimap, 'NW', (y, x), 0, 0, -1, -1)

        return minimap

    # Wall/space tiles needed
    def getWall(mapfile, yPos, xPos):
        mapPart = getCoordinates(mapfile, yPos, xPos)
        edges = [mapPart['N'], mapPart['S'], mapPart['W'], mapPart['E']]
        corners = [[mapPart['NE'], mapPart['N'], mapPart['E']],
                   [mapPart['SE'], mapPart['S'], mapPart['E']],
                   [mapPart['SW'], mapPart['S'], mapPart['W']],
                   [mapPart['NW'], mapPart['N'], mapPart['W']]]
        space = [mapPart['NW'], mapPart['N'],   mapPart['NE'],
                 mapPart['W'],  mapPart['M'],   mapPart['E'],
                 mapPart['SW'], mapPart['S'],   mapPart['SE']]

        wallArray = []

        # Tile logic (treat other tiles as 'floor')
        for key, items in enumerate(edges):
            if items != '':
                if (items[0] == 'D' or items[0] == 'S') and items != '_':
                    edges[key] = 'F'
        for supKey, items in enumerate(corners):
            for key, part in enumerate(items):
                if part != '':
                    if (part[0] == 'D' or part[0] == 'S') and part != '_':
                        corners[supKey][key] = 'F'
        for key, items in enumerate(space):
            if items == '_':
                space[key] = ''
        # Empty space if everything blank
        if space == ['', '', '', '', '', '', '', '', '']:
            wallArray.append(nameList['S'])

        # Straight walls
        wallType = ['WT', 'WB', 'WL', 'WR']
        for i, edge in enumerate(edges):
            if edge == 'F':
                wallArray.append(nameList[wallType[i]])

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

        return wallArray

    # Stair tiles needed
    def getStair(loc, stairType, stairKey):
        stairArray = []
        stairArray.append(txtSymbols['F'][0])

        for i, loc in enumerate(loc):
            if loc == stairKey:
                stairArray.append(nameList[stairType[i]])
        return stairArray

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

from pathlib import Path

# Determine where to save your generated map file
def createSaveDirectory(saveLoc):
    saveName = "Map.png"
    if saveLoc:
        saveParts = Path(saveLoc).parts
        
        # Only name specified
        if len(saveParts) == 1:
            default = Path.home().resolve()
            if Path(saveLoc).suffix == '':
                saveName = str(Path(Path.home(), saveLoc + ".png"))
            else:
                saveName = str(Path(Path.home(), saveLoc))
                
        # Only folder specified
        elif Path(saveLoc).is_dir():
            saveName = str(Path(saveLoc, "Map.png"))
            
        # Name and folder specified
        else:
            if Path(saveLoc).suffix == '':
                saveName = str(Path(saveLoc, '.png'))
            else:
                saveName = str(Path(saveLoc))
    else:
        saveName = str(Path(Path.home(), 'Map.png'))
    
    resParts = Path(saveName).parts
    print("Saving map to", Path(saveName).parent, "as", resParts[-1])
    return saveName

# Save an image
def saveMap(img, loc):
    img.save(loc)


import glob
import os


#class for shipNameLists
class ShipNameList:
    def __init__(self, shipName):
        self.shipName = shipName
        self.shipNameList = []
    writeFile = False
    codeName = ""
    
    #toStiring return shipName
    def __str__(self):
        return self.shipName

class FileShipList:
    def __init__(self, fileName):
        self.fileName = fileName
        self.catagoryList = []
    writeFile = False    
    #toStiring return shipName
    def __str__(self):
        return self.fileName
    
desiredList = ["ship_hull_heavy","ship_hull_submarine","ship_hull_carrier","ship_hull_cruiser"]
#glob all files in Input/names_ships

fileShipNameLists = []

def parseShipNameLists():
    files = glob.glob('Input/names_ships/*.txt')
    for f in files:
        fn = "z_mtge_" + f.split("\\")[-1]
        #print(fn)
        sf = FileShipList(f.replace("Input","Output").replace(f.split("\\")[-1],fn))
        #print each line in file f
        #ignore errors
        with open(f, 'r',encoding='utf-8',errors='ignore') as infile:
            indent = 0
            currentList = ""
            for line in infile:
                #skip blank lines or lines that start with #
                if line.strip() == '' or line.strip().startswith('#'):
                    pass
                #else if indent is 0 create new ShipNameList with ship name for first element in line
                elif indent == 0:
                    currentList = ShipNameList(line.strip().split()[0])
                    #print(currentList)
                #elif indent is 1
                elif indent == 1:
                    if line.strip().startswith("name"):
                        currentList.codeName = line.split("=")[1].strip()
                    elif line.strip().startswith("ship_types"):
                        #get all elemnts between { and }
                        nameStart = False
                        for e in line.strip().split():
                            if e.startswith('{'):
                                nameStart = True
                            elif e.startswith('}'):
                                break
                            elif nameStart:
                                currentList.shipNameList.append(e)
                                #print("\t" + e)
                                if e in desiredList:
                                    currentList.writeFile = True
                                    #print("\t" + e)
            


                #check if {, #, or } is in line
                if '{' in line or '}' in line or '#' in line:
                    #split line on spaces
                    #for every { add 1 to indent
                    #for every } subtract 1 from indent
                    #break on #
                    for e in line.split():
                        if e == '{':
                            indent += 1
                        elif e == '}':
                            indent -= 1
                        elif e == '#':
                            break
                        try:
                            if indent == 0 and currentList.writeFile:
                                sf.catagoryList.append(currentList)
                                currentList = ""
                                sf.writeFile = True
                        except:
                            pass
        if sf.writeFile:
            fileShipNameLists.append(sf)
            
def updateShipNameLists():
    for f in fileShipNameLists:
        #print(f)
        for e in f.catagoryList:
            if e.writeFile:
                #print(e)
                if "ship_hull_heavy" in e.shipNameList:
                    e.shipNameList.append("ship_hull_battle_carrier")
                    e.shipNameList.append("submarine_heavy")
                if "ship_hull_cruiser" in e.shipNameList:
                    e.shipNameList.append("ship_hull_cruiser_carrier")
                    e.shipNameList.append("ship_hull_submarine_cruiser")
                if "ship_hull_submarine" in e.shipNameList:
                    e.shipNameList.append("ship_hull_submarine_carrier")
                    e.shipNameList.append("ship_hullsubmarine_cruiser")
                if "ship_hull_carrier" in e.shipNameList:
                    e.shipNameList.append("ship_hull_battle_carrier")
                    e.shipNameList.append("ship_hull_cruiser_carrier")
                    e.shipNameList.append("ship_hull_submarine_carrier")
                #remove duplacets form shipNameList
                e.shipNameList = list(set(e.shipNameList))

def writeShipNameLists():
    if not os.path.exists("Output/names_ships"):
        os.makedirs("Output/names_ships/")
    for f in fileShipNameLists:
        if f.writeFile:
            print(f)
            with open(f.fileName, 'w',encoding='utf-8',errors='ignore') as outfile:
                #outfile.write("#" + f.fileName + "\n")
                for e in f.catagoryList:
                    outfile.write(e.shipName + " = {")
                    outfile.write("\n\tname = "+e.codeName)
                    outfile.write("\n\ttype = ship")
                    outfile.write("\n\tship_types = { ")
                    for l in e.shipNameList:
                        outfile.write(l + " ")
                    outfile.write("}")
                    outfile.write("\n\tprefix = \"\"")
                    outfile.write("\n}\n")


parseShipNameLists()
updateShipNameLists()
writeShipNameLists()
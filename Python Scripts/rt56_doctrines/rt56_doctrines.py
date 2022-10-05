import glob

class Tech:
    name = ""
    startingTypes = 0
    def __init__(self, name):
        self.name = name
        self.shipTypes = []
    def getTypeNames(self):
        nameList = []
        for st in self.shipTypes:
            nameList.append(st.name)
        return nameList
class ShipType:
    name = ""
    def __init__(self, name, tech):
        self.name = name
        self.tech = tech
        self.modiferName = []
        self.modiferValue = []
    def getModiferName(self):
        return self.modiferName
    def __str__(self):
        return self.name

doctorines = glob.glob("Input\\*.txt")

techList = []

shipList = ["battleship = ", "battle_cruiser = ", "heavy_cruiser = ", "light_cruiser = ", "submarine = ", "carrier = ", "destroyer = "] #what are the ships you are looking for (update if paradox added new ship types)

for doc in doctorines:
    f = open(doc)
    indintation = 0
    shipFound = False
    shipName = ""
    ship = ""
    techName = ""
    tech = ""
    for line in f:
        if indintation == 1:
            if "{" in line:
                techName = line.split("=")[0].strip()
                #print(tech)
                tech = Tech(techName)
        if indintation == 2:
            for s in shipList:
                if s in line:
                    shipFound = True
                    shipName = line.split("=")[0].strip()
                    ship = ShipType(shipName, tech.name)
                    tech.startingTypes += 1
                    print(line)
                    break
        if shipFound:  
            #print(line)
            if indintation == 3:
                if not line.strip() == "}":
                    ship.modiferName.append(line.split("=")[0].strip())
                    ship.modiferValue.append(float(line.split("=")[1].strip()))
                    #print(line.split("="))

        if "{" in line or "}" in line:
             for element in list(line.strip()):
                if "{" in element:
                    indintation +=1
                elif "}" in element:
                    indintation -=1
                    if indintation == 1:
                        techList.append(tech)
                    if indintation == 2:
                        shipFound = False
                        if not ship == "":
                            tech.shipTypes.append(ship)
                            ship = ""
                elif "#" in element:
                    break
    f.close()
pass

def generateModifiers(targetShip,targetList,multValueList):
    for m in techList:
        print("%s"%m.name)
        for i in m.shipTypes:
            multValue = 1
            ship = ""
            for t in range(0,len(targetList)):
                if targetList[t] == i.name:
                    multValue = multValueList[t]
                    for s in m.shipTypes:
                        if targetShip == s.name:
                            ship = s
                    if ship == "":
                        ship = ShipType(targetShip,m.name)
                    print("\t%s"%ship.name)
                    for j in range(0,len(i.modiferName)):
                        if i.modiferName[j] in ship.getModiferName():
                            ship.modiferValue[ship.modiferName.index(i.modiferName[j])] += i.modiferValue[j]*multValue
                        else:
                            ship.modiferName.append(i.modiferName[j])
                            ship.modiferValue.append(i.modiferValue[j]*multValue)
                        pass
                    for j in range(0,len(ship.modiferName)):
                        print("\t\t%s = %g"%(ship.modiferName[j],ship.modiferValue[j]))
                    if not ship in m.shipTypes:
                        m.shipTypes.append(ship)
pass

def writeTech():
    print("\n\n\n")
    for doc in doctorines:
        f1 = open(doc)
        f = open(doc.replace("Input","Output"),"w")

        techName = ""
        indintation = 0
        tech = ""
        shipName = ""

        for line in f1:
            f.write(line)
            if indintation == 1:
                if "{" in line:
                    techName = line.split("=")[0].strip()
                    print(techName)
                    for t in techList:
                        if t.name == techName:
                            tech = t
                            #print(len(t.shipTypes))
                            break
            if indintation == 2:
                for s in shipList:
                    if s in line:
                        shipFound = True
                        shipName = line.split("=")[0].strip()
                        for st in tech.shipTypes:
                            if st.name == shipName:
                                #print(st.name)
                                tech.shipTypes.remove(st)
                        tech.startingTypes -= 1
                        break
            if "{" in line or "}" in line:
                 for element in list(line.strip()):
                    if "{" in element:
                        indintation +=1
                    elif "}" in element:
                        indintation -=1
                        if indintation == 1:
                            techName = ""
                        if indintation == 2:
                            shipFound = False
                            if tech.startingTypes == 0 and len(tech.shipTypes)>0:
                                print(tech.getTypeNames())
                                for st in tech.shipTypes:
                                    f.write("\t\t%s = {\n"%st.name)
                                    for m in range(0,len(st.modiferName)):
                                        f.write("\t\t\t%s = %g\n"%(st.modiferName[m],st.modiferValue[m]))
                                    f.write("\t\t}\n")
                                tech.shipTypes = []
                    elif "#" in element:
                        break
        f1.close()
        f.close()
		
#Battle Carrier
targetList = ["battleship","carrier","battle_cruiser"] 	#the ship types you are looking for
multValueList = [0.4,0.3,0.3] 							#the amount of the modifier you want to take from that ship and apply to target ship
targetShip = "battle_carrier" 							#ship type you are applying those modifiers for
generateModifiers(targetShip,targetList,multValueList)

#Cruiser Carrier
targetList = ["heavy_cruiser","carrier","light_cruiser"]
multValueList = [0.4,0.3,0.3]
targetShip = "cruiser_carrier"
generateModifiers(targetShip,targetList,multValueList)

#Submarine Carrier
targetList = ["submarine","carrier"]
multValueList = [0.8,0.2]
targetShip = "submarine_carrier"
generateModifiers(targetShip,targetList,multValueList)

#Submarine Light Cruiser
targetList = ["submarine","light_cruiser"]
multValueList = [0.8,0.2]
targetShip = "submarine_cruiser"
generateModifiers(targetShip,targetList,multValueList)

#Submarine Heavy Cruiser
targetList = ["submarine","heavy_cruiser"]
multValueList = [0.8,0.2]
targetShip = "submarine_heavy"
generateModifiers(targetShip,targetList,multValueList)

writeTech()
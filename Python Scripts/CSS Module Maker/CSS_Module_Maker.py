import re
import glob

moduleFile = open("input/00_ship_modules.txt",'r',encoding='utf-8',errors='ignore')
indintation = 0
definingModule = False
add_statsSection = False
multiply_statsSection = False
add_average_statsSection = False

class moduleDefinition:
    name = ""
    newName = ""
    category = ""
    sfx = ""
    gfx = ""
    parent = ""
    add_equipment_type = ""
    dismantle_cost_ic = 0
    #add stats
    add_lg_attack = 0
    add_hg_attack = 0
    add_build_cost_ic = 0
    add_anti_air_attack = 0
    add_surface_visibility = 0
    add_sub_visibility = 0
    #multiply stats
    mult_naval_speed = 0
    mult_max_strength = 0
    mult_sub_visibility = 0
    mult_reliability = 0
    mult_naval_range = 0
    mult_sub_visibility = 0
    #build cost resources
    res_steel = 0
    res_chromium = 0
    #add average stats
    avg_lg_armor_piercing = 0
    avg_hg_armor_piercing = 0
    #critical_parts
    critical_parts = ""
    tech = ""
    level = 0
class techDefinition:
    techName = ""
    def __init__(self, techName):
        self.techName
        self.modules = []

class moduleGroup:
    size = ""
    level = 0
    def __init__(self, size, level):
        self.size
        self.level
        self.modules = []
def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

def writeLocal(file):
    tmpFile = file.replace("ship_","CSS_gun_")
    tmpFile = tmpFile.replace("input","output")
    localFile = open(file,'r',encoding='utf-8',errors='ignore')
    localCSSFile = open(tmpFile,'w',encoding='utf-8-sig',errors='ignore')
    count = 0
    localCSSFile.write("l_%s\n"%file.split("_l_")[1].replace(".yml",":"))
    for line in localFile:
        
        if "light_battery" in line or "ship_heavy_battery" in line or "medium_battery" in line:
            if "EQ_" in line:
                pass
            else:
                count +=1
                tmpLine = line
                if "ship_" in tmpLine:
                    tmpLine = tmpLine.replace("ship_", "submarine_")
                elif "dp_" in tmpLine:
                    tmpLine = tmpLine.replace("dp_", "submarine_dp_")
                if "english" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Submersible)\"",2))
                elif "german" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Tauchboot)\"",2))
                elif "spanish" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Sumergible)\"",2))
                elif "braz_por" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Submersível)\"",2))
                elif "french" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Submersible)\"",2))
                elif "polish" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Podwodny)\"",2))
                elif "russian" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (Погружной)\"",2))
                elif "japanese" in file:
                    localCSSFile.write(replacenth(tmpLine,"\""," (潜水艇)\"",2))
    #print(count)
    localCSSFile.close()

def writeModules(moduleList):
    moduleFile = open("output/CSS_gun_modules.txt",'w',encoding='utf-8',errors='ignore')
    moduleFileGFX = open("output/CSS_gun_modules.gfx",'w',encoding='utf-8',errors='ignore')
    moduleFile.write("equipment_modules = {")
    moduleFileGFX.write("spriteTypes = {")
    for module in moduleList:
        moduleFile.write("\n\t%s = {"%module.newName)
        moduleFile.write("\n\t\tcategory = %s"%module.category)
        moduleFile.write("\n\t\tsfx = %s"%module.sfx)
        if module.gfx == "": 
            moduleFile.write("\n\t\tgfx = %s"%module.name)
        else:
            moduleFile.write("\n\t\tgfx = %s"%module.gfx)
        if not module.parent == "": 
            moduleFile.write("\n\t\tparent = %s"%module.parent)
        if not module.add_equipment_type == "":
            if module.add_equipment_type.strip() == "capital_ship":
                moduleFile.write("\n\t\tgui_category = submarine_heavy_battery")
            moduleFile.write("\n\t\tadd_equipment_type = %s"%module.add_equipment_type)
        else:
            moduleFile.write("\n\t\tgui_category = submarine_light_battery")
        #add_stats
        moduleFile.write("\n\n\t\tadd_stats = {")
        if not module.add_lg_attack == 0:
            moduleFile.write("\n\t\t\tlg_attack = %s"%module.add_lg_attack)
        if not module.add_hg_attack == 0:
            moduleFile.write("\n\t\t\thg_attack = %s"%module.add_hg_attack)
        if not module.add_anti_air_attack == 0:
            moduleFile.write("\n\t\t\tanti_air_attack = %s"%module.add_anti_air_attack)
        moduleFile.write("\n\t\t\tbuild_cost_ic = %s"%module.add_build_cost_ic)
        moduleFile.write("\n\t\t\tsurface_visibility = %s"%module.add_surface_visibility)
        moduleFile.write("\n\t\t\tsub_visibility = %s"%module.add_sub_visibility)
        moduleFile.write("\n\t\t}")
        #multiply_stats
        moduleFile.write("\n\t\tmultiply_stats = {")
        if not module.mult_naval_speed == 0:
            moduleFile.write("\n\t\t\tnaval_speed = %s"%module.mult_naval_speed)
        if not module.mult_max_strength == 0:
            moduleFile.write("\n\t\t\tmax_strength = %s"%module.mult_max_strength)
        if not module.mult_sub_visibility == 0:
            moduleFile.write("\n\t\t\tsub_visibility = %s"%module.mult_sub_visibility)
        if not module.mult_reliability == 0:
            moduleFile.write("\n\t\t\treliability = %s"%module.mult_reliability)
        if not module.mult_naval_range == 0:
            moduleFile.write("\n\t\t\tnaval_range = %s"%module.mult_naval_range)
        moduleFile.write("\n\t\t}")
        #add_average_stats
        moduleFile.write("\n\t\tadd_average_stats = {")
        if not module.avg_lg_armor_piercing == 0:
            moduleFile.write("\n\t\t\tlg_armor_piercing = %s"%module.avg_lg_armor_piercing)
        if not module.avg_hg_armor_piercing == 0:
            moduleFile.write("\n\t\t\thg_armor_piercing = %s"%module.avg_hg_armor_piercing)
        moduleFile.write("\n\t\t}")
        #build_cost_resources
        if module.res_steel > 0 or module.res_chromium > 0:
            moduleFile.write("\n\t\tbuild_cost_resources = {")
            if not module.res_steel == 0:
                moduleFile.write("\n\t\t\tsteel = %s"%module.res_steel)
            if not module.res_chromium == 0:
                moduleFile.write("\n\t\t\tchromium = %s"%module.res_chromium)
            moduleFile.write("\n\t\t}")

        moduleFile.write("\n\t\tdismantle_cost_ic = %s"%module.dismantle_cost_ic)
        moduleFile.write("\n\t\tcritical_parts = { %s }"%module.critical_parts)
        moduleFile.write("\n\t}")

        moduleFileGFX.write("\n\tspriteType = {")
        moduleFileGFX.write("\n\t\tname = \"GFX_SMI_%s\""%module.newName)
        moduleFileGFX.write("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/naval/modules/icons/%s.dds\""%module.newName.replace("battery", "battery_icn"))
        moduleFileGFX.write("\n\t}")
    moduleFileGFX.write("\n}")

def writeTechs2(moduleList):
    techFile = open("output/CSS_gun_tech.txt",'w',encoding='utf-8',errors='ignore')
    techFile.write("technologies = {\n")
    for module in moduleList:
        techFile.write("\n\tcss_%s = {"%module.newName)
        techFile.write("\n\t\tenable_equipment_modules = {")
        techFile.write("\n\t\t\t%s"%module.newName)
        techFile.write("\n\t\t}")
        techFile.write("\n\t}")
        
    techFile.write("\n}")


def writeTechLocal(moduleList):
    #techFilelocal = open("output/localisation/CSS_gun_tech.yml",'w',encoding='utf-8',errors='ignore')
    localFiles=glob.glob("output/localisation/**/CSS_gun_modules_*.yml")
    #print(localFiles)
    for localFile in localFiles:
        
        print (localFile)
        local = open(localFile,'r',encoding='utf-8',errors='ignore')
        techLocal = open(localFile.replace("modules_","tech_"),'w',encoding='utf-8-sig',errors='ignore')
        techLocal.write("l_%s\n"%localFile.split("_l_")[1].replace(".yml",":"))
        for line in local:
            if "_short:" in line:
                pass
            else:
                if line.strip().startswith("submarine"):
                    techLocal.write(" css_%s\n"%line.strip())
                    #print(line)
                elif line[4] == "_":
                    techLocal.write("%scss_%s"%(line[:5],line[5:]))
        techLocal.close()
    pass

def moduleGroupCheck(module, eventGrouping, size):
    group = moduleGroup(size,module.level)
    group.size = size
    group.level = module.level
    group.modules.append(module)
    eventGrouping.append(group)
    #for e in group.modules:
        #print(group.modules[0].name)

def writeGunEvents(moduleList):
    eventGrouping = []
    for module in moduleList:
        if not eventGrouping:
            if "dp_" in module.name:
                moduleGroupCheck(module, eventGrouping, "dp")
            else:
                if "light" in module.name:
                    moduleGroupCheck(module, eventGrouping, "light")
                if "medium" in module.name:
                    moduleGroupCheck(module, eventGrouping, "medium")
                if "heavy" in module.name:
                    moduleGroupCheck(module, eventGrouping, "heavy")
        else:
            found = False
            for group in eventGrouping:
                if "dp_" in module.name and "dp" == group.size and module.level == group.level:
                    group.modules.append(module)
                    found = True
                else:
                    if "light" in module.name and "light" == group.size and module.level == group.level:
                        group.modules.append(module)
                        found = True
                    if "medium" in module.name and "medium" == group.size and module.level == group.level:
                        group.modules.append(module)
                        found = True
                    if "heavy" in module.name and "heavy" == group.size and module.level == group.level:
                        group.modules.append(module)
                        found = True
            if not found:
                if "dp_" in module.name:
                    moduleGroupCheck(module, eventGrouping, "dp")
                else:
                    if "light" in module.name:
                        moduleGroupCheck(module, eventGrouping, "light")
                    if "medium" in module.name:
                        moduleGroupCheck(module, eventGrouping, "medium")
                    if "heavy" in module.name:
                        moduleGroupCheck(module, eventGrouping, "heavy")
    
    for group in eventGrouping:
        print(group.modules)

    techFile = open("output/CSS_gun_events.txt",'w',encoding='utf-8',errors='ignore')
    techFile.write("add_namespace = css_gun_tech")
    id = 1
    for group in eventGrouping:
        techFile.write("\n\n#%s"%group.modules[0].newName)
        techFile.write("\ncountry_event = {")
        techFile.write("\n\tid = css_gun_tech.%i"%id)
        techFile.write("\n\ttitle = css_gun_tech.%i.t"%id)
        techFile.write("\n\tdesc = css_gun_tech.%i.desc"%id)
        #techFile.write("\n\tpicture = GFX_")
        techFile.write("\n\thidden = yes")
        techFile.write("\n\n\ttrigger = {")
        techFile.write("\n\t\tnot = { has_tech = css_%s }"%group.modules[0].newName)
        techFile.write("\n\t\thas_tech = %s"%group.modules[0].tech)
        if "light" in group.size or "dp" in group.size:
            techFile.write("\n\t\thas_country_flag = light_battery_submersible")
        elif "medium" in group.size:
            techFile.write("\n\t\thas_country_flag = medium_battery_submersible")
        elif "heavy" in group.size:
            techFile.write("\n\t\thas_country_flag = heavy_battery_submersible")
        techFile.write("\n\t}")

        techFile.write("\n\tmean_time_to_happen = {")
        techFile.write("\n\t\tdays = 0")
        techFile.write("\n\t}")

        techFile.write("\n\timmediate = {")
        techFile.write("\n\t\tset_technology = {")
        for module in group.modules:
            techFile.write("\n\t\t\tcss_%s = 1"%module.newName)
        techFile.write("\n\t\t}")
        techFile.write("\n\t}")
        
        techFile.write("\n}")
        id +=1

def writeTechGfx(moduleList):
    techFile = open("output/CSS_gun_tech.gfx",'w',encoding='utf-8',errors='ignore')
    techFile.write("spriteTypes = {")
    for module in moduleList:
        techFile.write("\n\tSpriteType = {")
        techFile.write("\n\t\tname = \"GFX_css_%s_medium\""%module.newName)
        tmpString = ("\n\t\ttextureFile = \"gfx/interface/equipmentdesigner/naval/modules/icons/%s.dds\""%module.newName)
        
        if "_dp_" in tmpString:
            tmpString = tmpString.replace(".dds","_icn.dds")
        else:
            tmpString = tmpString.replace("battery_","battery_icn_")
        techFile.write(tmpString)
        techFile.write("\n\t}")
    techFile.write("\n}")

moduleList = []
module = moduleDefinition()
for line in moduleFile:
    if indintation == 1:
        definingModule = False
        if "light_battery" in line or "ship_heavy_battery" in line or "medium_battery" in line:
            module = moduleDefinition()
            module.name = line.strip().split(" ")[0].strip()
            try:
                module.level = int(module.name[-1])
            except:
                pass
            definingModule = True
    if indintation == 2 and definingModule:
        if "category" in line:
            module.category = line.strip().split("=")[1].strip()
        elif "sfx" in line:
            module.sfx = line.strip().split("=")[1].strip()
        elif "gfx" in line:
            module.gfx = line.strip().split("=")[1].strip()
        elif "parent" in line:
            module.parent = line.strip().split("=")[1].strip()
        elif "add_equipment_type" in line:
            module.add_equipment_type = line.strip().split("=")[1].strip()
        elif "add_stats" in line:
            add_statsSection = True
        elif "multiply_stats" in line:
            multiply_statsSection = True
        elif "add_average_stats" in line:
            add_average_statsSection = True
        elif "critical_parts" in line:
            module.critical_parts = line.strip().split("=")[1].strip().lstrip("{").rstrip("}").strip()
    if indintation == 3 and add_statsSection:
        if "lg_attack" in line:
            module.add_lg_attack = float(line.strip().split("=")[1].strip())
        elif "hg_attack" in line:
            module.add_hg_attack = float(line.strip().split("=")[1].strip())
        elif "build_cost_ic" in line:
            module.add_build_cost_ic = float(line.strip().split("=")[1].strip())
        elif "anti_air_attack" in line:
            module.add_anti_air_attack = float(line.strip().split("=")[1].strip())
        elif "surface_visibility" in line:
            module.add_surface_visibility = float(line.strip().split("=")[1].strip())
    if indintation == 3 and multiply_statsSection:
        if "naval_speed" in line:
            module.mult_naval_speed = float(line.strip().split("=")[1].strip())
        elif "max_strength" in line:
            module.mult_max_strength = float(line.strip().split("=")[1].strip())
    if indintation == 3 and add_average_statsSection:
        if "lg_armor_piercing" in line:
            module.avg_lg_armor_piercing = float(line.strip().split("=")[1].strip())
        elif "hg_armor_piercing" in line:
            module.avg_hg_armor_piercing = float(line.strip().split("=")[1].strip())
    

    if "{" in line or "}" in line:
        for element in list(line.strip()):
            if "{" in element:
                indintation +=1
            elif "}" in element:
                indintation -=1
                add_statsSection = False
                multiply_statsSection = False
                add_average_statsSection = False
                if indintation == 1 and definingModule:
                    moduleList.append(module)
            elif "#" in element:
                break
i=0

for module in moduleList:    
    module.newName = "submarine_" + module.name.replace("ship_","")
    module.category = "submarine_" + module.category.replace("ship_","")
    #module.gfx = "submarine_" + module.gfx.replace("ship_","")
    module.gfx = module.newName
    if not module.parent == "":
        module.parent = "submarine_" + module.parent.replace("ship_","")
    module.add_lg_attack *= 0.9
    module.add_hg_attack *= 0.9
    module.add_anti_air_attack *= 0.8
    module.add_build_cost_ic *= 1.2
    

    if "light_medium" in module.name:
        module.category = "submarine_medium_battery"
        module.add_lg_attack = module.add_lg_attack / 2
        module.add_build_cost_ic *= 0.75
        module.add_surface_visibility = 3.0
        module.dismantle_cost_ic = 100
        module.add_sub_visibility = 3.0
        try:
            module.mult_reliability = -0.08 + (0.01*int(module.name[-1]))
        except:
            module.mult_reliability = -0.06

    elif "light" in module.name:
        module.add_surface_visibility = 1.5
        module.dismantle_cost_ic = 50
        module.add_sub_visibility = 1.5
        try:
            module.mult_reliability = -0.075 + (0.015*int(module.name[-1]))
        except:
            module.mult_reliability = -0.03

    elif "medium" in module.name:
        module.add_hg_attack = module.add_hg_attack / 3
        module.add_build_cost_ic *= 0.5
        module.add_surface_visibility = 3.0
        module.mult_max_strength = 0.1
        module.dismantle_cost_ic = 100
        module.add_sub_visibility = 3.0
        try:
            module.mult_reliability = -0.105 + (0.015*int(module.name[-1]))
        except:
            module.mult_reliability = -0.07

    elif "heavy" in module.name:
        module.add_hg_attack = module.add_hg_attack / 5
        module.add_build_cost_ic *= 0.3
        module.add_surface_visibility = 3.0
        module.mult_naval_range = -0.1
        module.mult_max_strength = 0.2
        module.dismantle_cost_ic = 200
        module.add_sub_visibility = 3.0
        try:
            module.mult_reliability = -0.14 + (0.02*int(module.name[-1]))
        except:
            module.mult_reliability = -0.1

i=0

writeModules(moduleList)

localFiles=glob.glob("input/localisation/**/ship_modules_l_*.yml")
for file in localFiles:
    #print(file)
    writeLocal(file)

indintation = 0
moduleSearch = False
techName = ""
techFile = open("input/MTG_naval_Support.txt",'r',encoding='utf-8',errors='ignore')
for line in techFile:
    if line.strip() == "":
        pass
    else:
        if indintation == 1:
            #print(line.split("=")[0].strip())
            techName = line.split("=")[0].strip()
            pass
        if indintation == 2 and "enable_equipment_modules" in line:
            moduleSearch = True
        if indintation == 3 and moduleSearch:
            if line.strip() == "}":
                pass
            else:
                for module in moduleList:
                    if module.name == line.strip():
                        #print("%s - %s"%(techName,line.strip()))
                        module.tech = techName
        if "{" in line or "}" in line:
            #print("l: "+line)
            for element in list(line.strip()):
                if "{" in element:
                    indintation +=1
                    #print("s: "+element)
                elif "}" in element:
                    indintation -=1
                    if indintation == 2:
                        moduleSearch = False
                    #print("e: "+element)
                elif "#" in element:
                    #print("c: "+element)
                    break
writeTechs2(moduleList)
writeGunEvents(moduleList)
writeTechGfx(moduleList)

writeTechLocal(moduleList)


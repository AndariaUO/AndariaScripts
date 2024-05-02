from Assistant import Engine
from AndariaLib import *

### Nastav True pokud chceš znovu dotázat ignorované předměty
promptIgnored = False

macroName = "AutoLoot"
memory = {}
selectedPreset = ""

def Main():
    global selectedPreset
    global memory
    ClearIgnoreList()
    item = FindTypeList("stahovaciNuz", 10, "self")
    if item is not None and not isinstance(item,bool):
        SetAlias("stahovak", item.Serial)
    else:
        SysMessageOrange("Nemáš kuchací kudlu!")
    item = FindTypeBy("nuzky", 10, "self")
    if item is not None:
        SetAlias("nuzky", item)
    item = FindTypeBy("umyvadlo", 10, "self")
    if item is not None:
        SetAlias("umyvadlo", item)
    LoadAlias("kontejner cil",1,1)
    selectedPreset = LoadPreset()
    memory = LoadMacroVariable(macroName, "preset_" + selectedPreset, {})
    while True:
        while not Dead("self") and not Hidden("self"):
            WaitForSave()
            Loot()
            LootChest()
            Unload()
            PickBones()
            Pause(500)
        Pause(1000)
    
def Loot():
    while FindTypeBy("mrtvola", 2):
        LootContainer(FindTypeBy("mrtvola", 2).Serial)
        
def IsPlayerBody():
    return InJournal("*prohledava telo*", Name("self"))
        
def LootChest():
    if FindAlias("pokladnice"):
        LootContainer(GetAlias("pokladnice"))
        UnsetAlias("pokladnice")
        SysMessageGreen("Pokladnice vyprázdněna!")     

def LootContainer(container):
    cont = Engine.Items.GetItem(container)
    if not cont.Count == 400 and not cont.Count == 401 and not cont.Count == 1:
        Skin(container)
    Pause(500)
    IgnoreObject(container)
    ClearJournal()
    UseObject(container)
    Pause(500)
    if IsPlayerBody():
        return
        
    cont = Engine.Items.GetItem(container)
    if cont is None:
        return
        
    if cont.Container == None:
        if not WaitForContents(container, 5000):
            return
        
    for item in cont.Container.GetItems():
        itemkey = GetTypeName(item)
        if itemkey is None:
            itemkey = Deaccent(Name(item))
        if itemkey not in memory.keys() or (promptIgnored and memory[itemkey] == 0):
            res = ConfirmPrompt("Předmět '" + Name(item) + "' zatím nemám v paměti. Chceš ho lootit v presetu " + selectedPreset + "?")
            if res:
                if IsHide(item):
                    res = ConfirmPrompt("Předmět '" + Name(item) + "' je kůže, chceš ji stříhat v presetu " + selectedPreset + "?")
                    if res:
                        memory[itemkey] = 2
                    else:
                        memory[itemkey] = 1
                elif IsClothes(item):
                    res = ConfirmPrompt("Předmět '" + Name(item) + "' je zbojnické oblečení, chceš ho stříhat v presetu " + selectedPreset + "? Chce to pak mít nůžky a umyvadlo")
                    if res:
                        memory[itemkey] = 2
                    else:
                        memory[itemkey] = 1
                else:
                    memory[itemkey] = 1
            else:
                memory[itemkey] = 0
            SaveMacroVariable(macroName, "preset_" + selectedPreset, memory)
        
        if memory[itemkey] > 0:
            MoveItem(item, "kontejner cil")
            Pause(500)
            if memory[itemkey] == 2:
                CutUpClothes(item)
                CutHides(item)
    Pause(500)

def LoadPreset():
    global memory
    savedPresets = LoadMacroVariable("AutoLoot", "Presets", [])
    presets = list(savedPresets)
    presets.insert(0, "Založit nový preset")
    res, index = SelectionPrompt(presets, "Vyber preset pro lootování")
    if res:
        if index == 0:
            res, msg = MessagePrompt("Zadej název nového presetu", "Např 'Dungeon'")
            if res:
                SysMessageBlue("Zakládám čistý preset " + msg)
                savedPresets.append(msg)
                SaveMacroVariable("AutoLoot", "Presets", savedPresets)
                return msg
        else:
            selectedPreset = presets[index]
            SysMessageGreen("Vybrán preset " + selectedPreset)
            return selectedPreset
    
def Skin(corpse):
    if FindAlias("stahovak"):
        UseObject("stahovak")
    else:
        Msg(".usehand")
    WaitForTarget(1000)
    Target(corpse)
    
def Unload():
    if FindAlias("autoloot_unload"):
        SetMacroAlias("tmp", "kontejner cil")
        SetMacroAlias("kontejner cil", "autoloot_unload")
        LootContainer(GetAlias("tmp"))
        SetMacroAlias("kontejner cil", "tmp")
        UnsetAlias("autoloot_unload")
    
def PickBones():
    bones = FindTypeList("kostiSber", 3, returnAllItems=True)
    for bone in bones:
        UseObject(bone)
        Pause(500)
        
def IsHide(item):
    return Graphic(item) == GetType("hromadaKuze")

def IsClothes(item):
    WaitForProperties(item, 500)
    val = PropertyValue[int](item, "vydrz")
    return (val is not None and val >= 1 and val <= 2)
        
def CutHides(item):
    if IsHide(item):
        UseObject(item)
        Pause(300)
        FindType(GetType("rozstrihanaKuze"), 0, "backpack")
        MoveItem("found", "kontejner cil")
        Pause(100)
        
def CutUpClothes(item):
    if not FindAlias("nuzky"):
        return
    if IsClothes(item):
        UseObject("nuzky")
        WaitForTarget(500)
        Target(item)
        Pause(500)
        FindType(GetType("obvaz"), 0, "backpack")
        UseObject("found")
        WaitForTarget(500)
        Target("umyvadlo")
        Pause(500)
        MoveItem("found", "kontejner cil")
        Pause(500)

Main()
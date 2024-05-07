from Assistant import Engine
from AndariaLib import *

macroName = "Kopání"
memName = "Pamet"

ignoreList = []

def Main():
    CheckVersion()
    Init()

def Init():
    ClearIgnoreList()
    IdentifyMine(FindTypeBy("krumpac", -1, "self"))
    SysMessageGreen("Hotovo")

def IdentifyMine(pickaxe):
    if pickaxe is not None:
        EquipItem(pickaxe, "TwoHanded")
    else:
        SysMessageOrange("Nemám krumpáč")
        return
    for pos in LoadRails(macroName, memName):
        if Distance(pos.x, pos.y) < 2:
            SysMessageGreen("Důl rozeznán jako " + pos.note)
            KnownMine(pos.note)
            return
    SysMessageGreen("Důl nerozeznán")
    return

def KnownMine(mineName):
    LoadAlias("kontejner cil", 1, 1)
    currentPos = LoadMacroVariable(macroName, "currentPos", 0)
    while PathfindToRail(macroName, mineName, currentPos):
        currentPos += 1
        SaveMacroVariable(macroName, "currentPos", currentPos)
        Dig()
        MoveMined()
        if DiffWeight() < 30:
            SaveMacroVariable(macroName, "currentPos", currentPos)
            if ConfirmPrompt("Vypnout?"):
                return
    SaveMacroVariable(macroName, "currentPos", 0)
    PathfindToRail(macroName, memName, mineName)

def Dig():
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            DigSpot(i,j)
            Pause(500)
    
    if Engine.Player.Y != 1249 or Engine.Player.X == 1260:
        Pathfind(Engine.Player.X, Engine.Player.Y + 1, Engine.Player.Z)
        Pause(500)
        DigSpot(0,-1)

def DigSpot(x, y):
    global fields, empty_fields, ignoreList
    xy = {'X': Engine.Player.X + x, 'Y': Engine.Player.Y + y}
    if xy in ignoreList:
        return
    ignoreList.append(xy)
    tries = 0
    while True:
        tries += 1
        Msg(".usehand")
        WaitForTarget(15000)
        TargetTileOffsetResource(x, y, 0)
        (idx, text) = WaitForJournal([
            "dalo dolovat", "vykopat", "Pokládá", "na to místo",
            "Zkus kopat"
        ], 15000)
        if idx != None:
            if text == "vykopat":
                if tries == 10:
                    return
            if text == "dalo dolovat" or text == "na to místo" or text == "Zkus kopat":
                return
                            
def MoveMined():
    mined = FindTypeList("dolovane", 0, loc="backpack", returnAllItems=True)
    for ore in mined:
        MoveItem(ore, "kontejner cil")
        Pause(500)

Main()

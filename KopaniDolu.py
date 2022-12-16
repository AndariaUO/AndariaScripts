from Assistant import Engine
from AndariaLib import *

macroName = "Kopání"
memName = "Pamet"

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
        if Distance(pos.x, pos.y, Engine.Player.X, Engine.Player.Y) < 2:
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
            if i != 0 and j != 0:
                tries = 0
                while True:
                    Msg(".usehand")
                    WaitForTarget(1000)
                    TargetTileOffsetResource(i, j, 0)
                    (idx, text) = WaitForJournal(["dalo dolovat", "vykopat", "Pokládá", "na to místo", "Zkus kopat"], 15000)
                    if idx != None:
                        if text == "vykopat":
                            tries += 1
                            if tries == 10:
                                break
                        if text == "dalo dolovat" or text == "na to místo" or text == "Zkus kopat":
                            break
                            
def MoveMined():
    mined = FindTypeList("dolovane", 0, loc="backpack", returnAllItems=True)
    for ore in mined:
        MoveItem(ore, "kontejner cil")
        Pause(500)

Main()

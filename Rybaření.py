from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO.Data import MapInfo
from ClassicAssist.UO import UOMath
from Assistant import Engine
from AndariaLib import *

macroName = "Rybaření"
memName = "Pamet"

mode = 0
ignoreList = []

def Main():
    CheckVersion()
    if not Init():
        return
    if not IdentifySpot():
        while True:
            Fish()
            MoveFish()
            if not ConfirmPrompt("Přejdi na nové místo"):
                return

def Init():
    global mode
    res, mode = SelectionPrompt(['Sbírat jen cennosti', 'Sbírat vše', 'Sbírat vše a kuchat'])
    if not res:
        return False
    LoadAlias("kontejner cil", 1, 1)
    FindType(GetType("rybarskyPrut"), -1, "self")
    if GetAlias("found"):
        SetAlias("prut", "found")
    else:
        SysMessageRed("Nemám prut!")
        return False
    FindType(GetType("dyka"), -1, "self")
    if GetAlias("found"):
        SetAlias("dyka", "found")
    else:
        SysMessageRed("Nemám dýku!")
        return False
    return True

def IdentifySpot():
    for pos in LoadRails(macroName, memName):
        if Distance(pos.x, pos.y) < 2:
            SysMessageGreen("Nalezeny rails " + pos.note)
            KnownSpot(pos.note)
            return True
    res, rails = MessagePrompt("Zadej rails ve kterých chceš pokračovat, případně zrušit pro ruční chození", "")
    if res:
        SysMessageBlue("Hledám nejbliží pozici rails...")
        SaveMacroVariable(macroName, "currentPos", FindClosestRail(macroName, rails))
        KnownSpot(rails)
        return True
    SysMessageGreen("Nenalezeny žádné rails")
    return False

def KnownSpot(spot):
    currentPos = LoadMacroVariable(macroName, "currentPos", 0)
    while True:
        rail = LoadRails(macroName, spot, currentPos)
        if rail is None:
            break
        if not PathfindToPos(rail, -1, 10, 1000):
            Msg(".roz")
            if not ConfirmPrompt("Nemůžu se dostat na pozici {0} {1}, dojdi ručně a dej ok".format(rail.x,rail.y)):
                return
        currentPos += 1
        if rail.note.Contains("pruchozi"):
            SysMessageViolet("Pozice {0} je označena jako průchozí, jdu na další".format(currentPos - 1))
            continue
        Fish()
        MoveFish()
        if DiffWeight() < 30:
            SaveMacroVariable(macroName, "currentPos", currentPos)
            if ConfirmPrompt("Vypnout?"):
                break
    SaveMacroVariable(macroName, "currentPos", 0)
    SysMessageGreen("Hotovo")

def MoveFish():
    if mode == 0:
        items = FindTypeList("rybolovCennosti",1,"ground",returnAllItems=True)
    else:
        items = FindTypeList("ryby", 1, "ground", returnAllItems=True)
    if len(items) > 0:
        for item in items:
            MoveItem(item.Serial, "kontejner cil")
            Pause(500)
    if mode != 1:
        GutFish()
    if mode == 0:
        MoveTypeOffset(GetType("rybiStejk"), "kontejner cil", 0, 0, 0)

def GutFish():
    EquipItem("dyka", "OneHanded")
    Pause(500)
    items = FindTypeList("ryby", -1, "kontejner cil", returnAllItems=True)
    if len(items) > 0:
        for item in items:
            UseObject(item.Serial)
            Pause(500)
    items = FindTypeList("rybolovKuch", -1, "backpack", returnAllItems=True)
    if len(items) > 0:
        for item in items:
            MoveItem(item.Serial, "kontejner cil")
            Pause(500)

def Fish():
    global ignoreList
    EquipItem("prut", "TwoHanded")
    Pause(500)
    WaterSpots = GetWaterSpots()
    WaterCount = len(WaterSpots)
    if WaterCount > 0:
        ignoreList.extend(WaterSpots)
        SysMessageBlue(str(WaterCount) + " políček vody v dosahu")
        for water in WaterSpots:
            while True:
                Msg(".usehand")
                WaitForTarget(5000)
                TargetXYZ(water['X'], water['Y'], 0)
                (idx, text) = WaitForJournal([
                    'Vytahuje z vody nìco hodnì velkého a silného...!',
                    'To je pøíli daleko.', 
                    'Tady nejsou ádné ryby.',
                    'Zkus chytat nìkde jinde'
                    'Loví ryby, ale ádnou nechytá.',
                    'Vytahuje z vody',
                ], 10000)
                Pause(500)
                if idx == 0:
                    UseSkill("Skryti S")
                    ConfirmPrompt("Chytil si hada! Až ho zabiješ tak dej ok")
                if idx < 4:
                    break

def GetWaterSpots():
    water = []
    for x in range(Engine.Player.X - 10, Engine.Player.X + 10):
        for y in range(Engine.Player.Y - 10, Engine.Player.Y + 10):
            xy = {'X': x, 'Y': y}
            if xy in ignoreList:
                continue
            d = Distance(x, y)
            if d > 6 or d == 1:
                continue
            statics = Statics.GetStatics(0, x, y)
            if statics == None:
                continue
            for s in statics:
                if s.Name.Contains("voda") or s.Name.Contains("water"):
                    water.append(xy)
                    continue
            land = MapInfo.GetLandTile(0, x, y)
            if land.Name.Contains("voda") or land.Name.Contains("water"):
                water.append(xy)
    return water

Main()
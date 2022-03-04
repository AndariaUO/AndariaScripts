from Assistant import Engine
from DorchLib import *

macroName = "Pole"
memName = "Pamet"

def Main():
    Init()

def Init():
	ClearIgnoreList()
	IdentifyField(FindTypeBy("lopata", -1, "self") is not None)
	CleanReags()
	SysMessageGreen("Hotovo")

def IdentifyField(sow):
	if not sow:
		SysMessageOrange("Nemám lopatu, nebudu sázet")
	for pos in LoadRails(macroName, memName):
		if Distance(pos.x, pos.y, Engine.Player.X, Engine.Player.Y) < 2:
			SysMessageGreen("Pole rozeznáno jako " + pos.note)
			KnownField(pos.note, sow)
			return
	SysMessageGreen("Pole nerozeznáno, spouštím obecný cyklus na sbírání")
	while True:
		Reap(sow)
		Pause(500)

def KnownField(fieldName, sow):
    currentPos = 0
    while PathfindToRail(macroName, fieldName, currentPos):
        currentPos += 1
        Reap(sow)
    PathfindToRail(macroName, memName, fieldName)

def Reap(sow):
	while FindTypeList("rostlinkyZasazene", 1):
		IgnoreObject("found")
		name = Name("found").lower()
		UseObject("found")
		Pause(500)
		if sow and FindAlias("found"):
			SetAlias("hlina", "found")
			UseObject("hlina")
			Pause(500)
			if FindTypeBy(name, -1, "self"):
				UseObject("hlina")
				Pause(500)
				Target("found")
			else:
				SysMessageOrange("Nemám " + name + " k zasazení..")
				
def CleanReags():
	if FindTypeBy("dyka"):
		UseObject("found")
		Pause(500)
		CancelTarget()
		while FindTypeList("rostlinkyVytrzena", 1):
			UseObject("found")
			Pause(500)

Main()